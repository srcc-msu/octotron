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
