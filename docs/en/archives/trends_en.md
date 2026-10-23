# Trends: viewing and exporting history

## About the module

Trends display the history of one or more archives on a shared timeline. Use them to analyze a shift, compare process variables, and locate the time of a deviation. You can configure series and two vertical axes, select a period, inspect values with the cursor and a fixed slice, save a group, pin a chart to a process screen, and export data.

Source configuration is described in [Archives: configuring sources and recording data](./archives_en.md). Calculations based on history and hourly summaries are covered in [Aggregates: calculating and exporting indicators](./aggregates_en.md).

The screenshots show the Russian interface. Russian button and field labels are retained below with English explanations so that you can match the instructions to the screen.

## Before viewing history

You need accessible archives with history for the selected period. A trend reads values that have already been recorded. Creating an archive now does not give it data for the previous shift.

A series is an individual line with a source, name, color, and axis. A group is a collection of series and chart settings that can be reopened. A chart can be opened in a separate Runtime window or placed on a process screen as a «Тренды» (Trends) element.

A chart may contain points prepared for displaying the window boundaries; its appearance is not a list of all stored records. A gap represents a missing value. In a historical window, the «Текущее значение» (Current value) column refers to the end of that window, which may differ from the equipment's present reading.

## Pressure and flow over a shift

Task: compare pump station pressure and flow for October 15, 2026, from 08:00 to 16:00. The training example uses local time in Asia/Almaty, UTC+5. PressureArchive and FlowArchive already contain the reference history.

| Series | Source | Unit | Axis |
| --- | --- | --- | --- |
| Давление, бар (Pressure, bar) | PressureArchive | bar | y |
| Расход, л/с (Flow, L/s) | FlowArchive | L/s | y2 |

1. In Runtime, open «Меню» (Menu) → «Тренды» (Trends). On the «Архивы» (Archives) tab, open the first series editor using the button to the right of its name.
2. Enter «Давление, бар» (Pressure, bar) and leave the axis at y. On the «Архивы» source tab, select PressureArchive through the project tree and click save.
3. Click «Добавить серию» (Add series). For the second series, enter «Расход, л/с» (Flow, L/s), select FlowArchive as the source, and choose the y2 axis. Save the series, then click «ОК» in «Выбор трендов» (Trend selection).
4. Click «Старт-Стоп» (Start–Stop) to stop the window from advancing automatically.
5. Click the button showing the current dates. In Set period, set «с:» (From) to 2026-10-15 08:00:00 and «по:» (To) to 2026-10-15 16:00:00. Use the calendar and time list to select them.
6. Under «Период» (Period) → «Задание интервала» (Set interval), select hour and a multiplier of 8. Check the «Час X8» (Hour X8) label and the actual dates, 08:00–16:00.
7. Hover over a known time: at 08:20, the training pressure is 6 bar and flow is 2 L/s. Check the captions and both axes.

![Pressure and flow over a shift](./images/trends-pressure-flow-shift-ui-4.0.6.subs.png)

*Figure 1. Pressure and flow over a shift: the pressure scale is on the left and the flow scale is on the right.*

The position of the flow line relative to the left scale does not give its numeric value: read flow against the right-hand y2 axis. Axes and captions do not convert units.

Pausing applies only to the chart. Archives continue collecting values while Runtime is running.

### Period, navigation, and values

An absolute period specifies a particular start and end. The unit and multiplier specify the window duration for viewing and navigation. After changing any of these settings, check the actual dates in the top toolbar.

The backward and forward step buttons move the window by its duration: for an eight-hour window of 08:00–16:00, the previous period is 00:00–08:00. To investigate a historical event, pause first, then set the dates.

The cursor tooltip shows the sample time and series values. To create a fixed slice, right-click inside the plotting area. «Таблица среза» (Slice table) shows values at the slice time; in a narrow window, this command is in the ⋮ menu. «Удалить аннотации и срезы» (Delete annotations and slices) removes the slice.

