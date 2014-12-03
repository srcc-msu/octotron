import collections

from ru.parallel.octotron.generators.tmpl import ConstantTemplate
from ru.parallel.octotron.generators.tmpl import SensorTemplate
from ru.parallel.octotron.generators.tmpl import VarTemplate

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

def ConstantsFromDict(attributes_dict):
	res = []

	for name, value in attributes_dict.items():
		if len(value) > 1:
			raise RuntimeError("duplicated attribute: " + name + " : " + str(value))

		res.append(ConstantTemplate(name, value[0]))

	return res


def SensorsFromDict(sensors_dict):
	res = []

	for name, sensor in sensors_dict.items():
		if len(sensor) > 1:
			raise RuntimeError("duplicated sensor: " + name + " : " + str(sensor))

		res.append(SensorTemplate(name, sensor[0].time, sensor[0].value))

	return res

def VarsFromDict(varyings_dict):
	res = []

	for name, rule in varyings_dict.items():
		if len(rule) > 1:
			raise RuntimeError("duplicated var: " + name + " : " + str(rule))

		res.append(VarTemplate(name, rule[0].GetOcto()))

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

def ConvertConstants(attributes):
	return ConstantsFromDict(attributes)

def ConvertSensors(var):
	return SensorsFromDict(var)

def ConvertVars(var):
	return VarsFromDict(var)

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
		CSVReader_java.Declare(context.model_service, *params)

class Enumerator:
	@staticmethod
	def Sequence(*params):
		Enumerator_java.Sequence(context.model_service, *params)

def Seconds(t):
	return t

def Minutes(t):
	return Seconds(t * 60)

def Hours(t):
	return Minutes(t * 60)

def Days(t):
	return Hours(t * 24)

class Sensor(object):
	def __init__(self, value, time):
		self.value = value
		self.time = time

class Long(Sensor):
	def __init__(self, time, value = None):
		super(Long, self).__init__(time, value)

class Double(Sensor):
	def __init__(self, time, value = None):
		super(Double, self).__init__(time, value)

class Boolean(Sensor):
	def __init__(self, time, value = None):
		super(Boolean, self).__init__(time, value)

class String(Sensor):
	def __init__(self, time, value = None):
		super(String, self).__init__(time, value)

UPDATE_TIME_NOT_SPECIFIED = -1
