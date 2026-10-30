$base = ".\docs\capstone\thought-leadership\everything-but-the-software"
$tectonic = "$env:LOCALAPPDATA\Programs\Tectonic\0.17.0\tectonic.exe"
$paper = Join-Path $base "main.tex"
$out = $base

New-Item -ItemType Directory -Path $out -Force | Out-Null

& $tectonic --untrusted --keep-logs --keep-intermediates --outdir $out $paper