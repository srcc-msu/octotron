#!/usr/bin/env python
#

import sys
import httplib
import base64

from urllib import quote

from optparse import OptionParser

def import_file(ip, port, fname, usr, pwd):
	headers = {}
	headers["Authorization"] = "Basic " + base64.b64encode(usr + ":" + pwd)
	headers['Connection'] = 'Keep-Alive'

	conn = httplib.HTTPConnection(ip, port)

	f = open(fname)
	for line in f.readlines():

		if len(line) < 1 or line[0] == '#':
			continue

		line = line.strip()

		if len(line) > 0:

			parts = line.split('?')

			if len(parts) == 1:
				pass
			elif len(parts) == 2:
				line = parts[0] + '?' + quote(parts[1])
			else:
				print "error, line:", line
				continue

			resp = None

			try:
				conn.request('POST', line, None, headers)
				resp = conn.getresponse()
			except Exception, e:
				print "exception: ", e
				print "line:", line
				print "headers:", headers

			if resp is not None:
				try:
					data = resp.read()
				except Exception, e:
					print e

	conn.close()
	f.close()

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-i", "--ip", dest="ip", default = "127.0.0.1")
	parser.add_option("-p", "--port", dest="port", type = int)
	parser.add_option("-f", "--fname", dest="fname")
	parser.add_option("--usr", dest="usr", default = "")
	parser.add_option("--pwd", dest="pwd", default = "")

	(options, args) = parser.parse_args()

	if not options.port:
		raise RuntimeError("specify port")

	if not options.fname:
		raise RuntimeError("specify fname")

	import_file(options.ip, options.port, options.fname
		, options.usr, options.pwd)
