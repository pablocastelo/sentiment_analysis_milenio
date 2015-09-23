## Credits to these guys:
# Peter Prettenhofer <peter.prettenhofer@gmail.com>
# Olivier Grisel <olivier.grisel@ensta.org>
# Mathieu Blondel <mathieu@mblondel.org>
# License: BSD 3 clause

from __future__ import print_function

from pprint import pprint
from time import time
import logging
import numpy as np
import csv

from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

import MySQLdb
from sklearn.cross_validation import train_test_split

print(__doc__)

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


###############################################################################
# Load some categories from the training set
categories = [
    'g',
    'b',
    'n',
]
# Uncomment the following to do the analysis on all the categories
#categories = None

stopwordsESf = open('commonwordsES.csv', 'rU')
reader = csv.reader(stopwordsESf, dialect=csv.excel_tab)
stopwordsES = [row for row in reader]
stopwordsES = map(list, zip(*stopwordsES))[0]

print("Loading data:")
print(categories)

connection = MySQLdb.connect (host = '', user = '', passwd = '', db = '')

cursor = connection.cursor ()
cursor.execute ("SELECT article, sentimient FROM milenio_articles_nd3;")

data = cursor.fetchall()
data = list(data)

cursor.close ()
connection.close ()

print('Data loaded')

###### Split data to get train and test sets

print("Splitting dataset...")

data_train, data_test = train_test_split(data, test_size=0.3, random_state=42)

print("Done")

# I think this is not necessary
#categories = data_train.target_names    # for case categories == None

# split target from txt
data_train_data, y_train = zip(*data_train)
data_test_data, y_test = zip(*data_test)

data_train_data = np.asarray(data_train_data)
y_train = np.asarray(y_train)

#print(data_train_data)
#print()
#print(y_train)

###############################################################################
# define a pipeline combining a text feature extractor with a simple
# classifier

"""
	clf__alpha: 0.0001
	clf__loss: 'hinge'
	clf__n_iter: 10
	clf__penalty: 'elasticnet'
	clf__power_t: 0.5
	tfidf__norm: 'l2'
	tfidf__use_idf: True
	vect__max_df: 0.7
	vect__max_features: 10000
	vect__ngram_range: (1, 3)
	vect__stop_words: None

"""


# Vectorizer
vectorizer = TfidfVectorizer(max_df=0.7, ngram_range=(1,3), max_features=10000,
                               decode_error='ignore', stop_words=None,
                               use_idf=True, norm='l2')
X_train = vectorizer.fit_transform(data_train_data)

X_test = vectorizer.transform(data_test_data)



feature_names = np.asarray(vectorizer.get_feature_names())


#Building the model

clf = SGDClassifier(alpha=0.0001, class_weight=None, epsilon=0.1, eta0=0.0,
                    fit_intercept=True, l1_ratio=0.15, learning_rate='optimal',
                    loss='hinge', n_iter=50, n_jobs=1, penalty='elasticnet', power_t=0.5,
                    random_state=None, shuffle=False, verbose=0, warm_start=False)

clf.fit(X_train, y_train)

t0 = time()
clf.fit(X_train, y_train)
train_time = time() - t0
print("train time: %0.3fs" % train_time)

t0 = time()
pred = clf.predict(X_test)
test_time = time() - t0
print("test time:  %0.3fs" % test_time)

score = metrics.f1_score(y_test, pred)
print("f1-score:   %0.3f" % score)

print("dimensionality: %d" % clf.coef_.shape[1])
print("density: %f" % density(clf.coef_))

print("top 10 keywords per class:")
for i, category in enumerate(categories):
    top10 = np.argsort(clf.coef_[i])[-20:]
    print("%s: %s"
          % (category, ", ".join(feature_names[top10])))
