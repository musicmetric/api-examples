#!/usr/bin/env python
# encoding: utf-8
"""
align_artists.py

Created by Benjamin Fields on 2011-10-27.
Copyright (c) 2011.
"""

import sys
import getopt
import simplejson
import urllib2
from time import sleep

from apikey_private import API_KEY

help_message = ''' <input_file> <output_file>

Basic alignment of the artists in the million song dataset against Musicmetric tracked artists.
input_file should be list of identifiers from the MSD of the sort available at:
	http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_artists.txt
	and described at 
	http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_artists.txt
the output file will be of the same form (using the seperator '<sep>') with an additional row on the end 
containing semetric artist UUIDs. Note that output_file will only contain the entries for the ids that 
matched the semetric API, those not found will be skipped.
'''

ID_LOOKUP_URL = "http://apib2.semetric.com/artist/musicbrainz:{mbzid}?token={key}"


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		if len(argv) != 3:
			raise Usage(help_message)
		infile = argv[1]
		outfile = argv[2]
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2
	with open(outfile, 'w') as wh:
		with open(infile) as fh:
			for enartistid, mbzid, entrackid, name in (line.strip().split('<SEP>') for line in fh.readlines()):
				sleep(0.5)#be polite.
				try:
					page = urllib2.urlopen(ID_LOOKUP_URL.format(mbzid=mbzid,key=API_KEY)).read()
					resp_env = simplejson.loads(page)
					if resp_env['success']:
						semetric_id = resp_env['response']['id']
						wh.write("{0}<SEP>{1}<SEP>{2}<SEP>{3}<SEP>{4}\n".format(enartistid,
				                                                                    mbzid, 
				                                                                    entrackid,
				                                                                    name,
				                                                                    semetric_id))
						print name,"has the mbzid:", mbzid, "found semetric id:", semetric_id
					else:
						print "couldn't find an id for", name, "mbzid:", mbzid
				except Exception, err:
					print "unable to process", name, "with mbzid", mbzid,"due to err:", err
				
	

if __name__ == "__main__":
	sys.exit(main())
