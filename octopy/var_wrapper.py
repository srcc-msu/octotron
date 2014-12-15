from octopy.utils import *

import java.lang
import jarray

from ru.parallel.octotron.core.primitive import EDependencyType
from ru.parallel.octotron.generators.tmpl import VarTemplate

OCTO_PACKAGE = "ru.parallel.octotron"

class Rule(object):
	def __init__(self, args):
		self.args = args

	def GetOcto(self):
		c = java.lang.Class.forName(OCTO_PACKAGE + ".rules." + type(self).__name__)
		cons = c.getConstructors()[0]

		return cons.newInstance(*self.args)


# ASoft

class ASoftDoubleSum(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class ASoftLongSum(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class ASoftMatchCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

class ASoftNotMatchCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

# AStrict

class AStrictDoubleSum(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class AStrictLongSum(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class AStrictMatchCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

class AStrictNotMatchCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

# valid/invalid

class AValidCount(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class AInvalidCount(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.String)))

class RequireSomeValid(Rule):
	def __init__(self, arg1, arg2, arg3, *arg4):
		Rule.__init__(self, (arg1, arg2, arg3, jarray.array(arg4, java.lang.String)))

class AInvalidCount(Rule):
	def __init__(self, arg1, arg2, *arg3):
		Rule.__init__(self, (arg1, arg2, jarray.array(arg3, java.lang.String)))

# logical

class StrictLogicalAnd(Rule):
	def __init__(self, *arg1):
		Rule.__init__(self, (jarray.array(arg1, java.lang.String),))

class StrictLogicalOr(Rule):
	def __init__(self, *arg1):
		Rule.__init__(self, (jarray.array(arg1, java.lang.String),))

class SoftLogicalAnd(Rule):
	def __init__(self, *arg1):
		Rule.__init__(self, (jarray.array(arg1, java.lang.String),))

class SoftLogicalOr(Rule):
	def __init__(self, *arg1):
		Rule.__init__(self, (jarray.array(arg1, java.lang.String),))

# single

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

class Interval(Rule):
	def __init__(self, arg1, *arg2):
		Rule.__init__(self, (arg1, jarray.array(arg2, java.lang.Object),))

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

# utils

def VarsFromDict(varyings_dict):
	res = []

	for name, rule in varyings_dict.items():
		if len(rule) > 1:
			raise RuntimeError("duplicated var: " + name + " : " + str(rule))

		res.append(VarTemplate(name, rule[0].GetOcto()))

	return res

def ConvertVars(var):
	return VarsFromDict(MergeDicts(var))
