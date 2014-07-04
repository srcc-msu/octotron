from octopy import *

queue_a = {
	"type" : "queue",

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
}

queue_r = {
	"tasks_total_ok"   : LowerArgThreshold("tasks_total", "tasks_total_req"),
	"tasks_running_ok" : LowerArgThreshold("tasks_running", "tasks_running_req"),
	"tasks_queued_ok"  : LowerArgThreshold("tasks_queued", "tasks_queued_req"),

	"cpus_total_free_ok"    : UpperArgThreshold("cpus_total_free", "cpus_free_max"),
	"cpus_total_number_ok"  : ArgMatch("cpus_total_number", "queue_req_cpus"),
	"cpus_blocked_count_ok" : UpperArgThreshold("cpus_blocked_count", "cpus_blocked_max"),
}

queue_react = {
	("tasks_total_ok", False) :
		Reaction(Warning("total tasks count is low", "type", "queue_name", "tasks_total")),

	("tasks_running_ok", False) :
		Reaction(Warning("running tasks count is low", "type", "queue_name", "tasks_running")),

	("tasks_queued_ok", False) :
		Reaction(Warning("queued tasks count is low", "type", "queue_name", "tasks_queued")),

	("cpus_total_free_ok", False) :
		Reaction(Danger("too many free cpus", "type", "queue_name", "cpus_total_free")),

	("cpus_total_number_ok", False) :
		Reaction(Danger("the queue has lost some cpus", "type", "queue_name", "cpus_total_number")),

	("cpus_blocked_count_ok", False) :
		Reaction(Danger("too many blocked cpus", "type", "queue_name", "cpus_blocked_count")),
}
