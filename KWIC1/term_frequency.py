'''
Count term frequency
Input:
 - Path to a directory of files.
Output:
- A CSV with:
    - word
    - count
    - frequency (to 4 decimals)
Description:
Given a list of terms, this script will return the count for each term in order.

v0.1 2021.5.1
'''

import json
import csv
import terms as TE
import common_utilities as CU


def main():
    '''Opens the config file, grabs the entity extractions, and uses the stop
    list to filter the corpus. The length of the corpus is number of words -
    stoplist removals. And then produces a CSV.'''
    config_file = open("config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    entity_extraction = path_out + "entity_extraction.csv"

    print("Starting count...")

    files = CU.get_files(path_in)
    corpus_collected = ""
    for i in files:
        file_body = CU.get_text_from_file(i).replace("\n", " ")
        file_clean = TE.filter_text(file_body)
        corpus_collected += file_clean

    wordcount = len(corpus_collected.split(" "))

    readit = open(entity_extraction)
    readit = csv.reader(readit)
    wordlist = [["word", "count", "frequency"]]
    for i in readit:
        word = i[3]
        count = corpus_collected.count(word)
        freq = count/wordcount
        wordlist.append([word, count, "{:.4f}".format(freq)])

    reportname = path_out + "word_frequency.csv"
    print("Done.\n Saved to {}".format(reportname))

    CU.write_csv(wordlist, reportname)

if __name__ == "__main__":
    main()
