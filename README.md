# Octotron project: Active Control and Efficient Autonomous Functioning of Supercomputers

## Overview
This is a distributive for Octotron system, it contains required binaries to create and run a basic model.

## Requirements:
#### To run a model:
- jre 1.7
- lockfile(from procmail) - for default mailinig script

#### To create a model:
- jdk 1.7
- jython (tested on 2.5.3)
- jre 1.7

#### Optional
- make/bash/cmd

## Model description
Every model is described by user-provided json configuration file and automatically generated files to store marks, reactions, rules and neo4j database folder.

## Creating a model
A model is created from one or more Jython files, written using 'octopy' module (see sample_src/sample.py)

To create a model, run Jython on your main model file, providing the path to octotron.jar and config file as a parameter.

`jython -J-cp bin/octotron.jar sample_src/sample.py sample_src/config.json`

#### Creating a model with Makefile
Replace next variables in Makefile.config:

- MODEL_FILE - path to the main Jython file
- MODEL_CFG - path to the config file

Run `make model`

## Configuration file layout desciption

Example of configuration:

    {
        "db":
        {
    		"name" : "sample",
    		"path" : "dbs/",
    	},

        "logs" :
        {
            "all" : "log/all.log",
            "errors" : "log/errors.log"
        },

        "scripts" :
        {
            "on_start" : "scripts/octotron_start.sh",
            "on_finish" : "scripts/octotron_finish.sh",
            "on_crash" : "scripts/octotron_crash.sh",

            "on_critical" : "scripts/react_mail.sh",
            "on_danger" : "scripts/react_mail.sh",
            "on_warning" : "scripts/react_mail.sh",
            "on_info" : "scripts/react_mail.sh",
            "on_recover" : "scripts/react_mail.sh"
        },

    	"graph":
    	{
        	"object_index" : ["type", "node", "ip"],
        	"link_index" : ["type"]
    	},
    
    	"http" :
    	{
    		"port" : 4448,

    		"request" : { "user" : "", "password" : "" },
    		"modify" : { "user" : "", "password" : "" },
    		"control" : { "user" : "", "password" : "" }
    	}
    }

- db.name - prefix for all model files
- db.path - the folder where the model will be stored

- graph.object_index - list of objects properties, which will be added to the DB index. 
- graph.object_index - list of links properties, which will be added to the DB index. 

- logs section specifies how a log's 'key' translates to log's filename. Log keys are used in reactions.
By default the system uses logs "all" and "errors", but you can use additional log files in customized reactions.

- scripts section specifies how a script's 'key' translates to scripts's filename. Scripts keys are used in reactions.
By default the system uses all specified scripts, but you can use additional scripts in customized reactions.
If default script key is missing - the action will not be executed.

- http.port - port where http component will listen
- http.request.{user,password} - user and password for http access to request operations, may be empty
- http.modify.{user,password} - user and password for http access to modify operations, may be empty
- http.control.{user,password} - user and password for http access to control operations, may be empty

## Start procedure
`java -Dsun.net.httpserver.nodelay=true -cp bin/octotron.jar main.java.ru.parallel.octotron.exec.StartOctotron sample_src/config.json`

The command calls the start procedure `main.java.ru.parallel.octotron.exec.StartOctotron` from main jar and passes the json configuration file.
It requires a param `-Dsun.net.httpserver.nodelay=true` to prevent the http component from slowing down (thank creators for inability to do it inside..)

#### Start procedure with a Makefile

`make run`

## Test if it works

1) Copy above commands to create sample DB or execute command: `make model run`

2) Check [127.0.0.1:4448/control/stat](127.0.0.1:4448/control/stat) in your browser.
