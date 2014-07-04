#!/usr/bin/env python
#
# TODO: add OptionParser
#

import httplib
import base64
from urllib import quote
import sys

def import_file(ip, port, fname, name, password):
	headers = {}
	headers["Authorization"] = "Basic " + base64.b64encode(name + ":" + password)
	headers['Connection'] = 'Keep-Alive'

	conn = httplib.HTTPConnection(ip, port)

	f = open(fname)
	for line in f.readlines():

		if len(line) < 2:
			print "error"
			continue

		line = line.strip()

		if len(line) > 0:

			parts = line.split('?')

			if len(parts) == 1:
				pass
			elif len(parts) == 2:
				line = parts[0] + '?' + quote(parts[1])
			else:
				print "error", line
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
	import_file(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), "admin", "admin")