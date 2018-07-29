# Sentiment-Analysis
Sentiment Analysis on Twitter Tweets using NLP library TextBlob.

# The Approach
The tasks performed in this project are as following:
```
◆ Stream twitter tweets into MongoDB </br>
◆ Analyze the tweets saved in mongoDb </br>
◆ Save the result into a csv file</br>
```

# Development Guide
Install MongoDb : https://www.mongodb.com/download-center </br>
( incoming tweets are stored in mongodb as part of the requirement )</br>

All the python dependencies can be installed using pip. Just use the following command from the root directory of the project. </br>

Install the requirements. pip install -r requirements.txt</br>
Add your ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET inside twitterKeys.py file.</br>
Run the code by executing the file tweets.py</br>
The tweets with currresponding result will be stored on out.csv file</br>
