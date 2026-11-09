#!/usr/bin/env pwsh
# Copyright (c) 2026 Microsoft Corporation. All rights reserved.
# SPDX-License-Identifier: MIT
#Requires -Version 7.4
<#
.SYNOPSIS
Test the fixed owner-approved cost-status exception and reject other changes.
.PARAMETER CandidatePath
Built candidate with the approved status revision.
.PARAMETER RepoRoot
Repository containing the immutable baseline and authoring helpers.
.EXAMPLE
./Test-CostStatus.ps1 -CandidatePath /external/build/deck.pptx -RepoRoot .
.NOTES
Uses only the baseline, candidate and owned temporary ZIP copies.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CandidatePath,
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).ProviderPath
)
$ErrorActionPreference = 'Stop'
. (Join-Path $RepoRoot 'tools/cowork-native-recovery/Invoke-StoryReview.ps1') -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())
. (Join-Path $RepoRoot 'tools/capstone/Invoke-Capstone.ps1') -Action Verify -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())

function Assert-CostRefusal {
    param([scriptblock]$Action, [string]$Expected)
    $Refused = $false
    try { & $Action | Out-Null }
    catch {
        if ($_.Exception.Message -notlike "*$Expected*") { throw }
        $Refused = $true
    }
    if (-not $Refused) { throw "Expected protected-cost refusal: $Expected" }
}

function New-CostMutant {
    param([int]$Number, [ValidateSet('number', 'geometry', 'notes')][string]$Kind)
    $Path = Join-Path ([IO.Path]::GetTempPath()) ("capstone-cost-" + [Guid]::NewGuid() + '.pptx')
    [IO.File]::Copy($CandidatePath, $Path)
    $script:Owned.Add($Path)
    $Archive = [IO.Compression.ZipFile]::Open($Path, [IO.Compression.ZipArchiveMode]::Update)
    try {
        $Part = if ($Kind -eq 'notes') { "ppt/notesSlides/notesSlide$Number.xml" } else { "ppt/slides/slide$Number.xml" }
        $Document = Get-PartDocument $Archive $Part
        $Namespaces = Get-Namespaces $Document
        if ($Kind -eq 'number') {
            $Node = @($Document.SelectNodes('//a:t', $Namespaces) | Where-Object { $_.InnerText -match '\d+' })[0]
            if (-not $Node) { throw 'Financial-number mutation fixture has no numeric text' }
            $Value = [regex]::Match($Node.InnerText, '\d+').Value
            $Node.InnerText = $Node.InnerText.Replace($Value, $Value + '0')
        } elseif ($Kind -eq 'geometry') {
            $Node = $Document.SelectSingleNode('//p:sp/p:spPr/a:xfrm/a:ext', $Namespaces)
            $Node.SetAttribute('cx', ([long]$Node.GetAttribute('cx') + 1).ToString())
        } else {
            $Node = $Document.SelectSingleNode("//p:sp[p:nvSpPr/p:nvPr/p:ph[@type='body']]/p:txBody//a:t", $Namespaces)
            if (-not $Node) { throw 'Protected-note mutation fixture has no body text' }
            $Node.InnerText += ' Unapproved extra words.'
        }
        $Archive.GetEntry($Part).Delete()
        $Entry = $Archive.CreateEntry($Part)
        $Stream = $Entry.Open()
        try {
            $Bytes = Get-XmlBytes $Document
            $Stream.Write($Bytes, 0, $Bytes.Length)
        } finally { $Stream.Dispose() }
    } finally { $Archive.Dispose() }
    return $Path
}

$Owned = [Collections.Generic.List[string]]::new()
$Baseline = [IO.Compression.ZipFile]::OpenRead((Join-Path $RepoRoot 'docs/capstone/source/baseline.pptx'))
$Candidate = [IO.Compression.ZipFile]::OpenRead($CandidatePath)
$Definition = Get-Content (Join-Path $RepoRoot 'docs/capstone/source/slides.json') -Raw | ConvertFrom-Json
try {
    if (Test-CostStatusRevision ([pscustomobject]@{})) { throw 'Missing approval enabled cost status' }
    if (-not (Test-CostStatusRevision ([pscustomobject]@{ cost_status_revision = 'owner-approved-2026-11-08-status-only' }))) { throw 'Fixed approved revision rejected' }
    Assert-CostRefusal { Test-CostStatusRevision ([pscustomobject]@{ cost_status_revision = 'arbitrary' }) } 'Unrecognised'
    foreach ($Number in @(6, 11, 21, 32, 36, 52)) {
        $Result = Assert-CostSlide $Baseline $Candidate $Number $true $Definition
        if ($Result.status_updated -ne ($Number -in @(21, 52))) { throw "Unexpected status revision on page $Number" }
    }
    foreach ($Number in @(21, 52)) {
        Assert-CostRefusal { Assert-CostSlide $Baseline $Candidate $Number $false $Definition } 'fixed approved status words'
    }
    foreach ($Kind in @('number', 'geometry', 'notes')) {
        $MutantPath = New-CostMutant 21 $Kind
        $Mutant = [IO.Compression.ZipFile]::OpenRead($MutantPath)
        try {
            Assert-CostRefusal { Assert-CostSlide $Baseline $Mutant 21 $true $Definition } 'Protected cost'
        } finally { $Mutant.Dispose() }
    }
    Write-Output 'Protected-cost tests passed: explicit fixed approval, all six pages, denied unapproved status, number, geometry and note mutations.'
} finally {
    $Candidate.Dispose()
    $Baseline.Dispose()
    foreach ($Path in $Owned) { Remove-Item -LiteralPath $Path }
}
