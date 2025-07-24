# -*- coding: utf-8 -*-
"""
Created on Sun May 07 02:20:45 2017

@author: binoy
"""

import pandas as pd
import matplotlib.pyplot as plt
from gensim import models
from gensim.models.doc2vec import TaggedDocument
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_distances
from rake_nltk import Rake
import nltk

# Optional: Download stopwords if not already done
nltk.download('stopwords')

# Read dataset
df = pd.read_csv('data.csv')
jd = df['Job Description'].tolist()
companies = df['company'].tolist()
positions = df['position'].tolist()

# Create Tagged Documents
docs = []
for i in range(len(jd)):
    sent = TaggedDocument(words=jd[i].split(), tags=['{}_{}'.format(companies[i], i)])
    docs.append(sent)

# Train Doc2Vec Model
model = models.Doc2Vec(alpha=0.025, min_alpha=0.025, min_count=1)
model.build_vocab(docs)

for epoch in range(10):
    model.train(docs, total_examples=model.corpus_count, epochs=1)
    model.alpha -= 0.002
    model.min_alpha = model.alpha

# Load resume text
with open('resumeconverted.txt', 'r', encoding='utf-8') as f:
    resume = f.read()

# Create document vectors
data = []
for i in range(len(jd)):
    data.append(model.dv[i])

data.append(model.infer_vector(resume.split()))

# 2D Visualization with MDS
mds = MDS(n_components=2, random_state=1)
pos = mds.fit_transform(data)
xs, ys = pos[:, 0], pos[:, 1]
for x, y in zip(xs, ys):
    plt.scatter(x, y)

xs2, ys2 = xs[-1], ys[-1]
plt.scatter(xs2, ys2, c='Red', marker='+')
plt.text(xs2, ys2, 'resume')
plt.savefig('distance.png')
plt.show()

# Calculate cosine distances
cos_dist = []
for i in range(len(data) - 1):
    print(i)
    dist = cosine_distances(
        [model.infer_vector(resume.split())],
        [data[i]]
    )[0][0]
    cos_dist.append(float(dist))

# ✅ Keyword Extraction using RAKE
r = Rake()
key_list = []
for j in jd:
    r.extract_keywords_from_text(j)
    key_words = r.get_ranked_phrases()
    key_list.append(" ".join(key_words))

# Create summary DataFrame
summary = pd.DataFrame({
    'Company': companies,
    'Postition': positions,
    'Cosine Distances': cos_dist,
    'Keywords': key_list,
    'Job Description': jd
})

# Sort by best match and save
z = summary.sort_values('Cosine Distances', ascending=True)  # Lower distance = better match
z.to_csv('Summary.csv', encoding="utf-8", index=False)
