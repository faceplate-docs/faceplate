## Instructions for installing and running the Faceplate application in a Docker container

Requirement: Docker Engine must be installed and running on your computer.

Step 1: Create a folder for the project

First, create a folder on your computer where the application will live. This will store the databases and logs so they don't get lost.

Open Terminal and run the following commands:

mkdir my-faceplate-app
cd my-faceplate-app

Step 2: Create data folders

Within this folder, create two subfolders. This will allow you to see the logs and
database files directly on your computer.

mkdir logs
mkdir db

Step 3: Run the application

Copy the entire code block below, paste it into the terminal, and press Enter. This
command will download the application and run it.

docker run -d \
-p 9000:9000 \
-p 7080:7080 \
-v $(pwd)/logs:/opt/faceplate/logs \
-v $(pwd)/db:/opt/faceplate/DB \
--name faceplate-instance \
fpcloud/faceplate:latest

Step 4: Verify that everything is working

1. Verify that the container is running with the command:
docker ps

2. Open a browser and navigate to: http://localhost:9000

Brief explanation of the command (optional)

-d: Runs the application in the background (to prevent the terminal from freezing).

-p 9000:9000: Connects port 9000 on your computer to the application.

-v ...: "Links" the folders you created (logs and db) to the
container. This ensures that your data is preserved even if the
application is restarted.

fpcloud/faceplate:latest: Tells Docker which version
to download.