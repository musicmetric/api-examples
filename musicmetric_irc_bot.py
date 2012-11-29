#!/usr/bin/python
"""IRC Bot that uses the Musicmetric API to respond to commands. 
   
   Uses oyoyo IRC library:
    http://code.google.com/p/oyoyo
   
   And Musicmetric API:
    http://developer.musicmetric.com
   
   It sometimes doesen't work with Quakenet.org so that's an 
   excercise for the reader...
   
   """
import logging
import re
from oyoyo.client import IRCClient
from oyoyo.cmdhandler import DefaultCommandHandler
from oyoyo import helpers
from simplejson import loads
import urllib2
import random

HOST = 'irc.freenode.net'
PORT = 6667
NICK = 'Musicmetric'
CHANNEL = '#your_channel'
API_KEY = "YOUR_API_KEY"
    

class MyHandler(DefaultCommandHandler):
    """Handler for the IRC bot"""
    def privmsg(self, nick, chan, msg):
        msg = msg.decode()

        match_sent = re.match('\!Musicmetric (.*)', msg)
        #Respond to a comment
        if match_sent:
            to_say = match_sent.group(1).strip()
            helpers.msg(self.client, chan, sentiment(to_say))

        match_question = re.match('\!question (.*)', msg)
        #Answer a yes/no question
        if match_question:
            to_say = match_question.group(1).strip()
            helpers.msg(self.client, chan, question(to_say))

        match_chart = re.match('\!chart', msg)
        #Generate a top 5 chart with Musicmetric stats
        if match_chart:
            helpers.msg(self.client, chan, "This is gunna take a while, \
                    I have to count all the stats to make this chart...")
            to_say = get_chart()
            helpers.msg(self.client, chan, to_say)      
        
        match_die = re.match('\!DIE MUSICMETRIC (.*)', msg)
        #Kill the bot
        if match_die:
            helpers.msg(self.client, chan, "blluauuaragghghhhhhhhh!!!!!!")
            exit(0)


def sentiment(text):
    """Function that takes some input text and reples with 
       something based on what the sentiment of the input text was"""
    sentiment_words = {1:"That's pretty offensive :'(", 
                       2:"That's pretty rude", 
                       3:"Meh", 4:"What a nice thing to say", 
                       5:"That's very nice of you to say!"}
    raw_senti = loads(urllib2.urlopen("http://apib1.semetric.com/musicmetric/sentiment?token="+ API_KEY, data = text).read())
    return sentiment_words[raw_senti['score']]


def question(text):
    """Function that takes a yes/no question and responds 
       based on the sentiment of the question. Basically 
       Magic 8 ball powered by sentiment algorithms :)"""
    sentiment_words = {1:["Definitely not!", "Hells no!", "TERRIBLE, NO!", 
                          "NOOOOOO!!!!", 
                          "That is the worst thing I've EVER heard suggested, so NO!"], 
                       2:["Signs point to no", "Most likely no", 
                          "NOT LIKELY", "No chance", "No way"],
                       3:["Undecided", "Hmmm, I'm not really sure...", 
                          "Maybe, I dunno", "I dunno", 
                          "You decide, I can't decide"],
                       4:["Signs point to yes", "Good one, yeah", "Yeeeah, why not?", 
                          "Absolutely yes", "I guess yeah... :)"], 
                       5:["Absolutely yes!", "DEFINITELY!!!", 
                          "Holy crap YES!!", "Genius - Yes!!", 
                          "AAWWWWWW YEAH!!!!!"]}
                       
    raw_senti = loads(urllib2.urlopen("http://apib1.semetric.com/musicmetric/sentiment?token="+ API_KEY, data = text).read())
    return random.sample(sentiment_words[raw_senti['score']], 1)[0]


def get_chart():
    """Make a chart of the top 5 artists tracked by Musicmetric right now"""
    import demjson as json
    print "This is gunna take a while., I have to count all the stats to make this chart..."
    base_url = 'http://apib1.semetric.com/'
    mbid_names_str = urllib2.urlopen("{0}/musicmetric/artist/mbid.json?token={1}". format(base_url, API_KEY)).read()
    mbid_names = json.decode(mbid_names_str)
    chart = []
    count = 0
    metrics = ["Facebook", "MySpace", "Twitter", "YouTube", "last.fm"]
    for mbid, name in mbid_names.items():
        try:  
            url = "{0}/musicmetric/artist/{1}/fans_snap.json?token={2}".format(base_url, mbid, API_KEY)
            kpis_str = urllib2.urlopen(url).read()
            kpis = json.decode(kpis_str)
            for kpi in kpis:
                if kpi[0] == metrics[0]:
                    chart.append([mbid_names[mbid], kpi[1]])
        except urllib2.HTTPError, exep:
            print exep
            pass
        except json.JSONDecodeError, exep:
            print exep
            pass
    chart.sort(key=lambda x: x[1], reverse=True)
    return "The top artists today are: %s, %s, %s and %s"  % (chart[0][0], chart[1][0], chart[2][0], chart[3][0])


def connect_cb(cli):
    """connect callback"""
    helpers.join(cli, CHANNEL)

def main():
    logging.basicConfig(level=logging.DEBUG)
    cli = IRCClient(MyHandler, host=HOST, port=PORT, nick=NICK, connect_cb=connect_cb)
    conn = cli.connect()

    while True:
        conn.next()


if __name__ == '__main__':
    """main function"""
    main()
