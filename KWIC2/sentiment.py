
''' Senitment (With lines in the KWIC assess sentiment.)
    Matt Briggs
    v.0.1 2020.10.10
'''

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import common_utilities as  CU

def get_sentiment(instring):
    '''Take in a natural langauge string and return a sentiment dictionary with the
    following schema: {'neg': 0.0, 'neu': 0.308, 'pos': 0.692, 'compound': 0.6697}.'''
    sentimentalizer = SentimentIntensityAnalyzer()
    score = sentimentalizer.polarity_scores(instring)
    return score


def main():
    '''Load KWIC and then get the sentiment for each line.'''
    print("Starting")

if __name__ == "__main__":
    main()
