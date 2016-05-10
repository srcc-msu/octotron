from octopy import *

def DrmsModule(timeout = Minutes(10), key = "queue"):
	return {
		"const" : {
#			"tasks_running_min" # user provided
#			"tasks_queued_min" # user provided
#			"nodes_total" # user provided
#			"nodes_free_max_pct" # user provided
#			"nodes_blocked_max_pct" # user provided
		},

		"sensor" : {
			"tasks_running" : Long(timeout),
			"tasks_queued"  : Long(timeout),

			"nodes_current"  : Long(timeout),

			"nodes_free"    : Long(timeout),
			"nodes_blocked" : Long(timeout),
		},

		"var" : {
			"nodes_free_pct"    : ToArgPct("nodes_free", "nodes_total"),
			"nodes_blocked_pct" : ToArgPct("nodes_blocked", "nodes_total"),
		},

		"trigger" : {
			"few_tasks_running" : LTArg("tasks_running", "tasks_running_min"),
			"few_tasks_queued" : LTArg("tasks_queued", "tasks_queued_min"),
			"nodes_missing" : NotMatchArg("nodes_current", "nodes_total"),
			"many_free" : GTArg("nodes_free_pct", "nodes_free_max_pct"),
			"many_blocked" : GTArg("nodes_blocked_pct", "nodes_blocked_max_pct"),
		},

		"react" : {
			"notify_few_tasks_running" : Reaction()
				.On("few_tasks_running")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: running tasks count is low")
					.Msg("msg"  , "{type}({" + key + "}): running tasks count is low: {tasks_running}"))
				.End(RDanger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: running tasks count is ok")
					.Msg("msg"  , "{type}({" + key + "}): running tasks count is ok: {tasks_running}")),

			"notify_few_tasks_queued" : Reaction()
				.On("few_tasks_queued")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: queued tasks count is low")
					.Msg("msg"  , "{type}({" + key + "}): queued tasks count is low: {tasks_queued}"))
				.End(RDanger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: queued tasks count is ok")
					.Msg("msg"  , "{type}({" + key + "}): queued tasks count is ok: {tasks_queued}")),

			"notify_nodes_missing" : Reaction()
				.On("nodes_missing")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: the queue has lost some nodes")
					.Msg("msg"  , "{type}({" + key + "}): the queue has lost some nodes: {nodes_current} / {nodes_total}"))
				.End(RDanger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: the queue nodes are ok")
					.Msg("msg"  , "{type}({" + key + "}): the queue apus are ok: {nodes_current} / {nodes_total}")),

			"notify_many_free" : Reaction()
				.On("many_free")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: too many free nodes")
					.Msg("msg"  , "{type}({" + key + "}): too many free nodes: {nodes_free} = {nodes_free_pct}%"))
				.End(RDanger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: free nodes percent is ok")
					.Msg("msg"  , "{type}({" + key + "}): free nodes percent is ok: {nodes_free} = {nodes_free_pct}%")),

			"notify_many_blocked" : Reaction()
				.On("many_blocked")
				.Begin(Danger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: too many blocked nodes")
					.Msg("msg"  , "{type}({" + key + "}): too many blocked nodes: {nodes_blocked} = {nodes_blocked_pct}%"))
				.End(RDanger("tag", "QUEUE").Msg("loc", "{" + key + "}")
					.Msg("descr", "{type}: blocked nodes percent is ok")
					.Msg("msg"  , "{type}({" + key + "}): blocked nodes percent is ok: {nodes_blocked} = {nodes_blocked_pct}%")),
		}
	}
