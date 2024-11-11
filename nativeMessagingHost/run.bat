@REM echo off is crucial to avoid disconnecting the port
@echo off 
powershell -ExecutionPolicy Bypass -File "C:\\Users\\KZhang\\Documents\\GitHub\\Script-Scheduler\\Chime.ps1" > nul
call python "C:\\Users\\KZhang\\Documents\\GitHub\\Powershell-Script-Executor-Extention\\nativeMessagingHost\\nativeMessagingHost.py" 
pause