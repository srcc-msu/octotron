# include all system wrappers
from octopy import *

# include our sample library
from sample_lib import *

NODES = 4
CPU_PER_NODE = 2

# create 4 objects with "type" = "node"
nodes = CreateObjects({"type" : "node"}, count = NODES)

# assign to every object ip from the file
nodes.SetAttributesFromCsv("sample_src/ip.csv")

# create 8 nodes and assign to them properties, declared in sample_lib.py
cpus = CreateObjects([{"type" : "cpu"}, cpu_attributes], cpu_rules, cpu_reactions, count = NODES * CPU_PER_NODE)

# add attribute "lid" to each cpu, that equals
# its position in list by module CPU_PER_NODE
# 0, 1, 0, 1, 0, 1, 0, 1
Enumerator.Sequence(cpus, "lid", CPU_PER_NODE)

# connect every node with 2 cpus
EveryToChunks(nodes, cpus, {"type" : "contain"})
