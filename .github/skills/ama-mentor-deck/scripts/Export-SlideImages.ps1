#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Exports every slide of a PPTX to slide-NNN.jpg through PowerPoint on Windows.
.DESCRIPTION
    Fallback for the powerpoint skill's LibreOffice export when LibreOffice is
    not installed. Opens the deck read-only and without a window, exports each
    slide at the requested size, then closes PowerPoint's copy of the file.
.PARAMETER PptxPath
    Path to the deck to export.
.PARAMETER OutputDir
    Folder that receives slide-001.jpg, slide-002.jpg and so on.
.PARAMETER Width
    Image width in pixels.
.PARAMETER Height
    Image height in pixels.
.EXAMPLE
    ./Export-SlideImages.ps1 -PptxPath slide-deck/deck.pptx -OutputDir slide-deck/validation
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PptxPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputDir,

    [Parameter(Mandatory = $false)]
    [int]$Width = 1600,

    [Parameter(Mandatory = $false)]
    [int]$Height = 900
)

$ErrorActionPreference = 'Stop'

$deck = (Resolve-Path -LiteralPath $PptxPath).Path
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
$outDir = (Resolve-Path -LiteralPath $OutputDir).Path

$app = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
    # ReadOnly = true, Untitled = false, WithWindow = false
    $presentation = $app.Presentations.Open($deck, $true, $false, $false)
    foreach ($slide in $presentation.Slides) {
        $target = Join-Path $outDir ('slide-{0:D3}.jpg' -f $slide.SlideIndex)
        $slide.Export($target, 'JPG', $Width, $Height)
    }
    Write-Output ("Exported {0} slides to {1}" -f $presentation.Slides.Count, $outDir)
}
finally {
    if ($presentation) { $presentation.Close() }
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
