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
			Warning("total tasks count is low", "type", "queue_name", "tasks_total"),

		Equals("tasks_running_ok", False) :
			Warning("running tasks count is low", "type", "queue_name", "tasks_running"),

		Equals("tasks_queued_ok", False) :
			Warning("queued tasks count is low", "type", "queue_name", "tasks_queued"),

		Equals("cpus_total_free_ok", False) :
			Danger("too many free cpus", "type", "queue_name", "cpus_total_free"),

		Equals("cpus_total_number_ok", False) :
			Danger("the queue has lost some cpus", "type", "queue_name", "cpus_total_number"),

		Equals("cpus_blocked_count_ok", False) :
			Danger("too many blocked cpus", "type", "queue_name", "cpus_blocked_count")
	}
}
