# include all system wrappers
from octopy import *

#
# module-style declaration
#
my_module = {
# declare constants
	"const" : {
		"temp_max" : 70,
	},

# declare sensors
	"sensor" : {
		"temperature" : 0,
	},

# declare varying attrbiutes
	"var" : {
		"temp_ok" : UpperArgThreshold("temperature", "temp_max"),
	},

# declare reactions
	"react" : {
	# invoke the Danger() reaction if "temperature" becomes greater
	# than "temp_max"
	# invoke the Recover() reaction when "temperature" lowers
		Equals("temp_ok", False).Repeatable() :
			(Danger("TEMPERATURE", "very high cpu temperature: {temperature}")
				, Recover("TEMPERATURE", "temperature is back to normal: {temperature}"))
	}
}

#
# separate declaration
#
my_const = {
		"load_max" : 90,
}

# declare sensors
my_sensor = {
	"avg_load" : 0,
}

# declare varying attrbiutes
my_var = {
	"load_ok" : UpperArgThreshold("avg_load", "load_max")
}

my_react = {
	# invoke the Warning() reaction when "avg_load" becomes greater
	# than "load_max" and stays so for 60 or more seconds
		Equals("load_ok", False).Delay(60) :
			Warning("high cpu load for last minute: {avg_load}")
}