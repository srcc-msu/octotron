from octopy import *

EMS_UPDATE_TIME = Minutes(1)

ems_sensor_module = {
	"static" : {
		"_static_ems_sensor_front_temp_max" : 30,
		"_static_ems_sensor_back_temp_max" : 50,

		"_static_ems_sensor_humidity_min" : 10,
		"_static_ems_sensor_humidity_max" : 70,
	},

	"sensor" : {
	# cold
		"front_humidity" : Long(EMS_UPDATE_TIME),
		"front_temp" : Long(EMS_UPDATE_TIME),

	# hot
		"back_humidity" : Long(EMS_UPDATE_TIME),
		"back_temp" : Long(EMS_UPDATE_TIME),
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
	"sensor" : {
		"state" : String(EMS_UPDATE_TIME),
		"normal_state" : String(EMS_UPDATE_TIME),
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

EMS_TRAP_UPDATE_TIME = UPDATE_TIME_NOT_SPECIFIED

ems_snmp_trap_module = {
	"sensor" : {
		"iemHighTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"iemHighTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"iemLowTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"iemLowTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"iemHighHumidThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"iemHighHumidThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"iemLowHumidThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"iemLowHumidThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),

		"emsCommunicationLost" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"emsCommunicationLost_descr" : String(EMS_TRAP_UPDATE_TIME, ""),

		"envMaxTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envMaxTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"envMinTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envMinTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"envMaxHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envMaxHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"envMinHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envMinHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvMaxTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvMaxTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvHighTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvHighTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvLowTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvLowTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvMinTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvMinTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvMaxHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvMaxHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvHighHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvHighHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvLowHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvLowHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcEnvMinHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcEnvMinHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),

		"envHighTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envHighTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"envLowTempThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envLowTempThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"envHighHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envHighHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"envLowHumidityThresholdViolation" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"envLowHumidityThresholdViolation_descr" : String(EMS_TRAP_UPDATE_TIME, ""),

		"apcInformationalDiscreteInputContactStateAbnormal" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcInformationalDiscreteInputContactStateAbnormal_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"apcInformationalDiscreteInputContactStateNormal" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"apcInformationalDiscreteInputContactStateNormal_descr" : String(EMS_TRAP_UPDATE_TIME, ""),

		"iemContactFault" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"iemContactFault_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"contactFault" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"contactFault_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
		"emsSensorFault" : Boolean(EMS_TRAP_UPDATE_TIME, True),
		"emsSensorFault_descr" : String(EMS_TRAP_UPDATE_TIME, ""),
	},

	"react" : {
		Equals("emsCommunicationLost", False).Repeatable() :
			( Danger("tag", "EMS").Msg("loc", "{ip}")
				.Msg("descr", "emsCommunicationLost")
				.Msg("msg"  , "emsCommunicationLost")
			, Recover("tag", "EMS").Msg("loc", "{ip}")
				.Msg("descr", "ems: emsCommunicationLost is OK")
				.Msg("msg"  , "ems: emsCommunicationLost is OK")),

		Equals("iemHighTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighTempThresholdViolation")
				.Msg("msg"  , "ems: iemHighTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighTempThresholdViolation is OK")
				.Msg("msg"  , "ems: iemHighTempThresholdViolation is OK {ip}")),
		Equals("iemLowTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowTempThresholdViolation")
				.Msg("msg"  , "ems: iemLowTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowTempThresholdViolation is OK")
				.Msg("msg"  , "ems: iemLowTempThresholdViolation is OK {ip}")),
		Equals("envMaxTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxTempThresholdViolation")
				.Msg("msg"  , "ems: envMaxTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envMaxTempThresholdViolation is OK {ip}")),
		Equals("envMinTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinTempThresholdViolation")
				.Msg("msg"  , "ems: envMinTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envMinTempThresholdViolation is OK {ip}")),
		Equals("apcEnvMaxTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMaxTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMaxTempThresholdViolation is OK {ip}")),
		Equals("apcEnvHighTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvHighTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvHighTempThresholdViolation is OK {ip}")),
		Equals("apcEnvLowTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvLowTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvLowTempThresholdViolation is OK {ip}")),
		Equals("apcEnvMinTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinTempThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMinTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinTempThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMinTempThresholdViolation is OK {ip}")),
		Equals("envHighTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighTempThresholdViolation")
				.Msg("msg"  , "ems: envHighTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envHighTempThresholdViolation is OK {ip}")),
		Equals("envLowTempThresholdViolation", False).Repeatable() :
			( Danger("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowTempThresholdViolation")
				.Msg("msg"  , "ems: envLowTempThresholdViolation {ip}")
			, Recover("tag", "TEMPERATURE").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowTempThresholdViolation is OK")
				.Msg("msg"  , "ems: envLowTempThresholdViolation is OK {ip}")),

		Equals("iemHighHumidThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighHumidThresholdViolation")
				.Msg("msg"  , "ems: iemHighHumidThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemHighHumidThresholdViolation is OK")
				.Msg("msg"  , "ems: iemHighHumidThresholdViolation is OK {ip}")),
		Equals("iemLowHumidThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowHumidThresholdViolation")
				.Msg("msg"  , "ems: iemLowHumidThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: iemLowHumidThresholdViolation is OK")
				.Msg("msg"  , "ems: iemLowHumidThresholdViolation is OK {ip}")),
		Equals("envMaxHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxHumidityThresholdViolation")
				.Msg("msg"  , "ems: envMaxHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMaxHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envMaxHumidityThresholdViolation is OK {ip}")),
		Equals("envMinHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinHumidityThresholdViolation")
				.Msg("msg"  , "ems: envMinHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envMinHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envMinHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvMaxHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMaxHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMaxHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMaxHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvHighHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvHighHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvHighHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvHighHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvLowHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvLowHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvLowHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvLowHumidityThresholdViolation is OK {ip}")),
		Equals("apcEnvMinHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinHumidityThresholdViolation")
				.Msg("msg"  , "ems: apcEnvMinHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: apcEnvMinHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: apcEnvMinHumidityThresholdViolation is OK {ip}")),
		Equals("envHighHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighHumidityThresholdViolation")
				.Msg("msg"  , "ems: envHighHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envHighHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envHighHumidityThresholdViolation is OK {ip}")),
		Equals("envLowHumidityThresholdViolation", False).Repeatable() :
			( Danger("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowHumidityThresholdViolation")
				.Msg("msg"  , "ems: envLowHumidityThresholdViolation {ip}")
			, Recover("tag", "ENVIRONMENT").Msg("loc", "{ip}")
				.Msg("descr", "ems: envLowHumidityThresholdViolation is OK")
				.Msg("msg"  , "ems: envLowHumidityThresholdViolation is OK {ip}")),

		Equals("iemContactFault", False).Repeatable() :
			Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
				.Msg("descr", "ems trap: iemContactFault")
				.Msg("msg"  , "ems trap: iemContactFault {ip}"),

		Equals("contactFault", False).Repeatable() :
			Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
				.Msg("descr", "ems trap: contactFault")
				.Msg("msg"  , "ems trap: contactFault {ip}"),

		Equals("emsSensorFault", False).Repeatable() :
			Danger("tag", "INFRASTRUCTURE").Msg("loc", "{ip}")
				.Msg("descr", "ems trap: emsSensorFault")
				.Msg("msg"  , "ems trap: emsSensorFault {ip}"),
	}
}
