#!/usr/bin/env pwsh
<#
.SYNOPSIS
Build, verify or natively render the six-slide cost recovery.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Build', 'Verify', 'Render')]
    [string]$Action,
    [Parameter(Mandatory = $true)]
    [string]$RepoRoot
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$Work = Join-Path $RepoRoot '.copilot-tracking/ppt/2026-10-24/cowork-cost-recovery'
$Output = Join-Path $Work 'slide-deck'
$Original = Join-Path $Output 'original.pptx'
$Candidate = Join-Path $Output 'zava-forward-cowork-v2-draft.pptx'
$Manifest = Get-Content -Raw (Join-Path $Work 'content/recovery.json') | ConvertFrom-Json
$Targets = @($Manifest.slides.number)

function Read-Part {
    param($Archive, [string]$Name)
    $Reader = [IO.StreamReader]::new($Archive.GetEntry($Name).Open())
    try { return $Reader.ReadToEnd() } finally { $Reader.Dispose() }
}

function Read-XmlPart {
    param($Archive, [string]$Name)
    $Document = [xml]::new()
    $Document.PreserveWhitespace = $true
    $Document.LoadXml((Read-Part $Archive $Name))
    return ,$Document
}

function Get-Namespaces {
    param($Document)
    $Namespaces = [Xml.XmlNamespaceManager]::new($Document.NameTable)
    $Namespaces.AddNamespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    $Namespaces.AddNamespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    return ,$Namespaces
}

function Set-ShapeText {
    param($Shape, $Definition, $Namespaces)
    $Body = $Shape.SelectSingleNode('p:txBody', $Namespaces)
    $Templates = @($Body.SelectNodes('a:p', $Namespaces))
    $RunTemplate = $Body.SelectSingleNode('.//a:r', $Namespaces)
    foreach ($Paragraph in $Templates) { [void]$Body.RemoveChild($Paragraph) }
    for ($Index = 0; $Index -lt $Definition.text.Count; $Index++) {
        $Paragraph = $Templates[[Math]::Min($Index, $Templates.Count - 1)].CloneNode($true)
        foreach ($Child in @($Paragraph.ChildNodes)) {
            if ($Child.LocalName -notin @('pPr', 'endParaRPr')) { [void]$Paragraph.RemoveChild($Child) }
        }
        $Run = $RunTemplate.CloneNode($true)
        $Run.SelectSingleNode('a:t', $Namespaces).InnerText = $Definition.text[$Index]
        if ($Definition.sizes) {
            $Properties = $Run.SelectSingleNode('a:rPr', $Namespaces)
            if (-not $Properties) {
                $Properties = $Shape.OwnerDocument.CreateElement('a', 'rPr', $Namespaces.LookupNamespace('a'))
                [void]$Run.PrependChild($Properties)
            }
            $Properties.SetAttribute('sz', [string]$Definition.sizes[[Math]::Min($Index, $Definition.sizes.Count - 1)])
        }
        $End = $Paragraph.SelectSingleNode('a:endParaRPr', $Namespaces)
        if ($End) { [void]$Paragraph.InsertBefore($Run, $End) } else { [void]$Paragraph.AppendChild($Run) }
        [void]$Body.AppendChild($Paragraph)
    }
    if ($Definition.box) {
        $Transform = $Shape.SelectSingleNode('p:spPr/a:xfrm', $Namespaces)
        $Transform.SelectSingleNode('a:off', $Namespaces).SetAttribute('x', [string]$Definition.box[0])
        $Transform.SelectSingleNode('a:off', $Namespaces).SetAttribute('y', [string]$Definition.box[1])
        $Transform.SelectSingleNode('a:ext', $Namespaces).SetAttribute('cx', [string]$Definition.box[2])
        $Transform.SelectSingleNode('a:ext', $Namespaces).SetAttribute('cy', [string]$Definition.box[3])
    }
}

function Write-XmlPart {
    param($Archive, [string]$Name, $Document)
    $Archive.GetEntry($Name).Delete()
    $Entry = $Archive.CreateEntry($Name, [IO.Compression.CompressionLevel]::Optimal)
    $Writer = [IO.StreamWriter]::new($Entry.Open(), [Text.UTF8Encoding]::new($false))
    try { $Writer.Write($Document.OuterXml) } finally { $Writer.Dispose() }
}

