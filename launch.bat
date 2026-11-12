@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "JAVA_CMD=javaw"
set "JAVA_CHECK=java"

if exist "%JAVA_HOME%\bin\javaw.exe" (
    set "JAVA_CMD=%JAVA_HOME%\bin\javaw.exe"
)
if exist "%JAVA_HOME%\bin\java.exe" (
    set "JAVA_CHECK=%JAVA_HOME%\bin\java.exe"
)

set "JAVA_OPTS="
set "JVER="
for /f "tokens=3" %%g in ('"%JAVA_CHECK%" -version 2^>^&1 ^| findstr /i "version"') do (
    set "JVER=%%~g"
)

if not "%JVER%"=="" (
    for /f "delims=." %%a in ("%JVER%") do set "MAJOR_VER=%%a"
    if not "!MAJOR_VER!"=="" (
        if !MAJOR_VER! GEQ 9 (
            set JAVA_OPTS=--add-opens java.desktop/sun.awt=ALL-UNNAMED --add-opens java.desktop/sun.awt.windows=ALL-UNNAMED --add-opens java.desktop/sun.java2d=ALL-UNNAMED --add-opens java.desktop/java.awt=ALL-UNNAMED --add-opens java.desktop/java.awt.peer=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.reflect=ALL-UNNAMED
        )
    )
)

start "" "%JAVA_CMD%" %JAVA_OPTS% -Xmx1000m -classpath Shimeji.jar -Djava.util.logging.config.file=./conf/logging.properties com.group_finity.mascot.Main %*
