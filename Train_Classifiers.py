#!/usr/bin/env python3

# Training the classifiers and then pickling.
# Executing it sucks time. :P

import pickle
import random
from datetime import datetime

import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.svm import SVC, LinearSVC

from utils import info, pickling
from vote_classifier import VoteClassifier

allowed_word_types = ["J", "R", "V"]


def read_corporas(positive: str="data/corporas/positive.txt", negative: str="data/corporas/negative.txt"):
    """Read corporas

    Keyword Arguments:
        positive {str} -- Path to positive text (default: {"data/corporas/positive.txt"})
        negative {str} -- Path to negative text (default: {"data/corporas/negative.txt"})

    Returns:
        list -- documents
        list -- all words
    """

    # Defining and Accessing the corporas.
    # In total, approx 10,000 feeds to be trained and tested on.
    all_words: list = []
    documents: list = []

    info("Accessing the corporas...")

    for p in open(positive, "r"):
        p = p.strip()
        documents.append((p, "pos"))
        words = word_tokenize(p)
        pos = nltk.pos_tag(words)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())

    for p in open(negative, "r"):
        documents.append((p, "neg"))
        words = word_tokenize(p)
        pos = nltk.pos_tag(words)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())

    return documents, all_words


def get_features(all_words: list, length: int=5000):
    """Calculate the most frequent words as features

    Arguments:
        all_words {list} -- All words of the string.

    Keyword Arguments:
        length {int} -- Length of features (default: {5000})

    Returns:
        list -- features
    """

    return list(nltk.FreqDist(all_words).keys())[:length]


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


if __name__ == '__main__':
    info("Training classifiers. This may take few minutes to finish.")
    documents, all_words = read_corporas()

    info("Getting top 5000 words as features...")
    word_features = get_features(all_words)
    pickling("data/pickles/word_features5k.pickle", word_features)

    info("Tokenizing and finding features for training...")
    featuresets = [(find_features(rev, word_features), category)
                   for (rev, category) in documents]

    # Shuffling
    random.shuffle(featuresets)
    info("Length of the feature sets: " + str(len(featuresets)))

    # Partitioning the training and the testing sets.
    testing_set = featuresets[10000:]
    training_set = featuresets[:10000]

    print()
    info("Training and successive pickling of the classifiers...")
    info("This will take much time. Be patient.")

    print()
    info("Current Algorithm: " + "NLTK Original Naive Bayes")
    nb_classifier = nltk.NaiveBayesClassifier.train(training_set)
    info("Accuracy Percent:", str((nltk.classify.accuracy(
        nb_classifier, testing_set)) * 100))
    pickling("data/pickles/original_naive_bayes.pickle", nb_classifier)

    print()
    info("Current Algorithm: " + "Sklearn Multinomial Naive Bayes")
    mnb_classifier = SklearnClassifier(MultinomialNB())
    mnb_classifier.train(training_set)
    info("Accuracy Percent:", str(
        (nltk.classify.accuracy(mnb_classifier, testing_set)) * 100))
    pickling("data/pickles/multinomial_naive_bayes.pickle", mnb_classifier)

    print()
    info("Current Algorithm: " + "Sklearn Bernoulli Naive Bayes")
    bnb_classifier = SklearnClassifier(BernoulliNB())
    bnb_classifier.train(training_set)
    info("Accuracy Percent:", str(
        (nltk.classify.accuracy(bnb_classifier, testing_set)) * 100))
    pickling("data/pickles/bernoulli_naive_bayes.pickle", bnb_classifier)

    print()
    info("Current Algorithm: " + "Sklearn Logistic Regression")
    lr_classifier = SklearnClassifier(LogisticRegression())
    lr_classifier.train(training_set)
    info("Accuracy Percent:", str(
        (nltk.classify.accuracy(lr_classifier, testing_set)) * 100))
    pickling("data/pickles/logistic_regression.pickle", lr_classifier)

    print()
    info("Current Algorithm: " + "Sklearn SGD classifier")
    SGD_classifier = SklearnClassifier(SGDClassifier())
    SGD_classifier.train(training_set)
    info("Accuracy Percent:", str(
        (nltk.classify.accuracy(SGD_classifier, testing_set)) * 100))
    pickling("data/pickles/sgd.pickle", SGD_classifier)

    print()
    info("Current Algorithm: " + "Sklearn Linear SVC")
    linearSVC_classifier = SklearnClassifier(LinearSVC())
    linearSVC_classifier.train(training_set)
    info("Accuracy Percent:", str(
        (nltk.classify.accuracy(linearSVC_classifier, testing_set)) * 100))
    pickling("data/pickles/linear_svc.pickle", linearSVC_classifier)

    print()
    info("Current Algorithm: " + "Sklearn SVC")
    SVC_classifier = SklearnClassifier(SVC())
    SVC_classifier.train(training_set)
    info("Accuracy Percent:", str(
        (nltk.classify.accuracy(SVC_classifier, testing_set)) * 100))
    pickling("data/pickles/svc.pickle", SVC_classifier)

    print()
    # Voting classifier.
    info("All classifiers are trained. Evaluating the voted classifier...")
    voted_classifier = VoteClassifier(
        nb_classifier, mnb_classifier, bnb_classifier, lr_classifier, linearSVC_classifier, SGD_classifier, SVC_classifier)

    info("Accuracy percent:",
          str((nltk.classify.accuracy(voted_classifier, testing_set)) * 100))
