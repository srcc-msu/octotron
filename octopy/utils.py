import collections

import ru.parallel.octotron.generators.CSVReader as CSVReader_java
import ru.parallel.octotron.generators.Enumerator as Enumerator_java

def GetCollection(thing):
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
			raise RuntimeError("dictionary is required, got: " + str(d))

		for key, value in d.items():
			for single in GetCollection(value):
				result[key].append(single)

	return result

__allowed = ["const", "static", "sensor", "var", "react"]

def CheckAllowed(params):
	for param in params.keys():
		if param not in __allowed:
			raise RuntimeError("unknown key: " + param)

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

class CSVReader:
	@staticmethod
	def Declare(*params):
		CSVReader_java.Declare(model_service, *params)

class Enumerator:
	@staticmethod
	def Sequence(*params):
		Enumerator_java.Sequence(model_service, *params)
