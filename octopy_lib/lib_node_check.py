from octopy import *

node_check_module = {
	"sensor" : {
		"chk_ssh" : True,
		"chk_ping" : True,
		"chk_mpi" : True,
		"chk_mem" : True,
		"chk_ib" : True,
		"chk_disk" : True,
		"chk_tmp" : True,
		"ib_visible" : True
	},

	"react" : {
		Equals("chk_ssh", False) :
			(Critical("node failure: ssh", "type", "node", "ip"), Recover("node is good: ssh", "type", "node", "ip")),

		Equals("chk_ping", False) :
			(Critical("node failure: ping", "type", "node", "ip"), Recover("node is good: ping", "type", "node", "ip")),

		Equals("chk_mpi", False) :
			(Critical("node failure: mpi", "type", "node", "ip"), Recover("node is good: mpi", "type", "node", "ip")),

		Equals("chk_mem", False) :
			(Critical("node failure: mem", "type", "node", "ip"), Recover("node is good: mem", "type", "node", "ip")),

		Equals("chk_ib", False) :
			(Critical("node failure: ib", "type", "node", "ip"), Recover("node is good: ib", "type", "node", "ip")),

		Equals("chk_disk", False) :
			(Critical("node failure: disk", "type", "node", "ip"), Recover("node is good: disk", "type", "node", "ip")),

		Equals("chk_tmp", False) :
			(Critical("node failure: tmp", "type", "node", "ip"), Recover("node is good: tmp", "type", "node", "ip")),

		Equals("ib_visible", False) :
			(Critical("node is not visible in SubNet manager", "type", "node", "ip"), Recover("node is visible in SubNet manager again", "type", "node", "ip"))
	}
}