In the tested training example, a slice at 11:11:46 showed pressure of 3.5 and flow of 2. The cursor tooltip may snap to a neighboring sample, so check the tooltip time and fixed slice time separately.

### Level lines

«Линии уровня» (Level lines) lets you add a constant reference line with a name, value, color, and thickness. For example, a training line named «Рабочая отметка» (Operating reference) with a value of 4 helps when reading pressure. Open the dialog, add a row, fill in the fields, and click «ОК». To remove a line, open the same dialog, delete the row, and confirm with «ОК». The line serves as a visual reference.

## Series and chart tools

The series editor is available during trend selection and through the edit icon in the legend. Use a clear name that includes the unit, especially when using two axes.

| Field | Purpose | Type / unit | Required | Default | If blank | Constraints |
| --- | --- | --- | --- | --- | --- | --- |
| Название (Name) | Series caption | Text | No | График / График 1 (Chart / Chart 1) | An archive path may be used | Does not change the source |
| Группа (Group) | Series membership | Selection | Yes | Группа (Group) | Select a group | Relates to chart composition |
| Ось (Axis) | Vertical scale | y / y2 | Yes | y | Leave y | Does not convert units |
| Архивы (Archives) | Line source | Path | Yes for a direct series | Not selected | No series data | Select the archive, rather than the source tag |
| Видимость (Visibility) | Show the line | Yes/no | No | Да (Yes) | Leave Да | History is not deleted |
| Толщина (Thickness) | Line thickness | Number | No | 1 | Leave 1 | Appearance |
| Цвет (Color) | Line color | Color | No | First is black; new colors are generated | Keep the selected color | Appearance |
| Ступенчатость (Stepped) | Steps between values | Yes/no | No | Да (Yes) | Leave Да | Does not change recording |
| Маркер (Marker) | Point appearance | Selection | No | Нет (None) | No markers | Appearance |
| Размер маркеров (Marker size) | Point size | Number | No | 1 | Leave 1 | Applies when a marker is enabled |
| Диапазон min/max (Range min/max) | Series value limits | Signal units | No | Blank | No series limits | Does not replace the axis scale |

The editor has three source tabs: «Архивы» (Archives), «Скрипты» (Scripts), and «Формула» (Formula). For a direct series, select one archive. «Скрипты» shows a variables table with archive bindings, a JavaScript editor, and Compile. «Формула» shows a variables table with archive bindings and an expression field. Variable names must match the expression. A calculated series is used for display and does not itself create a calculated archive. To store a calculated variable, create a script archive as described in the separate archive guide.

The series range limits the displayed values of that series; the axis range sets the scale. For an initial view, leave both ranges blank and use automatic scaling.

### Toolbar actions

| Action | Purpose | Available when | Result |
| --- | --- | --- | --- |
| Выбор архивов / Редактор групп (Select archives / Group editor) | Change chart composition | Chart is open | Series and group editor |
| Старт-Стоп (Start–Stop) | Update / pause | Chart is open | Window advances / stays fixed |
| Date button / Set period | Absolute boundaries | Chart is open | History for the selected period |
| Период (Period) | Unit and duration | Chart is open | New viewing interval |
| Backward / forward step | Adjacent interval | Chart is paused | Move by the window duration |
| Скрыть/Показать описание (Hide/Show description) | Legend | Chart is open | Legend hidden / shown |
| Задание шкалы (Set scale) | y and y2 settings | Chart is open | «Ограничение шкалы» (Scale limits) dialog |
| Линии уровня (Level lines) | Constant reference lines | Chart is open | Add and remove a level |
| Таблица среза (Slice table) | Values at a fixed time | Slice exists | Values table |
| Удалить аннотации и срезы (Delete annotations and slices) | Remove a slice | Slice exists | Slice removed |
| Настройки отображения (Display settings) | Update and appearance | Chart is open | Settings dialog |
| Сохранить как группу (Save as group) | Reuse settings | Chart is configured | New / updated group |
| Закрепить за экраном (Pin to screen) | Restore the chart with a screen | A process screen is open | Pin for the user and screen |
| Экспортировать тренды в файл (Export trends to file) | Transfer settings | Chart is configured | .tnd file |
| Импортировать тренды из файла (Import trends from file) | Load settings | A .tnd file is available | Series and settings restored |
| Аналитика / Экспорт аналитики (Analytics / Export analytics) | Calculate indicators | History is available | See the aggregate guide |

