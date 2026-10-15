@echo off
pushd "%~dp0" || exit /b 1
set "SHIMEJI_PYTHON=python"
if exist ".venv\Scripts\python.exe" set "SHIMEJI_PYTHON=.venv\Scripts\python.exe"
"%SHIMEJI_PYTHON%" shimeji.py %*
set "SHIMEJI_RESULT=%ERRORLEVEL%"
popd
exit /b %SHIMEJI_RESULT%
