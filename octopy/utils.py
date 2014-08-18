import ru.parallel.octotron as octotron

def AttributesFromDict(attributes_dict):
	res = []

	for pair in attributes_dict.items():
		res.append(octotron.core.primitive.SimpleAttribute(*pair))

	return res

def VaryingsFromDict(varyings_dict):
	res = []

	for arg_name, obj in varyings_dict.items():
		obj.SetArgName(arg_name)

		res.append(obj.GetOcto())

	return res

def ReactionsFromDict(react_dict):
	res = []

	for (name, value), reaction in react_dict.items():
		res.append(octotron.core.OctoReaction(name, value, reaction.response, reaction.delay, reaction.repeat, reaction.recover))

	return res

def FromNested(attributes):
	res = {}

	if isinstance(attributes, list):
		for attributes_dict in attributes:
			if isinstance(attributes_dict, dict):
				res.update(attributes_dict)
			else:
				print "got: ", attributes_dict
				raise RuntimeError("requires a dictionary or list of dictionaries")
	elif isinstance(attributes, dict):
		return attributes
	else:
		print "got: ", attributes
		raise RuntimeError("requires a dictionary or list of dictionaries")

	return res

def ConvertAttributes(attributes):
	return AttributesFromDict(FromNested(attributes))

def ConvertVar(var):
	return VaryingsFromDict(FromNested(var))

def ConvertReact(react):
	return ReactionsFromDict(FromNested(react))
