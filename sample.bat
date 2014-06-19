@echo off

set LIB=lib\octotron.jar
set SAMPLE_PATH=sample_src

set JYTHONPATH=%~dp0
set CLASSPATH=%~dp0%LIB%
set JAVA="C:\Program Files\Java\jdk1.7.0_51\bin\java.exe"

start /wait cmd /c jython %SAMPLE_PATH%\sample.py -c %SAMPLE_PATH%\config.json

%JAVA% -Dsun.net.httpserver.nodelay=true -cp %LIB% ru.parallel.octotron.exec.StartOctotron %SAMPLE_PATH%\config.json
