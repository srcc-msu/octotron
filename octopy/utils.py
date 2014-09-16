import ru.parallel.octotron as octotron

import collections

def GetCollection(thing):
	if isinstance(thing, (list, tuple)):
		return thing
	return (thing, )

	"""next is the correct method, but is not working in jython"""
	if isinstance(thing, collections.Iterable):
		return thing
	else:
		return (thing,)

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

	for event, response in react_dict.items():
		collection = GetCollection(response)

		if len(collection) == 2:
			res.append(event.Response(collection[0]).RecoverResponse(collection[1]))
		elif len(collection) == 1:
			res.append(event.Response(collection[0]))
		else:
			raise RuntimeError("expected a single response or list/tuple with 2 responses, got: " + response)

	return res

def ConvertAttributes(attributes):
	return AttributesFromDict(attributes)

def ConvertVars(var):
	return VaryingsFromDict(var)

def ConvertReacts(react):
	return ReactionsFromDict(react)

def MergeDicts(dicts):
	result = collections.defaultdict(list)

	for d in dicts:
		if not isinstance(d, dict):
			raise RuntimeError("dictionary is required, got: " + str(dicts))

		for key, value in d.items():
			for single in GetCollection(value):
				result[key].append(single)

	return result

def MergeUniqueDicts(dicts):
	result = collections.defaultdict(list)

	for d in dicts:
		if not isinstance(d, dict):
			raise RuntimeError("dictionary is required, got: " + str(dicts))

		for key, value in d.items():
			if key in result:
				raise RuntimeError("duplicated entry for: " + key)
			result[key] = value

	return result
