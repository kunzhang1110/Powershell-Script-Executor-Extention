param(
    [string]$url
    )

$outDir ="$HOME\Downloads\%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s"

$scriptDir = $PSScriptRoot
$ytDlpPath = Join-Path -Path $scriptDir -ChildPath "yt-dlp.exe"
& $ytDlpPath -o $outDir $url