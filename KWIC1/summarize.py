'''
Summarize
Input: 
 - Path to a directory of markdown files.
Output:
- A CSV with the path to each file and a summary of each section.
Description:
This script will collect markdown files, summarize each ones, and place it into a summary CSV.

v0.1 2019.3.26
'''

import os
import json
import csv
import re
import nltk
import heapq 

article_text = ""

def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        try:
            textout += line
        except:
            pass
    fh.close()
    return textout


def write_csv(outputlocation, inlist):
    '''Write the CSV file as output.'''
    csvout = open(outputlocation, 'w', newline="")
    csvwrite = csv.writer(csvout)
    for r in inlist:
        try:
            csvwrite.writerow(r)
        except Exception as e:
            print(e)
    csvout.close()


def get_files(inpath):
    '''With the directory path, returns a list of markdown file paths.'''
    outlist = []
    for (path, dirs, files) in os.walk(inpath):
        for filename in files:
            ext_index = filename.find(".")
            if filename[ext_index+1:] == "md":
                entry = path + "\\" + filename
                outlist.append(entry)
    return outlist


def summarize_text(intext):
    ''' '''

    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', intext)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text) 

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

def main():
    print("Summarizing...")
    config_file = open("config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    summary_new = path_out + "summary.csv"
    files = get_files(path_in)
    summaries = [["Section", "file", "summary"]]
    for f in files:
        record = []
        body_text = get_text_from_file(f)
        section = "sec-" + f[f.find("chapters//")+len("chapters//")+65:f.find(".md")]
        summary = summarize_text(body_text )
        record.append(section)
        record.append(f)
        record.append(summary)
        summaries.append(record)
    write_csv(summary_new)
    print("Done!")

if __name__ == "__main__":
    main()