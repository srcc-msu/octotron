include Makefile.config

OCTO_LIB=lib/octotron.jar
JAVA_PARAM=-d64 -Dsun.net.httpserver.nodelay=true -cp lib/jersey-core-1.18.1.jar:$(OCTO_LIB)

all: run

run: $(OCTO_LIB) $(MODEL_CFG)
	java -D_OCTOTRON_MAIN $(JAVA_PARAM) $(USR_JAVA_PARAM) ru.parallel.octotron.exec.Start $(MODEL_CFG)

TEST_CFG=test_model/config.json

test_run: $(OCTO_LIB) $(TEST_CFG)
	java -D_OCTOTRON_MAIN $(JAVA_PARAM) $(USR_JAVA_PARAM) ru.parallel.octotron.exec.Start $(TEST_CFG)

$(OCTO_LIB):
	wget -O $(OCTO_LIB) 'https://github.com/srcc-msu/octotron_core/releases/download/v4.3.0/octotron.jar'

clean:
	rm -f octopy/*.class
	rm -f octopy_lib/*.class

.PHONY: model run clean

# staff to keep distro up-to-date, ignore it
renew:
	cp ../octotron_core/bin/octotron.jar $(OCTO_LIB)
