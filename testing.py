# Sneek peek on the results.
# Importing sentiment_mod module and then testing on some feeds and statements.

import sentiment_mod as senti

test_cases = [
    "He is an incapable person. His projects are totally senseless.",
    "This movie was awesome! The acting was great, plot was wonderful !"
    "This movie was utter junk.. I don't see what the point was at all. Horrible movie, 0/10",
    "He is a freak.",
    "Movie was nice. Actors did very well. All together a nice experience.",
    "Are you fucking mad ?",
    "You are dumb."
]

for i in test_cases:
    print("The sentiment for tweet {} is {}.".format(i, senti.sentiment(i)))