Some commands move into ⋮ when the window is narrow. Button availability also depends on the embedded trend's properties. Hiding a button or line does not restrict the user's access to the source data.

## Saving and transferring settings

### Saving the «Насосная станция» (Pump station) group

1. Configure the two series from the previous example.
2. Click «Сохранить как группу» (Save as group).
3. In «Имя группы» (Group name), set «Название» (Name) to Насосная станция. Click «ОК».
4. Close the chart and the old trend selection window.
5. Reopen Runtime → «Тренды» (Trends) → «Группы» (Groups). Enter Насосная in «Искать по имени» (Search by name) and click «Найти» (Find).
6. Select «Насосная станция» and click «ОК».
7. Check both captions, sources, y/y2 axes, appearance, and the «Час X8» (Hour X8) duration.

![Saving a trend group](./images/trends-save-group-ui-4.0.6.subs.png)

*Figure 2. The new group name is entered in the save dialog.*

A group stores settings. In the check, the series, axes, colors, stepped appearance, and window duration were restored. The chart opened with the current eight-hour period and automatic updates. The specific historical dates and paused state were not restored: set them again to view the previous shift.

To update a group, change the open chart's settings, click «Сохранить как группу», and confirm the same name. Check the result through a newly opened «Выбор трендов» (Trend selection) window: a window that is already open may retain the previous selection. In the training check, a changed series caption was saved this way.

### The .tnd settings file

On a configured chart, select «Экспортировать тренды в файл» (Export trends to file); open ⋮ if necessary. This downloads trend_settings.tnd.

To load it, open «Выбор трендов» (Trend selection) → «Файл» (File) → Select files..., choose your .tnd file, and click «ОК». Check the series, paths, axes, and duration. Set the historical dates and pause again after loading.

A .tnd file does not contain a copy of the measurements. In another project, the archives selected in the file must be accessible at the corresponding paths.

### Pinning a chart to a process screen

Open the required process screen in Runtime. From that screen, open the configured chart and click «Закрепить за экраном» (Pin to screen). When the same user subsequently opens the screen, a separate chart window is restored.

A pinned chart and an embedded trend element are separate display objects: both can appear on the screen at the same time. Do not assume that changing a saved group automatically updates an existing pin; in the check, the pinned chart retained the settings it had when pinned.

## Exporting the selected period

Use direct archive series for export. Configure the chart's series, pause it, and set the required start and end before exporting.

1. Open the pressure and flow chart for October 15, 08:00–16:00.
2. Click «Сохранить в .csv» (Save to .csv) on the toolbar.
3. In File format, select .csv and click save.
4. Repeat the command for the same history, select .xlsx, and click save.
5. Open the downloaded files. Check the headers, first and last dates, and known values.

![Selecting the trend export format](./images/trends-export-format-ui-4.0.6.subs.png)

*Figure 3. File format selects the output format; the period and series come from the chart.*

The tested dialog provides only .csv and .xlsx, with save and cancel buttons. It has no separate selection of period, series, or calculation function.

For the training window, both files contain datetime, «Давление, бар» (Pressure, bar), «Расход, л/с» (Flow, L/s), and eight data rows. Reference rows:

| datetime | Давление, бар (Pressure, bar) | Расход, л/с (Flow, L/s) |
| --- | --- | --- |
| 2026-10-15 08:00:00.000 | 2 | 2 |
| 2026-10-15 08:20:00.000 | 6 | 2 |
| 2026-10-15 16:00:00.000 | 3 | 2 |

The row count depends on the chart data. This file includes a row at the right boundary, 16:00; do not apply this rule to aggregate calculation intervals.

