from ru.parallel.octotron.generators.tmpl import TriggerTemplate

from ru.parallel.octotron.triggers import Equals
from ru.parallel.octotron.triggers import NotEquals

# utils

def TriggersFromDict(triggers_dict):
	res = []

	for name, rule in varyings_dict.items():
		if len(rule) > 1:
			raise RuntimeError("duplicated trigger: " + name + " : " + str(rule))

		res.append(TriggerTemplate(name, trigger))

	return res

def ConvertTriggers(var):
	return TriggersFromDict(MergeDicts(var))
