include Makefile.config

OCTO_LIB=lib/octotron.jar
JAVA_PARAM=-Dsun.net.httpserver.nodelay=true

all : model

model: $(OCTO_LIB) $(MODEL_FILE) $(MODEL_CFG)
	jython -J-cp $(OCTO_LIB) $(MODEL_FILE) -c $(MODEL_CFG)

run: $(OCTO_LIB) $(MODEL_CFG)
	java $(JAVA_PARAM) -cp $(OCTO_LIB) main.java.ru.parallel.octotron.exec.StartOctotron $(MODEL_CFG)

.PHONY: model run

# staff to keep distro up-to-date, ignore it
renew:
	cp ~/workspace/octotron/bin/octotron.jar $(OCTO_LIB)
