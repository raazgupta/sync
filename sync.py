#Haven't had time to do much error checking and boundary case checking. So ENTER at your own RISK. Huhahahaha. 

#A simple check before the program runs to allow the user to command the OS to connect to the internet and also 
#check whether the program needs to run at all. As in my case this program will be scheduled for starting when the OS starts,
#it makes sense to have this check.
var = raw_input("Press Enter if you are ready to run Social Sync. Make sure the juice is flowing, uh, I mean that you are connected to the internet!")

#Import the necessary libraries
#Please download and install, along with the dependies, the python-twitter library - http://code.google.com/p/python-twitter/
#Also download and install BeautifulSoup http://www.crummy.com/software/BeautifulSoup/
import urllib2
from BeautifulSoup import BeautifulSoup
import shorten_url
import twitter

#VARIABLES THAT ARE DEPENDENT ON THE USER APP AND WILL NEED TO BE FILLED BEFORE THE PROGRAMS RUNS

#CHANGE THE PUBLIC PROFILE PAGE TO WHAT YOUR GOOGLE PLUS public profile page is
#Now query the Google+ Public progile page and get the statuses there
publicProfilePage = 'https://plus.google.com/<YOUR GOOGLE PLUS ID NUMBER GOES HERE>/posts'


#PLEASE READ THROUGH https://dev.twitter.com/docs/auth, setup your APP to get the consumerKey and consumerSecret
#Then run get_access_token which is in the python-twitter folder to get the accessTokenKey and accessTokenSecret

#This section creates a twitter api object
username = '<YOUR TWITTER USERNAME GOES HERE>'
consumerKey = '<YOUR TWITTER APP CONSUMER KEY GOES HERE>'
consumerSecret = '<YOUR TWITTER APP CONSUMER SECRET GOES HERE>'
accessTokenKey = '<YOUR TWITTER APP ACCESS TOKEN GORS HERE>'
accessTokenSecret = '<YOUR TWITTER APP ACCESS TOKEN SECRET GOES HERE>'
api = twitter.Api(consumer_key = consumerKey, consumer_secret = consumerSecret, access_token_key = accessTokenKey, access_token_secret = accessTokenSecret)

#Get the last 20 twitter posts of the user raazgupta and store it in a list
statuses = api.GetUserTimeline(username, count = 21)

#Query the page and create some Beautiful Soup
page = urllib2.urlopen(publicProfilePage)
soup = BeautifulSoup(''.join(page))

#Find all the main entries on this page
#The main entries use the div tag - a-f-i-p-R
mainEntries = soup.findAll("div", "a-f-i-p-r")

#Only go through the last 10 entries on the G+ profile
if len(mainEntries) > 10:
	mainEntries = mainEntries[:10]
	
numUpdates = 0

#Go through each entry and collect the text and appropriate link
for entry in mainEntries:
	
	#Scrape for the main text entry and url
	textString = None
	urlString = None
	urlFoundInText = False
	
	#In case it is a shared post, the user text is not in a-b-f-i-p-R. Why Google!!! :)
	#So first check for another class a-b-f-i-u-ki a-f-i-u-ki
	#If it exists then print that as user text, else look in a-b-f-i-p-R

	textEntry = entry.find("div", "a-b-f-i-u-ki a-f-i-u-ki")
	if textEntry != None and textEntry.div.string != None and len(textEntry.div.string) > 0 :
		textString = textEntry.div.string
	else:
		textEntry = entry.find("div", "a-b-f-i-p-R")
		if textEntry != None:
			textString = textEntry.next.string
			#Check if url present
			textUrl = textEntry.find("a")
			if textUrl != None:
				longUrl = textUrl["href"]
				urlShorten = shorten_url.ShortenURL()
				urlString = urlShorten.Shorten(longUrl)
				urlFoundInText = True
	
	if urlFoundInText == False:
		linkEntry = entry.find("div", "a-b-f-S-oa")
		if linkEntry != None:
			aEntry = linkEntry.find("a")
			if aEntry != None:
				longUrl = aEntry["href"]
				urlShorten = shorten_url.ShortenURL()
				urlString = urlShorten.Shorten(longUrl)
	
	if textString != None:
		textString = textString.strip()
	
	#Start building twitter post
	# #fb tells the post to be picked up by Facebook. Using an App on Facebook
	# called Selective Tweets. Works like a real charm actually. 
	# Whoeever developed that is AWESOME!
	twitterPost = "#fb"
	if urlString != None:
		twitterPost = urlString + " " + twitterPost
		
	#As twitter only allows 140 characters, find the number of remaining 
	#characters and post text or link to original G+ post accordingly
	
	remChars = 140 - len(twitterPost)
	if textString != None:
		if len(textString) <= remChars:
			twitterPost = textString + " " + twitterPost
		else:
			#Shorten the G+ profile link and post that along with as many
			#characters possible with ...
			gShort = shorten_url.ShortenURL()
			gShortString = gShort.Shorten(publicProfilePage)
			
			#Add to the twitter post
			twitterPost = gShortString + " " + twitterPost
			
			#Find the number of remaining characters for text and ...
			remCharsText = 140 - len(twitterPost) - 4
			#Add the text and ...
			twitterPost = textString[:remCharsText] + "... " + twitterPost
	
	print twitterPost, len(twitterPost)
	
	#Go through the 20 twitter posts and check if Google+ entry is found
	statusFound = False 
	for status in statuses:
		if status.text == twitterPost:
			statusFound = True
	
	#If status is not found on Twitter then post the G+ status on twitter
	if statusFound == False:
		status = api.PostUpdate(twitterPost)
		print "Updating status on twitter"
		numUpdates = numUpdates + 1
	else:
		print "Status found on Twitter"
	
	print 
	
print "Updated " + str(numUpdates) + " entries on Twitter and Facebook"