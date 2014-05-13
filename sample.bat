@echo off
:: set paths to commands
set python="C:\Python27\python.exe"
set java="C:\Program Files\Java\jdk1.7.0_51\bin\java.exe"
set javac="C:\Program Files\Java\jdk1.7.0_51\bin\javac.exe"

:: set names for current model (should be changed for every new model)
set src_dir=sample_src
set model_name=sample

@echo on
%python% bin\dsl_to_java.py -I%src_dir%\ -d %src_dir%\%model_name%.dsl -o %src_dir%\%model_name%.java
%javac% -cp bin\octotron.jar %src_dir%\%model_name%.java -d %src_dir%
%java% -cp bin\octotron.jar octotron.exec.CreateDB %src_dir%\config.json
%java% -Dsun.net.httpserver.nodelay=true -cp bin\octotron.jar main.java.ru.parallel.octotron.exec.StartOctotron %src_dir%\config.json
