from nltk.classify import ClassifierI
from statistics import mode


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        """Voting Classifier

        Arguments:
            classifiers {ClassifierI} -- List of classifiers
        """

        self._classifiers = classifiers

    def sentiment(self, features: list):
        """Classify the sentiment and get the confidence.

        Arguments:
            features {list} -- List of features

        Returns:
            str -- positive or negative
            int -- confidence
        """

        votes = [c.classify(features) for c in self._classifiers]
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return mode(votes), conf

    def classify(self, features: list):
        """Classify the sentiment

        Arguments:
            features {list} -- List of features

        Returns:
            str -- positive or negative
        """

        votes = [c.classify(features) for c in self._classifiers]
        try:
            return mode(votes)
        except:
            return "pos"

    def confidence(self, features: list):
        """Get the confidence by talling the votes for and against the winning vote

        Arguments:
            features {list} -- List of features

        Returns:
            int -- confidence
        """
        votes = [c.classify(features) for c in self._classifiers]
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf
