#!/usr/bin/env python
# -*- coding: UTF-8 -*-


#from nltk.corpus import stopwords

import csv
import re
import MySQLdb


def word_remover():
	
	reader = csv.reader(open('commonwordsES.csv', 'rU'), dialect=csv.excel_tab)
	REMOVE_LIST = []  
	for row in reader:
		REMOVE_LIST.append(row[0])
		

	texts = []
	db = MyDatabase()

	news_list = ["milenio_articles","jornada_articles","linea_articles","noroeste_articles","universal_articles"]
	remove = '|'.join(REMOVE_LIST)
	for article_source in news_list:
		article_query = "SELECT id,article from " + article_source
		article_resource = db.query(article_query)
		
		for article_x in article_resource:
			article_utf8 = article_x["article"]
			#print article_utf8
			regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)
			#print "***********************************"+regex.pattern
			article_out = regex.sub("", article_utf8)
			#print article_out
			article_out = article_out.encode("utf-8")
			article_out = MySQLdb.escape_string(article_out)
			query_u = "UPDATE "+article_source+" SET filtered_article=%s WHERE id=%s"
			params_u = (article_out,str(article_x["id"]))
			db.insert_row(query_u,params_u)
			


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


word_remover()
