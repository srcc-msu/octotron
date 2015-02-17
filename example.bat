@echo off

set LIB=lib\octotron.jar
set EXAMPLE_PATH=example_model
set JAVA="C:\Program Files\Java\jdk1.7.0_51\bin\java.exe"

start /wait cmd /c jython %EXAMPLE_PATH%\example.py -c %EXAMPLE_PATH%\config.json

%JAVA% -Dsun.net.httpserver.nodelay=true -cp %LIB% ru.parallel.octotron.exec.Start %EXAMPLE_PATH%\config.json
