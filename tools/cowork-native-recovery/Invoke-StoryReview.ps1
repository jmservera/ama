#!/usr/bin/env pwsh
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT
<#
.SYNOPSIS
Inspect, revise and natively render the owner-selected capstone deck.
.DESCRIPTION
Uses a source-backed manifest and changes exactly fifteen slide/note parts.
Build checks uncompressed package bytes; Render uses Windows PowerPoint only.
.PARAMETER Action
Inspect (default), Build, Verify, or Render. Render requires Windows PowerShell COM.
.PARAMETER RepoRoot
Repository containing the owner-selected current presentation.
.PARAMETER OutputDir
External working directory for the inventory and later review outputs.
.PARAMETER SourcePath
Optional source override for hash-refusal regression checks, never an output.
.EXAMPLE
./Invoke-StoryReview.ps1 -RepoRoot /repo -OutputDir /tmp/zava-story-review
.NOTES
Never modifies the canonical deck. Render closes only its own presentation.
#>
[CmdletBinding()]
param(
    [ValidateSet('Inspect', 'Build', 'Verify', 'Render')]
    [string]$Action = 'Inspect',
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$RepoRoot,
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputDir,
    [string]$SourcePath
)
$ErrorActionPreference = 'Stop'

function Get-PartDocument {
    param($Archive, [string]$Name)
    $Entry = $Archive.GetEntry($Name)
    if (-not $Entry) { throw "Missing package member: $Name" }
    $Reader = [IO.StreamReader]::new($Entry.Open())
    try {
        $Document = [xml]::new()
        $Document.PreserveWhitespace = $true
        $Document.LoadXml($Reader.ReadToEnd())
        return ,$Document
    } finally { $Reader.Dispose() }
}

function Get-SlideInventory {
    param($Archive, [int]$Number)
    $Document = Get-PartDocument $Archive "ppt/slides/slide$Number.xml"
    $Namespaces = [Xml.XmlNamespaceManager]::new($Document.NameTable)
    $Namespaces.AddNamespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    $Namespaces.AddNamespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    $Shapes = foreach ($Shape in $Document.SelectNodes('//p:sp | //p:pic | //p:graphicFrame', $Namespaces)) {
        $Properties = $Shape.SelectSingleNode('.//p:cNvPr', $Namespaces)
        $Transform = $Shape.SelectSingleNode('p:spPr/a:xfrm | p:xfrm', $Namespaces)
        $Box = $null
        if ($Transform) {
            $Offset = $Transform.SelectSingleNode('a:off', $Namespaces)
            $Extent = $Transform.SelectSingleNode('a:ext', $Namespaces)
            $Box = @([double]$Offset.x, [double]$Offset.y, [double]$Extent.cx, [double]$Extent.cy) | ForEach-Object { [Math]::Round($_ / 914400, 4) }
        }
        [ordered]@{
            id = $Properties.id
            name = $Properties.name
            kind = $Shape.LocalName
            text = @($Shape.SelectNodes('.//a:t', $Namespaces) | ForEach-Object InnerText) -join "`n"
            box = $Box
            fonts = @($Shape.SelectNodes('.//a:latin', $Namespaces) | ForEach-Object { $_.typeface } | Sort-Object -Unique)
            sizes = @($Shape.SelectNodes('.//a:rPr[@sz]', $Namespaces) | ForEach-Object { [double]$_.sz / 100 } | Sort-Object -Unique)
            colors = @($Shape.SelectNodes('.//a:srgbClr', $Namespaces) | ForEach-Object { $_.val } | Sort-Object -Unique)
            actions = @($Shape.SelectNodes('.//a:hlinkClick', $Namespaces) | ForEach-Object { $_.OuterXml })
        }
    }
    $Notes = Get-PartDocument $Archive "ppt/notesSlides/notesSlide$Number.xml"
    $Namespaces = [Xml.XmlNamespaceManager]::new($Notes.NameTable)
    $Namespaces.AddNamespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    $Namespaces.AddNamespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    $Body = $Notes.SelectSingleNode("//p:sp[p:nvSpPr/p:nvPr/p:ph[@type='body']]", $Namespaces)
    [ordered]@{
        number = $Number
        shapes = @($Shapes)
        notes = @($Body.SelectNodes('.//a:t', $Namespaces) | ForEach-Object InnerText) -join "`n"
    }
}

function Get-Namespaces {
    param([xml]$Document)
    $Namespaces = [Xml.XmlNamespaceManager]::new($Document.NameTable)
    $Namespaces.AddNamespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    $Namespaces.AddNamespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    return ,$Namespaces
}

function Get-PartBytes {
    param($Archive, [string]$Name)
    $Stream = $Archive.GetEntry($Name).Open()
    $Buffer = [IO.MemoryStream]::new()
    try { $Stream.CopyTo($Buffer); return ,$Buffer.ToArray() }
    finally { $Stream.Dispose(); $Buffer.Dispose() }
}

function Get-ByteHash {
    param([byte[]]$Bytes)
    $Hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($Hasher.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $Hasher.Dispose() }
}

function Get-XmlBytes {
    param([xml]$Document)
    foreach ($Node in $Document.ChildNodes) {
        if ($Node.NodeType -in @([Xml.XmlNodeType]::Whitespace, [Xml.XmlNodeType]::SignificantWhitespace)) {
            $Node.Value = $Node.Value.Replace("`r", '')
        }
    }
    $Buffer = [IO.MemoryStream]::new()
    $Settings = [Xml.XmlWriterSettings]::new()
    $Settings.Encoding = [Text.UTF8Encoding]::new($false)
    $Settings.Indent = $false
    $Settings.NewLineHandling = [Xml.NewLineHandling]::Entitize
    $Writer = [Xml.XmlWriter]::Create($Buffer, $Settings)
    try { $Document.Save($Writer); $Writer.Flush(); return ,$Buffer.ToArray() }
    finally { $Writer.Dispose(); $Buffer.Dispose() }
}

