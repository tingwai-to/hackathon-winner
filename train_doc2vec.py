import json

import os

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.externals import joblib

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.utils import shuffle
import numpy as np

tfidf = TfidfVectorizer(max_df=0.2, min_df=10, binary=True)
lc = LogisticRegression(C=0.1)
# lc = SVC(probability=True)
pipeline = make_pipeline(lc)

project_dir = 'projects'

limit = 9000

documents = []
y = []
n_winners = 0
n_losers = 0

analyze = CountVectorizer().build_analyzer()

for fname in os.listdir(project_dir):
    if n_winners >= limit and n_losers >= limit:
        break
    path = os.path.join(project_dir, fname)
    with open(path, 'r') as f:
        js = json.load(f)

    text = js['details_text'].strip()
    words = analyze(text)
    tags = [len(y)]
    document = TaggedDocument(words, tags)

    if js['is_winner']:
        if n_winners < limit:
            documents.append(document)
            y.append(1)
            n_winners += 1
    else:
        if n_losers < limit:
            documents.append(document)
            y.append(0)
            n_losers += 1
print(n_winners, n_losers)

documents, y = shuffle(documents, y)
doc2vec = Doc2Vec(documents)
X = np.array(doc2vec.docvecs)

print('cv scores', cross_val_score(MLPClassifier(), X, y, n_jobs=-1))
# pipeline.fit(X, y)
# joblib.dump(pipeline, 'model.pkl')
