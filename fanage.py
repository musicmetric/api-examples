"""Example code to sort the artists playing at SXSW 2011 based on the mean age of their
fans - e.g. bands with the oldest or youngest fans

Musicmetric at the Guardian SXSW Hack Day 2011"""

import urllib2
import demjson as json

from apikey import *

#base url
base_url = 'http://apib1.semetric.com/'

#Download and decode the list of artists playing at SXSW 2011 (and their MBID's )
mbid_names_str = urllib2.urlopen("{0}/musicmetric/artist/mbid.json?token={1}".format(base_url, API_KEY)).read()
mbid_names = json.decode(mbid_names_str)

#Setup a list to save the chart into
chart = []
count = 0

#Iterate through the list of artists and their MBID's
for mbid, name in mbid_names.items():
    try:  
        #Download, decode and load the artists fan age distribution
        age_url = "{0}/musicmetric/artist/{1}/myspace_profile_age.json?token={2}".format(base_url, mbid, API_KEY)
        age_str = urllib2.urlopen(age_url).read()
        ages = json.decode(age_str)
        
        #Calculate the mean age
        freq = 0
        age_sum = 0
        for age in ages:
            freq += age[0]
            age_sum += age[0] * age[1]
        
        average_age = age_sum / freq
        chart.append([mbid_names[mbid], average_age])
        
    except urllib2.HTTPError, e: #Some dodgy error handling
        pass
    count += 1


#Sort the results so the biggest is at the top
chart.sort(key=lambda x: x[1], reverse=False)
print chart[0:10] #print the top 10
