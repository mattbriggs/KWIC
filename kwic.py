''' KWIC (Keyword in context)
    Matt Briggs
    v.0.1 2019.5.9
'''

import csv
import json
import common_utilities as DR


def main():
    print("Starting")
    config_file = open("config.json")
    config_str = config_file.read()
    config = json.loads(config_str)
    path_in = config["repoinput"]
    path_out = config["reportoutput"]
    entity_extraction = path_out + "entity_extraction.csv"
    print(entity_extraction)
    readit = open(entity_extraction)
    readit = csv.reader(readit)
    wordlist = []
    for i in readit:
        wordlist.append(i[3])
    worduniques = set(wordlist)
    repo_lines = [["URL", "lineno", "line"]]
    files = DR.get_files(path_in)
    for f in files:
        with open(f, "rt") as parsefile:
            try:
                for indx, oneline in enumerate(parsefile):
                    file_path = f
                    repo_lines.append([file_path, indx+1, oneline])
            except Exception as e:
                print(e)
    kwic = [["word", "URL", "lineno", "line"]]
    for w in worduniques:
        print("Word from {}".format(w))
        for l in repo_lines:
            if w.lower() in l[2].lower():
                kwic.append([w, l[0], l[1], l[2]])
    reportname = path_out + "kwic_new.csv"
    DR.write_csv(kwic,reportname)
    print("Completed processing.")


if __name__ == "__main__":
    main()