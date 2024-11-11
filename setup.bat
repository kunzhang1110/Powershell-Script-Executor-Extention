set "dir=%~dp0"

call python "%dir%setup\setup.py"
regedit "%dir%nativeMessagingHost\nativeMessagingHost.reg"
pause