if ($Action -eq 'Build') {
    [void][IO.Directory]::CreateDirectory($Output)
    if (-not (Test-Path $Original)) {
        Copy-Item (Join-Path $RepoRoot 'docs/capstone/deck/zava-forward-cowork-v2-draft.pptx') $Original
        Copy-Item (Join-Path $RepoRoot 'docs/capstone/deck/zava-forward-cowork-v2-draft.pdf') (Join-Path $Output 'original.pdf')
    }
    Copy-Item $Original $Candidate -Force
    $Archive = [IO.Compression.ZipFile]::Open($Candidate, [IO.Compression.ZipArchiveMode]::Update)
    try {
        foreach ($Slide in $Manifest.slides) {
            $Name = 'ppt/slides/slide{0}.xml' -f $Slide.number
            $Document = Read-XmlPart $Archive $Name
            $Namespaces = Get-Namespaces $Document
            foreach ($Property in $Slide.shapes.PSObject.Properties) {
                $Shape = $Document.SelectSingleNode("//p:sp[p:nvSpPr/p:cNvPr[@id='$($Property.Name)']]", $Namespaces)
                if (-not $Shape) { throw "Missing shape $($Slide.number):$($Property.Name)" }
                Set-ShapeText $Shape $Property.Value $Namespaces
            }
            foreach ($Addition in $Slide.add) {
                $Template = $Document.SelectSingleNode("//p:sp[p:nvSpPr/p:cNvPr[@id='$($Addition.template)']]", $Namespaces)
                $Shape = $Template.CloneNode($true)
                $Properties = $Shape.SelectSingleNode('p:nvSpPr/p:cNvPr', $Namespaces)
                $Properties.SetAttribute('id', [string]$Addition.id)
                $Properties.SetAttribute('name', 'Cost recovery formula')
                Set-ShapeText $Shape $Addition $Namespaces
                [void]$Template.ParentNode.AppendChild($Shape)
            }
            Write-XmlPart $Archive $Name $Document
            $NoteName = 'ppt/notesSlides/notesSlide{0}.xml' -f $Slide.number
            $Notes = Read-XmlPart $Archive $NoteName
            $NoteNamespaces = Get-Namespaces $Notes
            $BodyShape = $Notes.SelectSingleNode("//p:sp[p:nvSpPr/p:nvPr/p:ph[@type='body']]", $NoteNamespaces)
            $OldText = ($BodyShape.SelectNodes('.//a:t', $NoteNamespaces) | ForEach-Object { $_.InnerText }) -join "`n"
            $Timing = [regex]::Match($OldText, '(?m)^TIMING:.*$').Value
            $NewNotes = $Slide.notes
            if ($Timing) { $NewNotes += "`n" + $Timing }
            Set-ShapeText $BodyShape ([pscustomobject]@{text = @($NewNotes -split "`n")}) $NoteNamespaces
            Write-XmlPart $Archive $NoteName $Notes
        }
    } finally { $Archive.Dispose() }
    Write-Output "Built $Candidate"
}

