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
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: ssh")
				.Msg("msg"  , "{node} failure: ssh")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: ssh")
				.Msg("msg"  , "{node} is good: ssh")),

		Equals("chk_ping", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: ping")
				.Msg("msg"  , "{node} failure: ping")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: ping")
				.Msg("msg"  , "{node} is good: ping")),

		Equals("chk_mpi", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: mpi")
				.Msg("msg"  , "{node} failure: mpi")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: mpi")
				.Msg("msg"  , "{node} is good: mpi")),

		Equals("chk_mem", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: mem")
				.Msg("msg"  , "{node} failure: mem")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: mem")
				.Msg("msg"  , "{node} is good: mem")),

		Equals("chk_ib", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: ib")
				.Msg("msg"  , "{node} failure: ib")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: ib")
				.Msg("msg"  , "{node} is good: ib")),

		Equals("chk_disk", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: disk")
				.Msg("msg"  , "{node} failure: disk")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: disk")
				.Msg("msg"  , "{node} is good: disk")),

		Equals("chk_tmp", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: tmp")
				.Msg("msg"  , "{node} failure: tmp")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: tmp")
				.Msg("msg"  , "{node} is good: tmp")),

		Equals("ib_visible", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is not visible in SubNet manager")
				.Msg("msg"  , "{node} is not visible in SubNet manager")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is visible in SubNet manager again")
				.Msg("msg"  , "{node} is visible in SubNet manager again")),
	}
}
