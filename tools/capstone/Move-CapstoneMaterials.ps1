#!/usr/bin/env pwsh
#Requires -Version 7.4
<#
.SYNOPSIS
Archive and consolidate the owner-approved, finite capstone selection.
.DESCRIPTION
Snapshots capstone and tracking without following links. Full archive readback,
selected-file restoration and protected-byte checks precede any removal.
.PARAMETER Action
Plan reports the exact selection. Apply also archives, restores and reorganizes.
.PARAMETER RepoRoot
Repository containing the capstone materials.
.PARAMETER OutputDir
New external archive directory; Apply refuses an existing destination.
.PARAMETER ApproveExactSelection
Required for Apply after owner approval of the fifteen listed exports.
.EXAMPLE
./Move-CapstoneMaterials.ps1 -Action Plan -RepoRoot . -OutputDir C:/scratch/capstone-archive
.NOTES
No Git history, original tracking evidence or thought-leadership files are pruned.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Plan', 'Apply')]
    [string]$Action,
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$RepoRoot,
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputDir,
    [switch]$ApproveExactSelection
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Get-EntryState {
    param([string]$Root, [string]$Relative)
    $Item = Get-Item -LiteralPath (Join-Path $Root $Relative) -Force
    $State = [ordered]@{ path = $Relative; type = 'file'; size = 0; sha256 = $null }
    if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        if ($null -eq $Item.LinkTarget) { throw "Opaque link identity unavailable: $Relative" }
        $Bytes = [Text.Encoding]::UTF8.GetBytes([string]$Item.LinkTarget)
        $State.type = 'symlink'
        $State.size = $Bytes.Length
        $State.sha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant()
        $State.link_target = [string]$Item.LinkTarget
    } elseif ($Item.PSIsContainer) {
        $State.type = 'directory'
    } else {
        $State.size = $Item.Length
        $State.sha256 = (Get-FileHash -LiteralPath $Item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        $After = Get-Item -LiteralPath $Item.FullName -Force
        if ($After.Length -ne $Item.Length -or $After.LastWriteTimeUtc -ne $Item.LastWriteTimeUtc) {
            throw "Input changed during hashing: $Relative"
        }
    }
    return [pscustomobject]$State
}

function Get-TreeState {
    param([string]$Root, [string]$Relative)
    $Entry = Get-EntryState $Root $Relative
    $Entry
    if ($Entry.type -eq 'directory') {
        foreach ($Path in [IO.Directory]::EnumerateFileSystemEntries((Join-Path $Root $Relative)) | Sort-Object) {
            Get-TreeState $Root ($Relative + '/' + [IO.Path]::GetFileName($Path))
        }
    }
}

function Assert-EntryState {
    param([string]$Root, $Expected, [string]$Relative = $Expected.path)
    $Actual = Get-EntryState $Root $Relative
    if ($Actual.type -cne $Expected.type -or $Actual.size -ne $Expected.size -or
        $Actual.sha256 -cne $Expected.sha256) { throw "Source bytes or identity changed: $Relative" }
}

function Write-Receipt {
    param([string]$Path, $Value)
    $Value | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath $Path -Encoding utf8NoBOM
}

