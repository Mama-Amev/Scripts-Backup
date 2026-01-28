$SourceDir = "C:\PATH\TO\FOLDER"
$OutDir    = "C:\PATH\TO\FOLDER"

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}

Get-ChildItem $SourceDir -Recurse -Include *.jpg,*.jpeg | ForEach-Object {
    $pngPath = Join-Path $OutDir ($_.BaseName + ".png")
    magick "$($_.FullName)" "$pngPath"
}
