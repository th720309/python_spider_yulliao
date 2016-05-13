#!/usr/bin/python
import sys, urllib2, re, json, socket, string
from bs4 import BeautifulSoup
from urllib2 import urlopen
socket.setdefaulttimeout(20)
item_dict = {}
try:
    enable_proxy = True

    proxy_handler = urllib2.ProxyHandler({"http" : 'http://127.0.0.1:8787'})

    null_proxy_handler = urllib2.ProxyHandler({})

    if enable_proxy:

        opener = urllib2.build_opener(proxy_handler)

    else:

        opener = urllib2.build_opener(null_proxy_handler)

    urllib2.install_opener(opener)
    for line in open("test_tweet_ids.tsv"):
        fields = line.rstrip('\n').split('\t')
        tweetid = fields[0]
        userid = fields[1]
	#print userid
	#print tweetid
	tweet = None
        text = "Not Available"
        if item_dict.has_key(tweetid):
            text = item_dict[tweetid]
            
        else:
            print tweetid
            try:

                #url='https://twitter.com/statuses/'+str(tweetid)
                #url="http://baidu.com"
                #url="http://www.twitter.com/mitdoc/status/353629216518057984"
                url="http://www.baidu.com"
                print url
                page=urllib2.urlopen(url)
                
                contents=page.read()
                print contents
                soup=BeautifulSoup(contents)
                #f = urllib.urlopen('http://twitter.com/'+str(userid)+'/status/'+str(tweetid))
               # f = urllib.urlopen('https://twitter.com/statuses/'+str(tweetid))
               # print tweetid
               # html = f.read().replace("</html>", "") + "</html>"
               # soup = BeautifulSoup(html)
                #jstt   = soup.find_all("p", "js-tweet-text")
                jstt   = soup.find('div', class_= "js-tweet-text-container")
                #question=soup.findAll('div',{'class':"js-tweet-text-container"})
		tweets = list(set([x.get_text() for x in jstt]))
		print tweets                
		                
		if(len(tweets)) > 1:#means there are more than one tweet being displayed (new twitter design)
			other_tweets = []
			
			cont   = soup.find_all("div", "content")
			for i in cont:
				o_t = i.find_all("p","js-tweet-text")
				other_text = list(set([x.get_text() for x in o_t]))
				other_tweets += other_text					
			tweets = list(set(tweets)-set(other_tweets))
			#print 'Other tweets\n'			
			#print other_tweets                
		        #print tweets
			#print '\n'        
			#continue
		
                text = tweets[0]
                item_dict[tweetid] = tweets[0]
                for j in soup.find_all("input", "json-data", id="init-data"):
                    js = json.loads(j['value'])
                    if(js.has_key("embedData")):
                        tweet = js["embedData"]["status"]
                        text  = js["embedData"]["status"]["text"]
                        item_dict[tweetid] = text
                        break
            except Exception:
		#print userid,tweetid
                continue
    
        if(tweet != None and tweet["id_str"] != tweetid):
                text = "This tweet has been removed or is not available"
                item_dict[tweetid] = "This tweet has been removed or is not available"
        text = text.replace('\n', ' ',)
        text = re.sub(r'\s+', ' ', text)
        print "\t".join(fields + [text]).encode('utf-8')
except IndexError:
    print 'Incorrect arguments specified (may be you didn\'t specify any arguments..'
    print 'Format: python [scriptname] [inputfilename] > [outputfilename]'
