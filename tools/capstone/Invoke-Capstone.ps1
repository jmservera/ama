#!/usr/bin/env pwsh
#Requires -Version 7.4
<#
.SYNOPSIS
Export complete authoring inputs or build and verify the current capstone deck.
.DESCRIPTION
Uses a pinned native template, a 54-slide JSON manifest and explicit media files.
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
    param($Archive, [string]$Part)
    $Used = @()
    foreach ($Number in 1..54) {
        $Entry = $Archive.GetEntry("ppt/slides/_rels/slide$Number.xml.rels")
        if (-not $Entry) { continue }
        $Relationships = Get-PartDocument $Archive $Entry.FullName
        foreach ($Relationship in $Relationships.DocumentElement.ChildNodes) {
            if ($Relationship.TargetMode -eq 'External') { continue }
            $Target = [Uri]::new([Uri]"https://package/ppt/slides/slide$Number.xml", [string]$Relationship.Target).AbsolutePath.TrimStart('/')
            if ($Target -ceq $Part) { $Used += $Number; break }
        }
    }
    return @($Used)
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

    function Get-DeckRevision {
    param($Archive, $Definition, [string]$Root)
    $Parts = @{}
    foreach ($Slide in $Definition.slides) {
        if ($Slide.revised_notes) {
            $NoteCode = ([string]$Slide.revised_notes[0] -split ' \| ', 2)[0]
            if ($NoteCode -cne $Slide.code) { throw "Revised notes ID $NoteCode does not match page $($Slide.number)/$($Slide.code)" }
        }
        foreach ($Source in @($Slide.sources)) {
            if ($Source) { [void](Resolve-LocalInput $RepoRoot $Source) }
        }
        $Name = "ppt/slides/slide$($Slide.number).xml"
        if ($Slide.layout -eq 'native') { $Parts[$Name] = Set-StorySlide $Archive $Slide }
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
        $Before = Get-SlideInventory $Archive $Slide.number
        $Text = $Slide.notes
        if ($Slide.revised_notes) { $Text = @($Slide.revised_notes) -join "`n" }
        $Text = Update-NavigationNote $Text
        if ($Before.notes -ceq $Text) { continue }
        $Timing = @([regex]::Matches($Before.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
        $NewTiming = @([regex]::Matches($Text, '(?m)^TIMING:.*$') | ForEach-Object Value)
        if (-not $NewTiming.Count -and $Timing.Count) { $Text += "`n" + ($Timing -join "`n") }
        elseif (($Timing -join "`n") -cne ($NewTiming -join "`n")) { throw "Timing changed on slide $($Slide.number)" }
        $NoteName = "ppt/notesSlides/notesSlide$($Slide.number).xml"
        $Document = Get-PartDocument $Archive $NoteName
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
        $Name = "ppt/slides/slide$($Slide.number).xml"
        $Document = Get-PartDocument $Archive $Name
        if ($Parts.ContainsKey($Name)) { $Document.LoadXml([Text.Encoding]::UTF8.GetString($Parts[$Name])) }
        $RelationshipName = "ppt/slides/_rels/slide$($Slide.number).xml.rels"
        $Relationships = Get-PartDocument $Archive $RelationshipName
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
            @(Compare-Object $ExpectedNames $OtherNames).Count) { throw 'Package member set differs from explicit baseline and added-media inputs' }
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
            $Before = Get-SlideInventory $BaselineArchive $Slide.number
            $After = Get-SlideInventory $Candidate $Slide.number
            if (-not $After.notes.Trim()) { throw "Empty notes on slide $($Slide.number)" }
            $BeforeTiming = @([regex]::Matches($Before.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
            $AfterTiming = @([regex]::Matches($After.notes, '(?m)^TIMING:.*$') | ForEach-Object Value)
            if (($BeforeTiming -join "`n") -cne ($AfterTiming -join "`n")) { throw 'Timing preservation failed' }
            if (($Before.shapes.actions -join "`n") -cne ($After.shapes.actions -join "`n")) { throw 'Native navigation changed' }
            $Document = Get-PartDocument $Candidate "ppt/slides/slide$($Slide.number).xml"
            $Ids = @($Document.SelectNodes('//p:cNvPr', (Get-Namespaces $Document)) | ForEach-Object id)
            if (@($Ids | Select-Object -Unique).Count -ne $Ids.Count) { throw 'Duplicate native shape IDs' }
            $Actions += @($Document.SelectNodes('//*[@action]')).Count
            $BaselineDocument = Get-PartDocument $BaselineArchive "ppt/slides/slide$($Slide.number).xml"
            $BaselineActions += @($BaselineDocument.SelectNodes('//*[@action]')).Count
        }
        if ($Actions -ne $BaselineActions) { throw 'Native action count differs from the pinned current template' }
        $CostNavigationUpdates = @()
        foreach ($Number in @(6, 11, 21, 32, 36, 52)) {
            if ("ppt/slides/slide$Number.xml" -in $Changed) { throw "Protected cost slide changed: $Number" }
            if ("ppt/notesSlides/notesSlide$Number.xml" -in $Changed) {
                $BeforeCost = Get-SlideInventory $BaselineArchive $Number
                $AfterCost = Get-SlideInventory $Candidate $Number
                if ($AfterCost.notes -cne (Update-NavigationNote $BeforeCost.notes)) {
                    throw "Protected cost note changed beyond the exact navigation correction: $Number"
                }
                $CostNavigationUpdates += $Number
            }
        }
        $Catalog = Get-Content -LiteralPath (Resolve-LocalInput $SourceRoot $Definition.assets) -Raw | ConvertFrom-Json
        foreach ($Asset in $Catalog.additional_media) {
            $ActualUsage = @(Get-MediaUsage $Candidate $Asset.part)
            if (($ActualUsage -join ',') -cne (@($Asset.slides | Sort-Object -Unique) -join ',')) { throw "Additional media usage mismatch: $($Asset.id)" }
        }
        return [ordered]@{
            status = 'pass'; slides = 54; nonempty_notes = 54; navigation_actions = $Actions
            package_members = $ExpectedNames.Count; baseline_members = $Names.Count; added_media_parts = $Added
            changed_members = $Changed; timing_preserved = $true
            native_navigation_preserved = $true; six_cost_slide_bytes_preserved = $true
            cost_note_calculations_preserved = $true; cost_note_navigation_only_updates = $CostNavigationUpdates
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
        if ($Presentation.Slides.Count -ne 54) { throw 'Native PowerPoint did not open 54 slides' }
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
            renderer = "Microsoft PowerPoint $($Application.Version) COM"; native_slides = 54
            candidate_sha256 = $Report.candidate_sha256
            pdf_sha256 = (Get-FileHash $Pdf -Algorithm SHA256).Hash.ToLowerInvariant()
            revised_text_overflow_count = @($Bounds | Where-Object { $_.revised -and $_.overflow }).Count
            inherited_text_bound_warnings = @($Bounds | Where-Object { -not $_.revised -and $_.overflow }).Count
            bounds = $Bounds; human_acceptance = $false
        } | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $Output 'native-render.json') -Encoding utf8NoBOM
        Write-Output "Native PowerPoint rendered all 54 slides and PDF to $Output."
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
            $Numbers = 1..26
            if ($Kind -eq 'answers') { $Title = 'Current Capstone Question Bank'; $Name = 'questions-and-answers.md'; $Numbers = 28..54 }
            $Lines = @(
                '---', "title: $Title"
                'description: Generated from the current 54-slide source; preparation, not a rehearsal transcript'
                "ms.date: $ContentDate", 'ms.topic: reference', '---', ''
                '## Authority', ''
                'Generated by tools/capstone/Invoke-Capstone.ps1 from the current deck. Edit the source manifest, not this generated copy.'
                "Candidate SHA-256: ``$($Report.candidate_sha256)``.", ''
                'These are reference notes, including evidence and caveats, not a claim that every paragraph fits the spoken slot.'
                'Build variants share their stated narration slot. Native buttons use the retained fixed slide-jump links, not dynamic caller return.'
                'No rehearsal, audience acceptance, live demo, spending authority or fresh rubric score is established.', ''
            )
            foreach ($Number in $Numbers) {
                $Spec = $Definition.slides[$Number - 1]
                $Inventory = Get-SlideInventory $Archive $Number
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
    if ($Definition.schema_version -ne 1 -or $Definition.baseline -cne 'baseline.pptx' -or
        $Definition.slide_count -ne 54 -or $Definition.slides.Count -ne 54 -or
        (@($Definition.slides.number) -join ',') -cne ((1..54) -join ',')) { throw 'Expected the complete ordered 54-slide manifest' }
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
        Write-Output "${RequestedAction}: 54 slides and notes; all assets, navigation, timing and protected cost evidence verified."
        Write-Output "Candidate: $CandidatePath"
        if ($RequestedAction -eq 'Render') { Export-NativeDeck $CandidatePath $OutputDir $Definition $Report }
    } finally { $BaselineArchive.Dispose() }
}