"""Example code to sort the artists playing at SXSW 2011 based on the mean age of their
fans - e.g. bands with the oldest or youngest fans

Musicmetric at the Guardian SXSW Hack Day 2011"""

import urllib2
import demjson as json

#Setup the password manager for basic auth in urllib2
url = 'http://sxsw-hacks.musicmetric.com/'
user = 'YOUR_API_USERNAME'
pwd = 'YOUR_API_PASSWORD'
pass_man = urllib2.HTTPPasswordMgrWithDefaultRealm()
pass_man.add_password(None, url, user, pwd)
authhandler = urllib2.HTTPBasicAuthHandler(pass_man)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

#Download and decode the list of artists playing at SXSW 2011 (and their MBID's )
mbid_names_str = urllib2.urlopen("http://sxsw-hacks.musicmetric.com/musicmetric/artist/mbid.json").read()
mbid_names = json.decode(mbid_names_str)

#Setup a list to save the chart into
chart = []
count = 0

#Iterate through the list of artists and their MBID's
for mbid, name in mbid_names.items():
    try:  
        #Download, decode and load the artists fan age distribution
        age_url = "http://sxsw-hacks.musicmetric.com/musicmetric/artist/%s/myspace_profile_age.json" % mbid
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
