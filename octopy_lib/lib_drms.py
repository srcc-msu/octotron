from octopy import *

def DrmsModule(timeout = Minutes(10), key = "queue"):
	return {
		"const" : {
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
			"cpus_free_pct"    : ToArgPct("cpus_free", "cpus_total"),
			"cpus_blocked_pct" : ToArgPct("cpus_blocked", "cpus_total"),
		},

		"trigger" : {
			"few_tasks_running" : LTArg("tasks_running", "tasks_running_min"),
			"few_tasks_queued" : LTArg("tasks_queued", "tasks_queued_min"),
			"cpus_missing" : NotMatchArg("cpus_current", "cpus_total"),
			"many_free" : GTArg("cpus_free_pct", "cpus_free_max_pct"),
			"many_blocked" : GTArg("cpus_blocked_pct", "cpus_blocked_max_pct"),
		},

		"react" : {
			"notify_few_tasks_running" : Reaction()
				.On("few_tasks_running")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: running tasks count is low")
					.Msg("msg"  , "{type}({" + key + "}): running tasks count is low: {tasks_running}")),

			"notify_few_tasks_queued" : Reaction()
				.On("few_tasks_queued")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: queued tasks count is low")
					.Msg("msg"  , "{type}({" + key + "}): queued tasks count is low: {tasks_queued}")),

			"notify_cpus_missing" : Reaction()
				.On("cpus_missing")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: the queue has lost some cpus")
					.Msg("msg"  , "{type}({" + key + "}): the queue has lost some cpus: {cpus_current} / {cpus_total}")),

			"notify_many_free" : Reaction()
				.On("many_free")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: too many free cpus")
					.Msg("msg"  , "{type}({" + key + "}): too many free cpus: {cpus_free} = {cpus_free_pct}%")),

			"notify_many_blocked" : Reaction()
				.On("many_blocked")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: too many blocked cpus")
					.Msg("msg"  , "{type}({" + key + "}): too many blocked cpus: {cpus_blocked} = {cpus_blocked_pct}%")),
		}
	}
