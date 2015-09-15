from octopy.utils import *

from ru.parallel.octotron.generators.tmpl import TriggerTemplate

def TriggersFromDict(triggers_dict):
	res = []

	for name, trigger in triggers_dict.items():
		if len(trigger) > 1:
			raise RuntimeError("duplicated trigger: " + name + " : " + str(trigger))

		res.append(TriggerTemplate(name, trigger[0].GetPlainOcto()))

	return res

def ConvertTriggers(var):
	return TriggersFromDict(MergeDicts(var))
