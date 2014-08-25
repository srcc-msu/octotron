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
	"""convert list of dictionaries to a single dictionary"""
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


# TODO: make better
def UnrollParams(const = None, static = None
	, sensor = None, var = None
	, react = None
	, count = None
	, modules = None):

	if const is None: const = {}
	if static is None: static = {}
	if sensor is None: sensor = {}
	if var is None: var = {}
	if react is None: react = {}

	const_dict = FromNested(const)
	static_dict = FromNested(static)
	sensor_dict = FromNested(sensor)
	var_dict = FromNested(var)
	react_dict = FromNested(react)


	for module in modules:
		if "const" in module:
			const_dict.update(module["const"])
		if "static" in module:
			static_dict.update(module["static"])
		if "sensor" in module:
			sensor_dict.update(module["sensor"])
		if "var" in module:
			var_dict.update(module["var"])
		if "react" in module:
			react_dict.update(module["react"])

	return (const_dict, static_dict, sensor_dict, var_dict, react_dict) 
