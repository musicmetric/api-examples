"""Example code to generate a top 50 (or top n) chart based on the total number of fans 
that artists playing at SXSW have on various social networks

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

#Download and decode the list of artists playing at SXSW 2011 who also played at SXSW2010 (and their MBID's )
mbid_names_str = urllib2.urlopen("http://sxsw-hacks.musicmetric.com/musicmetric/artist/mbid.json").read()
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
        url = "http://sxsw-hacks.musicmetric.com/musicmetric/artist/%s/fans_snap.json" % mbid
        kpis_str = urllib2.urlopen(url).read()
        kpis = json.decode(kpis_str)
        for kpi in kpis:
            if kpi[0] == metrics[0]: # Here I have used just Facebook fans as the metric to create the chart
                #This is where you could extend the code to calculate aggregates etc
                chart.append([mbid_names[mbid], kpi[1]])
                print mbid_names[mbid], kpi[1]
    except urllib2.HTTPError, e: #Some dodgy error handling
        pass
    count += 1
#    print count
#    if count >= 20:
#        break

#Sort the results so the biggest is at the top
chart.sort(key=lambda x: x[1], reverse=True)
print chart[0:50] #print the top 50

