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

CLEO_UPDATE_TIME = Minutes(10)

cleo_module = {
	"const" : {
		"type" : "queue"
	},

	"sensor" : {
		"tasks_total"   : Long(CLEO_UPDATE_TIME),
		"tasks_running" : Long(CLEO_UPDATE_TIME),
		"tasks_blocked" : Long(CLEO_UPDATE_TIME),
		"tasks_queued"  : Long(CLEO_UPDATE_TIME),
		"tasks_prerun"  : Long(CLEO_UPDATE_TIME),

		"tasks_completition" : Long(CLEO_UPDATE_TIME),

		"can_run_tasks"   : Long(CLEO_UPDATE_TIME),
		"can_queue_tasks" : Long(CLEO_UPDATE_TIME),

		"cpus_total_free"    : Long(CLEO_UPDATE_TIME),
		"cpus_total_number"  : Long(CLEO_UPDATE_TIME),
		"cpus_blocked_count" : Long(CLEO_UPDATE_TIME),
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
				.Msg("descr", "total tasks count is low")
				.Msg("msg"  , "total tasks count is low({tasks_total}) in queue {queue_name}"),

		Equals("tasks_running_ok", False) :
			Warning("tag", "QUEUE").Msg("loc", "{queue_name}")
				.Msg("descr", "running tasks count is low")
				.Msg("msg"  , "running tasks count is low({tasks_running}) in queue {queue_name}"),

		Equals("tasks_queued_ok", False) :
			Warning("tag", "QUEUE").Msg("loc", "{queue_name}")
				.Msg("descr", "queued tasks count is low")
				.Msg("msg"  , "queued tasks count is low({tasks_queued}) in queue {queue_name}"),

		Equals("cpus_total_free_ok", False) :
			Danger("tag", "QUEUE").Msg("loc", "{queue_name}")
				.Msg("descr", "too many free cpus")
				.Msg("msg"  , "too many free cpus({cpus_total_free}) in queue {queue_name}"),

		Equals("cpus_total_number_ok", False) :
			Danger("tag", "QUEUE").Msg("loc", "{queue_name}")
				.Msg("descr", "the queue has lost some cpus")
				.Msg("msg"  , "the queue has lost some cpus({cpus_total_number}) in queue {queue_name}"),

		Equals("cpus_blocked_count_ok", False) :
			Danger("tag", "QUEUE").Msg("loc", "{queue_name}")
				.Msg("descr", "too many blocked cpus")
				.Msg("msg"  , "too many blocked cpus({cpus_blocked_count}) in queue {queue_name}"),
	}
}
