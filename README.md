# Process Filter

## Description

A python script that utilizes scheduled Autoruns executions to monitor automatically starting applications and scripts in Windows. A common malware tactic is to enable persistence and autoruns is good at finding most the areas its possible to establish persistence from.

### Dependencies

- Python 3.10
- [watchdog 2.1.7](https://pypi.org/project/watchdog/)
- [Sysinternals Suite](https://apps.microsoft.com/store/detail/sysinternals-suite/9P7KNL5RWT25?hl=en-us&gl=US) 
- [autoruns](<https://docs.microsoft.com/en-us/sysinternals/downloads/autoruns>)

### Installing

1) Download the project and unzip it to a friendly directory
2) Install Autoruns by installing the from the Microsoft Store, or downloading and placing the  files into "C:\Program Files\SysinternalsSuite"
3) Open Task Scheduler in Windows and right-click/import task and select the autoruns.xml file and hit OK.
4) Place the python files and bat.bat into a directory with the path C:\logger

### Executing program

1) Wait for the scheduled task to execute a run, or right click the created task in Task Scheduler and import the task.
2) Execute the python script [main.py](https://github.com/Jester-Head/verbose-tribble/blob/51a76d31681ecf3e874ca364b8ba86e752cca748/main.py)