| Format | Contents | Export / import | Details |
| --- | --- | --- | --- |
| CSV | Time and chart series values | «Сохранить в .csv» → .csv | UTF-8 without BOM, TAB delimiter, CRLF line endings |
| XLSX | The same time and values | «Сохранить в .csv» → .xlsx | In the check: Sheet1, time stored as text, values as numbers |
| .tnd | Chart settings | Экспортировать тренды в файл; Файл → Select files | No copy of history |
| Analytics export | Indicators by interval | «Экспорт аналитики» | Settings and example are in the aggregate guide |

If the CSV opens in a single column, import it as text using UTF-8 and a tab delimiter. The file uses a period as the decimal separator. Timestamps have no explicit UTC offset, so retain the time zone information for the selected window.

The check offered the filenames archives.10_16_2026.csv and archives.10_16_2026.xlsx, although the history is for October 15. Check the period using the file's rows rather than the date in its name. The export contains data prepared by the chart; it does not guarantee a list of every original stored point.

## Settings reference

### Update and appearance of a separate chart

Open «Настройки отображения» (Display settings). Changes apply to viewing, rather than to the source archives' recording settings.

| Field | Purpose | Type / unit | Required | Default | If blank | Constraints |
| --- | --- | --- | --- | --- | --- | --- |
| Период обновления (Update period) | Chart refresh | Seconds | Yes | 1 | Leave 1 | Differs from the archive period |
| Цвет фона (Background color) | Plot background | Color | No | #fff | Keep the color | Appearance |
| Ylabel / Y2label | Axis captions | Text | No | Blank | No caption | Specify units explicitly |
| Кол-во символов после запятой (Decimal places) | Numbers in the legend | Integer | No | 2 | Leave 2 | Display format |
| Заполнить площадь (Fill area) | Fill below the line | Yes/no | No | Off | No fill | Appearance |
| Прозрачность (Transparency) | Fill | Number | No | 0.20 | Leave 0.20 | Applies to fill |
| Размер метки Y (Y label size) | Label size | Number | No | 18 | Leave 18 | Appearance |
| Отображать сетку (Show grid) | Grid visibility | Yes/no | No | On | Grid visible | Does not change history |
| Шаг сетки X / Y (X / Y grid step) | Grid density | Number | No | 100 / 20 | Keep the initial values | Display |
| Цвет сетки Y (Y grid color) | Grid color | Color | No | #000000 | Keep the color | Appearance |
| Тип отображения легенды (Legend display mode) | Tooltip behavior | Selection | No | onmouseover | Keep the mode | never / always / follow / onmouseover |
| Количество срезов (Number of slices) | Slice count | Integer | No | 2 | Leave 2 | Display |
| Отображение панели (Toolbar display) | Toolbar visibility | Selection | No | show | Leave show | Does not set permissions |
| Авто / min / max for Y, Y2 (Auto / min / max) | Axis scale | Series units | No | Limits blank | Auto | Separate for each axis |

Toolbar toggles let you choose the available viewing tools. For a typical chart, keep archive, period, interval, scale, legend, level, slice, and settings controls available. Data export and analytics are configured separately from the archive contents.

### Adding an embedded trend

In Studio, select the screen object → «Мнемосхема» (Process screen) → edit the screen row. In the graphical editor, open «Элементы управления» (Controls) and drag «Тренды» (Trends) onto the workspace.

Select the new element. Under «Свойства» (Properties) → value → archives, open the editor and add archive series with the required axes. Set the element's position and size, then click «Сохранить» (Save) at the top. Close and reopen the editor to check the bindings. Check actual data on the process screen in Runtime: the editor preview may show demonstration curves.

### Embedded element properties

The catalog below uses names visible in the property editor. Position values depend on where the element was dropped; they are not fixed defaults.

