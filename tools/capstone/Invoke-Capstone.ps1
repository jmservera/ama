#!/usr/bin/env pwsh
#Requires -Version 7.4
<#
.SYNOPSIS
Export complete authoring inputs or build and verify the current capstone deck.
.DESCRIPTION
Uses a pinned native template, an ordered JSON manifest and explicit media files.
Reuses the existing native-shape authoring functions; all outputs are external.
.PARAMETER Action
ExportSource creates inputs. Build and Verify use them; Render uses PowerPoint.
.PARAMETER RepoRoot
Repository containing docs/capstone/source.
.PARAMETER OutputDir
External directory for generated files and verification receipts.
.EXAMPLE
./Invoke-Capstone.ps1 -Action Build -RepoRoot . -OutputDir C:/scratch/capstone-run
.NOTES
No deployment, model call, publication, rubric score or canonical overwrite.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('ExportSource', 'Build', 'Verify', 'Render')]
    [string]$Action,
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$RepoRoot,
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputDir
)
$ErrorActionPreference = 'Stop'

function Get-CanonicalSourceHash {
    param([string]$Path)
    $Encoding = [Text.UTF8Encoding]::new($false, $true)
    $Text = $Encoding.GetString([IO.File]::ReadAllBytes($Path))
    $Text = $Text.Replace("`r`n", "`n").Replace("`r", "`n")
    return Get-ByteHash $Encoding.GetBytes($Text)
}