function Add-TextParagraph {
    param([xml]$Document, $Body, [string]$Text, [double]$Size = 14, [string]$Color = '173F35', [bool]$Bold = $false, [string]$Align = 'l')
    $Drawing = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    $Paragraph = $Document.CreateElement('a', 'p', $Drawing)
    $Properties = $Document.CreateElement('a', 'pPr', $Drawing)
    $Properties.SetAttribute('algn', $Align)
    $Line = $Document.CreateElement('a', 'lnSpc', $Drawing)
    $Spacing = $Document.CreateElement('a', 'spcPct', $Drawing)
    $Spacing.SetAttribute('val', '105000')
    [void]$Line.AppendChild($Spacing)
    [void]$Properties.AppendChild($Line)
    [void]$Properties.AppendChild($Document.CreateElement('a', 'buNone', $Drawing))
    [void]$Paragraph.AppendChild($Properties)
    $Run = $Document.CreateElement('a', 'r', $Drawing)
    $RunProperties = $Document.CreateElement('a', 'rPr', $Drawing)
    $RunProperties.SetAttribute('lang', 'en-GB')
    $RunProperties.SetAttribute('sz', ([int]($Size * 100)).ToString())
    $RunProperties.SetAttribute('b', ([int]$Bold).ToString())
    $Fill = $Document.CreateElement('a', 'solidFill', $Drawing)
    $Rgb = $Document.CreateElement('a', 'srgbClr', $Drawing)
    $Rgb.SetAttribute('val', $Color)
    [void]$Fill.AppendChild($Rgb)
    [void]$RunProperties.AppendChild($Fill)
    $Font = $Document.CreateElement('a', 'latin', $Drawing)
    $Font.SetAttribute('typeface', 'Arial')
    [void]$RunProperties.AppendChild($Font)
    [void]$Run.AppendChild($RunProperties)
    $Value = $Document.CreateElement('a', 't', $Drawing)
    $Value.InnerText = $Text
    [void]$Run.AppendChild($Value)
    [void]$Paragraph.AppendChild($Run)
    [void]$Body.AppendChild($Paragraph)
}

