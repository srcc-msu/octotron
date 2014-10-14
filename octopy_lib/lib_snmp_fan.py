from octopy import *

def __FanReactSetting(tag, msg1, msg2):
	return (Danger(tag, msg1).PrintParent("type", "descr")
		, Recover(msg2).PrintParent("type", "descr"))

fan_snmp_module = {
	"static" :
	{
		"_static_infra_air_in_temp"  : 35,
		"_static_infra_air_out_temp" : 25,

		"_static_infra_fluid_in_temp" : 20,

		"_static_infra_humidity" : 70,
	},

	"sensor" : {
		"inlet_1" : 0,
		"inlet_2" : 0,
		"inlet_3" : 0,
		"humidity_in"  : 0,
		"humidity_out" : 0,
		"air_in"  : 0,
		"air_out" : 0,
		"fluid_in"  : 0,
		"fluid_out" : 0,
	},

	"var" : {
		"inlet_1_ok" : UpperArgThreshold("inlet_1", "_static_infra_air_in_temp"),
		"inlet_2_ok" : UpperArgThreshold("inlet_2", "_static_infra_air_in_temp"),
		"inlet_3_ok" : UpperArgThreshold("inlet_3", "_static_infra_air_in_temp"),

		"humidity_in_ok"  : UpperArgThreshold("humidity_in", "_static_infra_humidity"),
		"humidity_out_ok" : UpperArgThreshold("humidity_out", "_static_infra_humidity"),
		"air_in_ok"  : UpperArgThreshold("air_in", "_static_infra_air_in_temp"),
		"air_out_ok" : UpperArgThreshold("air_out", "_static_infra_air_out_temp"),

		"fluid_in_ok"  : UpperArgThreshold("fluid_in", "_static_infra_fluid_in_temp"),
	},

	"react" : {
		Equals("inlet_1_ok", False) : __FanReactSetting("TEMPERATURE"
			, "air temp 1 is too high: {inlet_1}"
			, "air temp 1 is back to normal"),

		Equals("inlet_2_ok", False) :	__FanReactSetting("TEMPERATURE"
			, "air temp 2 is too high: {inlet_2}"
			, "air temp 2 is back to normal"),

		Equals("inlet_3_ok", False) : __FanReactSetting("TEMPERATURE"
			, "air temp 3 is too high: {inlet_3}"
			, "air temp 3 is back to normal"),

		Equals("humidity_in_ok", False) : __FanReactSetting("ENVIRONMENT"
			, "air humidity_in is too high: {humidity_in}"
			, "air humidity_in is back to normal"),

		Equals("humidity_out_ok", False) : __FanReactSetting("ENVIRONMENT"
			, "air humidity_out is too high: {humidity_out}"
			, "air humidity_out is back to normal"),

		Equals("air_in_ok", False) : __FanReactSetting("TEMPERATURE"
			, "air_in temp is too high: {air_in}"
			, "air_in temp is back to normal"),

		Equals("air_out_ok", False) : __FanReactSetting("TEMPERATURE"
			, "air_out temp  is too high: {air_out}"
			, "air_out temp  is back to normal"),

		Equals("fluid_in_ok", False) : __FanReactSetting("TEMPERATURE"
			, "fluid_in temp is too high: {fluid_in}"
			, "fluid_in temp is back to normal"),
	}
}

fan_snmp_trap_module = {
	# False = no trap
	"sensor" : {
		"airCriticalCondition_29" : False,
		"airCriticalCondition_29_descr" : "",

		"airWarningCondition_24" : False,
		"airWarningCondition_24_descr" : "",
		"airWarningCondition_27" : False,
		"airWarningCondition_27_descr" : "",
		"airWarningCondition_28" : False,
		"airWarningCondition_28_descr" : "",
		"airWarningCondition_32" : False,
		"airWarningCondition_32_descr" : "",
		"airWarningCondition_39" : False,
		"airWarningCondition_39_descr" : "",
		"airWarningCondition_40" : False,
		"airWarningCondition_40_descr" : "",
		"airWarningCondition_54" : False,
		"airWarningCondition_54_descr" : "",

		"airInformationalCondition_3" : False,
		"airInformationalCondition_3_descr" : "",
	},

	"var" : {
		"pump_fault" : ContainsString("airCriticalCondition_29_descr", "fault exists"),

		"water_detected" : ContainsString("airWarningCondition_28_descr", "fault exists"),

		"fan_fault" : ContainsString("airWarningCondition_27_descr", "fault exists"),

		"low_water_alarm" : ContainsString("airWarningCondition_32_descr", "alarm exists"),

		"entering_fluid_temp_fault" : ContainsString("airWarningCondition_39_descr", "violation exists"),

		"fluid_temp_sensor_fault" : ContainsString("airWarningCondition_40_descr", "sensor fault exists"),

		"communication_lost" : ContainsString("airWarningCondition_54_descr", "lost"),

		"relay_output_fault" : ContainsString("airInformationalCondition_3_descr", "abnormal state exists")
	},

	"react" : {
		Equals("airWarningCondition_24", True).Repeatable() :
			Warning("INFRASTRUCTURE", "Frequent Humidifier faults: {airWarningCondition_24_descr}"),

		Equals("pump_fault", True) :
			(Critical("INFRASTRUCTURE", "Condensate pump fault: {airCriticalCondition_29_descr}")
				, Recover("Condensate pump is ok: {airCriticalCondition_29_descr}")),

		Equals("water_detected", True) :
			(Danger("ENVIRONMENT", "Sensor detected a fluid leak!: {airWarningCondition_28_descr}")
				, Recover("Sensor is ok, no fluid detected: {airWarningCondition_28_descr}")),

		Equals("fan_fault", True) :
			(Warning("INFRASTRUCTURE", "Fan fault: {airWarningCondition_27_descr}")
				, Recover("Fan is ok: {airWarningCondition_27_descr}")),

		Equals("low_water_alarm", True) :
			(Warning("INFRASTRUCTURE", "Humidifier low water level alarm : {airWarningCondition_32_descr}")
				, Recover("Humidifier is ok: {airWarningCondition_32_descr}")),

		Equals("entering_fluid_temp_fault", True) :
			(Warning("TEMPERATURE", "Entering fluid temperature is too high: {airWarningCondition_39_descr}")
				, Recover("Entering fluid temperature is ok: {airWarningCondition_39_descr}")),

		Equals("fluid_temp_sensor_fault", True) :
			(Warning("INFRASTRUCTURE", "Entering fluid tempereature sensor failed: {airWarningCondition_40_descr}")
				, Recover("Entering fluid tempereature sensor is ok: {airWarningCondition_40_descr}")),

		Equals("communication_lost", True) :
			(Warning("INFRASTRUCTURE", "Group communication lost: {airWarningCondition_54_descr}")
				, Recover("Group communication restored: {airWarningCondition_54_descr}")),

		Equals("relay_output_fault", True) :
			(Info("INFRASTRUCTURE", "Relay output abnormal state: {airInformationalCondition_3_descr}")
				, Recover("Relay output is ok: {airInformationalCondition_3_descr}"))
	}
}
