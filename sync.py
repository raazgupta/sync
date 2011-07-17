import urllib2
from BeautifulSoup import BeautifulSoup

publicProfilePage = 'https://plus.google.com/107098304818057270518/posts'

page = urllib2.urlopen(publicProfilePage)
soup = BeautifulSoup(''.join(page))

#Find all the main entries on this page
#The main entries use the div tag - a-f-i-p-R
mainEntries = soup.findAll("div", "a-f-i-p-r")

print len(mainEntries)

#Go through each entry and print the text and any links
for entry in mainEntries:
	textEntry = entry.find("div", "a-b-f-i-p-R")
	if textEntry.string != None and len(textEntry.string) > 0 :
		print textEntry.string
	else:
		print "No text"	
	
	linkEntry = entry.find("div", "a-b-f-S-oa")
	if linkEntry != None:
		aEntry = linkEntry.find("a")
		if aEntry != None:
			print aEntry["href"]
	
	print 