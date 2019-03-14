# Election-Interference-Detection-and-Result-Prediction-Using-Twitter-and-Facebook

 Extracted and conducted sentiment analysis on tweets related to an election using extraction tools and NLTK library
 Explored Bokeh Python library to create an application which lets user input a keyword and get the prediction result
 Performed significant amount of feature engineering and developed a technique to detect any biased Ad bots and fake news used for illegal Campaigning
 
 Steps for Running this project:
Necessary python packages that need to be installed in the machine.
1.tweepy
2.mysqlclient
3.IMDbPY
4.nltk
5.textblob
6.jsonpickle
7.bokeh
8.pickleshare
9.scikit-learn
10.numpy
If these modules are not present, here is the installation guide for having all the packages in the machine.

Installation:
pip install tweepy
pip install mysqlclient
pip install IMDbPY
pip install nltk
pip install textblob
pip install jsonpickle
pip install bokeh
pip install pickleshare
pip install scikit-learn
pip install numpy

Twitter tokens that needs to be added.
Modify the properties file with your tokens to access through your tweeter.
Tokens Needed:
token:
token_secret:
consumer_key:
consumer_secret:

Steps In running the project
1. Training the classifier with the Positive and Negative list of words.
cd Project
python3.6 Train_Classifier.py
and run Tweet_stream.py



2. Database should be started:
create and install database and table using queries given below

run sentiment.py for sentiment analysis
run score_calculation and Vote_classifier respectively to get the confidence of the analysis
run testing for test data analysis

run myaap.py the bokeh file which shows graph






 Run the bokeh file.
bokeh serve --show myapp.py
this will open the browser window. 
 
