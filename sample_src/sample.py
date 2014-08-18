# include all system wrappers
from octopy import *

# include all standard library files
from octopy_lib import *

# include our sample library
from sample_lib import *

NODES = 4
CPU_PER_NODE = 2

# create 4 objects with "type" = "node"
# assigne to them attributes from collectd library module
nodes = CreateObjects(
	const  = {"type" : "node"}
	, sensor = cd_node_sensor
	, var = cd_node_var
	, react = cd_node_react
	, count  = NODES)

# assign to every object ip from the file
CSVReader.Declare(nodes, "sample_src/ip.csv")

# create 8 nodes and assign to them properties, declared in sample_lib.py
cpus = CreateObjects(
	const  = [cpu_const, {"type" : "cpu"}]
	, sensor = cpu_sensor
	, var    = cpu_var
	, react  = cpu_react
	, count  = NODES * CPU_PER_NODE)

# add attribute "lid" to each cpu, that equals
# its position in list by modulo CPU_PER_NODE
# 0, 1, 0, 1, 0, 1, 0, 1
Enumerator.Sequence(cpus, "lid", CPU_PER_NODE)

# connect every node with 2 cpus
EveryToChunks(nodes, cpus, "contain", "chill")
