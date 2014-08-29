import ru.parallel.octotron as octotron

def AttributesFromDict(attributes_dict):
	res = []

	for name, value in attributes_dict.items():
		if len(value) > 1:
			raise RuntimeError("duplicated attribute: " + name + " : " + str(value))
		value = value[0]

		res.append(octotron.core.primitive.SimpleAttribute(name, value))

	return res

def VaryingsFromDict(varyings_dict):
	res = []

	for name, rule in varyings_dict.items():
		if len(rule) > 1:
			raise RuntimeError("duplicated var: " + name + " : " + str(rule))
		rule = rule[0]

		rule.SetArgName(name)

		res.append(rule.GetOcto())

	return res

def ReactionsFromDict(react_dict):
	res = []

	for (name, value), reaction in react_dict.items():
		if len(reaction) > 1:
			raise RuntimeError("duplicated reaction: " + name + ", " + value + " : "  + str(reaction))

		reaction = reaction[0]
		res.append(octotron.core.OctoReaction(name, value, reaction.response, reaction.delay, reaction.repeat, reaction.recover))

	return res

def ConvertAttributes(attributes):
	return AttributesFromDict(attributes)

def ConvertVars(var):
	return VaryingsFromDict(var)

def ConvertReacts(react):
	return ReactionsFromDict(react)

import collections

def GetIterable(thing):
	if isinstance(thing, (list, tuple)):
		return thing
	return (thing, )

	"""next is the correct method, but is not working in jython"""
	if isinstance(thing, collections.Iterable):
		return thing
	else:
		return (thing,)

def MergeDicts(dicts):
	result = collections.defaultdict(list)

	for d in dicts:
		if not isinstance(d, dict):
			raise RuntimeError("dictionary is required, got: " + dicts)

		for key, value in d.items():
			for single in GetIterable(value):
				result[key].append(single)

	return result
