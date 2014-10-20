from octopy import *

ems_sensor_module = {
	"const" : {
		"type" : "ems_sensor"
	},

	"static" : {
		"_static_ems_sensor_front_temp_max" : 30,
		"_static_ems_sensor_back_temp_max" : 50,

		"_static_ems_sensor_humidity_min" : 10,
		"_static_ems_sensor_humidity_max" : 70,
	},

	"sensor" : {
	# cold
		"front_humidity" : 0,
		"front_temp" : 0,

	# hot
		"back_humidity" : 0,
		"back_temp" : 0,
	},

	"var" : {
		"front_temp_ok" : UpperArgThreshold("front_temp", "_static_ems_sensor_front_temp_max"),
		"back_temp_ok" : UpperArgThreshold("back_temp", "_static_ems_sensor_back_temp_max"),

		"front_humidity_max_ok" : UpperArgThreshold("front_humidity", "_static_ems_sensor_humidity_max"),
		"back_humidity_max_ok"  : UpperArgThreshold("back_humidity", "_static_ems_sensor_humidity_max"),

		"front_humidity_min_ok" : LowerArgThreshold("front_humidity", "_static_ems_sensor_humidity_min"),
		"back_humidity_min_ok"  : LowerArgThreshold("back_humidity", "_static_ems_sensor_humidity_min"),
	},

	"react" : {
		Equals("front_temp_ok", False) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: front temp is very high")
				.Msg("msg"  , "ems sensor: front temp in {descr} is very high: {front_temp}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: front temp is back to normal")
				.Msg("msg"  , "ems sensor: front temp in {descr} is back to normal: {front_temp}")),

		Equals("back_temp_ok", False) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: back temp is very high")
				.Msg("msg"  , "ems sensor: back temp in {descr} is very high: {back_temp}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: back temp is back to normal")
				.Msg("msg"  , "ems sensor: back temp in {descr} is back to normal: {back_temp}")),

		Equals("front_humidity_max_ok", False) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: front humidity is very high")
				.Msg("msg"  , "ems sensor: front humidity in {descr} is very high: {front_humidity}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: front humidity is back to normal")
				.Msg("msg"  , "ems sensor: front humidity in {descr} is back to normal: {front_humidity}")),

		Equals("back_humidity_max_ok", False) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: back humidity is very high")
				.Msg("msg"  , "ems sensor: back humidity in {descr} is very high: {back_humidity}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: back humidity is back to normal")
				.Msg("msg"  , "ems sensor: back humidity in {descr} is back to normal: {back_humidity}")),

		Equals("front_humidity_min_ok", False) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: front humidity is low")
				.Msg("msg"  , "ems sensor: front humidity in {descr} is low: {front_humidity}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: front humidity is back to normal")
				.Msg("msg"  , "ems sensor: front humidity in {descr} is back to normal: {front_humidity}")),

		Equals("back_humidity_min_ok", False) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: back humidity is low")
				.Msg("msg"  , "ems sensor: back humidity in {descr} is low: {back_humidity}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{descr}")
				.Msg("descr", "ems sensor: back humidity is back to normal")
				.Msg("msg"  , "ems sensor: back humidity in {descr} is back to normal: {back_humidity}")),
	}
}

ems_contact_module = {
	"const" : {
		"type" : "ems_contact"
	},

	"sensor" : {
		"state" : "",
		"normal_state" : ""
	},

	"var" : {
		"state_ok" : VarArgMatch("state", "normal_state")
	},

	"react" : {
		Equals("state_ok", False) :
			( Info("tag", "INFRASTRUCTURE").Msg("loc", "{descr}")
				.Msg("descr", "ems contact failed")
				.Msg("msg"  , "ems contact {descr} failed: state: {state} normal_state : {normal_state}")
			, Recover("tag", "INFRASTRUCTURE").Msg("loc", "{descr}")
				.Msg("descr", "ems contact is ok")
				.Msg("msg"  , "ems contact {descr} is ok")),
	}
}

