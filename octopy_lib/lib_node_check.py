from octopy import *

def NodeCheckModule(timeout = Hours(1)):
	return {
		"sensor" : {
			"chk_mpi" : Boolean(timeout),
			"chk_ib" : Boolean(timeout),
			"ib_visible" : Boolean(timeout),
		},

		"react" : {
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
