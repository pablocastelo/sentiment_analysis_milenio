#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from urllib import urlopen
from lxml.cssselect import CSSSelector
from lxml import html
from lxml import etree
from io import StringIO
from readability.readability import Document

import urllib
import lxml.etree
import re
import MySQLdb
import tinyurl
import feedparser



class MyDatabase:

    host = ''
    user = ''
    password = ''
    db = ''

    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db,use_unicode=1,charset="utf8")
        self.cursor = self.connection.cursor()

    def insert_row(self, query, params):
	    try:
		    self.cursor.execute(query, params)
		    self.connection.commit()
	    except:
		    self.connection.rollback()

    def query(self, query):
	    cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
	    cursor.execute(query)
	    return cursor.fetchall()

    def __del__(self):
        self.connection.close()



def universal_scraper():

	count = 0
	db = MyDatabase()
	rss_links = (
		'http://eluniversal.com.feedsportal.com/c/33765/f/604545/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604546/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604555/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604548/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604549/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604550/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604552/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604553/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604560/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604547/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604556/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604557/index.rss',
		'http://eluniversal.com.feedsportal.com/c/33765/f/604551/index.rss'
	)
	for rss_l in rss_links:
		#doc = etree.parse(rss_l)
		doc = feedparser.parse(rss_l)

		#channel = doc.find("channel")
		rss_items = doc["items"]

		for pub_item in rss_items:

			readable_url = pub_item["link"]
			readable_pubDate = unicode(pub_item["published"])
			readable_title = unicode(pub_item["title"])
			#readable_section = unicode(pub_item["category"])


			tinyLink = tinyurl.create_one(str(readable_url))
			query_a = "SELECT count(1) from universal_articles WHERE url='"+str(readable_url)+"'"
			query_link = "SELECT count(1) from universal_noarticle_lnks WHERE link='"+tinyLink+"'"

			rl =db.query(query_link)
			rl = rl[0]['count(1)']
			ra = db.query(query_a)
			ra = ra[0]['count(1)']

			readingError = False
			try:
				docHtml = urllib.urlopen(readable_url).read()
				tree = html.fromstring(docHtml)
			except:
				readingError = True

			if readable_url and not rl and not ra and not readingError:
				count+=1

				#using the lxml function html

				newsArticle_sel = CSSSelector('#SizeText div.PR10.txt51.color666')
				newsSection_sel = CSSSelector('div.DondeEstoy.floatL.W500')

				try:
					newsArticle = newsArticle_sel(tree)
					newsSection = newsSection_sel(tree)

					section_p = ""
					for x in newsSection:
						 section_p += x.text_content()
						 break

					section_p = section_p.encode('utf-8')
					section_split = section_p.split("&gt",2)
					readable_section = section_split[1]

					try:
						city_p = ""
						for x in newsArticle:
							 city_p += x.text_content()
							 break


						city_match = re.search('([\w\s\/\,áéíóúüñçåÁÉÍÓÚÜÑÇÐ\-]+\.\-)',city_p)

						readable_city = city_match.group(0)
						readable_city = readable_city[:-2]
					except:
						readable_city = "none"


					readable_article = ""
					for x in newsArticle:
						 readable_article += x.text_content()


					readable_url = unicode(readable_url)

				except:
					print "Url no good: "+readable_url
					readingError = True
					count -=1

					tinyLink = tinyurl.create_one(str(readable_url))
					query_noarticle = "INSERT into universal_noarticle_lnks VALUES (%s)"
					params = (tinyLink)
					db.insert_row(query_noarticle, params)


				if not readingError and readable_title and readable_url and readable_article:
					query_article = """INSERT into universal_articles VALUES (%s,%s,now(),%s,%s,%s,%s,%s,%s)"""
					params = (None,
							readable_url.encode("utf-8"),
							readable_title.encode("utf-8"),
							readable_pubDate.encode("utf-8"),
							readable_city,
							readable_article,
							None,
							readable_section)
					db.insert_row(query_article, params)
					print str(count)+") "+readable_url



	print "Finished! "+str(count)+"""items scraped!"""
