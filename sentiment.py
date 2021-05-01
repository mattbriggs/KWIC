
''' Senitment (With lines in the KWIC assess sentiment.)
    Matt Briggs
    v.0.1 2020.10.10
'''

import csv
import json
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import common_utilities as DR

def get_sentiment(instring):
    '''Take in a natural langauge string and return a sentiment dictionary with the
    following schema: {'neg': 0.0, 'neu': 0.308, 'pos': 0.692, 'compound': 0.6697}.'''
    sentimentalizer = SentimentIntensityAnalyzer()
    score = sentimentalizer.polarity_scores(instring)
    return score


def main():
    '''Load KWIC and then get the sentiment for each line.'''
    print("Starting")
    config_file = open("config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_out = config["reportoutput"]
    kwic_new = path_out + "kwic_new.csv"
    readit = open(kwic_new)
    readit = csv.reader(readit)
    print(readit)
    statements = []
    kwic = []
    for i in readit:
        statements.append(i[3])
        kwic.append(i)
    sent = [["word", "Interview", "lineno", "line", "neg", "neu", "pos", "composite"]]
    for indx, w in enumerate(statements):
        if indx > 0:
            print("Reading ... {}".format(w))
            sent_dict = get_sentiment(w)
            sent.append([kwic[indx][0], kwic[indx][1], kwic[indx][2], kwic[indx][3],
                        sent_dict["neg"], sent_dict["neu"], sent_dict["pos"], sent_dict["compound"]])
    reportname = path_out + "sentiment_new.csv"
    DR.write_csv(sent, reportname)
    print("Completed processing.")


if __name__ == "__main__":
    main()
