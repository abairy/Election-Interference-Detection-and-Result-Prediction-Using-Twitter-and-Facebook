print("Loading datasets... It may take a longer time.")
from sentiment import sentiment
import pickle
import pandas as pd
import numpy as np
from multiprocessing import cpu_count, Pool
from tqdm import tqdm

print("The following result should be neg and 1.0")
print(sentiment("He is an incapable person. His projects are totally senseless."))

tqdm.pandas(tqdm)

def main(i):
    print("Reading tweet file", i)
    cs = pd.read_csv("full_tweets_" + str(i) + ".csv")
    print("Total tweets", len(cs.index))
    print("Detecting sentiment in parallel...")
    cs["sentiment"] = cs["text"].progress_apply(sentiment)
    cs.to_csv("full_tweets_with_sentiment_" + str(i) + ".csv")
    print("---------")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Calculate tweets sentiment')
    parser.add_argument("index")
    args = parser.parse_args()

    main(args.index)
