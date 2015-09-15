from octopy import *

#
# checks require next attrbiutes:
# tasks_total_req
#
def CleoModule(timeout = Minutes(10)):
	return {
		"const" : {
			"type" : "queue"
		},

		"sensor" : {
			"tasks_total"   : Long(timeout),
			"tasks_blocked" : Long(timeout),
			"tasks_prerun"  : Long(timeout),

			"tasks_completition" : Long(timeout),

			"can_run_tasks"   : Long(timeout),
			"can_queue_tasks" : Long(timeout),
		},

		"trigger" : {
			"not_enough_tasks" : LTArg("tasks_total", "tasks_total_req"),
		},

		"react" : {
			"notify_tasks_count" : Reaction()
				.On("not_enough_tasks")
				.Begin(Warning("tag", "QUEUE")
					.Msg("loc", "{queue_name}")
					.Msg("descr", "{type}: total tasks count is low")
					.Msg("msg"  , "{type}({queue_name}): total tasks count is low({tasks_total})"))
		}
	}
