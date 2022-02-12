'''
Load the relational database with the corpus.
v.1.0.0 2022.2.10
'''

import summarize as SU
import common_utilities as CU
import sentiment as SE
import terms as TM
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

class parseCorpus():
    ''' '''
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
            except Exception as e:
                print("An error occurred trying to open {} : error: {}".format(f, e))
        
        conn = sqlite3.connect(pathtodatabase)
        cur = conn.cursor()
        cur.execute('INSERT INTO corpus (corpusid, nowords, docount) \
            VALUES ( ?, ?, ? )', ( self.corpusid, self.nowords, self.docount) )
        conn.commit()
        cur.close()
        return "Done!"

class parseContext():
    ''' '''
    def __init__(self):
        pass
    def find_matching_lines(pathtodatabase):
        '''  '''
        pass