# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("Loading all models for sentiment calculation...")
from sentiment import sentiment as s

from tqdm import tqdm, tqdm_notebook
tqdm.pandas(tqdm_notebook)

df = pd.read_pickle("data/all.pickle")

import ast


def score(senti):
    # Since the previous sentiment calulation will save the score and category into a string, we need to eval it.
    senti = ast.literal_eval(senti)
    if senti[0] == 'neg':
        return -1 * float(senti[1])
    return float(senti[1])


# Make the score range from [-1, 1]
df['sentiment_score'] = df['sentiment'].progress_apply(score)


def category(text):
    if any(map(lambda i: i in text, trump_keywords)) and any(map(lambda i: i in text, hillary_keywords)):
        return 0
    if any(map(lambda i: i in text, trump_keywords)):
        return -1
    elif any(map(lambda i: i in text, hillary_keywords)):
        return 1
    else:
        return 0


def sentiment(text):
    sen = s(text)
    if sen[0] == 'neg':
        return -1 * float(sen[1])
    return float(sen[1])


def category_and_score(entry):  # -1 trump, 1 hillary
    '''
    Find the category of tweet string.
    '''
    text = entry['text']
    if any(map(lambda i: i in text, trump_keywords)) and any(map(lambda i: i in text, hillary_keywords)):
        if "." in text:
            split_sentenses = text.split('.')
            s = {s: category(s) * sentiment(s) for s in split_sentenses}
            score = sum(s.values())

            if not score:
                return 0
            return score / len(s)
        else:
            return 0
    else:
        return float(category(text)) * float(entry['sentiment_score'])


trump_keywords = ['trump', 'yourefired', 'republi', 'gop']
hillary_keywords = ['hillary', 'madampresident', 'democrat']


df['score'] = df.progress_apply(category_and_score, axis=1)

df['score'].describe()

trump_scores = df[df['score'] < 0.0]['score']  # trump
hillary_scores = df[df['score'] > 0.0]['score']  # hillsry
non_scores = df[df['score'] == 0]['score']  # undeciable or no preference


trump_scores.describe()
hillary_scores.describe()
non_scores.describe()


results, edges = np.histogram(trump_scores, normed=True)
binWidth = edges[1] - edges[0]
plt.bar(edges[:-1], results * binWidth, binWidth)

results, edges = np.histogram(hillary_scores, normed=True)
binWidth = edges[1] - edges[0]
plt.bar(edges[:-1], results * binWidth, binWidth)
plt.show()