ems_snmp_trap_module = {
	"sensor" : {
		"iemHighTempThresholdViolation" : False,
		"iemLowTempThresholdViolation" : False,
		"iemHighHumidThresholdViolation" : False,
		"iemLowHumidThresholdViolation" : False,

		"emsCommunicationLost" : False,

		"envMaxTempThresholdViolation" : False,
		"envMinTempThresholdViolation" : False,
		"envMaxHumidityThresholdViolation" : False,
		"envMinHumidityThresholdViolation" : False,
		"apcEnvMaxTempThresholdViolation" : False,
		"apcEnvHighTempThresholdViolation" : False,
		"apcEnvLowTempThresholdViolation" : False,
		"apcEnvMinTempThresholdViolation" : False,
		"apcEnvMaxHumidityThresholdViolation" : False,
		"apcEnvHighHumidityThresholdViolation" : False,
		"apcEnvLowHumidityThresholdViolation" : False,
		"apcEnvMinHumidityThresholdViolation" : False,

		"envHighTempThresholdViolation" : False,
		"envLowTempThresholdViolation" : False,
		"envHighHumidityThresholdViolation" : False,
		"envLowHumidityThresholdViolation" : False,

		"iemContactFault" : False,
		"contactFault" : False,
		"emsSensorFault" : False,
	},

	"react" : {
		Equals("emsCommunicationLost", True) :
			( Danger("tag", "ems").Msg("loc", "{ip}")
				.Msg("descr", "emsCommunicationLost")
				.Msg("msg"  , "emsCommunicationLost")
			, Recover("tag", "ems").Msg("loc", "{ip}")
				.Msg("descr", "ems: emsCommunicationLost is OK")
				.Msg("msg"  , "ems: emsCommunicationLost is OK")),

		Equals("iemHighTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighTempThresholdViolation")
				.Msg("msg"  , "ems: iemHighTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighTempThresholdViolation is OK")
				.Msg("msg"  , "ems: iemHighTempThresholdViolation is OK {ip}")),
		Equals("iemLowTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowTempThresholdViolation")
				.Msg("msg"  , "ems: iemLowTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowTempThresholdViolation is OK")
				.Msg("msg"  , "ems: iemLowTempThresholdViolation is OK {ip}")),
		Equals("envMaxTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxTempThresholdViolation")
				.Msg("msg"  , "ems: envMaxTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envMaxTempThresholdViolation is OK {ip}")),
		Equals("envMinTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinTempThresholdViolation")
				.Msg("msg"  , "ems: envMinTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envMinTempThresholdViolation is OK {ip}")),
		Equals("apcEnvMaxTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMaxTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMaxTempThresholdViolation is OK {ip}")),
		Equals("apcEnvHighTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvHighTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvHighTempThresholdViolation is OK {ip}")),
		Equals("apcEnvLowTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvLowTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvLowTempThresholdViolation is OK {ip}")),
		Equals("apcEnvMinTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMinTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMinTempThresholdViolation is OK {ip}")),
		Equals("envHighTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighTempThresholdViolation")
				.Msg("msg"  , "ems: envHighTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envHighTempThresholdViolation is OK {ip}")),
		Equals("envLowTempThresholdViolation", True) :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowTempThresholdViolation")
				.Msg("msg"  , "ems: envLowTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envLowTempThresholdViolation is OK {ip}")),

		Equals("iemHighHumidThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighHumidThresholdViolation")
				.Msg("msg"  , "ems: iemHighHumidThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighHumidThresholdViolation is OK")
				.Msg("msg"  , "ems: iemHighHumidThresholdViolation is OK {ip}")),
		Equals("iemLowHumidThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowHumidThresholdViolation")
				.Msg("msg"  , "ems: iemLowHumidThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowHumidThresholdViolation is OK")
				.Msg("msg"  , "ems: iemLowHumidThresholdViolation is OK {ip}")),
		Equals("envMaxHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxHumidityThresholdViolation")
				.Msg("msg"  , "ems: envMaxHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envMaxHumidityThresholdViolation is OK {ip}")),
		Equals("envMinHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinHumidityThresholdViolation")
				.Msg("msg"  , "ems: envMinHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envMinHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvMaxHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMaxHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMaxHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvHighHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvHighHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvHighHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvLowHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvLowHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvLowHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvMinHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMinHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMinHumidityThresholdViolation is OK {ip}")),
		Equals("envHighHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighHumidityThresholdViolation")
				.Msg("msg"  , "ems: envHighHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envHighHumidityThresholdViolation is OK {ip}")),
		Equals("envLowHumidityThresholdViolation", True) :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowHumidityThresholdViolation")
				.Msg("msg"  , "ems: envLowHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envLowHumidityThresholdViolation is OK {ip}")),

		Equals("iemContactFault", True).Repeatable() :
			Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
				.Msg("descr", "ems trap: iemContactFault")
				.Msg("msg"  , "ems trap: iemContactFault {ip}"),

		Equals("contactFault", True).Repeatable() :
			Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
				.Msg("descr", "ems trap: contactFault")
				.Msg("msg"  , "ems trap: contactFault {ip}"),

		Equals("emsSensorFault", True).Repeatable() :
			Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
				.Msg("descr", "ems trap: emsSensorFault")
				.Msg("msg"  , "ems trap: emsSensorFault {ip}"),
	}
}