function Add-NativeShape {
    param([xml]$Document, $Tree, $Element, [int]$Id, [int]$SlideNumber)
    $Box = @($Element.box)
    if ($Box.Count -ne 4 -or @($Box | Where-Object { [double]::IsNaN([double]$_) -or [double]::IsInfinity([double]$_) }).Count -or
        $Box[2] -le 0 -or $Box[3] -le 0 -or $Box[0] -lt 0.5 -or $Box[1] -lt 0.5 -or
        $Box[0] + $Box[2] -gt 12.834 -or $Box[1] + $Box[3] -gt 7.0) { throw "Invalid margins: $($Element.key)" }
    if ($Element.text -and $Element.size -lt 12) { throw "Text below 12pt: $($Element.key)" }
    $Fragment = [xml]'<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:nvSpPr><p:cNvPr id="1" name="Story"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="18288" rIns="18288" tIns="9144" bIns="9144" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/></p:txBody></p:sp>'
    $Shape = $Document.ImportNode($Fragment.DocumentElement, $true)
    $Namespaces = Get-Namespaces $Document
    $Properties = $Shape.SelectSingleNode('p:nvSpPr/p:cNvPr', $Namespaces)
    $Properties.SetAttribute('id', $Id.ToString())
    $Properties.SetAttribute('name', "Story-$SlideNumber-$($Element.key)")
    $Properties.SetAttribute('descr', [string]$Element.text)
    if ($Element.geometry) {
        if ($Element.geometry -notin @('rect', 'chevron', 'downArrow', 'rightArrow', 'ellipse', 'roundRect', 'line', 'pie', 'can', 'polygon')) { throw "Unsupported native geometry: $($Element.geometry)" }
        $Geometry = $Shape.SelectSingleNode('p:spPr/a:prstGeom', $Namespaces)
        $Geometry.SetAttribute('prst', $Element.geometry)
        if ($Element.geometry -eq 'chevron') {
            $Adjustment = $Document.CreateElement('a', 'gd', $Namespaces.LookupNamespace('a'))
            $Adjustment.SetAttribute('name', 'adj')
            $Adjustment.SetAttribute('fmla', 'val 10000')
            [void]$Shape.SelectSingleNode('p:spPr/a:prstGeom/a:avLst', $Namespaces).AppendChild($Adjustment)
        }
        if ($Element.geometry -eq 'pie') {
            $Angles = @($Element.angles)
            if ($Angles.Count -ne 2 -or $Angles[0] -eq $Angles[1] -or
                @($Angles | Where-Object { [double]::IsNaN([double]$_) -or [double]::IsInfinity([double]$_) -or $_ -lt 0 -or $_ -ge 360 }).Count) {
                throw "Invalid pie angles: $($Element.key)"
            }
            foreach ($Index in 0..1) {
                $Adjustment = $Document.CreateElement('a', 'gd', $Namespaces.LookupNamespace('a'))
                $Adjustment.SetAttribute('name', "adj$($Index + 1)")
                $Adjustment.SetAttribute('fmla', "val $([int][Math]::Round($Angles[$Index] * 60000))")
                [void]$Geometry.SelectSingleNode('a:avLst', $Namespaces).AppendChild($Adjustment)
            }
        }
        if ($Element.geometry -eq 'polygon') {
            $Points = @($Element.points)
            if ($Points.Count -lt 3) { throw "A polygon needs three points: $($Element.key)" }
            $Custom = $Document.CreateElement('a', 'custGeom', $Namespaces.LookupNamespace('a'))
            foreach ($Name in @('avLst', 'gdLst', 'ahLst', 'cxnLst')) {
                [void]$Custom.AppendChild($Document.CreateElement('a', $Name, $Namespaces.LookupNamespace('a')))
            }
            $Rectangle = $Document.CreateElement('a', 'rect', $Namespaces.LookupNamespace('a'))
            foreach ($Pair in @(@('l', '0'), @('t', '0'), @('r', 'w'), @('b', 'h'))) { $Rectangle.SetAttribute($Pair[0], $Pair[1]) }
            [void]$Custom.AppendChild($Rectangle)
            $Paths = $Document.CreateElement('a', 'pathLst', $Namespaces.LookupNamespace('a'))
            $Path = $Document.CreateElement('a', 'path', $Namespaces.LookupNamespace('a'))
            $Path.SetAttribute('w', '100000')
            $Path.SetAttribute('h', '100000')
            for ($Index = 0; $Index -lt $Points.Count; $Index++) {
                $Point = @($Points[$Index])
                if ($Point.Count -ne 2 -or @($Point | Where-Object { [double]::IsNaN([double]$_) -or [double]::IsInfinity([double]$_) -or $_ -lt 0 -or $_ -gt 100 }).Count) {
                    throw "Invalid polygon point: $($Element.key)"
                }
                $Command = 'lnTo'
                if ($Index -eq 0) { $Command = 'moveTo' }
                $Step = $Document.CreateElement('a', $Command, $Namespaces.LookupNamespace('a'))
                $Coordinate = $Document.CreateElement('a', 'pt', $Namespaces.LookupNamespace('a'))
                $Coordinate.SetAttribute('x', [string][int][Math]::Round($Point[0] * 1000))
                $Coordinate.SetAttribute('y', [string][int][Math]::Round($Point[1] * 1000))
                [void]$Step.AppendChild($Coordinate)
                [void]$Path.AppendChild($Step)
            }
            [void]$Path.AppendChild($Document.CreateElement('a', 'close', $Namespaces.LookupNamespace('a')))
            [void]$Paths.AppendChild($Path)
            [void]$Custom.AppendChild($Paths)
            [void]$Geometry.ParentNode.ReplaceChild($Custom, $Geometry)
        }
    }
    $Offset = $Shape.SelectSingleNode('p:spPr/a:xfrm/a:off', $Namespaces)
    $Extent = $Shape.SelectSingleNode('p:spPr/a:xfrm/a:ext', $Namespaces)
    $Offset.SetAttribute('x', ([int][Math]::Round($Box[0] * 914400)).ToString())
    $Offset.SetAttribute('y', ([int][Math]::Round($Box[1] * 914400)).ToString())
    $Extent.SetAttribute('cx', ([int][Math]::Round($Box[2] * 914400)).ToString())
    $Extent.SetAttribute('cy', ([int][Math]::Round($Box[3] * 914400)).ToString())
    if ($Element.fill) {
        $Fill = $Shape.SelectSingleNode('p:spPr/a:noFill', $Namespaces)
        $Solid = $Document.CreateElement('a', 'solidFill', $Namespaces.LookupNamespace('a'))
        $Rgb = $Document.CreateElement('a', 'srgbClr', $Namespaces.LookupNamespace('a'))
        $Rgb.SetAttribute('val', $Element.fill)
        [void]$Solid.AppendChild($Rgb)
        [void]$Fill.ParentNode.ReplaceChild($Solid, $Fill)
    }
    if ($Element.stroke) {
        $Width = 1.25
        if ($null -ne $Element.stroke_width) { $Width = [double]$Element.stroke_width }
        if ($Element.stroke -cnotmatch '^[0-9A-Fa-f]{6}$' -or [double]::IsNaN($Width) -or [double]::IsInfinity($Width) -or $Width -le 0 -or $Width -gt 12) {
            throw "Invalid native outline: $($Element.key)"
        }
        $Line = $Shape.SelectSingleNode('p:spPr/a:ln', $Namespaces)
        $Line.RemoveAll()
        $Line.SetAttribute('w', [string][int][Math]::Round($Width * 12700))
        $Solid = $Document.CreateElement('a', 'solidFill', $Namespaces.LookupNamespace('a'))
        $Rgb = $Document.CreateElement('a', 'srgbClr', $Namespaces.LookupNamespace('a'))
        $Rgb.SetAttribute('val', $Element.stroke)
        [void]$Solid.AppendChild($Rgb)
        [void]$Line.AppendChild($Solid)
    }
    $Body = $Shape.SelectSingleNode('p:txBody', $Namespaces)
    if ($Element.valign) {
        if ($Element.valign -notin @('t', 'ctr', 'b')) { throw "Invalid vertical anchor: $($Element.key)" }
        $Body.SelectSingleNode('a:bodyPr', $Namespaces).SetAttribute('anchor', $Element.valign)
    }
    if ($Element.text) {
        $Color = '173F35'
        if ($Element.color) { $Color = $Element.color }
        $Align = 'l'
        if ($Element.align) { $Align = $Element.align }
        foreach ($Text in $Element.text -split "`n") {
            Add-TextParagraph $Document $Body $Text $Element.size $Color ([bool]$Element.bold) $Align
        }
    } else { Add-TextParagraph $Document $Body '' 12 }
    [void]$Tree.AppendChild($Shape)
}

