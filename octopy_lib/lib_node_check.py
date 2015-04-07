from octopy import *

def NodeCheckModule(timeout = Hours(1)):
	return {
		"sensor" : {
			"chk_mpi" : Boolean(timeout),
			"chk_ib" : Boolean(timeout),
			"ib_visible" : Boolean(timeout),
		},

		"var" : {
			"node_check_total_errors" : AStrictNotMatchCount(true, EDependencyType.SELF
				, "chk_mpi"
				, "ib_visible")
		},

		"react" : {
			Equals("chk_mpi", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: failure: mpi")
					.Msg("msg"  , "{node}: failure: mpi")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: is good: mpi")
					.Msg("msg"  , "{node}: is good: mpi")),

			Equals("ib_visible", False) :
				( Danger("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: is not visible in SubNet manager")
					.Msg("msg"  , "{node}: is not visible in SubNet manager")
				, Recover("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: is visible in SubNet manager again")
					.Msg("msg"  , "{node}: is visible in SubNet manager again")),
		}
	}
