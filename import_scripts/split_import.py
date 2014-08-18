#!/usr/bin/env python
#
# import data from stream, splitting them to chunks
# and feeding them to import_url_file.py
# skips data starting with '#' and empty lines
#
# TODO: add OptionParser
#

import sys
import os
import import_url_file

def split_import(ip, port, max_lines, fname, name, password):
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
			import_url_file.import_file(ip, port, fname, name, password)

			lines = 0
			file = None

	# import leftovers, when stream ends
	if file is not None:
		print "importing", lines
		import_url_file.import_file(ip, port, fname, name, password)

if __name__ == "__main__":
	ip = str(sys.argv[1])
	port = int(sys.argv[2])
	max_lines = int(sys.argv[3])

	split_import(ip, port, max_lines, "/tmp/octo_split_script", "", "")