function Set-StorySlide {
    param($Archive, $Spec)
    $Document = Get-PartDocument $Archive "ppt/slides/slide$($Spec.number).xml"
    $Namespaces = Get-Namespaces $Document
    $Tree = $Document.SelectSingleNode('/p:sld/p:cSld/p:spTree', $Namespaces)
    foreach ($Shape in @($Tree.ChildNodes)) {
        if ($Shape.LocalName -in @('nvGrpSpPr', 'grpSpPr', 'extLst')) { continue }
        $Properties = $Shape.SelectSingleNode('.//p:cNvPr', $Namespaces)
        if ($Properties.name -like '*Footer*' -or $Spec.keep_ids -contains [int]$Properties.id -or
            $Shape.SelectNodes('.//a:hlinkClick | .//a:hlinkMouseOver', $Namespaces).Count) { continue }
        [void]$Tree.RemoveChild($Shape)
    }
    foreach ($Replacement in $Spec.headers) {
        $Shape = $Tree.SelectSingleNode("p:sp[p:nvSpPr/p:cNvPr[@id='$($Replacement.id)']]", $Namespaces)
        if (-not $Shape) { throw "Missing preserved header $($Replacement.id)" }
        $Body = $Shape.SelectSingleNode('p:txBody', $Namespaces)
        foreach ($Paragraph in @($Body.SelectNodes('a:p', $Namespaces))) { [void]$Body.RemoveChild($Paragraph) }
        Add-TextParagraph $Document $Body $Replacement.text $Replacement.size '173F35' $true
        $Transform = $Shape.SelectSingleNode('p:spPr/a:xfrm', $Namespaces)
        $Transform.SelectSingleNode('a:off', $Namespaces).SetAttribute('x', ([int]($Replacement.box[0] * 914400)).ToString())
        $Transform.SelectSingleNode('a:off', $Namespaces).SetAttribute('y', ([int]($Replacement.box[1] * 914400)).ToString())
        $Transform.SelectSingleNode('a:ext', $Namespaces).SetAttribute('cx', ([int]($Replacement.box[2] * 914400)).ToString())
        $Transform.SelectSingleNode('a:ext', $Namespaces).SetAttribute('cy', ([int]($Replacement.box[3] * 914400)).ToString())
    }
    $Id = [Math]::Max(900000, ([int]($Tree.SelectNodes('.//p:cNvPr', $Namespaces) | ForEach-Object { [int]$_.id } | Measure-Object -Maximum).Maximum) + 1)
    foreach ($Element in $Spec.elements) { Add-NativeShape $Document $Tree $Element $Id $Spec.number; $Id++ }
    return ,(Get-XmlBytes $Document)
}

function Set-TargetedPart {
    param($Archive, [string]$Name, $Replacements, $Elements, [int]$SlideNumber)
    $Document = Get-PartDocument $Archive $Name
    $Namespaces = Get-Namespaces $Document
    foreach ($Replacement in $Replacements) {
        $Selector = '//a:t'
        if ($Replacement.id) { $Selector = "//p:sp[p:nvSpPr/p:cNvPr[@id='$($Replacement.id)']]//a:t" }
        $TextMatches = @($Document.SelectNodes($Selector, $Namespaces) | Where-Object { $_.InnerText.Contains($Replacement.from) })
        if ($TextMatches.Count -ne 1 -or ($TextMatches[0].InnerText.Split(@([string]$Replacement.from), [StringSplitOptions]::None).Count -ne 2)) {
            throw "Expected one exact replacement in $Name : $($Replacement.from)"
        }
        $TextMatches[0].InnerText = $TextMatches[0].InnerText.Replace([string]$Replacement.from, [string]$Replacement.to)
    }
    if (@($Elements).Count) {
        $Tree = $Document.SelectSingleNode('/p:sld/p:cSld/p:spTree', $Namespaces)
        $Id = [Math]::Max(900000, ([int]($Tree.SelectNodes('.//p:cNvPr', $Namespaces) | ForEach-Object { [int]$_.id } | Measure-Object -Maximum).Maximum) + 1)
        foreach ($Element in $Elements) { Add-NativeShape $Document $Tree $Element $Id $SlideNumber; $Id++ }
    }
    return ,(Get-XmlBytes $Document)
}

function Set-StoryNotes {
    param($Archive, $Spec)
    $Document = Get-PartDocument $Archive "ppt/notesSlides/notesSlide$($Spec.number).xml"
    $Namespaces = Get-Namespaces $Document
    $Body = $Document.SelectSingleNode("//p:sp[p:nvSpPr/p:nvPr/p:ph[@type='body']]/p:txBody", $Namespaces)
    $Original = @($Body.SelectNodes('.//a:t', $Namespaces) | ForEach-Object InnerText) -join "`n"
    $Timing = @([regex]::Matches($Original, '(?m)^TIMING:.*$') | ForEach-Object Value)
    $Text = @(
        "$($Spec.code) | $($Spec.subject)",
        ($Timing -join "`n"),
        'SPEAKER SCRIPT', ($Spec.script -join "`n"),
        'DIAGRAM TEXT EQUIVALENT', $Spec.diagram,
        'EVIDENCE AND LIMITS', ($Spec.caveats -join "`n"),
        'SOURCES', ($Spec.sources -join "`n"),
        'NAVIGATION', $Spec.navigation,
        'Existing source footers are retained verbatim; the paths above identify the sources for this revision.'
    ) -join "`n"
    foreach ($Paragraph in @($Body.SelectNodes('a:p', $Namespaces))) { [void]$Body.RemoveChild($Paragraph) }
    foreach ($Line in $Text -split "`n") { Add-TextParagraph $Document $Body $Line 12 '000000' }
    return ,(Get-XmlBytes $Document)
}

