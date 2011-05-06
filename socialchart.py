"""Example code to generate a top 50 (or top n) chart based on the total number of fans 
from various social networks from our top 1000 list

originally created by Musicmetric for the Guardian SXSW Hack Day 2011"""

import urllib2
import demjson as json
from apikey import *


#Setup the password manager for basic auth in urllib2
host = 'http://apib1.semetric.com/'

#Download and decode the list of artists of our top 1000 (and their MBID's )
mbid_names_str = urllib2.urlopen("{0}/musicmetric/artist/mbid.json?token={1}".\
                                     format(host, API_KEY)).read()
mbid_names = json.decode(mbid_names_str)

#Setup a list to save the chart into
chart = []
count = 0

#Here is a list of some metrics that can be used to create the chart
metrics = ["Facebook", "MySpace", "Twitter","YouTube","last.fm"]

#Iterate through the list of artists and their MBID's
for mbid, name in mbid_names.items():
    try:  
        #Download, decode and load the artist metric into a list using the MBID
        url = "{0}/musicmetric/artist/{1}/fans_snap.json?token={2}".format(host, mbid, API_KEY)
        kpis_str = urllib2.urlopen(url).read()
        kpis = json.decode(kpis_str)
        for kpi in kpis:
            if kpi[0] == metrics[0]: # Here I have used just Facebook fans as the metric to create the chart
                #This is where you could extend the code to calculate aggregates etc
                chart.append([mbid_names[mbid], kpi[1]])
                print mbid_names[mbid], kpi[1]
    except urllib2.HTTPError, e: #Some dodgy error handling
        pass
    except json.JSONDecodeError, e:
        pass
    count += 1
#    print count
#    if count >= 20:
#        break

#Sort the results so the biggest is at the top
chart.sort(key=lambda x: x[1], reverse=True)
print chart[0:50] #print the top 50

