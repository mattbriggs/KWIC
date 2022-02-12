'''
Load the relational database with the corpus.
v.1.0.0 2022.2.10
'''

import summarize as SU
import common_utilities as CU
import sentiment as SE
import terms as TM
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
nltk.download('popular')
import string
import sqlite3
import uuid

class processDocument():
    '''Class to parse a document and contains the parsed elements.'''

    def __int__(self):
        self.docid = ""
        self.path = ""
        self.wordcount = 0
        self.raw = ""
        self.summary = ""
        self.wordbag = ""
        self.lines = []
        self.entities = {}
        self.corpusid = ""


    def getcount(self, instring):
        '''With a string get the word count.'''
        wordcount = len(instring.replace("\n", "").split())
        if wordcount == 0:
            wordcount = 1
        return wordcount

    def getwordbag(self, indict):
        bag = []
        termkeys = indict.keys()
        for i in termkeys:
            bag.append(indict[i]["keyword"])
        bagset = set(bag)
        return bagset

    def parse(self, corpusid, filepath):
        '''With a filepath return the following elements:
        filepath: string
        numberofwords: interger
        Summary: string
        lines: array
        entities: array

        entity is frequency, location, name
        '''

        self.docid = str(uuid.uuid4())
        self.path = filepath
        self.raw = CU.get_text_from_file(filepath)
        self.summary = SU.summarize_text(self.raw)
        self.wordcount = self.getcount(self.raw)
        self.lines = self.raw.split("\n")
        self.entities = TM.get_top_fifty(self.raw, filepath, True)
        self.wordbag = self.getwordbag(self.entities )
        self.corpusid = corpusid

class loadDocument():
    '''Class takes a processDocument object and inserts into the database.'''
    def _init_(self):
        pass
    def load_table_document(self, pdoc, dbpath):
        '''Load the document table with a processDocument object.'''
        try:
            va = pdoc.docid
            vb = pdoc.corpusid
            vc = pdoc.path
            vd = pdoc.wordcount
            ve = pdoc.summary
            vf = str(pdoc.wordbag)

            conn = sqlite3.connect(dbpath)
            cur = conn.cursor()
            cur.execute('INSERT INTO document (documentid, corpusid, filepath, \
                nowords, summary, wordbag) VALUES ( ?, ?, ?, ?, ?, ? )', ( va, vb, vc, vd, ve, vf) )
            conn.commit()
            cur.close()
        except Exception as e:
            print("An error occurred in loadDocument/document {}".format(e))


    def load_table_entity(self, inprocessDocument, dbpath):
        """ """

        entities = inprocessDocument.entities.keys()
        for i in entities:
            try:
                va = inprocessDocument.entities[i]["keyword"]
                vb = ""
                conn = sqlite3.connect(dbpath)
                cur = conn.cursor()
                cur.execute('INSERT INTO entity (entityname, variants) \
                    VALUES ( ?, ? )', ( va, vb ) )
                conn.commit()
                cur.close()
            except Exception as e:
                print("An error occurred in loadDocument/entity {}".format(e))


    def load_table_lines(self, inprocessDocument, dbpath):
        """ """
        for c, i in enumerate(inprocessDocument.lines):
            try:
                count = c + 1
                sent = SE.get_sentiment(i)
                va = str(uuid.uuid4())
                vb = inprocessDocument.docid
                vc = count
                vd = i
                ve = sent["pos"]
                vf = sent["neu"]
                vg = sent["neg"]
                vh = sent["compound"]

                conn = sqlite3.connect(dbpath)
                cur = conn.cursor()
                cur.execute('INSERT INTO textline (lineid, documentid, lineno, \
                    linetext, possent, nuesent, negsent, compsent) \
                    VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )', ( va, vb, vc, \
                    vd, ve, vf, vg, vh ) )
                conn.commit()
                cur.close()
            except Exception as e:
                print("An error occurred in loadDocument/lines {}".format(e))
        
        return ("Done loading lines")

