#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
generate a sparkline for an artist's timeseries data using sparkplot
  ( http://agiletesting.blogspot.com/2005/04/sparkplot-creating-sparklines-with.html )
that's been fed data from the musicmetric api. Should be called like:

sparky.py [options] source_data artist_mbz_id

For the list of valid data sources see http://www.musicmetric.com/sf-api/

So this call:

python sparky.py -o delta_fans.png facebook_fans f9739c2f-d386-4b87-9258-03cd77e0ac55

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

HOST = 'http://apib1.semetric.com'


class Sparkweb(sparkplot.Sparkplot):
    def get_input_data(self, data_source, mbz_id):
        '''
        assembles and fetches data from a musicmetric timeseries datasource
        then formats the result for ploting timeseries
        '''
        raw_data = loads(urllib2.urlopen(\
                HOST+'/musicmetric/artist/'+mbz_id+'/'+data_source+'.json?token='+API_KEY)\
                             .read())
        self.data = map(lambda x:x[1], raw_data[0][0])

def main(argv):
    log.debug("argv: {0}".format(argv))
    source = argv[-2]
    mbz_id = argv[-1]
    sparker = Sparkweb()
    sparker.get_input_data(source, mbz_id)
    sparker.process_args()
    sparker.plot_sparkline()
    
 
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, 
        format='%(asctime)s %(levelname)s %(message)s')
    sys.exit(main(sys.argv))
