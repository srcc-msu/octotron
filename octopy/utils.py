import ru.parallel.octotron as octotron

def AttributesFromDict(attr_dict):
	res = []

	for pair in attr_dict.items():
		res.append(octotron.primitive.SimpleAttribute(*pair))

	return res

def RulesFromDict(rule_dict):
	res = []

	for pair in rule_dict.items():
		(arg_name, obj)	= pair
		obj.SetArgName(arg_name)

		res.append(obj.GetOcto())

	return res

def ReactionsFromDict(react_dict):
	res = []

	for key in react_dict:
		(name, value) = key

		reaction = react_dict[key]

		res.append(octotron.core.OctoReaction(name, value, reaction.response, reaction.delay, reaction.recover))

	return res

def FromNested(attributes, func):
	res = []

	if isinstance(attributes, list):
		for attr_dict in attributes:
			if isinstance(attr_dict, dict):
				res += func(attr_dict)
			else:
				print "got: ", attr_dict
				raise RuntimeError("requires a dictionary or list of dictionaries")
	elif isinstance(attributes, dict):
		res = func(attributes)
	else:
		print "got: ", attributes
		raise RuntimeError("requires a dictionary or list of dictionaries")

	return res
