# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tqdm import tqdm, tqdm_notebook
tqdm.pandas(tqdm_notebook)

df = pd.DataFrame()

# If failed to import, run
# `sed -e 's/\r/ /g' full_tweets_with_sentiment_7.csv > 7.csv` on all
for i in range(1, 8):
    print("Reading index", i)
    d = pd.read_csv(open("data/" + str(i) + ".csv", 'r'), encoding='utf-8',
                    engine='c', low_memory=False)
    df = pd.concat([d, df])
    print("File rows", len(d.index), "Total rows", len(df.index))


df['user.lang'] = df['user.lang'].astype('category')
df['user.time_zone'] = df['user.time_zone'].astype('category')
df['lang'] = df['lang'].astype('category')
df['source'] = df['source'].astype('category')
df['user.profile_background_color'] = df['user.profile_background_color'].astype(
    'category')

df['user.created_at'] = pd.to_datetime(df['user.created_at'])
df['created_at'] = pd.to_datetime(df['created_at'])

df['favorite_count'] = df['favorite_count'].apply(
    pd.to_numeric, downcast='unsigned')
df['user.listed_count'] = df['user.listed_count'].apply(
    pd.to_numeric, downcast='unsigned')

df.select_dtypes(include=['int64']).describe()  # Pick columns for improvement

df.to_pickle('data/all.pickle')  # Save the optimized object