| Field | Purpose | Type / unit | Required | Default | If blank | Constraints |
| --- | --- | --- | --- | --- | --- | --- |
| appearance: visible, opacity | Visibility and opacity | Boolean; number | No | true; 1 | Keep the initial values | Element display |
| border: color, radius, style, width | Border | Color; numbers; style | No | #808080; 0; solid; 0 | No visible border | UI names use border_ |
| geometry: width, height | Size | Editor coordinates | Yes | 800; 350 | Set the size | Check on the screen |
| geometry: left, top | Position | Editor coordinates | Yes | Drop location | Position with the mouse | Depends on the screen |
| grid: grid, color, x, y | Grid | Boolean; color; numbers | No | true; #000000; 100; 20 | Keep the initial values | UI names: grid_color/x/y |
| legend | Legend mode | Selection | No | onmouseover | Keep the mode | never / always / follow / onmouseover |
| legend: font, size, colors | Font and colors | Font; number; colors | No | system-ui; 12; background #7092be; text #fff | Keep the initial values | Names listed below |
| legend: digits, max_hairlines | Precision and slices | Integers | No | 2; 2 | Leave 2 | Display only |
| misc: background_color, cursor | Background and pointer | Color; selection | No | #fff; inherit | Keep the initial values | Appearance |
| misc: name, title | Name and tooltip | Text | No | Blank | No text | General element properties |
| misc: z_index | Stacking order | Number | No | 0 | Leave 0 | General geometry |
| scale: time_step, time_factor | Window duration | Unit; multiplier | Yes | minute; 10 | Keep the initial values | Check the resulting dates |
| scale: range_min/max, y2_range_min/max | Axis limits | Series units | No | Blank | Auto | Two independent axes |
| series_view: fill_graph, fill_opacity | Fill | Boolean; number | No | false; 0.20 | No fill | Appearance |
| series_view: ylabel, y2label, ylabel_width | Axis captions | Text; number | No | Blank; blank; 18 | No caption | Does not change units |
| value: archives | Series composition | Editor | Yes | No archives selected | No history | Bind the archives |
| value: cycle | Refresh | Seconds | Yes | 1 | Leave 1 | Does not set the recording period |
| value: update_depth | Reread the end of the window | Seconds | No | 5 | Leave 5 | For updating history |
| value: show_description | Show description | Boolean | No | true | Description visible | Appearance |
| toolbar: toolbar_visible | Toolbar | Selection | No | show | Toolbar visible | Does not set permissions |

The border group uses border_color, border_radius, border_style, and border_width. Font and color settings in legend are legend_background_color, legend_font_family, legend_font_size, and legend_text_color. Decimal places are set by legend_max_numbers_after_point; the number of slices is set by max_hairlines.

Separate toolbar toggles are available for the confirmed tools: select_archives, set_period, set_interval, set_show_description, set_scale, add_level_lines, hairline_grid, annotations, appearance, data_export, analytics, analytics_export, and export. They are initially enabled. Configure the toolbar for the operator's task; it does not replace access permissions.

## Diagnostics and limitations

| Observation | What to check | How to verify |
| --- | --- | --- |
| Chart is empty | An archive is selected; history exists; dates and time zone | Hover over a known point |
| Archive shows RUN, but history does not change | Source changes and minimum step | Compare the source with history |
| Parameters are visually difficult to compare | Units, y/y2 axes, and captions | Read each series against its own axis |
| Current legend differs from the source | Historical window end | Select the current period |
| Date changes after opening a group | Duration restored; chart is live | Pause and set the dates again |
| Group update is not visible | Old «Выбор трендов» (Trend selection) window | Close it and open a new selection window |
| .tnd file opens empty series | Source archives are accessible at their paths | Select the archives again |
| Preview shows different numbers | Editor demonstration preview | Check the process screen in Runtime |
| A closed chart appears again | A saved screen pin | Distinguish the pin from the embedded element |
| A command is missing in a narrow window | ⋮ menu and toolbar properties | Locate the available command |
| CSV opens in one column | File delimiter and encoding | Import using the settings in the export section |

When comparing results, use the same time, period, and units. Line visibility, a saved group, and a settings file do not change the source history contents.
