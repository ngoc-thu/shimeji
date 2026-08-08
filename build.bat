@echo off
cd /d "%~dp0"
echo Building Shimeji for Windows/Linux...
if exist classes rmdir /s /q classes
mkdir classes
if exist Shimeji.jar del /q Shimeji.jar

powershell -Command "javac -encoding UTF-8 -cp 'lib/*' -d classes (Get-ChildItem -Recurse -Filter *.java src, src_generic, src_x11, src_win | Select-Object -ExpandProperty FullName)"
if %ERRORLEVEL% NEQ 0 (
    echo Compilation failed.
    pause
    exit /b %ERRORLEVEL%
)

jar cfm Shimeji.jar MANIFEST.MF -C classes .
if %ERRORLEVEL% NEQ 0 (
    echo Jar creation failed.
    pause
    exit /b %ERRORLEVEL%
)

if exist ShimejiLauncher.cs (
    C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /nologo /target:winexe /out:Shimeji.exe /win32icon:shimeji.ico /r:System.Windows.Forms.dll ShimejiLauncher.cs >nul
)

if exist ShimejiSettingsLauncher.cs (
    C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /nologo /target:winexe /out:ShimejiSettings.exe /win32icon:shimeji.ico /r:System.Windows.Forms.dll ShimejiSettingsLauncher.cs >nul
)

echo Build successful! Created Shimeji.jar, Shimeji.exe, ShimejiSettings.exe
