#!/usr/bin/env pwsh
#Requires -Version 7.4
<#
.SYNOPSIS
Check canonical textual source hashes and the current delivery receipt.
.PARAMETER SemanticOnly
Test newline fixtures before the receipt is regenerated.
#>
[CmdletBinding()]
param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).ProviderPath,
    [switch]$SemanticOnly
)
$ErrorActionPreference = 'Stop'
. (Join-Path $RepoRoot 'tools/cowork-native-recovery/Invoke-StoryReview.ps1') -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())
. (Join-Path $RepoRoot 'tools/capstone/Invoke-Capstone.ps1') -Action Verify -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())

$Fixture = Join-Path ([IO.Path]::GetTempPath()) ("capstone-source-hash-" + [Guid]::NewGuid() + '.txt')
$Encoding = [Text.UTF8Encoding]::new($false, $true)
try {
    $Expected = Get-ByteHash $Encoding.GetBytes("first`nsecond`n")
    foreach ($Text in @("first`nsecond`n", "first`r`nsecond`r`n", "first`rsecond`r")) {
        [IO.File]::WriteAllBytes($Fixture, $Encoding.GetBytes($Text))
        if ((Get-CanonicalSourceHash $Fixture) -cne $Expected) { throw 'Canonical newline hash mismatch' }
    }
    foreach ($Text in @("first `nsecond`n", "first`nsecond", "First`nsecond`n", ([char]0xFEFF + "first`nsecond`n"))) {
        [IO.File]::WriteAllBytes($Fixture, $Encoding.GetBytes($Text))
        if ((Get-CanonicalSourceHash $Fixture) -ceq $Expected) { throw 'Meaningful source bytes lost' }
        if ((Get-CanonicalSourceHash $Fixture) -cne (Get-ByteHash $Encoding.GetBytes($Text))) { throw 'LF bytes changed' }
    }
    [IO.File]::WriteAllBytes($Fixture, [byte[]]@())
    if ((Get-CanonicalSourceHash $Fixture) -cne (Get-ByteHash ([byte[]]@()))) { throw 'Empty source hash mismatch' }
    [IO.File]::WriteAllBytes($Fixture, [byte[]]@(0xFF))
    $Refused = $false
    try { [void](Get-CanonicalSourceHash $Fixture) }
    catch {
        if ($_.Exception.InnerException -isnot [Text.DecoderFallbackException]) { throw }
        $Refused = $true
    }
    if (-not $Refused) { throw 'Invalid UTF-8 was not refused' }
} finally {
    if (Test-Path -LiteralPath $Fixture) { Remove-Item -LiteralPath $Fixture }
}
Write-Output 'Canonical source semantics passed: LF/CRLF/CR, whitespace, case, final newline, BOM, empty input and invalid UTF-8.'

if (-not $SemanticOnly) {
    $Receipt = Get-Content -LiteralPath (Join-Path $RepoRoot 'docs/capstone/source/validation.json') -Raw | ConvertFrom-Json
    $Inputs = [ordered]@{
        manifest_sha256 = 'docs/capstone/source/slides.json'
        asset_catalog_sha256 = 'docs/capstone/source/assets/catalog.json'
        builder_sha256 = 'tools/capstone/Invoke-Capstone.ps1'
        native_helper_sha256 = 'tools/cowork-native-recovery/Invoke-StoryReview.ps1'
    }
    foreach ($Input in $Inputs.GetEnumerator()) {
        if ((Get-CanonicalSourceHash (Join-Path $RepoRoot $Input.Value)) -cne $Receipt.package.($Input.Key)) {
            throw "Receipt source hash mismatch: $($Input.Value)"
        }
    }
    $Convention = 'SHA-256 of UTF-8 bytes with CRLF and CR normalized to LF; BOM and all other bytes preserved.'
    if ($Receipt.source_verification.source_hash_convention -cne $Convention) { throw 'Receipt hash convention mismatch' }
    $Delivery = Join-Path $RepoRoot 'docs/capstone/deck/zava-forward-cowork-v2-draft.pptx'
    if ((Get-FileHash $Delivery -Algorithm SHA256).Hash.ToLowerInvariant() -cne $Receipt.package.candidate_sha256) {
        throw 'Receipt delivery hash mismatch'
    }
    Write-Output 'Four canonical source bindings, convention and exact delivery hash passed.'
}
