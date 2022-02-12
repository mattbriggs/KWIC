'''
Load the relational database with the corpus.
v.1.0.0 2022.2.10
'''

from lib2to3.pgen2.token import VBAR
import string
import summarize as SU
import common_utilities as CU
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
            print("An error occurred in loadDocument. {}".format(e))


    def load_table_entity(self, inprocessDocument, dbpath):

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
                print("An error occurred in inprocessDocument {}".format(e))

