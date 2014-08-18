from octopy import *

ems_sensor_const = {"type" : "ems_sensor"}
ems_sensor_sensor = {
# cold
	"front_humidity" : 0,
	"front_temp" : 0,

# hot
	"back_humidity" : 0,
	"back_temp" : 0,

	"_static_ems_sensor_front_temp_max" : 30,
	"_static_ems_sensor_back_temp_max" : 50,

	"_static_ems_sensor_humidity_min" : 10,
	"_static_ems_sensor_humidity_max" : 70,
}

ems_sensor_var = {
	"front_temp_ok" : UpperArgThreshold("front_temp", "_static_ems_sensor_front_temp_max"),
	"back_temp_ok" : UpperArgThreshold("back_temp", "_static_ems_sensor_back_temp_max"),

	"front_humidity_max_ok" : UpperArgThreshold("front_humidity", "_static_ems_sensor_humidity_max"),
	"back_humidity_max_ok"  : UpperArgThreshold("back_humidity", "_static_ems_sensor_humidity_max"),

	"front_humidity_min_ok" : LowerArgThreshold("front_humidity", "_static_ems_sensor_humidity_min"),
	"back_humidity_min_ok"  : LowerArgThreshold("back_humidity", "_static_ems_sensor_humidity_min"),
}

ems_sensor_react = {
	("front_temp_ok", False) :
		Reaction(Danger("ems sensor: front temp is very high", "type", "descr", "front_temp")
			, Recover("ems sensor: front temp is back to normal", "type", "descr", "front_temp")),

	("back_temp_ok", False) :
		Reaction(Danger("ems sensor: back temp is very high", "type", "descr", "back_temp")
			, Recover("ems sensor: back temp is back to normal", "type", "descr", "back_temp")),

	("front_humidity_max_ok", False) :
		Reaction(Danger("ems sensor: front humidity is very high", "type", "descr", "front_humidity")
			, Recover("ems sensor: front humidity is back to normal", "type", "descr", "front_humidity")),

	("back_humidity_max_ok", False) :
		Reaction(Danger("ems sensor: back humidity is very high", "type", "descr", "back_humidity")
			, Recover("ems sensor: back humidity is back to normal", "type", "descr", "back_humidity")),

	("front_humidity_min_ok", False) :
		Reaction(Danger("ems sensor: front humidity is low", "type", "descr", "front_humidity")
			, Recover("ems sensor: front humidity is back to normal", "type", "descr", "front_humidity")),

	("back_humidity_min_ok", False) :
		Reaction(Danger("ems sensor: back humidity is low", "type", "descr", "back_humidity")
			, Recover("ems sensor: back humidity is back to normal", "type", "descr", "back_humidity")),
}

ems_sensor_const = {"type" : "ems_contact"}

ems_contact_sensor = {
	"state" : "",
	"normal_state" : ""
}

ems_contact_var = {
	"state_ok" : VarArgMatch("state", "normal_state")
}

ems_contact_react = {
	("state_ok", False) :
		Reaction(Info("ems contact failed", "type", "descr", "state", "normal_state")
			, Recover("ems contact is ok", "type", "descr", "state", "normal_state")),
}

ems_snmp_trap_sensor = {
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

	"iemContactFault" : 0,
	"contactFault" : 0,
	"emsSensorFault" : 0,
}

ems_snmp_trap_var = {
	"iemContactFault_changed" : UpdatedRecently("iemContactFault", 10),
	"contactFault_changed" : UpdatedRecently("contactFault", 10),
	"emsSensorFault_changed" : UpdatedRecently("emsSensorFault", 10),
}

