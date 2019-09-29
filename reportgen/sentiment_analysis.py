# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import pandas as pd

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Zabih/Documents/ramhacks19/MyFirstProject-af7478b67c52.json"
# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'PG&E sees $4.8B initial contribution to California wildfire fund'

df = pd.read_csv('/Users/Zabih/Documents/ramhacks19/data/QualitativeNewsData.csv')
df = df.loc[df['Symbol'] == df]
print(len(df))
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment
categories = client.analyze_entity_sentiment(document=document)

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
print(categories)