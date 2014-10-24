#!/usr/bin/env python
#
# import data from stream, splitting them to chunks
# and feeding them to import_url_file.py
# skips data starting with '#' and empty lines
#

import sys
import os
import import_url_file

from optparse import OptionParser

def split_import(ip, port, max_lines, fname, usr, pwd):
	file = None
	lines = 0

	for line in sys.stdin:
		if file is None:
			file = open(fname, "w")

		if len(line) < 1 or line[0] == '#':
			continue

		file.write(line)
		lines += 1

		if lines >= max_lines:
			file.close()

			print "importing", lines
			import_url_file.import_file(ip, port, fname, usr, pwd)

			lines = 0
			file = None

# import leftovers, when stream ends
	if file is not None:
		file.close()

		print "importing", lines
		import_url_file.import_file(ip, port, fname, usr, pwd)

if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("-i", "--ip", dest="ip", default = "127.0.0.1")
	parser.add_option("-p", "--port", dest="port", type = int)
	parser.add_option("-l", "--lines", dest="lines", type = int, default = 1)
	parser.add_option("--usr", dest="usr", default = "")
	parser.add_option("--pwd", dest="pwd", default = "")
	parser.add_option("--tmp", dest="tmp", default = "/tmp/octo_split_script")

	(options, args) = parser.parse_args()

	if not options.port:
		raise RuntimeError("specify port")

	split_import(options.ip, options.port, options.lines
		, options.tmp
		, options.usr, options.pwd)
