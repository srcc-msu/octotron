from octopy import *

def EmsSensorModule(timeout = Minutes(1)):
	return {
		"static" : {
			"static_ems_sensor_front_temp_max" : 30,
			"static_ems_sensor_back_temp_max" : 50,

			"static_ems_sensor_humidity_min" : 10,
			"static_ems_sensor_humidity_max" : 70,
		},

		"sensor" : {
		# cold
			"front_humidity" : Long(timeout),
			"front_temp" : Long(timeout),

		# hot
			"back_humidity" : Long(timeout),
			"back_temp" : Long(timeout),
		},

		"trigger" : {
			"front_temp_error" : GTArg("front_temp", "static_ems_sensor_front_temp_max"),
			"back_temp_error" : GTArg("back_temp", "static_ems_sensor_back_temp_max"),

			"front_humidity_max_error" : GTArg("front_humidity", "static_ems_sensor_humidity_max"),
			"back_humidity_max_error"  : GTArg("back_humidity", "static_ems_sensor_humidity_max"),

			"front_humidity_min_error" : LTArg("front_humidity", "static_ems_sensor_humidity_min"),
			"back_humidity_min_error"  : LTArg("back_humidity", "static_ems_sensor_humidity_min"),
		},

		"react" : {
			"notify_front_temp_error" : Reaction()
				.On("front_temp_error")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: front temp is very high")
					.Msg("msg"  , "ems sensor: front temp in {descr} is very high: {front_temp}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: front temp is back to normal")
					.Msg("msg"  , "ems sensor: front temp in {descr} is back to normal: {front_temp}")),

			"notify_back_temp_error" : Reaction()
				.On("back_temp_error")
				.Begin(Warning("tag", "TEMPERATURE").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: back temp is very high")
					.Msg("msg"  , "ems sensor: back temp in {descr} is very high: {back_temp}"))
				.End(RWarning("tag", "TEMPERATURE").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: back temp is back to normal")
					.Msg("msg"  , "ems sensor: back temp in {descr} is back to normal: {back_temp}")),

			"notify_front_humidity_max_error" : Reaction()
				.On("front_humidity_max_error")
				.Begin(Warning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: front humidity is very high")
					.Msg("msg"  , "ems sensor: front humidity in {descr} is very high: {front_humidity}"))
				.End(RWarning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: front humidity is back to normal")
					.Msg("msg"  , "ems sensor: front humidity in {descr} is back to normal: {front_humidity}")),

			"notify_back_humidity_max_error" : Reaction()
				.On("back_humidity_max_error")
				.Begin(Warning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: back humidity is very high")
					.Msg("msg"  , "ems sensor: back humidity in {descr} is very high: {back_humidity}"))
				.End(RWarning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: back humidity is back to normal")
					.Msg("msg"  , "ems sensor: back humidity in {descr} is back to normal: {back_humidity}")),

			"notify_front_humidity_min_error" : Reaction()
				.On("front_humidity_min_error")
				.Begin(Warning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: front humidity is low")
					.Msg("msg"  , "ems sensor: front humidity in {descr} is low: {front_humidity}"))
				.End(RWarning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: front humidity is back to normal")
					.Msg("msg"  , "ems sensor: front humidity in {descr} is back to normal: {front_humidity}")),

			"notify_back_humidity_min_error" : Reaction()
				.On("back_humidity_min_error")
				.Begin(Warning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: back humidity is low")
					.Msg("msg"  , "ems sensor: back humidity in {descr} is low: {back_humidity}"))
				.End(RWarning("tag", "ENVIRONMENT").Msg("loc", "{descr}")
					.Msg("descr", "ems sensor: back humidity is back to normal")
					.Msg("msg"  , "ems sensor: back humidity in {descr} is back to normal: {back_humidity}")),
		}
	}

def EmsContactModule(timeout = Minutes(1)):
	return {
		"sensor" : {
			"state" : String(timeout),
			"normal_state" : String(timeout),
		},

		"trigger" : {
			"state_error" : NotMatchArg("state", "normal_state")
		},

		"react" : {
			"notify_state_error" : Reaction()
				.On("state_error")
				.Begin(Info("tag", "INFRASTRUCTURE").Msg("loc", "{descr}")
					.Msg("descr", "ems contact failed")
					.Msg("msg"  , "ems contact {descr} failed: state: {state} normal_state : {normal_state}"))
				.End(RInfo("tag", "INFRASTRUCTURE").Msg("loc", "{descr}")
					.Msg("descr", "ems contact is ok")
					.Msg("msg"  , "ems contact {descr} is ok")),
		}
	}
