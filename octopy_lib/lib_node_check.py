from octopy import *

NODE_CHECK_UPDATE_TIME = Hours(1)

node_check_module = {
	"sensor" : {
		"chk_ssh" : Boolean(NODE_CHECK_UPDATE_TIME),
		"chk_mpi" : Boolean(NODE_CHECK_UPDATE_TIME),
		"chk_ib" : Boolean(NODE_CHECK_UPDATE_TIME),
		"ib_visible" : Boolean(NODE_CHECK_UPDATE_TIME),
	},

	"react" : {
		Equals("chk_ssh", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: ssh")
				.Msg("msg"  , "{node} failure: ssh")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: ssh")
				.Msg("msg"  , "{node} is good: ssh")),

		Equals("chk_mpi", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: mpi")
				.Msg("msg"  , "{node} failure: mpi")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: mpi")
				.Msg("msg"  , "{node} is good: mpi")),

		Equals("chk_ib", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node failure: ib")
				.Msg("msg"  , "{node} failure: ib")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is good: ib")
				.Msg("msg"  , "{node} is good: ib")),

		Equals("ib_visible", False) :
			( Critical("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is not visible in SubNet manager")
				.Msg("msg"  , "{node} is not visible in SubNet manager")
			, Recover("tag", "NODE").Msg("loc", "{node}")
				.Msg("descr", "node is visible in SubNet manager again")
				.Msg("msg"  , "{node} is visible in SubNet manager again")),
	}
}
