### Octotron framework: modeling and monitoring of complex computer systems

#### Overview
This is a distributive for Octotron framework, it contains required binaries and scripts to create and run a basic model.

Full project documentation is available in wiki: https://github.com/srcc-msu/octotron/wiki

If you are interested in full source code - visit http://github.com/srcc-msu/octotron_core

The current versions uses a v4.3.0 release of Octotron(https://github.com/srcc-msu/octotron_core/releases/tag/v4.3.0)

#### Requirements:
###### To run a model:
- jre 1.7 (java 7 runtime)

###### Optional
- make
- the system can be created and started on a windows system, but bash scripts will not work, unless you provide some kind of linux-like environment (not tested)

#### Model description
Every model is described by a python script, written using 'octopy' module (see [example_src/example.py](example_model/example.py)) and a user-provided json configuration file.
See [wiki](https://github.com/srcc-msu/octotron/wiki) for more information.

#### Model creation and running with a Makefile
Repace next variables in `Makefile.config`:

- MODEL_CFG - path to the configuration file

After that you can create the model by running:
```bash
make run
```

### Test if it works

Go to http://127.0.0.1:4448/control/selftest in your browser. Press enter if you are promted for credentials - empty username and password are set for the example model.


#### Alternative - Manual start procedure
You need to call the start procedure `ru.parallel.octotron.exec.Start` from main jar, providing the path to your json configuration file.
The command requires a param `-Dsun.net.httpserver.nodelay=true` to prevent the http component from slowing down (thank creators for inability to do it inside..)

```bash
java -Dsun.net.httpserver.nodelay=true -cp lib/octotron.jar ru.parallel.octotron.exec.Start example_model/config.json
```

#### Alternative - windows systems
example.bat will create and run the model (not tested)
