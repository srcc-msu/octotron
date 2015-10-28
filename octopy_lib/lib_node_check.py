from octopy import *

def NodeCheckModule(timeout = Hours(1)):
	return {
		"sensor" : {
			"mpi_check" : Boolean(timeout),
			"ib_check" : Boolean(timeout),
			"ib_visibility_check" : Boolean(timeout),
		},

		"trigger" : {
			"mpi_check_failed" : Match("mpi_check", False),
			"ib_check_failed" : Match("ib_check", False),
			"ib_visibility_check_failed" : Match("ib_visibility_check", False),
		},

		"react" : {
			"notify_mpi_check_failed" : Reaction()
				.On("mpi_check_failed")
				.Begin(Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: failure: mpi")
					.Msg("msg"  , "{node}: failure: mpi"))
				.End(RWarning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: is good: mpi")
					.Msg("msg"  , "{node}: is good: mpi")),

			"notify_ib_check_failed" : Reaction()
				.On("ib_check_failed")
				.Begin(Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: failure: ib check")
					.Msg("msg"  , "{node}: failure: ib check"))
				.End(RWarning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: is good: ib check")
					.Msg("msg"  , "{node}: is good: ib check")),

			"notify_ib_visibility_check_failed" : Reaction()
				.On("ib_visibility_check_failed")
				.Begin(Warning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: failure: node is not visible in subnet manager")
					.Msg("msg"  , "{node}: failure: node is not visible in subnet manager"))
				.End(RWarning("tag", "NODE").Msg("loc", "{node}")
					.Msg("descr", "{type}: is good: node is visible in subnet manager")
					.Msg("msg"  , "{node}: is good: node is visible in subnet manager")),
		}
	}


def ChassisNodeCheck(failed_nodes = 8, loc = "{id}"):
	return {
		"var" : {
			"mpi_check_failed_count" : ASoftMatchCount(EDependecyType.OUT, "mpi_check_failed"),
			"ib_check_failed_count" : ASoftMatchCount(EDependecyType.OUT, "ib_check_failed"),
			"ib_visibility_check_failed_count" : ASoftMatchCount(EDependecyType.OUT, "ib_visibility_check_failed"),

			"ping_failed_count" : ASoftMatchCount(EDependecyType.OUT, "ping_failed"),
		},

		"trigger" : {
			"many_mpi_check_failed" : GT("mpi_check_failed_count", failed_nodes),
			"many_ib_check_failed" : GT("ib_check_failed_count", failed_nodes),
			"many_ib_visibility_check_failed" : GT("ib_visibility_check_failed_count", failed_nodes),

			"many_ping_failed" : GT("ping_failed_count", failed_nodes),
		},

		"react" : {

			"notify_many_mpi_check_failed" : Reaction()
				.On("many_mpi_check_failed")
				.Begin(Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: many nodes failed mpi check")
					.Msg("msg", loc + ": many nodes failed mpi check"))
				.End(RDanger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: nodes mpi check is mostly ok")
					.Msg("msg", loc + ": nodes mpi check is mostly ok")),

			"notify_many_ib_check_failed" : Reaction()
				.On("many_ib_check_failed")
				.Begin(Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: many nodes failed ib check")
					.Msg("msg", loc + ": many nodes failed ib check"))
				.End(RDanger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: nodes ib check is mostly ok")
					.Msg("msg", loc + ": nodes ib check is mostly ok")),

			"notify_many_ib_visibility_check_failed" : Reaction()
				.On("many_ib_visibility_check_failed")
				.Begin(Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: many nodes failed ib visibility check")
					.Msg("msg", loc + ": many nodes failed ib visibility check"))
				.End(RDanger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: nodes ib visibility check is mostly ok")
					.Msg("msg", loc + ": nodes ib visibility check is mostly ok")),

			"notify_many_ping_failed" : Reaction()
				.On("many_ping_failed")
				.Begin(Danger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: many nodes failed ping check")
					.Msg("msg", loc + ": many nodes failed ping check"))
				.End(RDanger("tag", "NODE").Msg("loc", loc)
					.Msg("descr", "{type}: nodes ping check is mostly ok")
					.Msg("msg", loc + ": nodes ping check is mostly ok")),
		}
	}
