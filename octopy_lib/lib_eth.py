from octopy import *

link_module = {
	"var" : {
		"duplex_match" : LinkedVarArgMatch("duplex"),
		"speed_match" : LinkedVarArgMatch("speed"),
	},

	"react" : {
		Equals("duplex_match", False) :
			(Danger("mismatch duplex mode on two sides of the link", "type")
				, Recover("duplex on the link is ok", "type")),

		Equals("speed_match", False) :
			(Danger("mismatch speed on two sides of the link", "type")
				, Recover("speed on the link is ok", "type")),
	}
}
