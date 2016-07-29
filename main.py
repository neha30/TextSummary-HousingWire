#Program for article summarization using python library pyteaser
#Summaries are created by ranking sentences in a news article according to how relevant they are to the entire text. The top 5 sentences are used to form a "summary". Each sentence is ranked by using four criteria:
#    Relevance to the title
#    Relevance to keywords in the article
#    Position of the sentence
#    Length of the sentence

#.......................................article summarization using pyteaser................................................#

import io
import sys
import os
import itertools
#from operator import itemgetter
from pyteaser import *
import urllib
from goose import Goose
#import xml.etree.ElementTree as ET

#to make default encoding 'utf-8'
reload(sys)
sys.setdefaultencoding('utf-8')


#creating object of Goose
g=Goose()

texts=list()

#open the csv file which containg the tweet og housing wire
f=open('tweets.csv','r')

#extract the 2nd column from csv file i.e. text
for line in f:
	cells=line.split(',')
	texts.append(cells[2])

f.close()

#extract the link from every tweets. Here 'url_list' will contain the final result i.e links for articles
url_list=[]
for text in texts:
	lst=text.split()
	urls=[s for s in lst if "https://" in s]

	for url in urls:
		url_list.append(url)


for i,item in enumerate(url_list):

	#url=item.find('link').text

	article=g.extract(url=item)

	#writing the article from RSSfeed in 'articles' folder
	print "writitng article to"+"articles/"+str(i)
	articlefile=io.open('articles/'+str(i),'w')
	articlefile.write(unicode(item))
	articlefile.write(unicode('\n'))
	articlefile.write(unicode(article.title))
	articlefile.write(unicode(article.cleaned_text))
	articlefile.close()


	summaries = SummarizeUrl(item)
	summaries=''.join(summaries)
    

    #writing the summaries in summaries folder
	print "generating output summary to "+"summaries/"+str(i)
	summaryfile=io.open('summaries/'+str(i),'w')
	summaryfile.write(summaries)
	summaryfile.close()

	keys=ExtractKey(item)
    #writing the keywords in keywords folder
	print "generating output keywords to "+"keywords/"+str(i)
	keyfile=io.open('keywords/'+str(i),'w')

	for key in keys:
		keyfile.write(key+'\n')
	keyfile.close()

	print "\n"

#after generating summary and keywords for every articles, we will find the similarity between the articles
#based on the number of common keywords of two articles
print "comapring files:"
keywords_file=os.listdir("keywords")
pairs=itertools.combinations(keywords_file,2)

#similarity_file=io.open('similarities.txt','a')
sys.stdout=open('similarities.txt','a')

for pair in pairs:
	print "\npair is:",pair


	fhand1=open('keywords/'+pair[0])
	key1_list=list()

	fhand2=open('keywords/'+pair[1])
	key2_list=list()

	for line in fhand1:
		key1_list.append(line.strip())

	for line in fhand2:
		key2_list.append(line.strip())

	#make all the keywords lowercase
	key1_list=[x.lower() for x in key1_list]
	key2_list=[x.lower() for x in key2_list]

	result=[val for val in key1_list if val in key2_list]
	print "result:\n",len(result)

    
    
