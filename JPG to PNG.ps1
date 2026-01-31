$SourceDir = "C:\PATH\TO\FOLDER"
$OutDir    = "C:\PATH\TO\FOLDER"

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}

Get-ChildItem $SourceDir -Recurse -Include *.jpg,*.jpeg | ForEach-Object {
    $pngPath = Join-Path $OutDir ($_.BaseName + ".png")
    magick "$($_.FullName)" "$pngPath"
}

# ---- ADDITIONAL PART ----
# Move GIF, MP4, MP3, MOV to OutDir
Get-ChildItem $SourceDir -Recurse -Include *.gif,*.mp4,*.mp3,*.mov | ForEach-Object {
    $destination = Join-Path $OutDir $_.Name

    # Prevent overwrite
    if (Test-Path $destination) {
        $base = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        $ext  = $_.Extension
        $i = 1
        do {
            $destination = Join-Path $OutDir "$base`_$i$ext"
            $i++
        } while (Test-Path $destination)
    }

    Move-Item $_.FullName $destination
}
