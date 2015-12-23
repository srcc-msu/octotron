from octopy.utils import *

from ru.parallel.octotron.core.logic import Response
from ru.parallel.octotron.generators.tmpl import ReactionTemplate
from ru.parallel.octotron.generators.tmpl import ReactionAction as Reaction

def ReactsFromDict(reactions_dict):
	res = []

	for name, reaction in reactions_dict.items():
		if len(reaction) > 1:
			raise RuntimeError("duplicated reaction: " + name + " : " + str(reaction))

		res.append(ReactionTemplate(name, reaction[0]))

	return res

def ConvertReacts(var):
	return ReactsFromDict(MergeDicts(var))

def Info(tag, message):
	return Response("INFO", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_info")

def Warning(tag, message):
	return Response("WARNING", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_warning")

def Danger(tag, message):
	return Response("DANGER", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_danger")

def Critical(tag, message):
	return Response("CRITICAL", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_critical")


def RInfo(tag, message):
	return Response("RECOVER_INFO", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_info")

def RWarning(tag, message):
	return Response("RECOVER_WARNING", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_warning")

def RDanger(tag, message):
	return Response("RECOVER_DANGER", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_danger")

def RCritical(tag, message):
	return Response("RECOVER_CRITICAL", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_critical")

def GenRStatus(status):
		return {
			Info : RInfo
			, Warning : RWarning
			, Danger : RDanger
			, Critical : RCritical
		}[status]


def Prophecy(tag, message):
	return Response("PROPHECY", []).Msg(tag, message).Msg("_id", "{_id}").Exec("on_prophecy")
