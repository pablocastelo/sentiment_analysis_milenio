## Credits to these guys:
# Peter Prettenhofer <peter.prettenhofer@gmail.com>
# Olivier Grisel <olivier.grisel@ensta.org>
# Mathieu Blondel <mathieu@mblondel.org>
# Lars Buitinck <L.J.Buitinck@uva.nl>
# License: BSD 3 clause


from __future__ import print_function

import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time
import pylab as pl
import csv
import chardet

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.utils.extmath import density
from sklearn import metrics

import MySQLdb
from sklearn.cross_validation import train_test_split


###############################################################################
# Load some categories from the training set


categories = [
    'g',
    'b',
    'n',
]



##### Load data from MySQL

connection = MySQLdb.connect (host = 'newsdb.quody.co', user = 'news1',
                              passwd = 'db', db = 'newsdb')

cursor = connection.cursor ()
cursor.execute ("SELECT title, sentimient FROM milenio_articles_nd3;")

data = cursor.fetchall()

cursor.close()
connection.close()

cols = zip(*data ) # return a list of each column
                      # ( the * unpacks the 1st level of the tuple )
outlist = []

for col in cols:

    arr = np.asarray( col )

    type = arr.dtype

    if str(type)[0:2] == '|S':
        # it's a string array!
        outlist.append( arr )
    else:
        outlist.append( np.asarray(arr, numpy.float32) )


print(outlist)

result = chardet.detect(outlist)
charenc = result['encoding']

print('Data loaded')

###### Split data to get train and test sets

print("Splitting dataset...")

data_train, data_test = train_test_split(outlist, test_size=0.3, random_state=42)

print("Done")

# I think this is not necessary
#categories = data_train.target_names    # for case categories == None

# split target from txt
#data_train_data, y_train = zip(*data_train)
#data_test_data, y_test = zip(*data_test)



def size_mb(docs):
    return sum(len(s.encode('utf-8')) for s in docs) / 1e6

data_train_size_mb = size_mb(data_train_data)
data_test_size_mb = size_mb(data_test_data)

print("%d documents - %0.3fMB (training set)" % (
    len(data_train_data), data_train_size_mb))
print("%d documents - %0.3fMB (test set)" % (
    len(data_test_data), data_test_size_mb))
print("%d categories" % len(categories))
print()
