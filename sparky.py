#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
generate a sparkline for an artist's timeseries data using sparkplot
  ( http://agiletesting.blogspot.com/2005/04/sparkplot-creating-sparklines-with.html )
that's been fed data from the musicmetric api. 
Note that sparkplot uses matplotlib as it's underlying engine, so you'll need that too.
It's available here: http://matplotlib.sourceforge.net/ or via easy_install


Sparky should be called like:

sparky.py [options] source_data artist_mbz_id

For the list of valid data sources see http://www.musicmetric.com/sf-api/

So this call:

python sparky.py -o delta_fans.png fans/facebook f9739c2f-d386-4b87-9258-03cd77e0ac55

will produce a sparkline in delta_fans.png with no text labels (default) of the daily
change in facebook fans for Drop the Lime (mbz: f9739c2f-d386-4b87-9258-03cd77e0ac55)

'''
import sys
import logging
log = logging.getLogger(__name__)

import sparkplot
import urllib2
from simplejson import loads
from apikey import *

base_url = 'http://apib2.semetric.com'


class Sparkweb(sparkplot.Sparkplot):
    def get_input_data(self, dataset_name, MBID):
        '''
        assembles and fetches data from a musicmetric timeseries datasource
        then formats the result for ploting timeseries
        '''
        raw_response = loads(urllib2.urlopen(\
                base_url+'/artist/musicbrainz:'+MBID+'/'+dataset_name+'?token='+API_KEY)\
                             .read())
        self.data = raw_response['response']['data']

def main(argv):
    log.debug("argv: {0}".format(argv))
    dataset_name = argv[-2]
    MBID = argv[-1]
    sparker = Sparkweb()
    sparker.get_input_data(dataset_name, MBID)
    sparker.process_args()
    sparker.plot_sparkline()
    
 
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s')
    sys.exit(main(sys.argv))
