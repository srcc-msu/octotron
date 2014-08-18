from octopy import *

node_check_sensor = {
	"chk_ssh" : True,
	"chk_ping" : True,
	"chk_mpi" : True,
	"chk_mem" : True,
	"chk_ib" : True,
	"chk_disk" : True,
	"chk_tmp" : True,
	"ib_visible" : True
}

node_check_var = {
}

node_check_react = {
	("chk_ssh", False) :
		Reaction(Critical("node failure: ssh", "type", "node", "ip"), Recover("node is good: ssh", "type", "node", "ip")),

	("chk_ping", False) :
		Reaction(Critical("node failure: ping", "type", "node", "ip"), Recover("node is good: ping", "type", "node", "ip")),

	("chk_mpi", False) :
		Reaction(Critical("node failure: mpi", "type", "node", "ip"), Recover("node is good: mpi", "type", "node", "ip")),

	("chk_mem", False) :
		Reaction(Critical("node failure: mem", "type", "node", "ip"), Recover("node is good: mem", "type", "node", "ip")),

	("chk_ib", False) :
		Reaction(Critical("node failure: ib", "type", "node", "ip"), Recover("node is good: ib", "type", "node", "ip")),

	("chk_disk", False) :
		Reaction(Critical("node failure: disk", "type", "node", "ip"), Recover("node is good: disk", "type", "node", "ip")),

	("chk_tmp", False) :
		Reaction(Critical("node failure: tmp", "type", "node", "ip"), Recover("node is good: tmp", "type", "node", "ip")),

	("ib_visible", False) :
		Reaction(Critical("node is not visible in SubNet manager", "type", "node", "ip"), Recover("node is visible in SubNet manager again", "type", "node", "ip"))
}
