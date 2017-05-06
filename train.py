import json

import os
from sklearn.externals import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.utils import shuffle
import numpy as np

tfidf = TfidfVectorizer(max_df=0.2, min_df=10, binary=True)
lc = LogisticRegression(C=0.1)
# lc = SVC(probability=True)
pipeline = make_pipeline(tfidf, lc)

project_dir = 'projects'

limit = 9000

projects = []
y = []
n_winners = 0
n_losers = 0

for fname in os.listdir(project_dir):
    path = os.path.join(project_dir, fname)
    with open(path, 'r') as f:
        js = json.load(f)

    text = js['details_text'].strip()

    if js['is_winner']:
        if n_winners < limit:
            projects.append(text)
            y.append(1)
            n_winners += 1
    else:
        if n_losers < limit:
            projects.append(text)
            y.append(0)
            n_losers += 1

projects, y = shuffle(projects, y)

print('cv scores', cross_val_score(pipeline, projects, y, n_jobs=-1))
pipeline.fit(projects, y)
joblib.dump(pipeline, 'model.pkl')
