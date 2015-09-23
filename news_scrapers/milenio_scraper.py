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



def milenio_scraper():

	rss_page = urlopen('http://www.milenio.com/rss-milenio.html').read()
	rss_page_htmlel = html.fromstring(rss_page)

	rss_section_sel = CSSSelector('table.canalesRSS')

	rss_names_sel = CSSSelector('td:nth-child(2)')
	rss_links_sel = CSSSelector('td~ td+ td a')

	rss_section_match = rss_section_sel(rss_page_htmlel)

	rss_section_html = html.fromstring( html.tostring(rss_section_match[0]) )

	i=0
	count = 0
	db = MyDatabase()
	rss_sections = []
	rss_links = []
	for rss_section in rss_names_sel(rss_section_html):
		rss_sections.append( rss_section.text )

	for rss_link in rss_links_sel(rss_section_html):
		rss_links.append(rss_link.text)
		readable_section = rss_sections[i]

		#doc = etree.parse(rss_link.text)
		doc = feedparser.parse(rss_link.text)
		#channel = doc.find("channel")
		#items = channel.findall("item")
		rss_items = doc["items"]

		for rss_item in rss_items:

			readable_url = rss_item["link"]
			readable_pubDate = unicode(rss_item["published"])
			readable_title = unicode(rss_item["title"])

			tinyLink = tinyurl.create_one(str(readable_url))
			query_a = "SELECT count(1) from milenio_articles WHERE url='"+str(readable_url)+"'"
			query_link = "SELECT count(1) from milenio_noarticle_lnks WHERE link='"+tinyLink+"'"

			rl =db.query(query_link)
			rl = rl[0]['count(1)']
			ra = db.query(query_a)
			ra = ra[0]['count(1)']



			if readable_url and not ra and not rl:
				count+=1

				readingError = False

				docHtml = urllib.urlopen(readable_url).read()
				#using the lxml function html
				tree = html.fromstring(docHtml)

				article_sel = CSSSelector('#folding div.mce-body.mce')
				city_sel = CSSSelector('p.pg-bkn-location small')

				try:

					article_paragraphs = article_sel(tree)
					city_p = city_sel(tree)

					article_p1 = city_p[0].text
					readable_city = article_p1.encode("utf-8")

					readable_article = ""
					for x in article_paragraphs:
						 readable_article += x.text_content()


					#city_match = re.search('([\w\s\/áéíóúüñçåÁÉÍÓÚÜÑÇÐ\-]+\._)',city_p)

					#readable_city = city_match.group(0)
					#readable_city = readable_city[:-2]

					readable_url = unicode(readable_url)

				except:
					print "Url no good: "+readable_url
					readingError = True
					count -=1

					tinyLink = tinyurl.create_one(str(readable_url))
					query_noarticle = "INSERT into milenio_noarticle_lnks VALUES (%s)"
					params = (tinyLink)
					db.insert_row(query_noarticle, params)


				if not readingError and readable_title and readable_url and readable_article:
					query_article = """INSERT into milenio_articles VALUES (%s,%s,now(),%s,%s,%s,%s,%s,%s)"""
					params = (None,
							readable_url.encode("utf-8"),
							readable_title.encode("utf-8"),
							readable_pubDate.encode("utf-8"),
							readable_city,
							readable_article,
							None,
							readable_section.encode("utf-8"))
					db.insert_row(query_article, params)
					print str(count)+") "+readable_url

		i+=1

	print "Milenio finished! "+str(count)+"""items scraped!"""
