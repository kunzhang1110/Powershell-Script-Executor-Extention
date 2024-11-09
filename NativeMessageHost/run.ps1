param(
    [string]$url
    )


$outDir ="$HOME\Downloads\%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"
& "C:\\Users\kunzh\\yt-dlp.exe"  -o $outDir $url 
