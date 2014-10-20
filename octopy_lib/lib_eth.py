from octopy import *

link_module = {
	"var" : {
		"duplex_match" : LinkedVarArgMatch("duplex"),
		"speed_match" : LinkedVarArgMatch("speed"),
	},

	"react" : {
		Equals("duplex_match", False) :
			( Danger("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "mismatch duplex mode on two sides of the link")
				.Msg("msg"  , "mismatch duplex mode on two sides of the link from {target:ip} to {source:ip}")
			, Recover("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "duplex on the link is ok")
				.Msg("msg"  , "duplex on the link is ok from {target:ip} to {source:ip}")),

		Equals("speed_match", False) :
			( Danger("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "mismatch speed on two sides of the link")
				.Msg("msg"  , "mismatch speed on two sides of the link  from {target:ip} to {source:ip}")
			, Recover("tag", "ETH").Msg("loc", "{source.in_n:ip}")
				.Msg("descr", "speed on the link is ok")
				.Msg("msg"  , "speed on the link is ok from {target:ip} to {source:ip}")),
	}
}
