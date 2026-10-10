@echo off
rem Where autorunsc.exe lives. Change this if Sysinternals is installed somewhere else.
set "AUTORUNSC=C:\Program Files\SysinternalsSuite\autorunsc.exe"

"%AUTORUNSC%" -a * -c -u -vt -accepteula -nobanner > C:\logger\output.txt
echo %date% %time% > C:\logger\done.txt
