include Makefile.config

# assuming 8GB RAM total
# 4GB - for Octotron: 2GB - for heap, 2GB - for neo4j mapping
# attribute will take the most space in typical configs

OCTO_LIB=lib/octotron.jar
JAVA_PARAM=-d64 -Dsun.net.httpserver.nodelay=true -cp lib/jersey-core-1.18.1.jar:$(OCTO_LIB)

all: run

run: $(OCTO_LIB) $(MODEL_CFG)
	java $(JAVA_PARAM) $(USR_JAVA_PARAM) ru.parallel.octotron.exec.Start $(MODEL_CFG)

$(OCTO_LIB):
	wget -P lib 'https://github.com/srcc-msu/octotron_core/releases/download/v3.4.3-rc/octotron.jar'

clean:
	rm -f octopy/*.class
	rm -f octopy_lib/*.class

.PHONY: model run clean

# staff to keep distro up-to-date, ignore it
renew:
	cp ../octotron_core/bin/octotron.jar $(OCTO_LIB)
