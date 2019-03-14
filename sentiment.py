import pickle
import random
from statistics import mode

import nltk
from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.svm import SVC, LinearSVC

from vote_classifier import VoteClassifier


classifiers = {
    "NLTK Naive Bayes": "data/pickles/original_naive_bayes.pickle",
    "Multinomial Naive Bayes": "data/pickles/multinomial_naive_bayes.pickle",
    "Bernoulli Naive Bayes": "data/pickles/bernoulli_naive_bayes.pickle",
    "Logistic Regression": "data/pickles/logistic_regression.pickle",
    "LinearSVC": "data/pickles/linear_svc.pickle",
    "SVC": "data/pickles/svc.pickle",
    "SGDClassifier": "data/pickles/sgd.pickle"
}

trained_classifiers = []
for classifier in classifiers.values():
    with open(classifier, "rb") as fh:
        trained_classifiers.append(pickle.load(fh))

voted_classifier = VoteClassifier(*trained_classifiers)

word_features5k_f = open("pickles/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


def find_features(document: str, features: list):
    """The feature finding function, using tokenizing by word in the document.

    Arguments:
        document {str} -- Document
        features {list} -- List of features

    Returns:
        [type] -- [description]
    """

    words = word_tokenize(document)
    _features = {w: (w in words) for w in features}
    return _features


def sentiment(text):
    """Sentiment function.

    Arguments:
        text {str} -- Tweet string.

    Returns:
        str -- sentiment mode (pos or neg)
        int -- confidence
    """

    feats = find_features(text, word_features)
    return voted_classifier.sentiment(feats)
