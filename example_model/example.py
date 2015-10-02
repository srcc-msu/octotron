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
GenID(nodes)

# assign to every object ip from the file
CSVReader.Declare(nodes, "example_model/ip.csv")

# declare a ring connection using data in csv file
node_node_links = EveryWithEvery(CSVReader.OrderByColumn(nodes, "example_model/ip_ring.csv", 0)
	, CSVReader.OrderByColumn(nodes, "example_model/ip_ring.csv", 1)
	, "ethernet")
GenID(node_node_links, "n-n")

# create 8 nodes and assign to them properties
# declared in example_lib.py
cpus = CreateObjects(NODES * CPU_PER_NODE, my_module
	, {
		"const" : (my_const, {"type" : "cpu"}),
		"sensor" : my_sensor,
		"trigger" : my_trigger,
		"react" : my_react
	})
GenID(cpus)

# add attribute "lid" to each cpu, that equals
# its position in the list by modulo CPU_PER_NODE
# i.e. 0, 1, 0, 1, 0, 1, 0, 1
Enumerator.Sequence(cpus, "lid", CPU_PER_NODE)

# connect every node with 2 cpus using
# two links for connection with specified types
node_cpu_links = EveryToChunks(nodes, cpus, ["contain", "chill"])
GenID(node_cpu_links, "n-c")

DiscoverConnect(cpus, [("type", "cpu")], [("type", "contain"), ("type", "chill"), ("type", "ethernet")], "type", ["^.*cpu-node-node-cpu.*$"], "mega", 4)