if ($Action -in @('Build', 'Verify')) {
    $Before = [IO.Compression.ZipFile]::OpenRead($Original)
    $After = [IO.Compression.ZipFile]::OpenRead($Candidate)
    try {
        $Changed = @()
        foreach ($Entry in $Before.Entries) {
            if (-not $After.GetEntry($Entry.FullName)) { throw "Lost part: $($Entry.FullName)" }
            $BeforeStream = $Entry.Open()
            $AfterStream = $After.GetEntry($Entry.FullName).Open()
            $Hasher = [Security.Cryptography.SHA256]::Create()
            try {
                $BeforeHash = [Convert]::ToBase64String($Hasher.ComputeHash($BeforeStream))
                $AfterHash = [Convert]::ToBase64String($Hasher.ComputeHash($AfterStream))
            } finally { $BeforeStream.Dispose(); $AfterStream.Dispose(); $Hasher.Dispose() }
            if ($BeforeHash -ne $AfterHash) { $Changed += $Entry.FullName }
        }
        $Expected = @($Targets | ForEach-Object { "ppt/slides/slide$_.xml"; "ppt/notesSlides/notesSlide$_.xml" })
        if (@(Compare-Object $Expected $Changed).Count) { throw "Unexpected changed parts: $($Changed -join ', ')" }
        if ($Before.Entries.Count -ne $After.Entries.Count) { throw 'Package entry count changed' }
        $SlideCount = @($After.Entries | Where-Object { $_.FullName -match '^ppt/slides/slide\d+\.xml$' }).Count
        $NotesCount = @($After.Entries | Where-Object { $_.FullName -match '^ppt/notesSlides/notesSlide\d+\.xml$' }).Count
        $ReturnCount = 0
        foreach ($Entry in $After.Entries | Where-Object { $_.FullName -match '^ppt/slides/slide\d+\.xml$' }) {
            $SlideXml = Read-XmlPart $After $Entry.FullName
            $ReturnCount += @($SlideXml.SelectNodes('//*[@action="ppaction://hlinkshowjump?jump=lastslideviewed"]')).Count
        }
        if ($SlideCount -ne 54 -or $NotesCount -ne 54 -or $ReturnCount -ne 27) { throw "Counts invalid: $SlideCount/$NotesCount/$ReturnCount" }
        $Result = [ordered]@{status = 'pass'; slides = $SlideCount; notes = $NotesCount; last_slide_viewed = $ReturnCount; unchanged_other_parts = $true; changed_parts = $Changed; candidate_sha256 = (Get-FileHash $Candidate -Algorithm SHA256).Hash}
        $Result | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $Output 'package-validation.json') -Encoding utf8
        $Result | ConvertTo-Json -Depth 5
    } finally { $Before.Dispose(); $After.Dispose() }
}

if ($Action -eq 'Render') {
    $Temporary = Join-Path ([IO.Path]::GetTempPath()) ('zava-cost-recovery-' + [guid]::NewGuid().ToString('N'))
    [void][IO.Directory]::CreateDirectory($Temporary)
    $LocalPptx = Join-Path $Temporary 'candidate.pptx'
    Copy-Item $Candidate $LocalPptx
    $App = New-Object -ComObject PowerPoint.Application
    $Presentation = $null
    $RenderOutput = Join-Path $Output 'validation'
    [void][IO.Directory]::CreateDirectory($RenderOutput)
    try {
        $Presentation = $App.Presentations.Open($LocalPptx, -1, 0, 0)
        if ($Presentation.Slides.Count -ne 54) { throw 'Native PowerPoint slide count is not 54' }
        $Pdf = Join-Path $Temporary 'candidate.pdf'
        $Presentation.SaveAs($Pdf, 32)
        Copy-Item $Pdf (Join-Path $Output 'zava-forward-cowork-v2-draft.pdf') -Force
        $Scope = @($Targets | ForEach-Object { ($_ - 1); $_; ($_ + 1) } | Sort-Object -Unique)
        $Checks = @()
        foreach ($Number in $Scope) {
            $NativeSlide = $Presentation.Slides.Item($Number)
            $Image = Join-Path $Temporary ('slide-{0:D3}.png' -f $Number)
            $NativeSlide.Export($Image, 'PNG', 1600, 900)
            Copy-Item $Image $RenderOutput -Force
            if ($Number -in $Targets) {
                foreach ($Shape in $NativeSlide.Shapes) {
                    if ($Shape.HasTextFrame -eq -1 -and $Shape.TextFrame.HasText -eq -1) {
                        $Range = $Shape.TextFrame2.TextRange
                        $Checks += [ordered]@{slide=$Number; id=$Shape.Id; text=$Range.Text; height=$Shape.Height; bound_height=$Range.BoundHeight; width=$Shape.Width; bound_width=$Range.BoundWidth; font_size=$Range.Font.Size}
                    }
                }
            }
        }
        $Checks | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $RenderOutput 'native-text-bounds.json') -Encoding utf8
        Write-Output "Native PowerPoint exported 54-slide PDF and $($Scope.Count) preview slides to $RenderOutput"
    } finally {
        if ($Presentation) { $Presentation.Close() }
    }
}