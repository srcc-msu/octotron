from octopy.utils import *

from ru.parallel.octotron.generators.tmpl import ConstTemplate

def ConstsFromDict(attributes_dict):
	res = []

	for name, value in attributes_dict.items():
		if len(value) > 1:
			raise RuntimeError("duplicated attribute: " + name + " : " + str(value))

		res.append(ConstTemplate(name, value[0]))

	return res

def ConvertConsts(attributes):
	return ConstsFromDict(MergeDicts(attributes))