class parseCorpus():
    '''Entry class for the corpus processing pipeline.'''
    def __init__(self):
        self.corpusid = str(uuid.uuid4())
        self.nowords = 0
        self.docount = 0
    
    def parse(self, pathtocorpus, pathtodatabase):
        '''With the path to the corpus, get the Keywords in context and
        save to the a database.'''
        files = CU.get_files(pathtocorpus)
        for f in files:
            print("Processing: " + f)
            try:
                doc = processDocument()
                doc.parse(self.corpusid, f)
                loaddoc = loadDocument()
                loaddoc.load_table_document(doc, pathtodatabase)
                loaddoc.load_table_entity(doc, pathtodatabase)
                loaddoc.load_table_lines(doc, pathtodatabase)
                self.nowords += doc.wordcount
                self.docount += 1
            except Exception as e:
                print("An error occurred trying to open {} : error: {}".format(f, e))
        
        conn = sqlite3.connect(pathtodatabase)
        cur = conn.cursor()
        cur.execute('INSERT INTO corpus (corpusid, nowords, docount) \
            VALUES ( ?, ?, ? )', ( self.corpusid, self.nowords, self.docount) )
        conn.commit()
        cur.close()

        return ("Done parsing and loading document.")

class loadContext():
    ''' '''
    def __init__(self):
        self.created = True

    def find_matching_lines(self, pathtodatabase):
        '''  '''
        conn = sqlite3.connect(pathtodatabase)
        cur = conn.cursor()
        entities = list(cur.execute('SELECT entityname FROM entity'))
        lines = list(cur.execute('SELECT lineid, linetext FROM textline'))
        cur.close()

        try:
            size=len(entities)
            count=size
            print("Processing entities: {}".format(size))

            for e in entities:
                print("Getting {} of {} left {}".format(e[0], size, count))
                count -= 1
                for l in lines:
                    if e[0] in l[1]:
                        conn = sqlite3.connect(pathtodatabase)
                        cur = conn.cursor()
                        cur.execute('INSERT INTO context (contextid, entityname, lineid) \
                            VALUES ( ?, ?, ? )', ( str(uuid.uuid4()), e[0], l[0] ) )
                        conn.commit()
                        cur.close()

        except Exception as e:
            print("An error occurred in loadContext/lines {}".format(e))

        return "Done matching context."

class getSimilarity():
    ''' '''
    def __init__(self):
        # Get default English stopwords and extend with punctuation
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords.extend(string.punctuation)
        self.stopwords.append('')

    def tokenize(self, text):
        '''Create tokenizer and stemmer'''
        tokens = nltk.word_tokenize(text)
        return tokens

    def is_ci_token_stopword_set_match(self, a, b):
        """Check if a and b are matches using Jaccard similarity."""
        tokens_a = [token.lower().strip(string.punctuation) for token in self.tokenize(a) \
                        if token.lower().strip(string.punctuation) not in self.stopwords]
        tokens_b = [token.lower().strip(string.punctuation) for token in self.tokenize(b) \
                        if token.lower().strip(string.punctuation) not in self.stopwords]

        # Jaccard similarity
        ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))

        return ratio

    def get_similarity(self, pathtodatabase):
        '''With the path to the corpus database get similarity of summaries.'''

        # Get summaries as a list of tuples
        conn = sqlite3.connect(pathtodatabase)
        cur = conn.cursor()
        summaries = list(cur.execute('SELECT documentid, summary FROM document'))
        cur.close()

        size = len(summaries)
        count = 0

        # Get similarity score each pair
        for x in summaries:
            for y in summaries:
                count += 1
                if x[0] != y[0]:
                    print("Similarity {} of {} left {}".format(count, size-count, size))
                    sim = self.is_ci_token_stopword_set_match(x[1], y[1])
                    conn = sqlite3.connect(pathtodatabase)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO similarity (simmilarityid, \
                        similitary, sourceid, targetid) VALUES ( ?, ?, ?, ?)', \
                        ( str(uuid.uuid4()), sim, x[0], y[0]) )
                    conn.commit()
                    cur.close()

        return ("Done mapping similarities.")