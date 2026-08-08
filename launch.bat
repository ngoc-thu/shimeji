@echo off
cd /d "%~dp0"
if exist "%JAVA_HOME%\bin\javaw.exe" (
    start "" "%JAVA_HOME%\bin\javaw.exe" -Xmx512m -jar Shimeji.jar
) else (
    start "" javaw -Xmx512m -jar Shimeji.jar
)
