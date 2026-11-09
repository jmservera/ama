#!/usr/bin/env pwsh
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT
#Requires -Version 7.4
<#
.SYNOPSIS
Verify the single source-template insertion, immutable mapping and fixed links.
.PARAMETER CandidatePath
Optional built candidate for package/section/navigation checks.
.PARAMETER RepoRoot
Repository containing the current manifest and native baseline.
#>
[CmdletBinding()]
param(
    [string]$CandidatePath,
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).ProviderPath
)
$ErrorActionPreference = 'Stop'
. (Join-Path $RepoRoot 'tools/cowork-native-recovery/Invoke-StoryReview.ps1') -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())
. (Join-Path $RepoRoot 'tools/capstone/Invoke-Capstone.ps1') -Action Verify -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())
$Definition = Get-Content (Join-Path $RepoRoot 'docs/capstone/source/slides.json') -Raw | ConvertFrom-Json
Assert-DeckDefinition $Definition
$Original = [IO.Compression.ZipFile]::OpenRead((Join-Path $RepoRoot 'docs/capstone/source/baseline.pptx'))
try {
    foreach ($Slide in $Definition.slides | Where-Object part_number -ne 55) {
        if ($Slide.notes -cne (Get-SlideInventory $Original $Slide.baseline_number).notes) { throw 'Captured original notes changed' }
    }
    $Structural = Get-InsertionParts $Original $Definition
    if ($Structural.Count -ne 6) { throw 'Insertion structural member allowlist changed' }
} finally { $Original.Dispose() }
foreach ($Mutation in @('template', 'count', 'mapping', 'asset', 'timing', 'note-timing')) {
    $Mutant = $Definition | ConvertTo-Json -Depth 60 | ConvertFrom-Json
    switch ($Mutation) {
        'template' { $Mutant.insertion.template_slide = 11 }
        'count' { $Mutant.slide_count = 56 }
        'mapping' { $Mutant.slides[13].part_number = 14 }
        'asset' { $Mutant.slides[12].images[0].asset = 'arbitrary' }
        'timing' { $Mutant.insertion.narration_seconds = 46 }
        'note-timing' { $Mutant.slides[12].revised_notes[1] = 'TIMING: 99 s' }
    }
    $Refused = $false
    try { Assert-DeckDefinition $Mutant } catch { $Refused = $true }
    if (-not $Refused) { throw "Insertion mutation was not refused: $Mutation" }
}
$UniqueTimings = @{}
foreach ($Slide in $Definition.slides | Where-Object { $_.number -lt 28 }) {
    $Timing = [regex]::Match($Slide.notes, '(?m)^TIMING: (\d+) s')
    if (-not $Timing.Success) { throw 'Main-route source timing is missing' }
    $Seconds = [int]$Timing.Groups[1].Value
    if ($UniqueTimings.ContainsKey($Slide.code) -and $UniqueTimings[$Slide.code] -ne $Seconds) { throw 'Build variants have different slots' }
    $UniqueTimings[$Slide.code] = $Seconds
}
if (($UniqueTimings.Values | Measure-Object -Sum).Sum -ne 1470) { throw 'Expected 24:30 narration including added 45 seconds' }
if ($Definition.slides[27].code -cne 'QX' -or $Definition.slides[28].code -cne 'B01' -or $Definition.slides[54].code -cne 'B27') { throw 'Question-index or answer order changed' }
Write-Output 'Insertion source checks pass: original notes, six denied mutations, baseline mapping, 24:30 shared-build timing, QX28 and answers29-55.'
if (-not $CandidatePath) { return }
$Baseline = [IO.Compression.ZipFile]::OpenRead((Join-Path $RepoRoot 'docs/capstone/source/baseline.pptx'))
$Candidate = [IO.Compression.ZipFile]::OpenRead($CandidatePath)
try {
    $Before = Get-PartDocument $Baseline 'ppt/presentation.xml'
    $After = Get-PartDocument $Candidate 'ppt/presentation.xml'
    $NS = Get-Namespaces $After
    $NS.AddNamespace('p14', 'http://schemas.microsoft.com/office/powerpoint/2010/main')
    $Ids = @($After.SelectNodes('/p:presentation/p:sldIdLst/p:sldId', $NS))
    $NewId = $Ids[12]
    if ($NewId.GetAttribute('id', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships') -cne 'rIdDeployment55') { throw 'New slide is not physically after12' }
    [void]$NewId.ParentNode.RemoveChild($NewId)
    $SectionNew = $After.SelectSingleNode("//p14:section/p14:sldIdLst/p14:sldId[@id='$($NewId.GetAttribute('id'))']", $NS)
    if (-not $SectionNew -or $SectionNew.ParentNode.ParentNode.name -cne '3 · The product') { throw 'New slide is not in the product section' }
    [void]$SectionNew.ParentNode.RemoveChild($SectionNew)
    if ((Get-ByteHash (Get-XmlBytes $Before)) -cne (Get-ByteHash (Get-XmlBytes $After))) { throw 'Existing presentation IDs/sections/metadata changed' }
    $ActionCount = 0
    foreach ($Number in 1..54) {
        $Source = Get-PartDocument $Baseline "ppt/slides/slide$Number.xml"
        $Actual = Get-PartDocument $Candidate "ppt/slides/slide$Number.xml"
        $SourceActions = @($Source.SelectNodes('//a:hlinkClick | //a:hlinkMouseOver', (Get-Namespaces $Source)) | ForEach-Object OuterXml)
        $ActualActions = @($Actual.SelectNodes('//a:hlinkClick | //a:hlinkMouseOver', (Get-Namespaces $Actual)) | ForEach-Object OuterXml)
        if (($SourceActions -join "`n") -cne ($ActualActions -join "`n")) { throw "Original action changed on part$Number" }
        $ActionCount += $ActualActions.Count
        $SourceRels = Get-PartDocument $Baseline "ppt/slides/_rels/slide$Number.xml.rels"
        $ActualRels = Get-PartDocument $Candidate "ppt/slides/_rels/slide$Number.xml.rels"
        $SourceTargets = @($SourceRels.DocumentElement.ChildNodes | Where-Object { $_.Type.EndsWith('/slide') } | ForEach-Object OuterXml)
        $ActualTargets = @($ActualRels.DocumentElement.ChildNodes | Where-Object { $_.Type.EndsWith('/slide') } | ForEach-Object OuterXml)
        if (($SourceTargets -join "`n") -cne ($ActualTargets -join "`n")) { throw "Fixed destination changed on part$Number" }
    }
    if ($ActionCount -ne 108) { throw 'Expected all 108 original fixed actions' }
    $Index = Get-PartDocument $Candidate 'ppt/slides/slide27.xml'
    $IndexText = @($Index.SelectNodes('//a:t', (Get-Namespaces $Index)) | ForEach-Object InnerText)
    foreach ($Answer in $Definition.slides | Where-Object code -match '^B\d\d$') {
        if (@($IndexText | Where-Object { $_ -match ("^" + $Answer.code + " · " + $Answer.number + "\s") }).Count -ne 1) {
            throw "Visible index number differs from the physical destination: $($Answer.code)"
        }
    }
    $Deployment = Get-PartDocument $Candidate 'ppt/slides/slide55.xml'
    $DeploymentNS = Get-Namespaces $Deployment
    $Equivalent = (Get-SlideInventory $Candidate 55).notes + "`n" +
        (@($Deployment.SelectNodes('//p:cNvPr[@descr]', $DeploymentNS) | ForEach-Object { $_.GetAttribute('descr') }) -join "`n")
    foreach ($Required in @('home sensors', 'IoT Hub', 'Event Hubs', 'validated', 'idempotent',
        'SQL', 'accepted observations', 'history', 'derived on read', 'Workbench',
        'five current helpers', 'Quality Verification', 'resident site', 'identity',
        'own-case', 'assisted', 'Blob', 'Foundry', 'private endpoints', 'DNS',
        'registry', 'Vault', 'Monitor', 'edge', 'token', 'background', 'queue', 'model', 'simulator', 'gated')) {
        if ($Equivalent -notmatch [regex]::Escape($Required)) { throw "Required deployment meaning is absent from actual notes/alternative text: $Required" }
    }
    if ($Deployment.SelectNodes("//p:pic[p:nvPicPr/p:cNvPr[@name='Roadmap-13-architecture-azure-deployment']]", $DeploymentNS).Count -ne 1) {
        throw 'Expected exactly one declared full deployment projection'
    }
    Write-Output 'Insertion package checks pass: main position13, product section, every existing slide ID/section and all108 original actions/destinations retained.'
    Write-Output 'Actual deployment notes/alternative-text extraction contains the full sensor chain, SQL derived-average responsibility, resident/quality boundaries, supporting services and all gated options.'
} finally {
    $Candidate.Dispose()
    $Baseline.Dispose()
}
