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
			(Critical("NODE", "{node} failure: ssh"), Recover("{node} is good: ssh")),

		Equals("chk_ping", False) :
			(Critical("NODE", "{node} failure: ping"), Recover("{node} is good: ping")),

		Equals("chk_mpi", False) :
			(Critical("NODE", "{node} failure: mpi"), Recover("{node} is good: mpi")),

		Equals("chk_mem", False) :
			(Critical("NODE", "{node} failure: mem"), Recover("{node} is good: mem")),

		Equals("chk_ib", False) :
			(Critical("NODE", "{node} failure: ib"), Recover("{node} is good: ib")),

		Equals("chk_disk", False) :
			(Critical("NODE", "{node} failure: disk"), Recover("{node} is good: disk")),

		Equals("chk_tmp", False) :
			(Critical("NODE", "{node} failure: tmp"), Recover("{node} is good: tmp")),

		Equals("ib_visible", False) :
			(Critical("NODE", "{node} is not visible in SubNet manager"), Recover("{node} is visible in SubNet manager again"))
	}
}
