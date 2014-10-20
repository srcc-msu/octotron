@echo off

set LIB=lib\octotron.jar
set SAMPLE_PATH=sample_model
set JAVA="C:\Program Files\Java\jdk1.7.0_51\bin\java.exe"

start /wait cmd /c jython %SAMPLE_PATH%\sample.py -c %SAMPLE_PATH%\config.json

%JAVA% -Dsun.net.httpserver.nodelay=true -cp %LIB% ru.parallel.octotron.exec.Start %SAMPLE_PATH%\config.json
