#!/usr/bin/env pwsh
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT
#Requires -Version 7.4
<#
.SYNOPSIS
Check editable diagram primitives without Office or third-party modules.
.PARAMETER RepoRoot
Repository containing the shared native shape helper.
.EXAMPLE
pwsh -NoProfile -File tools/capstone/Test-NativeShapes.ps1 -RepoRoot .
.NOTES
Constructs XML in memory; no presentation or working data is modified.
#>
[CmdletBinding()]
param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).ProviderPath
)
$ErrorActionPreference = 'Stop'

function Assert-NativeShape {
    param($Element, [string]$XPath)
    $Document = [xml]'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree/></p:cSld></p:sld>'
    $Namespaces = Get-Namespaces $Document
    $Tree = $Document.SelectSingleNode('/p:sld/p:cSld/p:spTree', $Namespaces)
    Add-NativeShape $Document $Tree ([pscustomobject]$Element) 900000 3
    if (-not $Document.SelectSingleNode($XPath, $Namespaces)) { throw "Missing native shape property: $XPath" }
}

function Assert-RefusedShape {
    param($Element, [string]$Reason)
    $Refused = $false
    try { Assert-NativeShape $Element '//p:sp' }
    catch {
        if ($_.Exception.Message -notlike "*$Reason*") { throw }
        $Refused = $true
    }
    if (-not $Refused) { throw "Expected refusal: $Reason" }
}

if ($MyInvocation.InvocationName -ne '.') {
    . (Join-Path $RepoRoot 'tools/cowork-native-recovery/Invoke-StoryReview.ps1') -RepoRoot $RepoRoot -OutputDir ([IO.Path]::GetTempPath())
    foreach ($Geometry in @('rect', 'ellipse', 'roundRect', 'line', 'can', 'chevron', 'rightArrow', 'downArrow')) {
        Assert-NativeShape @{ key = 'primitive'; box = @(0.6, 2, 2, 1); geometry = $Geometry } "//a:prstGeom[@prst='$Geometry']"
    }
    $Polygon = @{ key = 'polygon'; box = @(0.6, 2, 2, 1); geometry = 'polygon'; points = @(@(0, 0), @(100, 0), @(42, 100)); fill = 'E8F1ED'; stroke = '173F35' }
    Assert-NativeShape $Polygon '//a:custGeom/a:pathLst/a:path/a:close'
    Assert-NativeShape @{ key = 'pie'; box = @(0.6, 2, 2, 2); geometry = 'pie'; angles = @(315, 45) } "//a:gd[@name='adj1'][@fmla='val 18900000']"
    Assert-NativeShape @{ key = 'centred'; box = @(0.6, 2, 2, 1); text = 'Choice'; size = 20; valign = 'ctr'; stroke = '173F35'; stroke_width = 1.5 } "//a:bodyPr[@anchor='ctr']"
    Assert-NativeShape @{ key = 'outline'; box = @(0.6, 2, 2, 1); stroke = '173F35'; stroke_width = 1.5 } "//a:ln[@w='19050']/a:solidFill/a:srgbClr[@val='173F35']"
    Assert-RefusedShape @{ key = 'negative-size'; box = @(0.6, 2, -1, 1) } 'Invalid margins'
    Assert-RefusedShape @{ key = 'nonfinite'; box = @(0.6, 2, [double]::NaN, 1) } 'Invalid margins'
    Assert-RefusedShape @{ key = 'off-slide'; box = @(12, 2, 2, 1) } 'Invalid margins'
    Assert-RefusedShape @{ key = 'unknown'; box = @(0.6, 2, 2, 1); geometry = 'hexagon' } 'Unsupported native geometry'
    Assert-RefusedShape @{ key = 'pie'; box = @(0.6, 2, 2, 2); geometry = 'pie'; angles = @(30, 30) } 'Invalid pie angles'
    Assert-RefusedShape @{ key = 'polygon'; box = @(0.6, 2, 2, 1); geometry = 'polygon'; points = @(@(0, 0), @(100, 0)) } 'three points'
    Assert-RefusedShape @{ key = 'polygon'; box = @(0.6, 2, 2, 1); geometry = 'polygon'; points = @(@(0, 0), @(101, 0), @(50, 100)) } 'Invalid polygon point'
    Assert-RefusedShape @{ key = 'outline'; box = @(0.6, 2, 2, 1); stroke = 'red' } 'Invalid native outline'
    Assert-RefusedShape @{ key = 'anchor'; box = @(0.6, 2, 2, 1); valign = 'middle' } 'Invalid vertical anchor'
    Write-Output '21 native-shape checks passed: geometry, path closure, pie angles, outlines, centring and invalid-input refusal.'
}
