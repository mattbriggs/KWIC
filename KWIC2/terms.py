''' Extract terms from a document.

    This script will parse a markdown document. It will extract noun
    entities with more than one word from each markdown topic.

    1. Call `get_top_fifty(inpath, False)`
    2. Output will output a dict object with the following attributes:
    - Count. Number of words in the topic.
    - Keyword: the keyword entity. Default is to find 2 or more word phrases.
    - Page: filepath to the file.

    Note: stoplist.py contains a list of strings to remove from the parse.

    Matt Briggs V1.3: 5.25.2021
'''

import nltk
import pandas as pd

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
    '''With a list of characters strips them from the text.'''
    glyphs = '[]|<>*=@_+Â/~'
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
    '''Iterate over the list to remove stop items from the stoplist.py'''
    stoplist = SP.stoplist.split("\n")
    outlist = []
    for i in inlist:
        if i not in stoplist:
            outlist.append(i)
    return outlist


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
    '''Takes a list with strings and removes single items.'''
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




def extract_entities(bodytext, single=False):
    '''Take a multisentence text and return a list of unique entities.
    Can set a value 'single' to collect single entities as well.'''
    remove_list = SP.stoplist.split("\n")
    for i in remove_list:
        bodytext = bodytext.replace(i, "")
    breakdown = parse_sentences(bodytext)
    entities = []
    for sent in breakdown:
        for i in extract_chunks(sent):
            entities.append(i)
    step1_entities = clean_keyword(entities)
    step2_entities = remove_blank(step1_entities)
    step3_entities = set(step2_entities) # remove duplicates
    if single:
        step4_entities = step3_entities
    else:
        step4_entities = only_word_pairs(list(step3_entities))
    return step4_entities


def get_top_fifty(bodytext, path, single=False):
    '''With a text string return the top 50 frequency ranked
    keywords in the file as a dictionary.'''
    wordcount = len(bodytext.replace("\n", "").split())
    if wordcount == 0:
        wordcount = 1
    try:
        record_terms = extract_entities(bodytext, single)
        pagedata = {"count" : [], "keyword" : [], "page" : []}
        for term in record_terms:
            pagedata["count"].append(bodytext.count(term))
            pagedata["keyword"].append(term)
            pagedata["page"].append(path)
        term_df_full = pd.DataFrame(pagedata).sort_values(by=["count"], ascending=False).reset_index()
        term_summary = term_df_full.loc[0:49].to_dict()
        term_out = {}
        count = 0
        for i in term_summary['index']:
            freq = int(term_summary['count'][i])/wordcount
            count += 1
            record = {}
            record['rank'] = i + 1
            record['frequency'] = f"{freq:.6f}"
            record['keyword'] = term_summary['keyword'][i]
            record['page'] = term_summary['page'][i]
            term_out[count] = record
    except Exception as e:
        term_out = {1: {"error": "Unable to process file.", "message": str(e)}}
    return term_out


def main():
    '''This will run if this script attempt to run.'''
    print("This is the script that contains the functional logic.")

if __name__ == "__main__":
    main()
