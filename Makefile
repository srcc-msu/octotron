include Makefile.config

OCTO_LIB=lib/octotron.jar
JAVA_PARAM=-Dsun.net.httpserver.nodelay=true

all : model

model: $(OCTO_LIB) $(MODEL_FILE) $(MODEL_CFG) clean
	jython -J-cp $(OCTO_LIB) $(MODEL_FILE) -c $(MODEL_CFG)

run: $(OCTO_LIB) $(MODEL_CFG)
	java $(JAVA_PARAM) -cp $(OCTO_LIB) ru.parallel.octotron.exec.StartOctotron $(MODEL_CFG)

clean:
	rm -f octopy/*.class

.PHONY: model run clean

# staff to keep distro up-to-date, ignore it
renew:
	cp ../octotron_core/bin/octotron.jar $(OCTO_LIB)
