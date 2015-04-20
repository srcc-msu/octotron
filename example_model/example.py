# include all system wrappers
from octopy import *

# include all standard library files
from octopy_lib import *

# include our example library
from example_lib import *

NODES = 4
CPU_PER_NODE = 2

# create 4 objects with "type" = "node" and assign
# to them attributes from the collectd library module
nodes = CreateObjects(NODES, lib_collectd.NodeModule()
	, { "const" : {"type" : "node"}})

# assign to every object ip from the file
CSVReader.Declare(nodes, "example_model/ip.csv")

# declare a ring connection using data in csv file
EveryWithEvery(CSVReader.OrderByColumn(nodes, "example_model/ip_ring.csv", 0)
	, CSVReader.OrderByColumn(nodes, "example_model/ip_ring.csv", 1)
	, "ethernet")

# create 8 nodes and assign to them properties
# declared in example_lib.py
cpus = CreateObjects(NODES * CPU_PER_NODE, my_module
	, {
		"const" : (my_const, {"type" : "cpu"}),
		"sensor" : my_sensor,
		"var" : my_var,
		"react" : my_react
	})

# add attribute "lid" to each cpu, that equals
# its position in the list by modulo CPU_PER_NODE
# i.e. 0, 1, 0, 1, 0, 1, 0, 1
Enumerator.Sequence(cpus, "lid", CPU_PER_NODE)

# connect every node with 2 cpus using
# two links for connection with specified types
EveryToChunks(nodes, cpus, ["contain", "chill"])
