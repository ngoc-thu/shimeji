param([string]$SampleDirectory)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$oldSampleDirectory = $env:SHIMEJI_SAMPLE_DIR
Push-Location -LiteralPath $projectRoot
try {
    if ($SampleDirectory) { $env:SHIMEJI_SAMPLE_DIR = $SampleDirectory }
    $python = 'python'
    $venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
    if (Test-Path -LiteralPath $venvPython) { $python = $venvPython }
    & $python -B -m unittest discover -s tests -p 'test_*.py' -v
    if ($LASTEXITCODE -ne 0) { throw 'Python tests failed.' }
    & $python -B shimeji.py --smoke-test
    if ($LASTEXITCODE -ne 0) { throw 'Qt runtime smoke test failed.' }
}
finally {
    Pop-Location
    $env:SHIMEJI_SAMPLE_DIR = $oldSampleDirectory
}
