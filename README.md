1. put yt-dlp in non-admin privedledge required directories, such as user/
   `& "C:\\Users\kunzh\\yt-dlp.exe"  -o $outDir $url `
2. do not print out anything in nativeMessagingHost.py and download_video.ps1to stdout, this will cause error

Steps

1. edge://extensions/ enable Developer mode and Load unpacked manifest folder
1. nativeMessagingHost\nativeMessagingHost.json change
   - allowed_origins extention ID
   - path
1. Change path and run.reg file
1. Change yt-dlp location in nativeMessagingHost\PowerSellScripts\download_video.ps1