function Test-StoryPackage {
    param([string]$InputPath, [string]$CandidatePath, $Manifest)
    $Source = [IO.Compression.ZipFile]::OpenRead($InputPath)
    $Candidate = [IO.Compression.ZipFile]::OpenRead($CandidatePath)
    try {
        $SourceNames = @($Source.Entries.FullName | Sort-Object)
        $CandidateNames = @($Candidate.Entries.FullName | Sort-Object)
        if (@(Compare-Object $SourceNames $CandidateNames).Count -or $SourceNames.Count -ne $CandidateNames.Count -or
            @($CandidateNames | Select-Object -Unique).Count -ne $CandidateNames.Count) { throw 'Package member set changed' }
        $Allowed = @(@($Manifest.slides) + @($Manifest.text_only_slides) | ForEach-Object { "ppt/slides/slide$($_.number).xml"; "ppt/notesSlides/notesSlide$($_.number).xml" })
        $Allowed += @($Manifest.notes_only | ForEach-Object { "ppt/notesSlides/notesSlide$($_.number).xml" })
        $Expected = @(@(8, 13, 15, 22, 39, 40, 51) | ForEach-Object { "ppt/slides/slide$_.xml"; "ppt/notesSlides/notesSlide$_.xml" }) + @('ppt/notesSlides/notesSlide7.xml')
        if (@(Compare-Object ($Allowed | Sort-Object) ($Expected | Sort-Object)).Count -or $Allowed.Count -ne 15) { throw 'Expected exact fifteen-member manifest allowlist' }
        $Changed = @()
        foreach ($Name in $SourceNames) {
            if ((Get-ByteHash (Get-PartBytes $Source $Name)) -ne (Get-ByteHash (Get-PartBytes $Candidate $Name))) {
                if ($Name -notin $Allowed) { throw "Unexpected changed member: $Name" }
                $Changed += $Name
            }
        }
        if ($Changed.Count -ne 15 -or @(Compare-Object ($Changed | Sort-Object) ($Expected | Sort-Object)).Count) { throw "Expected exact fifteen changed parts, got $($Changed.Count)" }
        $Slides = @($CandidateNames | Where-Object { $_ -match '^ppt/slides/slide\d+\.xml$' })
        $Notes = @($CandidateNames | Where-Object { $_ -match '^ppt/notesSlides/notesSlide\d+\.xml$' })
        if ($Slides.Count -ne 54 -or $Notes.Count -ne 54) { throw 'Expected 54 slides and 54 notes parts' }
        $Actions = 0
        $FooterCount = 0
        $TimingEvidence = @()
        $TextEvidence = @()
        $LegalBefore = "Legal dates come from official government publications (Oct 2026); Zava's legal review confirms them."
        $LegalAfter = 'Dated official-source snapshots; currentness and named legal review required before consequential use.'
        foreach ($Number in 1..54) {
            $Before = Get-PartDocument $Source "ppt/slides/slide$Number.xml"
            $After = Get-PartDocument $Candidate "ppt/slides/slide$Number.xml"
            $Namespaces = Get-Namespaces $After
            $BeforeActions = @($Before.SelectNodes('//a:hlinkClick | //a:hlinkMouseOver', $Namespaces) | ForEach-Object OuterXml)
            $AfterActions = @($After.SelectNodes('//a:hlinkClick | //a:hlinkMouseOver', $Namespaces) | ForEach-Object OuterXml)
            if (($BeforeActions -join "`n") -cne ($AfterActions -join "`n")) { throw "Navigation changed on slide $Number" }
            $Actions += @($After.SelectNodes('//a:hlinkClick', $Namespaces) | Where-Object { $_.action -eq 'ppaction://hlinkshowjump?jump=lastslideviewed' }).Count
            $Ids = @($After.SelectNodes('//p:cNvPr', $Namespaces) | ForEach-Object id)
            if (@($Ids | Select-Object -Unique).Count -ne $Ids.Count) { throw "Duplicate shape IDs on slide $Number" }
            if ($Number -eq 51) {
                $Selector = "//p:sp[p:nvSpPr/p:cNvPr[@id='19627']]"
                $Legal = $Before.SelectSingleNode($Selector, $Namespaces)
                $LegalText = $Legal.SelectSingleNode('.//a:t', $Namespaces)
                if ($LegalText.InnerText -cne $LegalBefore) { throw 'Legal-caption exception source mismatch' }
                $LegalText.InnerText = $LegalAfter
                if ($Legal.OuterXml -cne $After.SelectSingleNode($Selector, $Namespaces).OuterXml) { throw 'Legal-caption exception changed more than the authorised text' }
            }
            foreach ($Shape in $Before.SelectNodes('//p:sp', $Namespaces)) {
                $Properties = $Shape.SelectSingleNode('p:nvSpPr/p:cNvPr', $Namespaces)
                if ($Properties.name -notlike '*Footer*') { continue }
                $Other = $After.SelectSingleNode("//p:sp[p:nvSpPr/p:cNvPr[@id='$($Properties.id)']]", $Namespaces)
                if (-not $Other -or $Shape.OuterXml -cne $Other.OuterXml) { throw "Footer changed on slide $Number : $($Properties.id)" }
                $FooterCount++
            }
            $BeforeInventory = Get-SlideInventory $Source $Number
            $AfterInventory = Get-SlideInventory $Candidate $Number
            $BeforeTiming = @([regex]::Matches($BeforeInventory.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
            $AfterTiming = @([regex]::Matches($AfterInventory.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
            if (($BeforeTiming -join "`n") -cne ($AfterTiming -join "`n")) { throw "TIMING changed on slide $Number" }
            $TimingEvidence += [ordered]@{ slide = $Number; exact_lines = $AfterTiming; preserved = $true }
            if (-not $AfterInventory.notes.Trim()) { throw "Empty speaker notes on slide $Number" }
            $Targeted = @($Manifest.text_only_slides | Where-Object number -eq $Number)
            if ($Targeted.Count) {
                $Targeted = $Targeted[0]
                $ExpectedSlide = Set-TargetedPart $Source "ppt/slides/slide$Number.xml" $Targeted.replacements $Targeted.elements $Number
                $ExpectedNotes = Set-TargetedPart $Source "ppt/notesSlides/notesSlide$Number.xml" $Targeted.note_replacements @() $Number
                if ((Get-ByteHash $ExpectedSlide) -cne (Get-ByteHash (Get-PartBytes $Candidate "ppt/slides/slide$Number.xml")) -or
                    (Get-ByteHash $ExpectedNotes) -cne (Get-ByteHash (Get-PartBytes $Candidate "ppt/notesSlides/notesSlide$Number.xml"))) { throw "Targeted preservation failed on slide $Number" }
            }
            $NotesOnly = @($Manifest.notes_only | Where-Object number -eq $Number)
            if ($NotesOnly.Count) {
                $ExpectedNotes = Set-TargetedPart $Source "ppt/notesSlides/notesSlide$Number.xml" $NotesOnly[0].replacements @() $Number
                if ((Get-ByteHash $ExpectedNotes) -cne (Get-ByteHash (Get-PartBytes $Candidate "ppt/notesSlides/notesSlide$Number.xml"))) { throw "Notes-only preservation failed on slide $Number" }
            }
            $Spec = @($Manifest.slides | Where-Object number -eq $Number)
            if (-not $Spec.Count) { continue }
            $Spec = $Spec[0]
            $ExpectedSlide = Set-StorySlide $Source $Spec
            $ExpectedNotes = Set-StoryNotes $Source $Spec
            if ((Get-ByteHash $ExpectedSlide) -cne (Get-ByteHash (Get-PartBytes $Candidate "ppt/slides/slide$Number.xml")) -or
                (Get-ByteHash $ExpectedNotes) -cne (Get-ByteHash (Get-PartBytes $Candidate "ppt/notesSlides/notesSlide$Number.xml"))) {
                throw "Story content mismatch on slide $Number"
            }
            foreach ($Id in $Spec.keep_ids | Where-Object { $_ -notin @($Spec.headers.id) }) {
                $Selector = "//p:sp[p:nvSpPr/p:cNvPr[@id='$Id']]"
                if ($Before.SelectSingleNode($Selector, $Namespaces).OuterXml -cne $After.SelectSingleNode($Selector, $Namespaces).OuterXml) {
                    throw "Preserved shape $Id changed on slide $Number"
                }
            }
            foreach ($Element in $Spec.elements | Where-Object text) {
                $Selector = "//p:sp[p:nvSpPr/p:cNvPr[@name='Story-$Number-$($Element.key)']]"
                $Shape = $After.SelectSingleNode($Selector, $Namespaces)
                $Text = @($Shape.SelectNodes('.//a:t', $Namespaces) | ForEach-Object InnerText) -join "`n"
                if ($Text -cne $Element.text) { throw "Manifest text mismatch: $Number/$($Element.key)" }
            }
            foreach ($Text in @($Spec.script) + @($Spec.caveats) + @($Spec.sources) + @($Spec.diagram)) {
                if (-not $AfterInventory.notes.Contains($Text)) { throw "Missing notes claim on slide $Number : $Text" }
            }
            $TextEvidence += [ordered]@{ slide = $Number; elements_verified = @($Spec.elements | Where-Object text).Count; notes_and_sources_verified = $true }
        }
        if ($Actions -ne 27) { throw "Expected 27 Last Slide Viewed actions, got $Actions" }
        return [ordered]@{
            status = 'package-and-content-checks-passed'; input_sha256 = (Get-FileHash $InputPath -Algorithm SHA256).Hash.ToLowerInvariant()
            candidate_sha256 = (Get-FileHash $CandidatePath -Algorithm SHA256).Hash.ToLowerInvariant()
            member_count = $SourceNames.Count; unchanged_member_count = $SourceNames.Count - $Changed.Count; changed_members = $Changed
            slides = 54; nonempty_notes = 54; last_slide_viewed_actions = $Actions; all_navigation_actions_unchanged = $true
            exact_preserved_footer_shapes = $FooterCount
            legal_caption_exception = [ordered]@{ slide = 51; shape_id = 19627; before = $LegalBefore; after = $LegalAfter; text_only = $true }
            presentation_order_sections_relationships_unchanged = $true; preserved_cost_slides = @(6, 11, 21, 32, 36, 52)
            unchanged_autonomy_slide = 41; timing = $TimingEvidence; manifest_text = $TextEvidence
        }
    } finally { $Source.Dispose(); $Candidate.Dispose() }
}

function Invoke-StoryBuild {
    param([string]$InputPath, [string]$Output, $Manifest)
    $Archive = [IO.Compression.ZipFile]::OpenRead($InputPath)
    $Parts = @{}
    try {
        foreach ($Spec in $Manifest.slides) {
            $Parts["ppt/slides/slide$($Spec.number).xml"] = Set-StorySlide $Archive $Spec
            $Parts["ppt/notesSlides/notesSlide$($Spec.number).xml"] = Set-StoryNotes $Archive $Spec
        }
        foreach ($Spec in $Manifest.text_only_slides) {
            $Parts["ppt/slides/slide$($Spec.number).xml"] = Set-TargetedPart $Archive "ppt/slides/slide$($Spec.number).xml" $Spec.replacements $Spec.elements $Spec.number
            $Parts["ppt/notesSlides/notesSlide$($Spec.number).xml"] = Set-TargetedPart $Archive "ppt/notesSlides/notesSlide$($Spec.number).xml" $Spec.note_replacements @() $Spec.number
        }
        foreach ($Spec in $Manifest.notes_only) {
            $Parts["ppt/notesSlides/notesSlide$($Spec.number).xml"] = Set-TargetedPart $Archive "ppt/notesSlides/notesSlide$($Spec.number).xml" $Spec.replacements @() $Spec.number
        }
        $CandidatePath = Join-Path $Output 'zava-forward-story-review.pptx'
        $Stream = [IO.File]::Open($CandidatePath, [IO.FileMode]::Create)
        $Destination = [IO.Compression.ZipArchive]::new($Stream, [IO.Compression.ZipArchiveMode]::Create)
        try {
            foreach ($Entry in $Archive.Entries) {
                $NewEntry = $Destination.CreateEntry($Entry.FullName, [IO.Compression.CompressionLevel]::Optimal)
                $NewEntry.LastWriteTime = $Entry.LastWriteTime
                $NewEntry.ExternalAttributes = $Entry.ExternalAttributes
                $Target = $NewEntry.Open()
                try {
                    if ($Parts.ContainsKey($Entry.FullName)) { $Bytes = $Parts[$Entry.FullName]; $Target.Write($Bytes, 0, $Bytes.Length) }
                    else { $Original = $Entry.Open(); try { $Original.CopyTo($Target) } finally { $Original.Dispose() } }
                } finally { $Target.Dispose() }
            }
        } finally { $Destination.Dispose(); $Stream.Dispose() }
    } finally { $Archive.Dispose() }
    $Report = Test-StoryPackage $InputPath $CandidatePath $Manifest
    $Report | ConvertTo-Json -Depth 15 | Set-Content (Join-Path $Output 'build-report.json') -Encoding utf8
    Write-Output "Build passed: 54 slides, 54 notes, fifteen changed parts; $($Report.unchanged_member_count) member bytes unchanged; 27 return actions."
    Write-Output "Candidate: $CandidatePath"
    Write-Output "SHA256: $($Report.candidate_sha256)"
}

function Invoke-StoryRender {
    param([string]$InputPath, [string]$Output, $Manifest)
    if ($env:OS -ne 'Windows_NT') { throw 'Render requires Windows PowerShell and native PowerPoint COM' }
    $CandidatePath = Join-Path $Output 'zava-forward-story-review.pptx'
    $Report = Test-StoryPackage $InputPath $CandidatePath $Manifest
    $BuildReport = Get-Content (Join-Path $Output 'build-report.json') -Raw | ConvertFrom-Json
    if ($BuildReport.candidate_sha256 -cne $Report.candidate_sha256) { throw 'Candidate differs from the most recent Build' }
    $Native = Join-Path $Output 'native'
    [void][IO.Directory]::CreateDirectory($Native)
    $Scratch = Join-Path $env:TEMP ("zava-story-" + [Guid]::NewGuid().ToString('N'))
    [void][IO.Directory]::CreateDirectory($Scratch)
    $LocalCandidate = Join-Path $Scratch 'candidate.pptx'
    Copy-Item -LiteralPath $CandidatePath -Destination $LocalCandidate
    $Application = $null
    $Presentation = $null
    $Bounds = @()
    try {
        try { $Application = [Runtime.InteropServices.Marshal]::GetActiveObject('PowerPoint.Application') }
        catch { $Application = New-Object -ComObject PowerPoint.Application }
        $InitialPresentations = $Application.Presentations.Count
        $Presentation = $Application.Presentations.Open($LocalCandidate, -1, 0, 0)
        if ($Presentation.Slides.Count -ne 54) { throw 'Native PowerPoint did not open 54 slides' }
        foreach ($Slide in $Presentation.Slides) {
            $ImageName = 'slide-{0:D3}.png' -f $Slide.SlideIndex
            $LocalImage = Join-Path $Scratch $ImageName
            $Slide.Export($LocalImage, 'PNG', 2000, 1125)
            Copy-Item -LiteralPath $LocalImage -Destination (Join-Path $Native $ImageName)
            if ($Slide.SlideIndex -notin @(7, 8, 13, 15, 22, 39, 40, 51)) { continue }
            $StorySpec = @($Manifest.slides | Where-Object number -eq $Slide.SlideIndex)
            $HeaderIds = @()
            if ($StorySpec.Count) { $HeaderIds = @($StorySpec[0].headers | ForEach-Object { [int]$_.id }) }
            foreach ($Shape in $Slide.Shapes) {
                if (-not $Shape.HasTextFrame -or -not $Shape.TextFrame2.HasText) { continue }
                $Frame = $Shape.TextFrame2
                $Range = $Frame.TextRange
                $AvailableHeight = $Shape.Height - $Frame.MarginTop - $Frame.MarginBottom
                $AvailableWidth = $Shape.Width - $Frame.MarginLeft - $Frame.MarginRight
                $Bounds += [ordered]@{
                    slide = $Slide.SlideIndex; name = $Shape.Name; text = $Range.Text
                    box_points = @($Shape.Left, $Shape.Top, $Shape.Width, $Shape.Height)
                    bound_height = $Range.BoundHeight; available_height = $AvailableHeight
                    bound_width = $Range.BoundWidth; available_width = $AvailableWidth
                    overflow = ($Range.BoundHeight -gt $AvailableHeight + 0.75 -or $Range.BoundWidth -gt $AvailableWidth + 0.75)
                    new_shape = ($Shape.Name.StartsWith('Story-') -or
                        $Shape.Id -in $HeaderIds -or
                        ($Slide.SlideIndex -eq 15 -and $Shape.Id -in @(55656, 55715)) -or
                        ($Slide.SlideIndex -eq 51 -and $Shape.Id -eq 19627))
                }
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Range)
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Frame)
            }
        }
        $LocalPdf = Join-Path $Scratch 'zava-forward-story-review.pdf'
        $Presentation.SaveAs($LocalPdf, 32)
        $PdfPath = Join-Path $Output 'zava-forward-story-review.pdf'
        Copy-Item -LiteralPath $LocalPdf -Destination $PdfPath
        $Images = @(Get-ChildItem -LiteralPath $Native -Filter 'slide-*.png')
        if ($Images.Count -ne 54 -or -not (Test-Path -LiteralPath $PdfPath)) { throw 'Native export incomplete' }
        $RenderReport = [ordered]@{
            renderer = "Microsoft PowerPoint $($Application.Version) COM"; candidate_sha256 = $Report.candidate_sha256
            pdf_sha256 = (Get-FileHash $PdfPath -Algorithm SHA256).Hash.ToLowerInvariant(); native_slides = $Presentation.Slides.Count
            png_count = $Images.Count; initial_presentations = $InitialPresentations; bounds = $Bounds
            overflow_count = @($Bounds | Where-Object overflow).Count
            new_text_overflow_count = @($Bounds | Where-Object { $_.overflow -and $_.new_shape }).Count
            inherited_text_bound_warnings = @($Bounds | Where-Object { $_.overflow -and -not $_.new_shape }).Count
            independent_acceptance = $false
        }
        $RenderReport | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $Output 'render-report.json') -Encoding utf8
        Write-Output "Native Render: 54 PNGs and PDF; $($RenderReport.overflow_count) text-bound warnings."
        Write-Output "PDF SHA256: $($RenderReport.pdf_sha256)"
    } finally {
        if ($Presentation) { $Presentation.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Presentation) }
        if ($Application) { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Application) }
        if (Test-Path -LiteralPath $Scratch) { Remove-Item -LiteralPath $Scratch -Recurse -Force }
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).ProviderPath
    $Output = [IO.Path]::GetFullPath($OutputDir)
    $Prefix = $RepoRoot.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if ($Output -eq $RepoRoot -or $Output.StartsWith($Prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'OutputDir must be external to the repository'
    }
    $Ancestor = $Output
    while ($Ancestor) {
        if (Test-Path -LiteralPath $Ancestor) {
            $Item = Get-Item -LiteralPath $Ancestor -Force
            if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'OutputDir must not traverse links' }
            if (-not $Item.PSIsContainer) { throw 'OutputDir ancestors must be directories' }
        }
        $Ancestor = [IO.Path]::GetDirectoryName($Ancestor)
    }
    [void][IO.Directory]::CreateDirectory($Output)
    $InputPath = Join-Path $RepoRoot 'docs/capstone/deck/zava-forward-cowork-v2-draft.pptx'
    if ($SourcePath) { $InputPath = (Resolve-Path -LiteralPath $SourcePath).ProviderPath }
    $ExpectedHash = '39659a3ad9974f802a8418177a9ca0ca8daf7478e71cd82d04cd7677d9ad2cc0'
    if ((Get-FileHash $InputPath -Algorithm SHA256).Hash.ToLowerInvariant() -cne $ExpectedHash) { throw 'Source SHA256 mismatch; refusing a different native deck' }
    if ($Action -ne 'Inspect') {
        $Manifest = Get-Content (Join-Path $PSScriptRoot 'content/story-review.json') -Raw | ConvertFrom-Json
        if ($Manifest.source_sha256 -cne $ExpectedHash -or (@($Manifest.slides.number | Sort-Object) -join ',') -ne '8,13,22,39,40' -or
            (@($Manifest.text_only_slides.number | Sort-Object) -join ',') -ne '15,51' -or
            (@($Manifest.notes_only.number) -join ',') -ne '7') { throw 'Manifest source or slide scope mismatch' }
        foreach ($Spec in $Manifest.slides) {
            foreach ($Source in $Spec.sources) {
                if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot $Source))) { throw "Missing evidence path: $Source" }
            }
        }
        if ($Action -eq 'Build') { Invoke-StoryBuild $InputPath $Output $Manifest }
        elseif ($Action -eq 'Verify') { Test-StoryPackage $InputPath (Join-Path $Output 'zava-forward-story-review.pptx') $Manifest | ConvertTo-Json -Depth 15 }
        else { Invoke-StoryRender $InputPath $Output $Manifest }
        return
    }
    $Archive = [IO.Compression.ZipFile]::OpenRead($InputPath)
    try {
        $Slides = @(1..54 | ForEach-Object { Get-SlideInventory $Archive $_ })
        $Inventory = [ordered]@{
            input_sha256 = (Get-FileHash $InputPath -Algorithm SHA256).Hash.ToLowerInvariant()
            slides = $Slides
        }
        $Inventory | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $Output 'inventory.json') -Encoding utf8
        foreach ($Slide in $Slides | Where-Object { $_.number -in @(8, 13, 22, 39, 40) }) {
            Write-Output "SLIDE $($Slide.number)"
            foreach ($Shape in $Slide.shapes | Where-Object text) {
                Write-Output "$($Shape.id) [$($Shape.box -join ',')] $($Shape.sizes -join ',') $($Shape.colors -join ',') :: $($Shape.text -replace "`n", ' / ')"
            }
            Write-Output ([regex]::Match($Slide.notes, '(?m)^TIMING:.*$').Value)
        }
        Write-Output "Inventory: $Output/inventory.json"
        Write-Output "Input SHA-256: $($Inventory.input_sha256)"
    } finally { $Archive.Dispose() }
}