ems_snmp_trap_react = {
	("iemHighTempThresholdViolation", True)
		: Reaction(Danger("ems: iemHighTempThresholdViolation", "type", "ip")
			, Recover("ems: iemHighTempThresholdViolation is OK", "type", "ip")),
	("iemLowTempThresholdViolation", True)
		: Reaction(Danger("ems: iemLowTempThresholdViolation", "type", "ip")
			, Recover("ems: iemLowTempThresholdViolation is OK", "type", "ip")),
	("iemHighHumidThresholdViolation", True)
		: Reaction(Danger("ems: iemHighHumidThresholdViolation", "type", "ip")
			, Recover("ems: iemHighHumidThresholdViolation is OK", "type", "ip")),
	("iemLowHumidThresholdViolation", True)
		: Reaction(Danger("ems: iemLowHumidThresholdViolation", "type", "ip")
			, Recover("ems: iemLowHumidThresholdViolation is OK", "type", "ip")),

	("emsCommunicationLost", True)
		: Reaction(Danger("ems: emsCommunicationLost", "type", "ip")
			, Recover("ems: emsCommunicationLost is OK", "type", "ip")),

	("envMaxTempThresholdViolation", True)
		: Reaction(Danger("ems: envMaxTempThresholdViolation", "type", "ip")
			, Recover("ems: envMaxTempThresholdViolation is OK", "type", "ip")),
	("envMinTempThresholdViolation", True)
		: Reaction(Danger("ems: envMinTempThresholdViolation", "type", "ip")
			, Recover("ems: envMinTempThresholdViolation is OK", "type", "ip")),
	("envMaxHumidityThresholdViolation", True)
		: Reaction(Danger("ems: envMaxHumidityThresholdViolation", "type", "ip")
			, Recover("ems: envMaxHumidityThresholdViolation is OK", "type", "ip")),
	("envMinHumidityThresholdViolation", True)
		: Reaction(Danger("ems: envMinHumidityThresholdViolation", "type", "ip")
			, Recover("ems: envMinHumidityThresholdViolation is OK", "type", "ip")),
	("apcEnvMaxTempThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvMaxTempThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvMaxTempThresholdViolation is OK", "type", "ip")),
	("apcEnvHighTempThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvHighTempThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvHighTempThresholdViolation is OK", "type", "ip")),
	("apcEnvLowTempThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvLowTempThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvLowTempThresholdViolation is OK", "type", "ip")),
	("apcEnvMinTempThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvMinTempThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvMinTempThresholdViolation is OK", "type", "ip")),
	("apcEnvMaxHumidityThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvMaxHumidityThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvMaxHumidityThresholdViolation is OK", "type", "ip")),
	("apcEnvHighHumidityThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvHighHumidityThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvHighHumidityThresholdViolation is OK", "type", "ip")),
	("apcEnvLowHumidityThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvLowHumidityThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvLowHumidityThresholdViolation is OK", "type", "ip")),
	("apcEnvMinHumidityThresholdViolation", True)
		: Reaction(Danger("ems: apcEnvMinHumidityThresholdViolation", "type", "ip")
			, Recover("ems: apcEnvMinHumidityThresholdViolation is OK", "type", "ip")),

	("envHighTempThresholdViolation", True)
		: Reaction(Danger("ems: envHighTempThresholdViolation", "type", "ip")
			, Recover("ems: envHighTempThresholdViolation is OK", "type", "ip")),
	("envLowTempThresholdViolation", True)
		: Reaction(Danger("ems: envLowTempThresholdViolation", "type", "ip")
			, Recover("ems: envLowTempThresholdViolation is OK", "type", "ip")),
	("envHighHumidityThresholdViolation", True)
		: Reaction(Danger("ems: envHighHumidityThresholdViolation", "type", "ip")
			, Recover("ems: envHighHumidityThresholdViolation is OK", "type", "ip")),
	("envLowHumidityThresholdViolation", True)
		: Reaction(Danger("ems: envLowHumidityThresholdViolation", "type", "ip")
			, Recover("ems: envLowHumidityThresholdViolation is OK", "type", "ip")),

	("iemContactFault_changed", True)
		: Reaction(Danger("ems trap: iemContactFault", "type", "ip")),

	("contactFault_changed", True)
		: Reaction(Danger("ems trap: contactFault", "type", "ip")),

	("emsSensorFault_changed", True)
		: Reaction(Danger("ems trap: emsSensorFault", "type", "ip")),
}
