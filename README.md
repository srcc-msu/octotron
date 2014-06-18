### Octotron framewrok: modeling and operational control of complex computer systems

#### Overview
This is a distributive for Octotron framework, it contains required binaries and scripts to create and run a basic model.
If you are interested in full source code - visit http://github.com/srcc-msu/octotron_core

#### Requirements:
###### To run a model:
- jre 1.7

###### To create a model:
- jdk 1.7
- jre 1.7
- [jython](http://www.jython.org/downloads.html) (tested on 2.5.3)

###### Optional
- make
- the system can be created and started on a windows system, but bash scripts will not work, unless you provide some kind of linux-like environment (not tested)

#### Model description
Every model is described by a python script, written using 'octopy' module (see [sample_src/sample.py](sample_src/sample.py)) and a user-provided json configuration file.
See [wiki](https://github.com/srcc-msu/octotron/wiki) for more information.

#### Creating a model
To create a model, run jython(*not* a standart python) on your main model file, providing the path to octotron.jar and configuration file as a parameter.

`jython -J-cp lib/octotron.jar sample_src/sample.py sample_src/config.json`

###### Creating a model with Makefile
Repace next variables in `Makefile.config`:

- MODEL_FILE - path to the main model file
- MODEL_CFG - path to the configuration file

Run `make model`

#### Start procedure
`java -Dsun.net.httpserver.nodelay=true -cp lib/octotron.jar ru.parallel.octotron.exec.StartOctotron sample_src/config.json`

The command calls the start procedure `ru.parallel.octotron.exec.StartOctotron` from main jar and passes the json configuration file.
It requires a param `-Dsun.net.httpserver.nodelay=true` to prevent the http component from slowing down (thank creators for inability to do it inside..)

##### Start procedure with a Makefile

`make run`

### Test if it works

1) Copy above commands to create sample database or run command: `make model run`

2) Go to http://127.0.0.1:4448/control/selftest in your browser.
