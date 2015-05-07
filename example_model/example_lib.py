# include all system wrappers
from octopy import *

#
# module-style declaration
#
my_module = {
# declare constants
	"const" : {
		"temperature_max" : 70,
	},

# declare sensors
# the sensor must be updated every minute or timeout notification will be triggered
	"sensor" : {
		"temperature" : Long(Minutes(1))
	},

# declare varying attribute
# temp_threshold is a boolean attribute,
# which shows is temperature below threshold or not
	"var" : {
		"temp_threshold" : UpperArgThreshold("temperature", "temperature_max"),
	},

# declare triggers
# bad_temperature will be triggered, when temperature check attribute becomes false
	"trigger" :
	{
		"bad_temperature" : Equals("temp_threshold", False),
		"disable_all" : Manual()
	},

# declare reactions
# it will be execute when required trigger is turned on (by user or by condition)
# in thi case - when temperature is above threshold
	"react" : [
		ReactionTemplate("notify_temperature")
			.On("bad_temperature")
			.Off("disable_all")
			.Begin(Danger("tag", "TEMPERATURE")
				.Msg("msg", "very high cpu temperature: {temperature}"))
			.Repeatable()
			.End(Recover("tag", "TEMPERATURE")
				.Msg("msg", "temperature is back to normal: {temperature}"))
	]
}

#
# separate declaration
#
my_const = {
	"load_max" : 90,
}

# declare sensors
my_sensor = {
	"avg_load" : Long(Minutes(1)),
}

# declare varying attrbiutes
my_var = {
	"load_threshold" : UpperArgThreshold("avg_load", "load_max")
}

my_trigger = {
	"bad_load" :  Equals("load_ok", False)
}

my_react = [
	# invoke the Warning() reaction when "avg_load" becomes greater
	# than "load_max" and stays so for 60 or more seconds
		ReactionTemplate("notify_load")
		.Require("bad_load", 0, 60)
		.Response(Warning("msg", "high cpu load for last minute: {avg_load}"))
]