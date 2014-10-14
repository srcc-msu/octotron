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

cleo_module = {
	"sensor" : {
		"tasks_total"   : 0,
		"tasks_running" : 0,
		"tasks_blocked" : 0,
		"tasks_queued"  : 0,
		"tasks_prerun"  : 0,

		"tasks_completition" : 0,

		"can_run_tasks"   : 0,
		"can_queue_tasks" : 0,

		"cpus_total_free"    : 0,
		"cpus_total_number"  : 0,
		"cpus_blocked_count" : 0
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
			Warning("QUEUE", "total tasks count is low({tasks_total}) in queue {queue_name}"),

		Equals("tasks_running_ok", False) :
			Warning("QUEUE", "running tasks count is low({tasks_running}) in queue {queue_name}"),

		Equals("tasks_queued_ok", False) :
			Warning("QUEUE", "queued tasks count is low({tasks_queued}) in queue {queue_name}"),

		Equals("cpus_total_free_ok", False) :
			Danger("QUEUE", "too many free cpus({cpus_total_free}) in queue {queue_name}"),

		Equals("cpus_total_number_ok", False) :
			Danger("QUEUE", "the queue has lost some cpus({cpus_total_number}) in queue {queue_name}"),

		Equals("cpus_blocked_count_ok", False) :
			Danger("QUEUE", "too many blocked cpus({cpus_blocked_count}) in queue {queue_name}")
	}
}
