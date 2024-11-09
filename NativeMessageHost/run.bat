@REM powershell -ExecutionPolicy Bypass -NoProfile  -File ".\run.js" >> ".\native_host.log" 2>&1
@REM echo off is crucial to avoid disconnecting the port
@echo off 
call python ".\run.py"
powershell -ExecutionPolicy Bypass -File "C:\\GitHub\\Utilities\\Chime-Scheduler\\Chime.ps1"
pause