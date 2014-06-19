### Octotron framework: modeling and monitoring of complex computer systems

#### Overview
This is a distributive for Octotron framework, it contains required binaries and scripts to create and run a basic model.

Full project documentation is available in wiki: https://github.com/srcc-msu/octotron/wiki

If you are interested in full source code - visit http://github.com/srcc-msu/octotron_core

#### Requirements:
###### To run a model:
- jre 1.7 (java 7 runtime)

###### To create a model:
- jdk 1.7 (java 7 sdk)
- jre 1.7 (java 7 runtime)
- jython 2.5.3 [see here for details](http://www.jython.org/downloads.html)

###### Optional
- make
- the system can be created and started on a windows system, but bash scripts will not work, unless you provide some kind of linux-like environment (not tested)

#### Model description
Every model is described by a python script, written using 'octopy' module (see [sample_src/sample.py](sample_src/sample.py)) and a user-provided json configuration file.
See [wiki](https://github.com/srcc-msu/octotron/wiki) for more information.

#### Model creation with a Makefile
Repace next variables in `Makefile.config`:

- MODEL_FILE - path to the main model file
- MODEL_CFG - path to the configuration file

After that you can create the model by running:
```bash
make model
```

#### Start procedure with a Makefile
Assuming you have set the required variables in Makefile.config on last step, run:
```bash
make run
```

### Test if it works

1) Copy above commands to create sample database or run:
```bash
make model run
```

2) Go to http://127.0.0.1:4448/control/selftest in your browser. Press enter if you are promted for credentials - empty username and password are set for a sample model.


#### Alternative - Manual model creation
To create a model, run `jython`(*not* a standart python) from main folder, providing the path to octotron.jar, relative path to your model file and `-c` flag with the path to your configuration file.

```bash
jython -J-cp lib/octotron.jar sample_src/sample.py -c sample_src/config.json
```

#### Alternative - Manual start procedure
You need to call the start procedure `ru.parallel.octotron.exec.StartOctotron` from main jar, providing the path to your json configuration file.
The command requires a param `-Dsun.net.httpserver.nodelay=true` to prevent the http component from slowing down (thank creators for inability to do it inside..)

```bash
java -Dsun.net.httpserver.nodelay=true -cp lib/octotron.jar ru.parallel.octotron.exec.StartOctotron sample_src/config.json
```

#### Alternative - windows systems
sample.bat will create and run the model (not tested)
