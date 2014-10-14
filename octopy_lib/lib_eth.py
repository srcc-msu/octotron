from octopy import *

link_module = {
	"var" : {
		"duplex_match" : LinkedVarArgMatch("duplex"),
		"speed_match" : LinkedVarArgMatch("speed"),
	},

	"react" : {
		Equals("duplex_match", False) :
			(Danger("ETH", "mismatch duplex mode on two sides of the link")
				, Recover("duplex on the link is ok")),

		Equals("speed_match", False) :
			(Danger("ETH", "mismatch speed on two sides of the link")
				, Recover("speed on the link is ok")),
	}
}
