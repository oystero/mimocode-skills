# Export PPTX slides to 1920x1080 PNG via PowerPoint COM.
# Usage: powershell -File export_slides.ps1 -Src deck.pptx -OutDir qa\
param(
    [Parameter(Mandatory = $true)][string]$Src,
    [Parameter(Mandatory = $true)][string]$OutDir
)

$ErrorActionPreference = "Stop"
$srcFull = (Resolve-Path $Src).Path
if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}
$outFull = (Resolve-Path $OutDir).Path

# PowerPoint COM works better with ASCII paths when possible
$asciiSrc = Join-Path $env:TEMP ("pptx-export-" + [guid]::NewGuid().ToString("N") + ".pptx")
Copy-Item $srcFull $asciiSrc -Force

$pp = New-Object -ComObject PowerPoint.Application
try {
    $pp.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
    $pres = $pp.Presentations.Open($asciiSrc, $true, $false, $false)
    $n = $pres.Slides.Count
    foreach ($i in 1..$n) {
        $outPath = Join-Path $outFull ("slide-{0:D2}.png" -f $i)
        $pres.Slides.Item($i).Export($outPath, "PNG", 1920, 1080)
    }
    $pres.Close()
    Write-Host "Exported $n slides to $outFull"
}
finally {
    $pp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($pp) | Out-Null
    Remove-Item $asciiSrc -ErrorAction SilentlyContinue
}
