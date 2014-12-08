from octopy.utils import *

from ru.parallel.octotron.generators.tmpl import SensorTemplate

def Seconds(t):
	return t

def Minutes(t):
	return Seconds(t * 60)

def Hours(t):
	return Minutes(t * 60)

def Days(t):
	return Hours(t * 24)

class Sensor(object):
	def __init__(self, time, value):
		self.time = time
		self.value = value

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

def SensorsFromDict(sensors_dict):
	res = []

	for name, sensor in sensors_dict.items():
		if len(sensor) > 1:
			raise RuntimeError("duplicated sensor: " + name + " : " + str(sensor))

		if sensor[0].value is None:
			res.append(SensorTemplate(name, sensor[0].time))
		else:
			res.append(SensorTemplate(name, sensor[0].time, sensor[0].value))

	return res

def ConvertSensors(var):
	return SensorsFromDict(MergeDicts(var))
