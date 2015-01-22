from octopy import *

#
# checks require next attrbiutes:
# tasks_total_req
# tasks_running_req
# tasks_queued_req
# cpus_free_max
# queue_req_cpus
# cpus_blocked_max
#
# TODO: make more clear
#

def CleoModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "queue"
		},

		"sensor" : {
			"tasks_total"   : Long(timeout),
			"tasks_running" : Long(timeout),
			"tasks_blocked" : Long(timeout),
			"tasks_queued"  : Long(timeout),
			"tasks_prerun"  : Long(timeout),

			"tasks_completition" : Long(timeout),

			"can_run_tasks"   : Long(timeout),
			"can_queue_tasks" : Long(timeout),

			"cpus_total_free"    : Long(timeout),
			"cpus_total_number"  : Long(timeout),
			"cpus_blocked_count" : Long(timeout),
		},

		"var" : {
			"tasks_total_ok"   : LowerArgThreshold("tasks_total", "tasks_total_req"),
			"tasks_running_ok" : LowerArgThreshold("tasks_running", "tasks_running_req"),
			"tasks_queued_ok"  : LowerArgThreshold("tasks_queued", "tasks_queued_req"),

			"cpus_total_free_ok"    : UpperArgThreshold("cpus_total_free", "cpus_free_max"),
			"cpus_total_number_ok"  : ArgMatch("cpus_total_number", "queue_req_cpus"),
			"cpus_blocked_count_ok" : UpperArgThreshold("cpus_blocked_count", "cpus_blocked_max"),
		},

		"react" : {
			Equals("tasks_total_ok", False) :
				Warning("tag", "QUEUE").Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: total tasks count is low")
					.Msg("msg"  , "{type}({queue_name}): total tasks count is low({tasks_total})"),

			Equals("tasks_running_ok", False) :
				Warning("tag", "QUEUE").Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: running tasks count is low")
					.Msg("msg"  , "{type}({queue_name}): running tasks count is low({tasks_running})"),

			Equals("tasks_queued_ok", False) :
				Warning("tag", "QUEUE").Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: queued tasks count is low")
					.Msg("msg"  , "{type}({queue_name}): queued tasks count is low({tasks_queued})"),

			Equals("cpus_total_free_ok", False) :
				Danger("tag", "QUEUE").Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: too many free cpus")
					.Msg("msg"  , "{type}({queue_name}): too many free cpus({cpus_total_free})"),

			Equals("cpus_total_number_ok", False) :
				Danger("tag", "QUEUE").Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: the queue has lost some cpus")
					.Msg("msg"  , "{type}({queue_name}): the queue has lost some cpus({cpus_total_number})"),

			Equals("cpus_blocked_count_ok", False) :
				Danger("tag", "QUEUE").Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: too many blocked cpus")
					.Msg("msg"  , "{type}({queue_name}): too many blocked cpus({cpus_blocked_count})"),
		}
	}
