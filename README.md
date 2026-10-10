# verbose-tribble

## Description

A Python script that utilizes scheduled Autoruns executions to monitor automatically starting applications and scripts in Windows. A common malware tactic is to enable persistence, and Autoruns is good at finding most of the areas it's possible to establish persistence from.

Entries that VirusTotal flags are shown on a local web page.

### Dependencies

- Python 3.10 or later
- [watchdog](https://pypi.org/project/watchdog/) and [tabulate](https://pypi.org/project/tabulate/) (`pip install -r requirements.txt`)
- [Sysinternals Suite](https://apps.microsoft.com/store/detail/sysinternals-suite/9P7KNL5RWT25?hl=en-us&gl=US) or [Autoruns](https://docs.microsoft.com/en-us/sysinternals/downloads/autoruns)

### Installing

1) Download the project and unzip it to a friendly directory
2) Install the Python dependencies with `pip install -r requirements.txt`
3) Install Autoruns by downloading it and placing the files into "C:\Program Files\SysinternalsSuite". If you install it somewhere else, update the `AUTORUNSC` path at the top of bat.bat
4) Open Task Scheduler in Windows, right-click and import a task, select the autorunsc.xml file, and hit OK
5) Place the Python files and bat.bat into a directory with the path C:\logger

### Executing program

1) Wait for the scheduled task to execute a run, or right-click the created task in Task Scheduler and select Run
2) Execute the Python script [main.py](main.py)
3) Open http://localhost:8080 to see the flagged entries. The page updates after each scan
4) Press Ctrl+C to stop
