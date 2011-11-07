import feedparser
eztv_rss_link = "http://www.ezrss.it/feed/"

eztv = feedparser.parse(eztv_rss_link)

def shell(command):
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	output = process.communicate()[0]
	output = output.splitlines()
	return output

f = open("shows.txt")
shows = []
for line in f:
	if len(line) >1:
		line = line[:len(line)-1] # remove \n
		shows.append(line)
f.close()


infoHashes = []
f = open("infoHashes.txt")
for line in f:
	if len(line) > 1:
		line = line[:len(line)-1]
		infoHashes.append(line)
f.close()

detailed = [] 	# log detailed.txt
simple = [] 	# log simple.txt
wget = [] 	# wget.txt


def test():
	for entry in eztv.entries:
		print entry.infohash
		print "\n"


write = False
def parseShows():
	for entry in eztv.entries:
		for show in shows:
			present = False
			if show.upper() in entry.title.upper():
				for hash in infoHashes:
					if entry.infohash == hash:
						present = True
						break
				if present == False:			
					detailed.append(entry.title + " url: " + entry.link)
					simple.append(entry.title)
					wget.append(entry.link)
					infoHashes.append(entry.infohash)
					global write 
					write = True


def writeLogs():
	f = open("log/simple.txt",'r+')
	global simple
	global detailed
	global wget
	for line in f:
		if len(line) > 1:
			simple.append(line)
	for line in simple:
		f.write(line+'\n')
	f.close()
	f = open("log/detailed.txt",'r+')
	for line in f:
		if len(line) > 1:
			detailed.append(line)
	for line in detailed:
		f.write(line+'\n')
	f.close()
	f = open("log/wget.txt",'r+')
	for line in f:
		if len(line) > 1:
			wget.append(line)
	for line in wget:
		f.write(line+'\n')
	f.close()
	f = open("infoHashes.txt",'w')
	for line in infoHashes:
		f.write(line+"\n")

parseShows()
if write == True:
	print "+---------------------------------"
	print "| "+ str(len(simple)) + " New Torrents! "
	print "+---------------------------------"
	i = 1
	for l in simple:
		print " "+str(i)+".\t"+l
		i += 1
	writeLogs()
else:
	pass
	#print "no new torrents!"

