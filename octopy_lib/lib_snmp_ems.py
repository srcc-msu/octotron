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
			(Danger("TEMPERATURE", "ems sensor: front temp in {descr} is very high: {front_temp}")
				, Recover("ems sensor: front temp in {descr} is back to normal: {front_temp}")),

		Equals("back_temp_ok", False) :
			(Danger("TEMPERATURE", "ems sensor: back temp in {descr} is very high: {back_temp}")
				, Recover("ems sensor: back temp in {descr} is back to normal: {back_temp}")),

		Equals("front_humidity_max_ok", False) :
			(Danger("ENVIRONMENT", "ems sensor: front humidity in {descr} is very high: {front_humidity}")
				, Recover("ems sensor: front humidity in {descr} is back to normal: {front_humidity}")),

		Equals("back_humidity_max_ok", False) :
			(Danger("ENVIRONMENT", "ems sensor: back humidity in {descr} is very high: {back_humidity}")
				, Recover("ems sensor: back humidity in {descr} is back to normal: {back_humidity}")),

		Equals("front_humidity_min_ok", False) :
			(Danger("ENVIRONMENT", "ems sensor: front humidity in {descr} is low: {front_humidity}")
				, Recover("ems sensor: front humidity in {descr} is back to normal: {front_humidity}")),

		Equals("back_humidity_min_ok", False) :
			(Danger("ENVIRONMENT", "ems sensor: back humidity in {descr} is low: {back_humidity}")
				, Recover("ems sensor: back humidity in {descr} is back to normal: {back_humidity}")),
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
			(Info("INFRASTRUCTURE", "ems contact failed", "type", "descr", "state", "normal_state")
				, Recover("ems contact is ok", "type", "descr", "state", "normal_state")),
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
			(Danger("ems: emsCommunicationLost")
				, Recover("ems: emsCommunicationLost is OK")),

		Equals("iemHighTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: iemHighTempThresholdViolation")
				, Recover("ems: iemHighTempThresholdViolation is OK")),
		Equals("iemLowTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: iemLowTempThresholdViolation")
				, Recover("ems: iemLowTempThresholdViolation is OK")),
		Equals("envMaxTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: envMaxTempThresholdViolation")
				, Recover("ems: envMaxTempThresholdViolation is OK")),
		Equals("envMinTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: envMinTempThresholdViolation")
				, Recover("ems: envMinTempThresholdViolation is OK")),
		Equals("apcEnvMaxTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: apcEnvMaxTempThresholdViolation")
				, Recover("ems: apcEnvMaxTempThresholdViolation is OK")),
		Equals("apcEnvHighTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: apcEnvHighTempThresholdViolation")
				, Recover("ems: apcEnvHighTempThresholdViolation is OK")),
		Equals("apcEnvLowTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: apcEnvLowTempThresholdViolation")
				, Recover("ems: apcEnvLowTempThresholdViolation is OK")),
		Equals("apcEnvMinTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: apcEnvMinTempThresholdViolation")
				, Recover("ems: apcEnvMinTempThresholdViolation is OK")),
		Equals("envHighTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: envHighTempThresholdViolation")
				, Recover("ems: envHighTempThresholdViolation is OK")),
		Equals("envLowTempThresholdViolation", True) :
			(Danger("TEMPERATURE", "ems: envLowTempThresholdViolation")
				, Recover("ems: envLowTempThresholdViolation is OK")),

		Equals("iemHighHumidThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: iemHighHumidThresholdViolation")
				, Recover("ems: iemHighHumidThresholdViolation is OK")),
		Equals("iemLowHumidThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: iemLowHumidThresholdViolation")
				, Recover("ems: iemLowHumidThresholdViolation is OK")),
		Equals("envMaxHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: envMaxHumidityThresholdViolation")
				, Recover("ems: envMaxHumidityThresholdViolation is OK")),
		Equals("envMinHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: envMinHumidityThresholdViolation")
				, Recover("ems: envMinHumidityThresholdViolation is OK")),
		Equals("apcEnvMaxHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: apcEnvMaxHumidityThresholdViolation")
				, Recover("ems: apcEnvMaxHumidityThresholdViolation is OK")),
		Equals("apcEnvHighHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: apcEnvHighHumidityThresholdViolation")
				, Recover("ems: apcEnvHighHumidityThresholdViolation is OK")),
		Equals("apcEnvLowHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: apcEnvLowHumidityThresholdViolation")
				, Recover("ems: apcEnvLowHumidityThresholdViolation is OK")),
		Equals("apcEnvMinHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: apcEnvMinHumidityThresholdViolation")
				, Recover("ems: apcEnvMinHumidityThresholdViolation is OK")),
		Equals("envHighHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: envHighHumidityThresholdViolation")
				, Recover("ems: envHighHumidityThresholdViolation is OK")),
		Equals("envLowHumidityThresholdViolation", True) :
			(Danger("ENVIRONMENT", "ems: envLowHumidityThresholdViolation")
				, Recover("ems: envLowHumidityThresholdViolation is OK")),

		Equals("iemContactFault", True).Repeatable() :
			Danger("INFRASTRUCTURE", "ems trap: iemContactFault"),

		Equals("contactFault", True).Repeatable() :
			Danger("INFRASTRUCTURE", "ems trap: contactFault"),

		Equals("emsSensorFault", True).Repeatable() :
			Danger("INFRASTRUCTURE", "ems trap: emsSensorFault"),
	}
}
