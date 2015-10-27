from octopy import *

def InitDuplication(host1, host2, timeout = Minutes(10)):
	def dup_module(host1, host2):
		return {
			"const" : {
				"type" : "octotron",
				"host" : host1,
				"dup_host" : host2
			},

			"sensor" : {
				"working" : Boolean(timeout)
			},

			"trigger" : {
				"not_working" : Match("working", False)
			},

			"react" : {
				"notify1" : Reaction()
					.On("not_working")
					.Begin(Danger("tag", "OCTOTRON")
						.Msg("loc", "{host}")
						.Msg("descr", "octotron on {host} failed one check")
						.Msg("msg", "don't panic - might be just a false alarm"))
					.End(Recover("tag", "OCTOTRON")
						.Msg("loc", "{host}")
						.Msg("descr", "octotron on {host} is ok")
						.Msg("msg", "that was close..")),

				"notify2" : Reaction()
					.On("not_working", 2, 0)
					.Begin(Danger("tag", "OCTOTRON")
						.Msg("loc", "{host}")
						.Msg("descr", "octotron on {host} failed TWO checks, emergency protocol activated")
						.Msg("msg", "self-destruct sequence initiated. please panic")
						.Exec("on_octotron_fail", "{host}", "{dup_host}")),
			}
		}

	CreateObject(dup_module(host1, host2))
	CreateObject(dup_module(host2, host1))
