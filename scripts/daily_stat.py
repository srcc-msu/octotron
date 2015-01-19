#!/usr/bin/env python

import sys

from collections import defaultdict
from optparse import OptionParser

import json

def Generate(lines):
	data = defaultdict(int)

	for line in lines:
		if len(line) <= 1:
			continue

		try:
			fields = json.loads(line)

			suppressed = fields["reaction"]["suppressed"]

			status = fields["info"]["status"]
			descr = fields["usr"]["descr"]

			data[(status, descr, suppressed)] += 1

		except Exception, ignore:
			print >> sys.stderr, "error parsing: ", line

	return data

if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("-f", "--file", dest="fname", default = None)

	(options, args) = parser.parse_args()

	if not options.fname:
		raise RuntimeError("specify file name")


	with open(options.fname) as file:
		data = Generate(file.readlines())

		linear = [(suppressed, status, count, descr) for ((status, descr, suppressed), count) in data.items()]
		linear = sorted(linear, reverse=True)

		order = [
			"CRITICAL",
			"DANGER",
			"WARNING",
			"INFO",
			"RECOVER",
		]

		print "*** reported events ***"
		print

		for entry in order:
			printed = False
			for suppressed, status, count, descr in linear:
				if not suppressed and status == entry:
					print '{}, {}, "{}"'.format(count, status, descr)
					printed = True
			if printed:
				print

		print "*** suppressed events ***"
		print

		for entry in order:
			printed = False
			for suppressed, status, count, descr in linear:
				if suppressed and status == entry:
					print '{}, {}, "{}"'.format(count, status, descr)
					printed = True
			if printed:
				print

