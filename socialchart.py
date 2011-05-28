"""Example code to generate a top 50 (or top n) chart based on the total number of fans 
from various social networks from our top 1000 list

originally created by Musicmetric for the Guardian SXSW Hack Day 2011"""

import urllib2
import demjson as json
from apikey import *


#Setup the password manager for basic auth in urllib2
base_url = 'http://apib2.semetric.com/'

#Download and decode the list of artists of our top 1000 (and their MBID's )
artist_ids_str = urllib2.urlopen("{0}/artist/?token={1}".\
                                     format(base_url, API_KEY)).read()
artist_ids = json.decode(artist_ids_str)['response']['artists']

#Setup a list to save the chart into
chart = []
count = 0

#Here is a list of some metrics that can be used to create the chart
metrics = ["Facebook", "MySpace", "Twitter","YouTube","lastfm"]

#Iterate through the list of artists and their MBID's
for sem_id, name in [(a['id'],a['name']) for a in artist_ids]:
    try:  
        #Download, decode and load the artist metric into a list using the MBID
        url = "{0}/artist/{1}/kpi?token={2}".format(base_url, sem_id, API_KEY)
        kpis_str = urllib2.urlopen(url).read()
        kpis = json.decode(kpis_str)['response']['fans']
        # Here I have used just Facebook fans as the metric to create the chart
        # Other metrics availabe: "myspace", "twitter","youtube","lastfm", "total"
        try:
            total_fans = kpis['facebook']['total']
        except KeyError:
            #no facebook data for an artist, so just continue
            continue
        #This is where you could extend the code to calculate aggregates etc
        chart.append([name, total_fans])
        print chart[-1]
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

