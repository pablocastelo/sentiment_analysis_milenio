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


	
	 
class MyDatabase:

    host = 'localhost'
    user = 'news'
    password = 'db'
    db = 'newsdb'

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
        
        
        
def jornada_scraper():
	
	count = 0
	db = MyDatabase()
	rss_links = (
		'http://www.jornada.unam.mx/rss/edicion.xml',
		'http://www.jornada.unam.mx/rss/opinion.xml',
		'http://www.jornada.unam.mx/rss/politica.xml',
		'http://www.jornada.unam.mx/rss/economia.xml',
		'http://www.jornada.unam.mx/rss/mundo.xml',
		'http://www.jornada.unam.mx/rss/estados.xml',
		'http://www.jornada.unam.mx/rss/capital.xml',
		'http://www.jornada.unam.mx/rss/sociedad.xml',
		'http://www.jornada.unam.mx/rss/ciencias.xml',
		'http://www.jornada.unam.mx/rss/cultura.xml',
		'http://www.jornada.unam.mx/rss/gastronomia.xml',
		'http://www.jornada.unam.mx/rss/espectaculos.xml',
		'http://www.jornada.unam.mx/rss/deportes.xml',
		'http://www.jornada.unam.mx/rss/cartones.xml'
	)
	for rss_l in rss_links:
		doc = etree.parse(rss_l)
		channel = doc.find("channel")
		items = channel.findall("item")

		for pub_item in items:
			readable_url = pub_item.findtext("link")
			readable_pubDate = unicode(pub_item.findtext("pubDate"))
			readable_title = unicode(pub_item.findtext("title"))
			
			
			tinyLink = tinyurl.create_one(str(readable_url))
			query_a = "SELECT count(1) from jornada_articles WHERE url='"+str(readable_url)+"'" 
			query_link = "SELECT count(1) from jornada_noarticle_lnks WHERE link='"+tinyLink+"'"

			rl =db.query(query_link)
			rl = rl[0]['count(1)'] 
			ra = db.query(query_a)
			ra = ra[0]['count(1)']

			
			
			if readable_url and not rl and not ra:
				count+=1
			
				readingError = False
				
				docHtml = urllib.urlopen(readable_url).read()
				#using the lxml function html
				tree = html.fromstring(docHtml)
				
				citydate_sel = CSSSelector('#article-text div.col.col1 p.s-s')
				newsArticle_sel = CSSSelector('#article-cont')
				newsSection_sel = CSSSelector('div.spritemenu.selected')
				
				try:
					
					citydate = citydate_sel(tree)
					newsArticle = newsArticle_sel(tree)
					newsSection = newsSection_sel(tree)
					
					if citydate:
						city_p = citydate[0].text
						if len(city_p) < 50:
							city_match = re.search('([^,]+)',city_p)
							readable_city = city_match.group(0)
						else:
							readable_city = "none"
					else:
							readable_city = "none"
					
						
					readable_section = newsSection[0].text
					readable_section = readable_section.encode('utf-8')
					
					readable_article = ""
					for x in newsArticle:
						 readable_article += x.text_content()
						 
					 
					readable_url = unicode(readable_url)
					
				except:
					print "Url no good: "+readable_url
					readingError = True
					count -=1
					
					tinyLink = tinyurl.create_one(str(readable_url))		
					query_noarticle = "INSERT into jornada_noarticle_lnks VALUES (%s)"
					params = (tinyLink)
					db.insert_row(query_noarticle, params)
					

				if not readingError and readable_title and readable_url and readable_article:
					query_article = """INSERT into jornada_articles VALUES (%s,%s,now(),%s,%s,%s,%s,%s,%s)"""
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
	
	
	

	





