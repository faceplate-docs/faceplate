#!/usr/bin/env python3
"""Local Modbus TCP training fixture. CLI addresses 1..5 map to PDU 0..4."""
import argparse
import socket
import socketserver
import struct
import threading


class RegisterMap:
    def __init__(self):
        self.values = [1000, 65535, 1000, 1000, 1000]
        self.lock = threading.Lock()

    def transact(self, pdu):
        if not pdu:
            return b""
        function = pdu[0]
        with self.lock:
            if function == 3 and len(pdu) == 5:
                start, count = struct.unpack(">HH", pdu[1:])
                if not 1 <= count <= 125:
                    return bytes([function | 128, 3])
                if start + count > len(self.values):
                    return bytes([function | 128, 2])
                data = struct.pack(">" + "H" * count, *self.values[start:start + count])
                return bytes([3, len(data)]) + data
            if function == 6 and len(pdu) == 5:
                address, value = struct.unpack(">HH", pdu[1:])
                if address >= len(self.values):
                    return bytes([function | 128, 2])
                self.values[address] = value
                return pdu
            if function == 16 and len(pdu) >= 6:
                start, count, length = struct.unpack(">HHB", pdu[1:6])
                if not 1 <= count <= 123 or length != count * 2 or len(pdu) != 6 + length:
                    return bytes([function | 128, 3])
                if start + count > len(self.values):
                    return bytes([function | 128, 2])
                self.values[start:start + count] = struct.unpack(">" + "H" * count, pdu[6:])
                return struct.pack(">BHH", 16, start, count)
            return bytes([function | 128, 1 if function not in (3, 6, 16) else 3])


def receive_exact(stream, size):
    chunks = bytearray()
    while len(chunks) < size:
        part = stream.recv(size - len(chunks))
        if not part:
            raise EOFError
        chunks.extend(part)
    return bytes(chunks)


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(10)
        try:
            while True:
                transaction, protocol, length, unit = struct.unpack(">HHHB", receive_exact(self.request, 7))
                if protocol != 0 or not 2 <= length <= 254:
                    return
                pdu = receive_exact(self.request, length - 1)
                reply = self.server.registers.transact(pdu) if unit == 1 else bytes([pdu[0] | 128, 11])
                self.request.sendall(struct.pack(">HHHB", transaction, 0, len(reply) + 1, unit) + reply)
        except (EOFError, OSError):
            return


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address):
        self.registers = RegisterMap()
        super().__init__(address, Handler)


def client(port, address, value=None):
    if not 1 <= address <= 5:
        raise ValueError("CLI address must be 1..5")
    pdu = struct.pack(">BHH", 3 if value is None else 6, address - 1, 1 if value is None else value)
    with socket.create_connection(("127.0.0.1", port), timeout=3) as stream:
        stream.sendall(struct.pack(">HHHB", 1, 0, len(pdu) + 1, 1) + pdu)
        transaction, protocol, length, unit = struct.unpack(">HHHB", receive_exact(stream, 7))
        if (transaction, protocol, unit) != (1, 0, 1) or not 2 <= length <= 254:
            raise ValueError("Invalid response header")
        reply = receive_exact(stream, length - 1)
        if reply[0] & 128:
            raise ValueError(f"Modbus exception {reply[1]}")
        if value is None:
            if len(reply) != 4 or reply[:2] != bytes([3, 2]):
                raise ValueError("Invalid read response")
            return struct.unpack(">H", reply[2:])[0]
        if reply != pdu:
            raise ValueError("Invalid write echo")
        return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=15022)
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("--get", type=int, metavar="ADDRESS")
    operation.add_argument("--set", type=int, nargs=2, metavar=("ADDRESS", "VALUE"))
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be 1..65535")
    if args.get is not None or args.set is not None:
        address, value = (args.get, None) if args.set is None else args.set
        if not 1 <= address <= 5 or value is not None and not 0 <= value <= 65535:
            parser.error("address must be 1..5; value must be 0..65535")
        print(client(args.port, address, value))
    else:
        with Server(("127.0.0.1", args.port)) as server:
            print(f"Training source 127.0.0.1:{args.port}, Unit 1, HR 1..5", flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
