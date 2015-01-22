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
					.Msg("descr", "{type} failure: mpi")
					.Msg("msg"  , "{type}({node}) failure: mpi")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type} is good: mpi")
					.Msg("msg"  , "{type}({node}) is good: mpi")),

			Equals("chk_ib", False) :
				( Critical("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type} failure: ib")
					.Msg("msg"  , "{type}({node}) failure: ib")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type} is good: ib")
					.Msg("msg"  , "{type}({node}) is good: ib")),

			Equals("ib_visible", False) :
				( Critical("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type} is not visible in SubNet manager")
					.Msg("msg"  , "{type}({node}) is not visible in SubNet manager")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type} is visible in SubNet manager again")
					.Msg("msg"  , "{type}({node}) is visible in SubNet manager again")),
		}
	}
