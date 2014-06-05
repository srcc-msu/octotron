import ru.parallel.octotron as octotron
import java.lang
import jarray

OCTO_PACKAGE = "ru.parallel.octotron"

class Rule(object):
	def __init__(self, args):
		self.args = args
		self.arg_name = None

	def SetArgName(self, arg_name):
		self.arg_name = arg_name

	def GetOcto(self):
		params = (self.arg_name,) + self.args

		c = java.lang.Class.forName(OCTO_PACKAGE + ".rules." + type(self).__name__)
		cons = c.getConstructors()[0]

		return cons.newInstance(*params)

	#return octotron.rules.__getattr__(type(self).__name__).__call__(*params)

class AggregateDoubleSum(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class AggregateIntSum(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class AggregateMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class AggregateNotMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ArgMatchAprx(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ArgMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class CalcSpeed(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class Changed(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ContainsString(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class LogicalOr(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class LogicalAnd(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorString(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorBoolean(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorDouble(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorLong(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class CheckBoolRules(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

	def GetOcto(self):
		params = (self.arg_name, jarray.array(self.args, java.lang.String))

		c = java.lang.Class.forName(OCTO_PACKAGE + ".rules." + type(self).__name__)
		cons = c.getConstructors()[0]

		return cons.newInstance(params)


class LocalErrors(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class LowerArgThreshold(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class LowerThreshold(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MatchAprx(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class Match(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class NotMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class UpperArgThreshold(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class UpperThreshold(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)