include Makefile.config

# assuming 8GB RAM total
# 4GB - for Octotron: 2GB - for heap, 2GB - for neo4j mapping
# attribute will take the most space in typical configs

OCTO_LIB=lib/octotron.jar
JAVA_PARAM=-d64 -XX:+UseConcMarkSweepGC -Xms1G -Xmx2G -Dsun.net.httpserver.nodelay=true -cp $(OCTO_LIB)

all : model

run: $(OCTO_LIB) $(MODEL_CFG)
	java $(JAVA_PARAM) ru.parallel.octotron.exec.Start $(MODEL_CFG)

clean:
	rm -f octopy/*.class
	rm -f octopy_lib/*.class
	rm -f $(MODEL_DIR)/*.class

.PHONY: model run clean

# staff to keep distro up-to-date, ignore it
renew:
	cp ../octotron_core/bin/octotron.jar $(OCTO_LIB)
