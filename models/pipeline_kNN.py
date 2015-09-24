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

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
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

"""
print("%d documents" % len(data.filenames))
print("%d categories" % len(data.target_names))
print()
"""

#print(data_train_data)
#print()
#print(y_train)

###############################################################################
# define a pipeline combining a text feature extractor with a simple
# classifier
pipeline = Pipeline([
    ('vect', TfidfVectorizer(decode_error='ignore')),
    ('tfidf', TfidfTransformer()),
    ('clf', KNeighborsClassifier()),
])

# uncommenting more parameters will give better exploring power but will
# increase processing time in a combinatorial way
parameters = {
    'vect__max_df': (0.7, 0.85, 1.0),
    'vect__stop_words': (None, stopwordsES),
    'vect__max_features': (None, 10000, 50000),
    'vect__ngram_range': ((1, 1), (1, 2), (1,3), (1,4)),  # unigrams or bigrams
    'tfidf__use_idf': (True, False),
    'tfidf__norm': ('l1', 'l2'),
    'clf__weights': ('uniform', 'distance'),
    'clf__p': (1, 2),
    'clf__n_neighbors': (5, 10, 20),
}

if __name__ == "__main__":
    # multiprocessing requires the fork to happen in a __main__ protected
    # block

    # find the best parameters for both the feature extraction and the
    # classifier
    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    print("Performing grid search...")
    print("pipeline:", [name for name, _ in pipeline.steps])
    print("parameters:")
    pprint(parameters)
    t0 = time()
    grid_search.fit(data_train_data, y_train)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Best score: %0.3f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
    with open('out.csv','w') as out:
        csv_out=csv.writer(out)
        for row in grid_search.grid_scores_:
            csv_out.writerow(row)