if ($MyInvocation.InvocationName -ne '.') {
    $RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).ProviderPath
    $OutputDir = [IO.Path]::GetFullPath($OutputDir)
    $Prefix = $RepoRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if ($OutputDir -eq $RepoRoot -or $OutputDir.StartsWith($Prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Archive output must be outside the checkout'
    }
    $Ancestor = $OutputDir
    while ($Ancestor) {
        if (Test-Path -LiteralPath $Ancestor) {
            $Item = Get-Item -LiteralPath $Ancestor -Force
            if (-not $Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                throw 'Archive ancestors must be directories without links'
            }
        }
        $Ancestor = [IO.Path]::GetDirectoryName($Ancestor)
    }
    $Names = @(
        'draft/zava-forward-executive-draft.pptx'
        'draft/architecture-runtime-native.png'
        'draft/architecture-operations-native.png'
        'draft/architecture-executive-native.png'
        'draft/architecture-deferred-native.png'
        'draft/agents-in-retrofit-process.svg'
        'draft/agents-in-retrofit-process.png'
        'draft/agents-in-retrofit-process-native.png'
        'cowork-generated/Zava Forward v2 - More homes ready with control intact.pdf'
        'cowork-generated/Zava Forward v2 - contact sheet.png'
        'cowork-generated/refinement-2026-10-23/slide-9.png'
        'cowork-generated/refinement-2026-10-23/slide-46.png'
        'cowork-generated/refinement-2026-10-23/slide-33.png'
        'cowork-generated/refinement-2026-10-23/slide-19.png'
        'cowork-generated/refinement-2026-10-23/slide-13.png'
    )
    $Selection = @($Names | ForEach-Object { Get-EntryState $RepoRoot "docs/capstone/deck/$_" })
    if ($Selection.Count -ne 15 -or @($Selection | Where-Object type -ne 'file').Count) {
        throw 'Exactly fifteen regular generated exports are required'
    }
    $Moves = @(
        @{ from = 'docs/capstone/pitch/cowork-main-presentation'; to = 'docs/capstone/history/cowork-main-presentation' }
        @{ from = 'docs/capstone/pitch/tokenomics-pitch-brief.md'; to = 'docs/capstone/history/tokenomics-pitch-brief.md' }
        @{ from = 'docs/capstone/deck/cowork-generated'; to = 'docs/capstone/history/cowork-generated' }
    )
    foreach ($Move in $Moves) {
        if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot $Move.from)) -or
            (Test-Path -LiteralPath (Join-Path $RepoRoot $Move.to))) { throw 'Move source missing or destination already exists' }
    }
    $Baseline = 'docs/capstone/source/baseline.pptx'
    if (Test-Path -LiteralPath (Join-Path $RepoRoot $Baseline)) { throw 'A source baseline already exists; refusing overwrite' }
    if ($Action -eq 'Plan') {
        $Selection | Select-Object path, size | Format-Table -AutoSize
        Write-Output "Exact selection: 15 exports / $(($Selection | Measure-Object size -Sum).Sum) bytes. Three history moves; no deletion performed."
        return
    }
    if (-not $ApproveExactSelection) { throw 'Apply requires explicit approval of the exact selection' }
    if (Test-Path -LiteralPath $OutputDir) { throw 'Use a new archive directory; inspect any earlier interrupted run first' }
    [void][IO.Directory]::CreateDirectory($OutputDir)
    $Snapshot = @(
        Get-TreeState $RepoRoot '.copilot-tracking'
        Get-TreeState $RepoRoot 'docs/capstone'
    )
    Write-Receipt (Join-Path $OutputDir 'inventory.json') $Snapshot
    $ZipPath = Join-Path $OutputDir 'snapshot.zip'
    $Zip = [IO.Compression.ZipFile]::Open($ZipPath, [IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($State in $Snapshot) {
            Assert-EntryState $RepoRoot $State
            $Name = $State.path
            if ($State.type -eq 'directory') { $Name += '/' }
            $Entry = $Zip.CreateEntry($Name, [IO.Compression.CompressionLevel]::Optimal)
            $Target = $Entry.Open()
            try {
                if ($State.type -eq 'file') {
                    $Source = [IO.File]::OpenRead((Join-Path $RepoRoot $State.path))
                    try { $Source.CopyTo($Target) } finally { $Source.Dispose() }
                } elseif ($State.type -eq 'symlink') {
                    $Bytes = [Text.Encoding]::UTF8.GetBytes($State.link_target)
                    $Target.Write($Bytes, 0, $Bytes.Length)
                }
            } finally { $Target.Dispose() }
            Assert-EntryState $RepoRoot $State
        }
    } finally { $Zip.Dispose() }
    $Zip = [IO.Compression.ZipFile]::OpenRead($ZipPath)
    $RestoreRoot = Join-Path $OutputDir 'restore-selected'
    [void][IO.Directory]::CreateDirectory($RestoreRoot)
    try {
        if ($Zip.Entries.Count -ne $Snapshot.Count) { throw 'Archive member count differs from inventory' }
        foreach ($State in $Snapshot) {
            $Name = $State.path
            if ($State.type -eq 'directory') { $Name += '/' }
            $Entry = $Zip.GetEntry($Name)
            if (-not $Entry -or $Entry.Length -ne $State.size) { throw "Archive member mismatch: $Name" }
            if ($State.type -ne 'directory') {
                $Stream = $Entry.Open()
                try { $Hash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Stream)).ToLowerInvariant() }
                finally { $Stream.Dispose() }
                if ($Hash -cne $State.sha256) { throw "Archive readback mismatch: $Name" }
            }
        }
        foreach ($State in $Selection) {
            $Path = Join-Path $RestoreRoot $State.path
            [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Path))
            $Target = [IO.File]::Open($Path, [IO.FileMode]::CreateNew)
            $Source = $Zip.GetEntry($State.path).Open()
            try { $Source.CopyTo($Target) } finally { $Source.Dispose(); $Target.Dispose() }
            Assert-EntryState $RestoreRoot $State
        }
    } finally { $Zip.Dispose() }
    foreach ($State in $Snapshot) { Assert-EntryState $RepoRoot $State }
    Write-Receipt (Join-Path $OutputDir 'restore-proof.json') ([ordered]@{
        full_archive_readback = $true; selected_restored = $Selection; protected_bytes_before = $true
    })
    $Journal = Join-Path $OutputDir 'prune-journal.jsonl'
    foreach ($State in $Selection) {
        Assert-EntryState $RepoRoot $State
        @{ path = $State.path; event = 'pending'; sha256 = $State.sha256 } | ConvertTo-Json -Compress | Add-Content $Journal
        Remove-Item -LiteralPath (Join-Path $RepoRoot $State.path)
        @{ path = $State.path; event = 'removed'; sha256 = $State.sha256 } | ConvertTo-Json -Compress | Add-Content $Journal
    }
    [void][IO.Directory]::CreateDirectory((Join-Path $RepoRoot 'docs/capstone/source'))
    Copy-Item -LiteralPath (Join-Path $RepoRoot 'docs/capstone/deck/zava-forward-cowork-v2-draft.pptx') -Destination (Join-Path $RepoRoot $Baseline)
    [void][IO.Directory]::CreateDirectory((Join-Path $RepoRoot 'docs/capstone/history'))
    foreach ($Move in $Moves) {
        Move-Item -LiteralPath (Join-Path $RepoRoot $Move.from) -Destination (Join-Path $RepoRoot $Move.to)
    }
    foreach ($State in $Snapshot | Where-Object { $_.path -notin $Selection.path -and $_.type -ne 'directory' }) {
        $Path = $State.path
        foreach ($Move in $Moves) {
            if ($Path -eq $Move.from -or $Path.StartsWith($Move.from + '/', [StringComparison]::Ordinal)) {
                $Path = $Move.to + $Path.Substring($Move.from.Length)
                break
            }
        }
        Assert-EntryState $RepoRoot $State $Path
    }
    $Receipt = [ordered]@{
        date = [DateTime]::UtcNow.ToString('o'); approved_selection_count = 15
        approval = 'Owner approved this exact finite selection in the capstone reorganization session.'
        archive = $ZipPath; archive_sha256 = (Get-FileHash $ZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
        inventory_members = $Snapshot.Count; full_archive_readback = $true; selected_restore_verified = $true
        protected_bytes_before_and_after = $true; selected_removed = $Selection; moves = $Moves
        active_baseline = $Baseline; baseline_sha256 = (Get-FileHash (Join-Path $RepoRoot $Baseline) -Algorithm SHA256).Hash.ToLowerInvariant()
        local_custody_only = $true; git_history_rewritten = $false
    }
    Write-Receipt (Join-Path $OutputDir 'receipt.json') $Receipt
    Write-Receipt (Join-Path $RepoRoot 'docs/capstone/history/reorganization-2026-10-29.json') $Receipt
    Write-Output "Archived and read back $($Snapshot.Count) members; restored and removed exactly 15 exports."
    Write-Output 'Protected bytes verified after three history moves. Current deck and thought-leadership bytes are unchanged.'
    Write-Output "Archive and restoration proof: $OutputDir"
}