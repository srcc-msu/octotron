import sys
import atexit
import time
import inspect

from optparse import OptionParser

import ru.parallel.octotron as octotron

class SystemCtx(object):
	creator = None
	debug = False

	@staticmethod
	def Init(fname, debug):
		SystemCtx.debug = debug

		SystemCtx.start = time.time()

		if not SystemCtx.creator:

			atexit.register(SystemCtx.__Finish)

			def ClearAtexitExcepthook(exctype, value, traceback):
				atexit._exithandlers[:] = []
				sys.__excepthook__(exctype, value, traceback)

			sys.excepthook = ClearAtexitExcepthook

			print
			print "Creating a model, using config file " + fname
			print

			SystemCtx.creator = octotron.exec.DBCreator(fname)
			SystemCtx.creator.Begin()

		else:
			raise RuntimeError("config alredy loaded")

	@staticmethod
	def __Finish():
		if not SystemCtx.creator:
			raise RuntimeError("init not done")
		else:
			SystemCtx.end = time.time()

			print
			print "Creation finished, took %.2f sconds" % (SystemCtx.end - SystemCtx.start)
			print

			SystemCtx.creator.End()
			SystemCtx.creator = None

	@staticmethod
	def GetGraphService():
		if not SystemCtx.creator:
			raise RuntimeError("init not done")

		return SystemCtx.creator.GetGraphService()

	@staticmethod
	def Debug(msg):
		if not SystemCtx.debug:
			return

		(frame, filename, line_number,
			function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[-1]

		print filename + ":" + str(line_number), msg

parser = OptionParser()
parser.add_option("-c", "--config", dest="config",
                  help="[REQUIRED] configuration file")
parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="print debug information")

(options, args) = parser.parse_args()

if not options.config:
	raise RuntimeError("specify configuration file")

SystemCtx.Init(options.config, options.debug)