function Resolve-LocalInput {
    param([string]$Root, [string]$Relative)
    if ([IO.Path]::IsPathRooted($Relative) -or $Relative -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Input path must be relative without traversal' }
    $Path = [IO.Path]::GetFullPath((Join-Path $Root $Relative))
    $Ancestor = $Path
    while ($Ancestor -and $Ancestor -ne $Root) {
        $Item = Get-Item -LiteralPath $Ancestor -Force
        if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Input must not traverse links: $Relative" }
        $Ancestor = [IO.Path]::GetDirectoryName($Ancestor)
    }
    return $Path
}

function Get-MediaUsage {
    param($Archive, [string]$Part, $Definition = $null)
    $Used = @()
    foreach ($Number in 1..55) {
        $Entry = $Archive.GetEntry("ppt/slides/_rels/slide$Number.xml.rels")
        if (-not $Entry) { continue }
        $Relationships = Get-PartDocument $Archive $Entry.FullName
        foreach ($Relationship in $Relationships.DocumentElement.ChildNodes) {
            if ($Relationship.TargetMode -eq 'External') { continue }
            $Target = [Uri]::new([Uri]"https://package/ppt/slides/slide$Number.xml", [string]$Relationship.Target).AbsolutePath.TrimStart('/')
            if ($Target -ceq $Part) {
                $Physical = $Number
                if ($Definition.insertion) { $Physical = @($Definition.slides | Where-Object part_number -eq $Number)[0].number }
                $Used += $Physical
                break
            }
        }
    }
    return @($Used)
}

function Get-DeckPartNumber {
    param($Slide)
    if ($Slide.part_number) { return [int]$Slide.part_number }
    return [int]$Slide.number
}

function Get-DeckTemplateNumber {
    param($Slide)
    if ($Slide.baseline_number) { return [int]$Slide.baseline_number }
    return [int]$Slide.number
}

function Assert-DeckDefinition {
    param($Definition)
    if ($Definition.baseline -cne 'baseline.pptx') { throw 'Expected the pinned baseline' }
    if ($Definition.schema_version -eq 1) {
        if ($Definition.slide_count -ne 54 -or $Definition.slides.Count -ne 54 -or
            (@($Definition.slides.number) -join ',') -cne ((1..54) -join ',') -or $Definition.insertion) {
            throw 'Expected the complete ordered 54-slide manifest'
        }
        return
    }
    $Insertion = $Definition.insertion
    if ($Definition.schema_version -ne 2 -or $Definition.slide_count -ne 55 -or
        $Definition.slides.Count -ne 55 -or (@($Definition.slides.number) -join ',') -cne ((1..55) -join ',') -or
        $Insertion.after_baseline_slide -ne 12 -or $Insertion.template_slide -ne 12 -or
        $Insertion.new_part_number -ne 55 -or $Insertion.code -cne 'S11A' -or $Insertion.narration_seconds -ne 45) {
        throw 'Only the declared single deployment-slide insertion is supported'
    }
    foreach ($Slide in $Definition.slides) {
        $Part = $Slide.number
        if ($Slide.number -eq 13) { $Part = 55 }
        elseif ($Slide.number -gt 13) { $Part-- }
        $Template = $Part
        if ($Part -eq 55) { $Template = 12 }
        if ($Slide.part_number -ne $Part -or $Slide.baseline_number -ne $Template) { throw 'Baseline slide mapping changed' }
        if ($Part -eq 55 -and ($Slide.code -cne 'S11A' -or $Slide.layout -cne 'native' -or
            $Slide.images.Count -ne 1 -or $Slide.images[0].asset -cne 'architecture-azure-deployment' -or
            $Slide.notes -notmatch '(?m)^TIMING: 45 s')) { throw 'Inserted deployment-slide contract changed' }
        if ($Part -eq 55) {
            $ExpectedTiming = 'TIMING: 45 s for this added main-route slide · 11:40-12:25 on the 24:30 narration clock.'
            $NoteTiming = @([regex]::Matches($Slide.notes, '(?m)^TIMING:.*$') | ForEach-Object Value) -join "`n"
            $RevisedTiming = @($Slide.revised_notes | Where-Object { $_ -like 'TIMING:*' }) -join "`n"
            if ($NoteTiming -cne $ExpectedTiming -or $RevisedTiming -cne $ExpectedTiming) { throw 'Inserted deployment timing changed' }
        }
    }
}

function Get-InsertionParts {
    param($Archive, $Definition)
    $Parts = @{}
    if (-not $Definition.insertion) { return ,$Parts }
    # Keep every old slide/notes part, ID, action and destination. Add only slide55,
    # its notes/relationships, and the four exact structural metadata members.
    $Presentation = Get-PartDocument $Archive 'ppt/presentation.xml'
    $Namespaces = Get-Namespaces $Presentation
    $Namespaces.AddNamespace('p14', 'http://schemas.microsoft.com/office/powerpoint/2010/main')
    $RelationshipNamespace = 'http://schemas.openxmlformats.org/package/2006/relationships'
    $List = $Presentation.SelectSingleNode('/p:presentation/p:sldIdLst', $Namespaces)
    if ($List.ChildNodes.Count -ne 54) { throw 'Insertion requires the immutable 54-slide baseline' }
    $Anchor = $List.ChildNodes[11]
    $Id = ([long]($List.ChildNodes | ForEach-Object { [long]$_.GetAttribute('id') } | Measure-Object -Maximum).Maximum) + 1
    $New = $Presentation.CreateElement('p', 'sldId', $Namespaces.LookupNamespace('p'))
    $New.SetAttribute('id', [string]$Id)
    [void]$New.SetAttribute('id', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'rIdDeployment55')
    [void]$List.InsertAfter($New, $Anchor)
    $SectionAnchor = $Presentation.SelectSingleNode("//p14:section/p14:sldIdLst/p14:sldId[@id='$($Anchor.GetAttribute('id'))']", $Namespaces)
    if (-not $SectionAnchor) { throw 'Deployment template is missing its native section' }
    $SectionId = $Presentation.CreateElement('p14', 'sldId', $Namespaces.LookupNamespace('p14'))
    $SectionId.SetAttribute('id', [string]$Id)
    [void]$SectionAnchor.ParentNode.InsertAfter($SectionId, $SectionAnchor)
    $Parts['ppt/presentation.xml'] = Get-XmlBytes $Presentation
    $Relationships = Get-PartDocument $Archive 'ppt/_rels/presentation.xml.rels'
    if ($Relationships.DocumentElement.ChildNodes | Where-Object Id -CEQ 'rIdDeployment55') { throw 'Insertion relationship collision' }
    $Relationship = $Relationships.CreateElement('Relationship', $RelationshipNamespace)
    $Relationship.SetAttribute('Id', 'rIdDeployment55')
    $Relationship.SetAttribute('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
    $Relationship.SetAttribute('Target', 'slides/slide55.xml')
    [void]$Relationships.DocumentElement.AppendChild($Relationship)
    $Parts['ppt/_rels/presentation.xml.rels'] = Get-XmlBytes $Relationships
    foreach ($Pair in @(
        @('ppt/slides/_rels/slide12.xml.rels', 'ppt/slides/_rels/slide55.xml.rels', '/notesSlide', '../notesSlides/notesSlide55.xml'),
        @('ppt/notesSlides/_rels/notesSlide12.xml.rels', 'ppt/notesSlides/_rels/notesSlide55.xml.rels', '/slide', '../slides/slide55.xml')
    )) {
        $Document = Get-PartDocument $Archive $Pair[0]
        $Matches = @($Document.DocumentElement.ChildNodes | Where-Object { $_.Type.EndsWith($Pair[2]) })
        if ($Matches.Count -ne 1) { throw 'Template slide/notes relationship is ambiguous' }
        $Matches[0].SetAttribute('Target', $Pair[3])
        $Parts[$Pair[1]] = Get-XmlBytes $Document
    }
    $Types = Get-PartDocument $Archive '[Content_Types].xml'
    foreach ($Pair in @(
        @('/ppt/slides/slide55.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'),
        @('/ppt/notesSlides/notesSlide55.xml', 'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
    )) {
        $Override = $Types.CreateElement('Override', $Types.DocumentElement.NamespaceURI)
        $Override.SetAttribute('PartName', $Pair[0])
        $Override.SetAttribute('ContentType', $Pair[1])
        [void]$Types.DocumentElement.AppendChild($Override)
    }
    $Parts['[Content_Types].xml'] = Get-XmlBytes $Types
    $App = Get-PartDocument $Archive 'docProps/app.xml'
    $AppNamespaces = [Xml.XmlNamespaceManager]::new($App.NameTable)
    $AppNamespaces.AddNamespace('ep', $App.DocumentElement.NamespaceURI)
    $AppNamespaces.AddNamespace('vt', 'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes')
    foreach ($Name in @('Slides', 'Notes')) { $App.SelectSingleNode("/ep:Properties/ep:$Name", $AppNamespaces).InnerText = '55' }
    $Count = $App.SelectSingleNode("//vt:variant[vt:lpstr='Slide Titles']/following-sibling::vt:variant[1]/vt:i4", $AppNamespaces)
    if ($Count.InnerText -cne '54') { throw 'Unexpected native slide-title count' }
    $Count.InnerText = '55'
    $Titles = $App.SelectSingleNode('/ep:Properties/ep:TitlesOfParts/vt:vector', $AppNamespaces)
    if ($Titles.size -cne '57') { throw 'Unexpected native titles vector' }
    $Title = $App.CreateElement('vt', 'lpstr', $AppNamespaces.LookupNamespace('vt'))
    $Title.InnerText = $Definition.slides[12].title
    [void]$Titles.InsertAfter($Title, $Titles.ChildNodes[14])
    $Titles.SetAttribute('size', '58')
    $Parts['docProps/app.xml'] = Get-XmlBytes $App
    return ,$Parts
}

function Convert-BaselineSlideNumber {
    param([string]$Value)
    $Number = [int]$Value
    if ($Number -ge 13 -and $Number -le 54) { $Number++ }
    return [string]$Number
}

function Update-BaselineNavigationNumbers {
    param([string]$Text)
    # One baseline-to-physical mapping for page/slide/index references, with or
    # without a space and with range endpoints; delimiters are preserved.
    return [regex]::Replace($Text, '(?i)\b(pages?|slides?|index)( ?)(\d+)(?:([-\u2013/])(\d+))?\b', {
        param($Match)
        $Result = $Match.Groups[1].Value + $Match.Groups[2].Value + (Convert-BaselineSlideNumber $Match.Groups[3].Value)
        if ($Match.Groups[4].Success) { $Result += $Match.Groups[4].Value + (Convert-BaselineSlideNumber $Match.Groups[5].Value) }
        return $Result
    })
}

function Update-RouteNote {
    param([string]$Text, [int]$PartNumber, $Definition)
    if (-not $Definition.insertion) { return $Text }
    if ($PartNumber -ne 55) { $Text = Update-BaselineNavigationNumbers $Text }
    if ($PartNumber -le 26) {
        $Timing = [regex]::Match($Text, '(?m)^TIMING: (\d+) s.*?(\d\d):(\d\d)-(\d\d):(\d\d)')
        if (-not $Timing.Success) { throw 'Main-route timing source is missing' }
        $Start = [int]$Timing.Groups[2].Value * 60 + [int]$Timing.Groups[3].Value
        $End = [int]$Timing.Groups[4].Value * 60 + [int]$Timing.Groups[5].Value
        if ($PartNumber -ge 13) { $Start += 45; $End += 45 }
        $Window = ('{0:00}:{1:00}-{2:00}:{3:00}' -f [Math]::Floor($Start / 60), ($Start % 60), [Math]::Floor($End / 60), ($End % 60))
        $Text += "`nCURRENT ROUTE TIMING: $($Timing.Groups[1].Value) s (builds share one slot); $Window on the 24:30 clock. Original TIMING is retained source provenance."
    }
    return $Text
}

function Update-VisibleNavigation {
    param([byte[]]$Bytes, [int]$PartNumber, $Definition)
    if (-not $Definition.insertion -or $PartNumber -lt 27 -or $PartNumber -gt 54) { return ,$Bytes }
    $Document = [xml]::new()
    $Document.PreserveWhitespace = $true
    $Document.LoadXml([Text.Encoding]::UTF8.GetString($Bytes))
    $Namespaces = Get-Namespaces $Document
    foreach ($Text in $Document.SelectNodes('//a:t', $Namespaces)) {
        # Only the baseline's explicit index/topic/answer numbering labels.
        # No financial text, question wording, font, geometry or action changes.
        if ($Text.InnerText -match '^(?:QX · slide |B\d\d · Index: slide |Topic: S\d\d / slide )\d+$') {
            $Text.InnerText = [regex]::Replace($Text.InnerText, '\d+$', {
                param($Match)
                $Number = [int]$Match.Value
                if ($Number -ge 13) { $Number++ }
                return [string]$Number
            })
        } elseif ($PartNumber -eq 27 -and $Text.InnerText -match '^B\d\d · \d+\s') {
            $Text.InnerText = [regex]::Replace($Text.InnerText, '^(B\d\d · )(\d+)', {
                param($Match)
                return $Match.Groups[1].Value + [string]([int]$Match.Groups[2].Value + 1)
            })
        }
    }
    return ,(Get-XmlBytes $Document)
}

function Export-AuthoringSource {
    param([string]$TemplatePath, [string]$Output)
    $SourceRoot = Join-Path $Output 'source'
    if (Test-Path -LiteralPath $SourceRoot) { throw 'ExportSource requires a new source output directory' }
    [void][IO.Directory]::CreateDirectory((Join-Path $SourceRoot 'assets/media'))
    $Archive = [IO.Compression.ZipFile]::OpenRead($TemplatePath)
    try {
        $Slides = @(foreach ($Number in 1..54) {
            $Inventory = Get-SlideInventory $Archive $Number
            $Heading = ($Inventory.notes -split "`n")[0] -split ' \| ', 2
            [ordered]@{
                number = $Number; code = $Heading[0]; title = $Heading[-1]
                layout = 'baseline'; notes = $Inventory.notes
            }
        })
        $Media = @(foreach ($Entry in $Archive.Entries | Where-Object FullName -like 'ppt/media/*') {
            if ($Entry.FullName -notmatch '^ppt/media/[^/]+$') { throw 'Unexpected nested media path' }
            $Bytes = Get-PartBytes $Archive $Entry.FullName
            $Relative = 'assets/media/' + [IO.Path]::GetFileName($Entry.FullName)
            [IO.File]::WriteAllBytes((Join-Path $SourceRoot $Relative), $Bytes)
            [ordered]@{
                part = $Entry.FullName; path = $Relative; sha256 = Get-ByteHash $Bytes
                slides = @(Get-MediaUsage $Archive $Entry.FullName)
                provenance = 'Owner-supplied native Cowork deck. Embedded source bytes retained; individual original URL, prompt and licence are not established by extraction.'
                clearance = 'Repository clearance was recorded for the supplied Cowork outputs; no new external-publication clearance is inferred.'
            }
        })
        [ordered]@{
            schema_version = 1; baseline = 'baseline.pptx'
            baseline_sha256 = (Get-FileHash $TemplatePath -Algorithm SHA256).Hash.ToLowerInvariant()
            assets = 'assets/catalog.json'; slide_count = 54; slides = $Slides
        } | ConvertTo-Json -Depth 20 | Set-Content (Join-Path $SourceRoot 'slides.json') -Encoding utf8NoBOM
        [ordered]@{ schema_version = 1; media = $Media } | ConvertTo-Json -Depth 10 |
            Set-Content (Join-Path $SourceRoot 'assets/catalog.json') -Encoding utf8NoBOM
        Write-Output "Exported 54 slide definitions/notes and $($Media.Count) original embedded assets. Native template owns baseline layouts."
    } finally { $Archive.Dispose() }
}

    function Update-NavigationNote {
        param([string]$Text)
        $Current = 'NAVIGATION: Native buttons retain fixed slide-jump destinations, not Last Slide Viewed. Return deliberately to the actual interrupted page; the Topic button has a fixed destination. PDF reader history is viewer-specific.'
        $Text = [regex]::Replace($Text, '(?m)^NAVIGATION \(PR438 correction\):[^\r\n]*', $Current)
        $Text = $Text.Replace('Return to caller uses Last Slide Viewed; separate topic link S18 slide 21 only for index entry.', 'Native buttons use fixed slide jumps, not dynamic caller return. Navigate deliberately to the interrupted page; topic S18 slide 21 is fixed.')
        $Text = $Text.Replace('Return to caller: Last Slide Viewed; separate topic S10 slide 11 for index entry only.', 'Native buttons use fixed slide jumps, not dynamic caller return. Navigate deliberately to the interrupted page; topic S10 slide 11 is fixed.')
        $Text = $Text.Replace('Return to caller via Last Slide Viewed; fixed topic S18 slide 21 only for index entry.', 'Native buttons use fixed slide jumps, not dynamic caller return. Navigate deliberately to the interrupted page; topic S18 slide 21 is fixed.')
        return $Text
    }

function Test-CostStatusRevision {
    param($Definition)
    if (-not $Definition.cost_status_revision) { return $false }
    if ($Definition.cost_status_revision -cne 'owner-approved-2026-11-08-status-only') {
        throw 'Unrecognised protected cost-status revision'
    }
    return $true
}

function Get-CostStatusReplacements {
    param([int]$Number)
    if ($Number -eq 21) {
        return @(
            [pscustomobject]@{ id = 63877; from = 'controls proposed'; to = 'controls coded' }
            [pscustomobject]@{ id = 64007; from = 'IN PLACE'; to = 'CODED' }
            [pscustomobject]@{ id = 64042; from = 'NEXT'; to = 'HELD' }
            [pscustomobject]@{ id = 64061; from = 'proposed money budgets per task and period'; to = 'coded money budgets per task and period' }
        )
    }
    if ($Number -eq 52) {
        return @(
            [pscustomobject]@{ id = 21807; from = 'DESIGNED · NEXT MILESTONE'; to = 'SOURCE-CODED · GATED' }
            [pscustomobject]@{ id = 21877; from = 'Not hard currency or request-depth limits.'; to = 'Coded money / request-depth admission.' }
            [pscustomobject]@{ id = 21897; from = 'Proposed: not run'; to = 'Live gates: not run' }
            [pscustomobject]@{ id = 21918; from = 'Complete attribution; task/period money stops'; to = 'Full attribution; live money-stop proof' }
            [pscustomobject]@{ id = 21918; from = 'Request/depth bounds; billing reconciliation.'; to = 'Request-bound proof; billing reconciliation.' }
        )
    }
    return @()
}

function Update-CostStatusNote {
    param([string]$Text, [int]$Number, [bool]$Enabled)
    if (-not $Enabled) { return $Text }
    $From = $null
    $To = $null
    if ($Number -eq 21) {
        $From = 'Complete metering and task, period and request-depth controls remain proposed.'
        $To = 'Task/period money and root call/depth admission are source-coded; live approval and full billing remain unproved.'
    } elseif ($Number -eq 52) {
        $From = 'Complete attribution, task/period monetary budgets with hard termination, per-request calls/depth and billing reconciliation are proposed'
        $To = 'Task/period monetary and root call/depth admission are source-coded; complete attribution and billing reconciliation remain unproved'
    }
    if (-not $From) { return $Text }
    if ($From -match '\d|\b(?:USD|GBP|EUR)\b' -or $To -match '\d|\b(?:USD|GBP|EUR)\b') {
        throw 'Cost-status note substitution must not contain financial numbers or currencies'
    }
    if (($Text.Split(@([string]$From), [StringSplitOptions]::None).Count - 1) -ne 1) {
        throw "Expected one fixed cost-status note fragment on page $Number"
    }
    return $Text.Replace($From, $To)
}

function Assert-CostSlide {
    param($BaselineArchive, $CandidateArchive, [int]$Number, [bool]$StatusRevision, $Definition = $null)
    $Name = "ppt/slides/slide$Number.xml"
    $Before = Get-PartBytes $BaselineArchive $Name
    $Expected = $Before
    if ($StatusRevision -and $Number -in @(21, 52)) {
        $Replacements = @(Get-CostStatusReplacements $Number)
        foreach ($Replacement in $Replacements) {
            if ($Replacement.from -match '\d|\b(?:USD|GBP|EUR)\b' -or $Replacement.to -match '\d|\b(?:USD|GBP|EUR)\b') {
                throw 'Cost-status substitutions must not contain financial numbers or currencies'
            }
        }
        $Expected = Set-TargetedPart $BaselineArchive $Name $Replacements @() $Number
    }
    $StatusUpdated = ((Get-ByteHash $Before) -cne (Get-ByteHash $Expected))
    $BeforeNavigation = $Expected
    $Expected = Update-VisibleNavigation $Expected $Number $Definition
    $Actual = Get-PartBytes $CandidateArchive $Name
    if ((Get-ByteHash $Expected) -cne (Get-ByteHash $Actual)) {
        throw "Protected cost slide changed beyond the fixed approved status words: $Number"
    }
    $BeforeCost = Get-SlideInventory $BaselineArchive $Number
    $AfterCost = Get-SlideInventory $CandidateArchive $Number
    $ExpectedNotes = Update-CostStatusNote (Update-NavigationNote $BeforeCost.notes) $Number $StatusRevision
    $ExpectedNotes = Update-RouteNote $ExpectedNotes $Number $Definition
    if ($AfterCost.notes -cne $ExpectedNotes) {
        throw "Protected cost note changed beyond fixed navigation/status corrections: $Number"
    }
    return [pscustomobject]@{
        status_updated = $StatusUpdated
        navigation_labels_updated = ((Get-ByteHash $BeforeNavigation) -cne (Get-ByteHash $Expected))
        notes_updated = ($AfterCost.notes -cne $BeforeCost.notes)
    }
}

    function Get-DeckRevision {
    param($Archive, $Definition, [string]$Root)
    $Parts = Get-InsertionParts $Archive $Definition
    $CostStatusRevision = Test-CostStatusRevision $Definition
    foreach ($Slide in $Definition.slides) {
        if ($Slide.revised_notes) {
            $NoteCode = ([string]$Slide.revised_notes[0] -split ' \| ', 2)[0]
            if ($NoteCode -cne $Slide.code) { throw "Revised notes ID $NoteCode does not match page $($Slide.number)/$($Slide.code)" }
        }
        foreach ($Source in @($Slide.sources)) {
            if ($Source) { [void](Resolve-LocalInput $RepoRoot $Source) }
        }
        $PartNumber = Get-DeckPartNumber $Slide
        $TemplateNumber = Get-DeckTemplateNumber $Slide
        $Name = "ppt/slides/slide$PartNumber.xml"
        if ($Slide.layout -eq 'native') { $Parts[$Name] = Set-StorySlide $Archive $Slide $TemplateNumber }
        elseif ($Slide.layout -eq 'text') {
            $Parts[$Name] = Set-TargetedPart $Archive $Name $Slide.replacements @() $Slide.number
            foreach ($Replacement in $Slide.replacements | Where-Object { $_.box }) {
                $Box = @($Replacement.box)
                if (-not $Replacement.id -or $Box.Count -ne 4 -or $Box[0] -lt 0.5 -or $Box[1] -lt 0.5 -or
                    $Box[2] -le 0 -or $Box[3] -le 0 -or $Box[0] + $Box[2] -gt 12.834 -or $Box[1] + $Box[3] -gt 7.0) {
                    throw 'Text-only bounds correction is invalid'
                }
                $TextDocument = [xml]::new()
                $TextDocument.PreserveWhitespace = $true
                $TextDocument.LoadXml([Text.Encoding]::UTF8.GetString($Parts[$Name]))
                $TextNamespaces = Get-Namespaces $TextDocument
                $Shape = $TextDocument.SelectSingleNode("//p:sp[p:nvSpPr/p:cNvPr[@id='$($Replacement.id)']]", $TextNamespaces)
                if (-not $Shape) { throw 'Text bounds target missing' }
                $Transform = $Shape.SelectSingleNode('p:spPr/a:xfrm', $TextNamespaces)
                $Offset = $Transform.SelectSingleNode('a:off', $TextNamespaces)
                $Extent = $Transform.SelectSingleNode('a:ext', $TextNamespaces)
                $Offset.SetAttribute('x', [string][int][Math]::Round($Box[0] * 914400))
                $Offset.SetAttribute('y', [string][int][Math]::Round($Box[1] * 914400))
                $Extent.SetAttribute('cx', [string][int][Math]::Round($Box[2] * 914400))
                $Extent.SetAttribute('cy', [string][int][Math]::Round($Box[3] * 914400))
                $Parts[$Name] = Get-XmlBytes $TextDocument
            }
        }
        elseif ($Slide.layout -ne 'baseline') { throw "Unsupported slide layout: $($Slide.layout)" }
        if ($CostStatusRevision -and $PartNumber -in @(21, 52)) {
            if ($Slide.layout -cne 'baseline' -or $Slide.images) {
                throw 'Protected cost-status pages must retain their complete baseline layouts'
            }
            $Parts[$Name] = Set-TargetedPart $Archive $Name @(Get-CostStatusReplacements $PartNumber) @() $Slide.number
        }
        if ($Definition.insertion -and $PartNumber -ge 27 -and $PartNumber -le 54) {
            $Bytes = Get-PartBytes $Archive $Name
            if ($Parts.ContainsKey($Name)) { $Bytes = $Parts[$Name] }
            $Parts[$Name] = Update-VisibleNavigation $Bytes $PartNumber $Definition
        }
        $Before = Get-SlideInventory $Archive $TemplateNumber
        $Text = $Slide.notes
        if ($Slide.revised_notes) { $Text = @($Slide.revised_notes) -join "`n" }
        $Text = Update-NavigationNote $Text
        $Text = Update-CostStatusNote $Text $PartNumber $CostStatusRevision
        if ($Before.notes -ceq $Text -and -not $Definition.insertion) { continue }
        $Timing = @([regex]::Matches($Before.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
        $NewTiming = @([regex]::Matches($Text, '(?m)^TIMING:.*$') | ForEach-Object Value)
        if ($PartNumber -ne 55) {
            if (-not $NewTiming.Count -and $Timing.Count) { $Text += "`n" + ($Timing -join "`n") }
            elseif (($Timing -join "`n") -cne ($NewTiming -join "`n")) { throw "Timing changed on slide $($Slide.number)" }
        }
        $Text = Update-RouteNote $Text $PartNumber $Definition
        $NoteName = "ppt/notesSlides/notesSlide$PartNumber.xml"
        $Document = Get-PartDocument $Archive "ppt/notesSlides/notesSlide$TemplateNumber.xml"
        $Namespaces = Get-Namespaces $Document
        $Body = $Document.SelectSingleNode("//p:sp[p:nvSpPr/p:nvPr/p:ph[@type='body']]/p:txBody", $Namespaces)
        foreach ($Paragraph in @($Body.SelectNodes('a:p', $Namespaces))) { [void]$Body.RemoveChild($Paragraph) }
        foreach ($Line in $Text -split "`n") { Add-TextParagraph $Document $Body $Line 12 '000000' }
        $Parts[$NoteName] = Get-XmlBytes $Document
    }
    $Catalog = Get-Content -LiteralPath (Resolve-LocalInput $Root $Definition.assets) -Raw | ConvertFrom-Json
    $TemplateMedia = @($Archive.Entries.FullName | Where-Object { $_ -like 'ppt/media/*' } | Sort-Object)
    $InputMedia = @($Catalog.media.part | Sort-Object)
    if ($InputMedia.Count -ne @($InputMedia | Select-Object -Unique).Count -or
        @(Compare-Object $TemplateMedia $InputMedia).Count) { throw 'Asset catalog must cover every template media member exactly once' }
    foreach ($Asset in $Catalog.media) {
        $Path = Resolve-LocalInput $Root $Asset.path
        $Bytes = [IO.File]::ReadAllBytes($Path)
        if ((Get-ByteHash $Bytes) -cne $Asset.sha256) { throw "Asset SHA256 mismatch: $($Asset.path)" }
        $Usage = @(Get-MediaUsage $Archive $Asset.part)
        if (($Usage -join ',') -cne (@($Asset.slides) -join ',')) { throw "Asset usage mismatch: $($Asset.part)" }
        $Parts[$Asset.part] = $Bytes
    }
    $Additional = @($Catalog.additional_media | Where-Object { $_ })
    if (@($Additional.id | Select-Object -Unique).Count -ne $Additional.Count -or
        @($Additional.part | Select-Object -Unique).Count -ne $Additional.Count) { throw 'Duplicate additional-media identity' }
    foreach ($Asset in $Additional) {
        if ($Asset.id -cnotmatch '^[a-z][a-z0-9-]*$' -or $Asset.part -cnotmatch '^ppt/media/(roadmap|journey)-[a-z0-9-]+\.png$' -or
            $Archive.GetEntry($Asset.part)) { throw 'Invalid or colliding additional-media part' }
        $Bytes = [IO.File]::ReadAllBytes((Resolve-LocalInput $Root $Asset.path))
        if ((Get-ByteHash $Bytes) -cne $Asset.sha256) { throw "Additional media hash mismatch: $($Asset.id)" }
        if ($Asset.source_svg) {
            $VectorBytes = [IO.File]::ReadAllBytes((Resolve-LocalInput $Root $Asset.source_svg))
            if ((Get-ByteHash $VectorBytes) -cne $Asset.source_sha256) { throw "Original SVG hash mismatch: $($Asset.id)" }
        }
        if ($Asset.source_native) {
            $NativeBytes = [IO.File]::ReadAllBytes((Resolve-LocalInput $Root $Asset.source_native))
            if ((Get-ByteHash $NativeBytes) -cne $Asset.source_native_sha256) { throw "Editable diagram hash mismatch: $($Asset.id)" }
        }
        $Parts[$Asset.part] = $Bytes
    }
    foreach ($Slide in $Definition.slides | Where-Object { $_.images }) {
        $PartNumber = Get-DeckPartNumber $Slide
        $Name = "ppt/slides/slide$PartNumber.xml"
        $Document = Get-PartDocument $Archive "ppt/slides/slide$(Get-DeckTemplateNumber $Slide).xml"
        if ($Parts.ContainsKey($Name)) { $Document.LoadXml([Text.Encoding]::UTF8.GetString($Parts[$Name])) }
        $RelationshipName = "ppt/slides/_rels/slide$PartNumber.xml.rels"
        $Relationships = Get-PartDocument $Archive "ppt/slides/_rels/slide$(Get-DeckTemplateNumber $Slide).xml.rels"
        if ($Parts.ContainsKey($RelationshipName)) { $Relationships.LoadXml([Text.Encoding]::UTF8.GetString($Parts[$RelationshipName])) }
        Add-DeckImage $Document $Relationships $Slide.images $Additional $Slide.number
        $Parts[$Name] = Get-XmlBytes $Document
        $Parts[$RelationshipName] = Get-XmlBytes $Relationships
    }
    return ,$Parts
}

function Add-DeckImage {
    param([xml]$Document, [xml]$Relationships, $Images, $Assets, [int]$SlideNumber)
    $Namespaces = Get-Namespaces $Document
    $Tree = $Document.SelectSingleNode('/p:sld/p:cSld/p:spTree', $Namespaces)
    $Id = [Math]::Max(2000000, ([int]($Tree.SelectNodes('.//p:cNvPr', $Namespaces) | ForEach-Object { [int]$_.id } | Measure-Object -Maximum).Maximum) + 1)
    $RelationshipNamespace = 'http://schemas.openxmlformats.org/package/2006/relationships'
    foreach ($Image in $Images) {
        $Matches = @($Assets | Where-Object id -CEQ $Image.asset)
        if ($Matches.Count -ne 1 -or $SlideNumber -notin @($Matches[0].slides)) { throw 'Image is not in the approved asset/slide mapping' }
        $Asset = $Matches[0]
        $Box = @($Image.box)
        if ($Box.Count -ne 4 -or $Box[0] -lt 0.5 -or $Box[1] -lt 0.5 -or $Box[2] -le 0 -or $Box[3] -le 0 -or
            $Box[0] + $Box[2] -gt 12.834 -or $Box[1] + $Box[3] -gt 7.0 -or -not $Image.alt) { throw 'Image bounds or alternative text invalid' }
        if ($Asset.pixel_width -le 0 -or $Asset.pixel_height -le 0) { throw 'Image aspect ratio unavailable' }
        $Scale = [Math]::Min($Box[2] / $Asset.pixel_width, $Box[3] / $Asset.pixel_height)
        $Width = $Asset.pixel_width * $Scale
        $Height = $Asset.pixel_height * $Scale
        $Left = $Box[0] + ($Box[2] - $Width) / 2
        $Top = $Box[1] + ($Box[3] - $Height) / 2
        $RelationshipId = 'rIdRoadmap' + $Id
        if ($Relationships.DocumentElement.ChildNodes | Where-Object Id -CEQ $RelationshipId) { throw 'Image relationship collision' }
        $Relationship = $Relationships.CreateElement('Relationship', $RelationshipNamespace)
        $Relationship.SetAttribute('Id', $RelationshipId)
        $Relationship.SetAttribute('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
        $Relationship.SetAttribute('Target', '../media/' + [IO.Path]::GetFileName($Asset.part))
        [void]$Relationships.DocumentElement.AppendChild($Relationship)
        $Fragment = [xml]'<p:pic xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:nvPicPr><p:cNvPr id="1" name="Roadmap image"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="image"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="1" cy="1"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:ln><a:noFill/></a:ln></p:spPr></p:pic>'
        $Picture = $Document.ImportNode($Fragment.DocumentElement, $true)
        $Properties = $Picture.SelectSingleNode('p:nvPicPr/p:cNvPr', $Namespaces)
        $Properties.SetAttribute('id', [string]$Id)
        $Properties.SetAttribute('name', "Roadmap-$SlideNumber-$($Asset.id)")
        $Properties.SetAttribute('descr', [string]$Image.alt)
        [void]$Picture.SelectSingleNode('p:blipFill/a:blip', $Namespaces).SetAttribute('embed', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', $RelationshipId)
        $Offset = $Picture.SelectSingleNode('p:spPr/a:xfrm/a:off', $Namespaces)
        $Extent = $Picture.SelectSingleNode('p:spPr/a:xfrm/a:ext', $Namespaces)
        $Offset.SetAttribute('x', [string][int][Math]::Round($Left * 914400))
        $Offset.SetAttribute('y', [string][int][Math]::Round($Top * 914400))
        $Extent.SetAttribute('cx', [string][int][Math]::Round($Width * 914400))
        $Extent.SetAttribute('cy', [string][int][Math]::Round($Height * 914400))
        [void]$Tree.AppendChild($Picture)
        $Id++
    }
}

function Test-DeckCandidate {
    param($BaselineArchive, [string]$CandidatePath, $Parts, $Definition)
    $Candidate = [IO.Compression.ZipFile]::OpenRead($CandidatePath)
    try {
        $Names = @($BaselineArchive.Entries.FullName | Sort-Object)
        $Added = @($Parts.Keys | Where-Object { -not $BaselineArchive.GetEntry($_) } | Sort-Object)
        $ExpectedNames = @($Names + $Added | Sort-Object)
        $OtherNames = @($Candidate.Entries.FullName | Sort-Object)
        if ($ExpectedNames.Count -ne $OtherNames.Count -or @($OtherNames | Select-Object -Unique).Count -ne $OtherNames.Count -or
            @(Compare-Object $ExpectedNames $OtherNames).Count) { throw 'Package member set differs from explicit baseline and declared inputs' }
        $AllowedAdded = @(Get-Content -LiteralPath (Resolve-LocalInput $SourceRoot $Definition.assets) -Raw | ConvertFrom-Json).additional_media.part
        if ($Definition.insertion) {
            $AllowedAdded += @('ppt/slides/slide55.xml', 'ppt/slides/_rels/slide55.xml.rels',
                'ppt/notesSlides/notesSlide55.xml', 'ppt/notesSlides/_rels/notesSlide55.xml.rels')
        }
        if (($Added -join "`n") -cne (@($AllowedAdded | Sort-Object) -join "`n")) { throw 'Undeclared added package member' }
        $Changed = @()
        foreach ($Name in $ExpectedNames) {
            $Original = $null
            if ($BaselineArchive.GetEntry($Name)) { $Original = Get-PartBytes $BaselineArchive $Name }
            $Expected = $Original
            if ($Parts.ContainsKey($Name)) { $Expected = $Parts[$Name] }
            $Actual = Get-PartBytes $Candidate $Name
            if ((Get-ByteHash $Expected) -cne (Get-ByteHash $Actual)) { throw "Candidate content mismatch: $Name" }
            if ($null -eq $Original -or (Get-ByteHash $Original) -cne (Get-ByteHash $Actual)) { $Changed += $Name }
        }
        $Actions = 0
        $BaselineActions = 0
        foreach ($Slide in $Definition.slides) {
            $PartNumber = Get-DeckPartNumber $Slide
            $TemplateNumber = Get-DeckTemplateNumber $Slide
            $Before = Get-SlideInventory $BaselineArchive $TemplateNumber
            $After = Get-SlideInventory $Candidate $PartNumber
            if (-not $After.notes.Trim()) { throw "Empty notes on slide $($Slide.number)" }
            $BeforeTiming = @([regex]::Matches($Before.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
            $AfterTiming = @([regex]::Matches($After.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
            if ($PartNumber -ne 55 -and ($BeforeTiming -join "`n") -cne ($AfterTiming -join "`n")) { throw 'Timing preservation failed' }
            if (($Before.shapes.actions -join "`n") -cne ($After.shapes.actions -join "`n")) { throw 'Native navigation changed' }
            $Document = Get-PartDocument $Candidate "ppt/slides/slide$PartNumber.xml"
            $Ids = @($Document.SelectNodes('//p:cNvPr', (Get-Namespaces $Document)) | ForEach-Object id)
            if (@($Ids | Select-Object -Unique).Count -ne $Ids.Count) { throw 'Duplicate native shape IDs' }
            $Actions += @($Document.SelectNodes('//*[@action]')).Count
            $BaselineDocument = Get-PartDocument $BaselineArchive "ppt/slides/slide$TemplateNumber.xml"
            $BaselineActions += @($BaselineDocument.SelectNodes('//*[@action]')).Count
        }
        if ($Actions -ne $BaselineActions) { throw 'Native action count differs from the pinned current template' }
        $Presentation = Get-PartDocument $Candidate 'ppt/presentation.xml'
        $Namespaces = Get-Namespaces $Presentation
        $Relationships = Get-PartDocument $Candidate 'ppt/_rels/presentation.xml.rels'
        $Order = @($Presentation.SelectNodes('/p:presentation/p:sldIdLst/p:sldId', $Namespaces) | ForEach-Object {
            $Id = $_.GetAttribute('id', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
            @($Relationships.DocumentElement.ChildNodes | Where-Object Id -CEQ $Id)[0].Target
        })
        $ExpectedOrder = @($Definition.slides | ForEach-Object { "slides/slide$(Get-DeckPartNumber $_).xml" })
        if (($Order -join ',') -cne ($ExpectedOrder -join ',')) { throw 'Physical presentation order differs from manifest' }
        $CostNavigationUpdates = @()
        $CostStatusUpdates = @()
        $CostLabelUpdates = @()
        $CostStatusRevision = Test-CostStatusRevision $Definition
        foreach ($Number in @(6, 11, 21, 32, 36, 52)) {
            $CostResult = Assert-CostSlide $BaselineArchive $Candidate $Number $CostStatusRevision $Definition
            $Physical = $Number
            if ($Definition.insertion -and $Number -ge 13) { $Physical++ }
            if ($CostResult.status_updated) { $CostStatusUpdates += $Physical }
            if ($CostResult.navigation_labels_updated) { $CostLabelUpdates += $Physical }
            if ($CostResult.notes_updated -and $Physical -notin $CostStatusUpdates) { $CostNavigationUpdates += $Physical }
        }
        $Catalog = Get-Content -LiteralPath (Resolve-LocalInput $SourceRoot $Definition.assets) -Raw | ConvertFrom-Json
        foreach ($Asset in $Catalog.additional_media) {
            $ActualUsage = @(Get-MediaUsage $Candidate $Asset.part $Definition | Sort-Object -Unique)
            if (($ActualUsage -join ',') -cne (@($Asset.slides | Sort-Object -Unique) -join ',')) { throw "Additional media usage mismatch: $($Asset.id)" }
        }
        return [ordered]@{
            status = 'pass'; slides = $Definition.slide_count; nonempty_notes = $Definition.slide_count; navigation_actions = $Actions
            package_members = $ExpectedNames.Count; baseline_members = $Names.Count
            added_media_parts = @($Added | Where-Object { $_ -like 'ppt/media/*' })
            added_slide_parts = @($Added | Where-Object { $_ -notlike 'ppt/media/*' })
            changed_members = $Changed; timing_preserved = $true
            baseline_mapping_preserved = $true; physical_slide_order_verified = $true
            inserted_main_slide = $(if ($Definition.insertion) { 13 } else { $null })
            narration_seconds = $(if ($Definition.insertion) { 1470 } else { 1425 })
            native_navigation_preserved = $true; six_cost_slide_bytes_preserved = ($CostStatusUpdates.Count -eq 0 -and $CostLabelUpdates.Count -eq 0)
            cost_financial_evidence_preserved = $true; approved_cost_status_updates = $CostStatusUpdates
            cost_navigation_label_updates = $CostLabelUpdates
            cost_note_calculations_preserved = $true; cost_note_navigation_and_route_updates = $CostNavigationUpdates
            full_manifest_and_media_verified = $true; candidate_sha256 = (Get-FileHash $CandidatePath -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    } finally { $Candidate.Dispose() }
}

function Export-NativeDeck {
    param([string]$CandidatePath, [string]$Output, $Definition, $Report)
    if ($env:OS -ne 'Windows_NT') { throw 'Render requires native Windows PowerPoint COM' }
    $Native = Join-Path $Output 'native'
    [void][IO.Directory]::CreateDirectory($Native)
    $Application = $null
    $Presentation = $null
    $Bounds = @()
    try {
        $Application = New-Object -ComObject PowerPoint.Application
        $InitialPresentations = $Application.Presentations.Count
        $Presentation = $Application.Presentations.Open($CandidatePath, -1, 0, 0)
        if ($Presentation.Slides.Count -ne $Definition.slide_count) { throw 'Native PowerPoint slide count differs from manifest' }
        foreach ($Slide in $Presentation.Slides) {
            $Slide.Export((Join-Path $Native ('slide-{0:D3}.png' -f $Slide.SlideIndex)), 'PNG', 1600, 900)
            $Spec = $Definition.slides[$Slide.SlideIndex - 1]
            foreach ($Shape in $Slide.Shapes) {
                if (-not $Shape.HasTextFrame -or -not $Shape.TextFrame2.HasText) { continue }
                $Frame = $Shape.TextFrame2
                $Range = $Frame.TextRange
                $AvailableHeight = $Shape.Height - $Frame.MarginTop - $Frame.MarginBottom
                $AvailableWidth = $Shape.Width - $Frame.MarginLeft - $Frame.MarginRight
                $Bounds += [ordered]@{
                    slide = $Slide.SlideIndex; name = $Shape.Name; text = $Range.Text
                    bound_height = $Range.BoundHeight; available_height = $AvailableHeight
                    bound_width = $Range.BoundWidth; available_width = $AvailableWidth
                    overflow = ($Range.BoundHeight -gt $AvailableHeight + 0.75 -or $Range.BoundWidth -gt $AvailableWidth + 0.75)
                    revised = (($Spec.layout -eq 'native' -and ($Shape.Name.StartsWith('Story-') -or $Shape.Id -in @($Spec.headers.id))) -or
                        ($Spec.layout -eq 'text' -and $Shape.Id -in @($Spec.replacements.id)))
                }
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Range)
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Frame)
            }
        }
        $Pdf = Join-Path $Output 'zava-forward-cowork-v2-draft.pdf'
        $Presentation.SaveAs($Pdf, 32)
        [ordered]@{
            renderer = "Microsoft PowerPoint $($Application.Version) COM"; native_slides = $Definition.slide_count
            candidate_sha256 = $Report.candidate_sha256
            pdf_sha256 = (Get-FileHash $Pdf -Algorithm SHA256).Hash.ToLowerInvariant()
            revised_text_overflow_count = @($Bounds | Where-Object { $_.revised -and $_.overflow }).Count
            inherited_text_bound_warnings = @($Bounds | Where-Object { -not $_.revised -and $_.overflow }).Count
            bounds = $Bounds; human_acceptance = $false
        } | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $Output 'native-render.json') -Encoding utf8NoBOM
        Write-Output "Native PowerPoint rendered all $($Definition.slide_count) slides and PDF to $Output."
    } finally {
        if ($Presentation) { $Presentation.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Presentation) }
        if ($Application) {
            if ($InitialPresentations -eq 0 -and $Application.Presentations.Count -eq 0) { $Application.Quit() }
            [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Application)
        }
    }
}

function Export-PitchMaterials {
    param([string]$CandidatePath, [string]$Output, $Definition, $Report)
    $ContentDate = '2026-10-29'
    if ($Definition.content_date) { $ContentDate = [string]$Definition.content_date }
    $Pitch = Join-Path $Output 'pitch'
    [void][IO.Directory]::CreateDirectory($Pitch)
    $Archive = [IO.Compression.ZipFile]::OpenRead($CandidatePath)
    try {
        foreach ($Kind in @('main', 'answers')) {
            $Title = 'Current Capstone Speaker Notes'
            $Name = 'speaker-script.md'
            $Index = @($Definition.slides | Where-Object code -CEQ 'QX')[0].number
            $Numbers = 1..($Index - 1)
            if ($Kind -eq 'answers') { $Title = 'Current Capstone Question Bank'; $Name = 'questions-and-answers.md'; $Numbers = ($Index + 1)..$Definition.slide_count }
            $TimingAuthority = 'Original TIMING windows are operative; build variants share one narration slot.'
            if ($Definition.insertion) {
                $TimingAuthority = 'CURRENT ROUTE TIMING is operative where present; original TIMING windows are preserved baseline provenance. The added architecture has its own 45-second slot.'
            }
            $Lines = @(
                '---', "title: $Title"
                "description: Generated from the current $($Definition.slide_count)-slide source; preparation, not a rehearsal transcript"
                "ms.date: $ContentDate", 'ms.topic: reference', '---', ''
                '## Authority', ''
                'Generated by tools/capstone/Invoke-Capstone.ps1 from the current deck. Edit the source manifest, not this generated copy.'
                "Candidate SHA-256: ``$($Report.candidate_sha256)``.", ''
                'These are reference notes, including evidence and caveats, not a claim that every paragraph fits the spoken slot.'
                'Build variants share their stated narration slot. Native buttons use the retained fixed slide-jump links, not dynamic caller return.'
                $TimingAuthority
                'No rehearsal, audience acceptance, live demo, spending authority or fresh rubric score is established.', ''
            )
            foreach ($Number in $Numbers) {
                $Spec = $Definition.slides[$Number - 1]
                $Inventory = Get-SlideInventory $Archive (Get-DeckPartNumber $Spec)
                $Lines += @("## Page $Number / $($Spec.code)", '', $Spec.title, '', $Inventory.notes, '')
            }
            $Content = ($Lines -join "`n").Replace("`r", '')
            $Content = [regex]::Replace($Content, '(?m)[ \t]+$', '')
            [IO.File]::WriteAllText((Join-Path $Pitch $Name), $Content + "`n", [Text.UTF8Encoding]::new($false))
        }
    } finally { $Archive.Dispose() }
}

if ($MyInvocation.InvocationName -ne '.') {
    $RequestedAction = $Action
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).ProviderPath
    $OutputDir = [IO.Path]::GetFullPath($OutputDir)
    $Prefix = $RepoRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if ($OutputDir -eq $RepoRoot -or $OutputDir.StartsWith($Prefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'OutputDir must be external' }
    $Ancestor = $OutputDir
    while ($Ancestor) {
        if (Test-Path -LiteralPath $Ancestor) {
            $Item = Get-Item -LiteralPath $Ancestor -Force
            if (-not $Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'OutputDir must not traverse links' }
        }
        $Ancestor = [IO.Path]::GetDirectoryName($Ancestor)
    }
    . (Join-Path $PSScriptRoot '../cowork-native-recovery/Invoke-StoryReview.ps1') -RepoRoot $RepoRoot -OutputDir $OutputDir
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $SourceRoot = Join-Path $RepoRoot 'docs/capstone/source'
    $TemplatePath = Resolve-LocalInput $SourceRoot 'baseline.pptx'
    [void][IO.Directory]::CreateDirectory($OutputDir)
    if ($RequestedAction -eq 'ExportSource') { Export-AuthoringSource $TemplatePath $OutputDir; return }
    $Definition = Get-Content -LiteralPath (Resolve-LocalInput $SourceRoot 'slides.json') -Raw | ConvertFrom-Json
    Assert-DeckDefinition $Definition
    if ((Get-FileHash $TemplatePath -Algorithm SHA256).Hash.ToLowerInvariant() -cne $Definition.baseline_sha256) { throw 'Pinned template SHA256 mismatch' }
    $BaselineArchive = [IO.Compression.ZipFile]::OpenRead($TemplatePath)
    $CandidatePath = Join-Path $OutputDir 'zava-forward-cowork-v2-draft.pptx'
    try {
        $Parts = Get-DeckRevision $BaselineArchive $Definition $SourceRoot
        if ($RequestedAction -eq 'Build') {
            $Destination = [IO.Compression.ZipFile]::Open($CandidatePath, [IO.Compression.ZipArchiveMode]::Create)
            try {
                foreach ($Entry in $BaselineArchive.Entries) {
                    $NewEntry = $Destination.CreateEntry($Entry.FullName, [IO.Compression.CompressionLevel]::Optimal)
                    $NewEntry.LastWriteTime = $Entry.LastWriteTime
                    $NewEntry.ExternalAttributes = $Entry.ExternalAttributes
                    $Bytes = Get-PartBytes $BaselineArchive $Entry.FullName
                    if ($Parts.ContainsKey($Entry.FullName)) { $Bytes = $Parts[$Entry.FullName] }
                    $Stream = $NewEntry.Open()
                    try { $Stream.Write($Bytes, 0, $Bytes.Length) } finally { $Stream.Dispose() }
                }
                foreach ($Name in $Parts.Keys | Where-Object { -not $BaselineArchive.GetEntry($_) } | Sort-Object) {
                    $Entry = $Destination.CreateEntry($Name, [IO.Compression.CompressionLevel]::Optimal)
                    $Entry.LastWriteTime = [DateTimeOffset]::Parse('2026-10-30T00:00:00Z')
                    $Stream = $Entry.Open()
                    try { $Stream.Write($Parts[$Name], 0, $Parts[$Name].Length) } finally { $Stream.Dispose() }
                }
            } finally { $Destination.Dispose() }
        }
        $Report = Test-DeckCandidate $BaselineArchive $CandidatePath $Parts $Definition
        $Report.baseline_sha256 = $Definition.baseline_sha256
        $Report.source_hash_convention = 'SHA-256 of UTF-8 bytes with CRLF and CR normalized to LF; BOM and all other bytes preserved.'
        $Report.manifest_sha256 = Get-CanonicalSourceHash (Join-Path $SourceRoot 'slides.json')
        $Report.asset_catalog_sha256 = Get-CanonicalSourceHash (Join-Path $SourceRoot $Definition.assets)
        $Report.builder_sha256 = Get-CanonicalSourceHash $PSCommandPath
        $Report.native_helper_sha256 = Get-CanonicalSourceHash (Join-Path $PSScriptRoot '../cowork-native-recovery/Invoke-StoryReview.ps1')
        Export-PitchMaterials $CandidatePath $OutputDir $Definition $Report
        $Report | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $OutputDir 'verification.json') -Encoding utf8NoBOM
        Write-Output "${RequestedAction}: $($Definition.slide_count) slides and notes; all assets, navigation, timing and protected cost evidence verified."
        Write-Output "Candidate: $CandidatePath"
        if ($RequestedAction -eq 'Render') { Export-NativeDeck $CandidatePath $OutputDir $Definition $Report }
    } finally { $BaselineArchive.Dispose() }
}