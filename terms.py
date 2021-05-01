''' Extract terms from a document.

    This script will parse a markdown document. It will extract noun 
    entities with more than one word from each markdown topic.

    1. call `get_top_ten(inpath)`
    2. output a dictionary of the top ten keywords.

    Matt Briggs V1.2: 4.14.2019
'''

import os
import datetime
import nltk
import pandas as pd
from prettytable import PrettyTable

import common_utilities as  CU
import stoplist as SP


def print_dict_rank(indict):
    '''With the dict provided by the term tool, print a list for pretty print'''
    x = PrettyTable()
    print("Keyword scores for + {}\n".format(indict[1]["page"]))
    x.field_names = ["Rank", "Keyword"]
    for i in indict.keys():
        x.add_row([indict[i]["score rank"], indict[i]["keyword"]])
    x.align["Keyword"] = "l"
    print(x)


def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout


def clean_keyword(inlist):
    glyphs = '[]|<>*=@_+Â'
    outlist = []
    for i in inlist:
        for char in glyphs:
            i = i.replace(char, "")
        outlist.append(i)
    return outlist


def remove_blank(inlist):
    '''Iterate over the list to remove blank entries.'''
    noblank = []
    for i in inlist:
        x = i.strip()
        if x:
            noblank.append(x)
    return noblank

def apply_stoplist(inlist):
    '''Iterate over the list to remove stop items.'''
    stoplist = SP.stoplist.split("\n")
    outlist = []
    for i in inlist:
        if i not in stoplist:
            outlist.append(i)
    return outlist


def clear_dissallows(instring):
    '''Apply disallow list as strings to remove.'''
    dissallows = SP.stoplist.split("\n")
    outstring = instring
    for i in dissallows:
        outstring = outstring.replace("i", " ")
    return outstring


def print_dict_rank(indict):
    '''With the dict provided by the SEO rank, print a list for pretty print'''
    x = PrettyTable()
    print("Keyword scores for + {}\n".format(indict[1]["page"]))
    x.field_names = ["Rank", "Keyword"]
    for i in indict.keys():
        x.add_row([indict[i]["score rank"], indict[i]["keyword"]])
    x.align["Keyword"] = "l"
    print(x)


# Parser Functions using NLTK

def extract_chunks(sent):
    '''With a parsed sentence, return sets of entities.'''
    grammar = r"""
    NBAR:
        # Nouns and Adjectives, terminated with Nouns
        {<NN.*>*<NN.*>}

    NP:
        {<NBAR>}
        # Above, connected with in/of/etc...
        {<NBAR><IN><NBAR>}
    """
    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sent)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne


def parse_sentences(incorpus):
    '''Take a body text and return sentences in a list.'''
    sentences = nltk.sent_tokenize(incorpus)
    return sentences

def only_word_pairs(inlist):
    '''Takes an list with strings and removes single items.'''
    outlist = []
    for i in inlist:
        j = i.split()
        if len(j) > 1:
            outlist.append(i)
    return outlist


def remove_blank(inlist):
    '''Iterate over the list to remove blank entries.'''
    noblank = []
    for i in inlist:
        x = i.strip()
        if x:
            noblank.append(x)
    return noblank


def extract_entities(bodytext):
    '''Take a multisentence text and return a list of unique entities.'''
    breakdown = parse_sentences(bodytext)
    entities = []
    for sent in breakdown:
        for i in extract_chunks(sent):
            entities.append(i)
    step1_entities = clean_keyword(entities)
    step2_entities = remove_blank(step1_entities)
    step3_entities = set(step2_entities) # remove duplicates
    #step4_entities = only_word_pairs(list(step3_entities))
    #step5_entities = apply_stoplist(step3_entities )
    return step3_entities 


def filter_text(instring):
    '''Get a raw string and return a prepped string for entity extraction.'''
    prep = instring.replace("\n", " ").lower()
    stoplist = SP.stoplist.lower()
    stoplist = stoplist.split("\n")
    stopset = set(stoplist)
    list_filtered = list(filter(lambda x: x not in stopset, prep.split()))
    filtered = ""
    for i in list_filtered:
        filtered += i + " "
    return filtered.strip()


def get_top_files(path, term_count=50):
    '''With a path name to a markdown file return the indicated top terms ranked keywords in the file as a dictionary.'''
    try:
        bodytext = get_text_from_file(path)
        prep_text = filter_text(bodytext)
        record_terms = extract_entities(prep_text)
        pagedata = {"Count" : [], "Keyword" : [], "File" : []}
        for term in record_terms:
            pagedata["Count"].append(prep_text.count(term))
            pagedata["Keyword"].append(term)
            pagedata["File"].append(path)
        Term_df_full = pd.DataFrame(pagedata).sort_values(by=["Count"], ascending=False).reset_index()
        Term_summary = Term_df_full.loc[0:term_count].to_dict()
        Term_out = {}
        count = 0
        for i in Term_summary['index']:
            count += 1
            record = {}
            record['score rank'] = i + 1
            record['keyword'] = Term_summary['Keyword'][i]
            record['file'] = Term_summary['File'][i]
            Term_out[count] = record
    except Exception as e:
        Term_out = {1: {"error": "Unable to process file.", "message": str(e)}}
    return Term_out


def main():
    print("This is the script that contains the functional logic.")

if __name__ == "__main__":
    main()