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

class AggregateDoubleSum(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class AggregateLongSum(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class AggregateMatchCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

class AggregateNotMatchCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

class ArgMatchAprx(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ArgMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class CalcSpeed(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ToPct(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ToArgPct(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class Changed(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class ContainsString(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class LogicalAnd(Rule):
	def __init__(self, *arg1):
		Rule.__init__(self, (jarray.array(arg1, java.lang.String),))

class LogicalOr(Rule):
	def __init__(self, *arg1):
		Rule.__init__(self, (jarray.array(arg1, java.lang.String),))

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

class MirrorBoolean(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorDouble(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorLong(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class MirrorString(Rule):
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

class VarArgMatchAprx(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class VarArgMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

class LinkedVarArgMatch(Rule):
	def __init__(self, *args):
		Rule.__init__(self, args)

import ru.parallel.octotron.core.primitive.EDependencyType as EDependencyType
