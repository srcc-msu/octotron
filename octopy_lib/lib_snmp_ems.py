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


	"""{
		Equals("front_temp_ok", Equals, False) :
		{
			"response" : Warning("ems sensor: front temp is very high {descr} {front_temp} {p:AID} {AID}")
				.Exec("usr_sms", "3 {33} {test} {AID} {^:AID}")

			"delay" : 2,
			"repeat" : 2,
			"repetable" : True,

			Danger("ems sensor: front temp is very high", "type", "descr", "front_temp")
				, Recover("ems sensor: front temp is back to normal", "type", "descr", "front_temp")),
		}
	}"""

	"react" : {
		Equals("front_temp_ok", False) :
			(Danger("ems sensor: front temp is very high", "type", "descr", "front_temp")
				, Recover("ems sensor: front temp is back to normal", "type", "descr", "front_temp")),

		Equals("back_temp_ok", False) :
			(Danger("ems sensor: back temp is very high", "type", "descr", "back_temp")
				, Recover("ems sensor: back temp is back to normal", "type", "descr", "back_temp")),

		Equals("front_humidity_max_ok", False) :
			(Danger("ems sensor: front humidity is very high", "type", "descr", "front_humidity")
				, Recover("ems sensor: front humidity is back to normal", "type", "descr", "front_humidity")),

		Equals("back_humidity_max_ok", False) :
			(Danger("ems sensor: back humidity is very high", "type", "descr", "back_humidity")
				, Recover("ems sensor: back humidity is back to normal", "type", "descr", "back_humidity")),

		Equals("front_humidity_min_ok", False) :
			(Danger("ems sensor: front humidity is low", "type", "descr", "front_humidity")
				, Recover("ems sensor: front humidity is back to normal", "type", "descr", "front_humidity")),

		Equals("back_humidity_min_ok", False) :
			(Danger("ems sensor: back humidity is low", "type", "descr", "back_humidity")
				, Recover("ems sensor: back humidity is back to normal", "type", "descr", "back_humidity")),
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
			(Info("ems contact failed", "type", "descr", "state", "normal_state")
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
		Equals("iemHighTempThresholdViolation", True) :
			(Danger("ems: iemHighTempThresholdViolation", "type", "ip")
				, Recover("ems: iemHighTempThresholdViolation is OK", "type", "ip")),
		Equals("iemLowTempThresholdViolation", True) :
			(Danger("ems: iemLowTempThresholdViolation", "type", "ip")
				, Recover("ems: iemLowTempThresholdViolation is OK", "type", "ip")),
		Equals("iemHighHumidThresholdViolation", True) :
			(Danger("ems: iemHighHumidThresholdViolation", "type", "ip")
				, Recover("ems: iemHighHumidThresholdViolation is OK", "type", "ip")),
		Equals("iemLowHumidThresholdViolation", True) :
			(Danger("ems: iemLowHumidThresholdViolation", "type", "ip")
				, Recover("ems: iemLowHumidThresholdViolation is OK", "type", "ip")),

		Equals("emsCommunicationLost", True) :
			(Danger("ems: emsCommunicationLost", "type", "ip")
				, Recover("ems: emsCommunicationLost is OK", "type", "ip")),

		Equals("envMaxTempThresholdViolation", True) :
			(Danger("ems: envMaxTempThresholdViolation", "type", "ip")
				, Recover("ems: envMaxTempThresholdViolation is OK", "type", "ip")),
		Equals("envMinTempThresholdViolation", True) :
			(Danger("ems: envMinTempThresholdViolation", "type", "ip")
				, Recover("ems: envMinTempThresholdViolation is OK", "type", "ip")),
		Equals("envMaxHumidityThresholdViolation", True) :
			(Danger("ems: envMaxHumidityThresholdViolation", "type", "ip")
				, Recover("ems: envMaxHumidityThresholdViolation is OK", "type", "ip")),
		Equals("envMinHumidityThresholdViolation", True) :
			(Danger("ems: envMinHumidityThresholdViolation", "type", "ip")
				, Recover("ems: envMinHumidityThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvMaxTempThresholdViolation", True) :
			(Danger("ems: apcEnvMaxTempThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvMaxTempThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvHighTempThresholdViolation", True) :
			(Danger("ems: apcEnvHighTempThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvHighTempThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvLowTempThresholdViolation", True) :
			(Danger("ems: apcEnvLowTempThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvLowTempThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvMinTempThresholdViolation", True) :
			(Danger("ems: apcEnvMinTempThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvMinTempThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvMaxHumidityThresholdViolation", True) :
			(Danger("ems: apcEnvMaxHumidityThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvMaxHumidityThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvHighHumidityThresholdViolation", True) :
			(Danger("ems: apcEnvHighHumidityThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvHighHumidityThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvLowHumidityThresholdViolation", True) :
			(Danger("ems: apcEnvLowHumidityThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvLowHumidityThresholdViolation is OK", "type", "ip")),
		Equals("apcEnvMinHumidityThresholdViolation", True) :
			(Danger("ems: apcEnvMinHumidityThresholdViolation", "type", "ip")
				, Recover("ems: apcEnvMinHumidityThresholdViolation is OK", "type", "ip")),

		Equals("envHighTempThresholdViolation", True) :
			(Danger("ems: envHighTempThresholdViolation", "type", "ip")
				, Recover("ems: envHighTempThresholdViolation is OK", "type", "ip")),
		Equals("envLowTempThresholdViolation", True) :
			(Danger("ems: envLowTempThresholdViolation", "type", "ip")
				, Recover("ems: envLowTempThresholdViolation is OK", "type", "ip")),
		Equals("envHighHumidityThresholdViolation", True) :
			(Danger("ems: envHighHumidityThresholdViolation", "type", "ip")
				, Recover("ems: envHighHumidityThresholdViolation is OK", "type", "ip")),
		Equals("envLowHumidityThresholdViolation", True) :
			(Danger("ems: envLowHumidityThresholdViolation", "type", "ip")
				, Recover("ems: envLowHumidityThresholdViolation is OK", "type", "ip")),

		Equals("iemContactFault", True).Repeatable() :
			Danger("ems trap: iemContactFault", "type", "ip"),

		Equals("contactFault", True).Repeatable() :
			Danger("ems trap: contactFault", "type", "ip"),

		Equals("emsSensorFault", True).Repeatable() :
			Danger("ems trap: emsSensorFault", "type", "ip"),
	}
}
