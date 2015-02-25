from octopy import *

def DrmsModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "queue",
#			"tasks_running_min" # user provided
#			"tasks_queued_min" # user provided
#			"cpus_total" # user provided
#			"cpus_free_max_pct" # user provided
#			"cpus_blocked_max_pct" # user provided
		},

		"sensor" : {
			"tasks_running" : Long(timeout),
			"tasks_queued"  : Long(timeout),

			"cpus_current"  : Long(timeout),

			"cpus_free"    : Long(timeout),
			"cpus_blocked" : Long(timeout),
		},

		"var" : {
			"tasks_running_ok" : LowerArgThreshold("tasks_running", "tasks_running_min"),
			"tasks_queued_ok"  : LowerArgThreshold("tasks_queued", "tasks_queued_min"),

			"all_cpus_present" : ArgMatch("cpus_current", "cpus_total"),

			"cpus_free_pct"    : ToArgPct("cpus_free", "cpus_total"),
			"cpus_blocked_pct" : ToArgPct("cpus_blocked", "cpus_total"),

			"cpus_free_ok"    : UpperArgThreshold("cpus_free_pct", "cpus_free_max_pct"),
			"cpus_blocked_ok" : UpperArgThreshold("cpus_blocked_pct", "cpus_blocked_max_pct"),
		},

		"react" : {
			Equals("tasks_running_ok", False) :
				Warning("tag", "QUEUE").Msg("loc", "{name}")
					.Msg("descr", "{type}: running tasks count is low")
					.Msg("msg"  , "{type}({name}): running tasks count is low({tasks_running})"),

			Equals("tasks_queued_ok", False) :
				Warning("tag", "QUEUE").Msg("loc", "{name}")
					.Msg("descr", "{type}: queued tasks count is low")
					.Msg("msg"  , "{type}({name}): queued tasks count is low({tasks_queued})"),

			Equals("all_cpus_present", False) :
				Danger("tag", "QUEUE").Msg("loc", "{name}")
					.Msg("descr", "{type}: the queue has lost some cpus")
					.Msg("msg"  , "{type}({name}): the queue has lost some cpus({cpus_current} / {cpus_total})"),

			Equals("cpus_free_ok", False) :
				Danger("tag", "QUEUE").Msg("loc", "{name}")
					.Msg("descr", "{type}: too many free cpus")
					.Msg("msg"  , "{type}({name}): too many free cpus({cpus_free} - {cpus_free_pct}%)"),

			Equals("cpus_blocked_ok", False) :
				Danger("tag", "QUEUE").Msg("loc", "{name}")
					.Msg("descr", "{type}: too many blocked cpus")
					.Msg("msg"  , "{type}({name}): too many blocked cpus({cpus_blocked} - {cpus_blocked_pct}%)"),
		}
	}
