import sqlite3
import uuid

import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
nltk.download('popular')
import string

database = r"C:\data\20220210corpus\20222111855corpusdata.db"

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

    def get_similiarity(pathtodatabase):
        '''With the path to the corpus database get similarity of summaries.'''

        # Get summaries as a list of tuples
        conn = sqlite3.connect(pathtodatabase)
        cur = conn.cursor()
        summaries = list(cur.execute('SELECT documentid summary FROM document'))
        cur.close()

        # Get similarity score each pair
        for x in summaries:
            for y in summaries:
                if x[0] != y[0]:
                    sim = self.is_ci_token_stopword_set_match(x[1], y[1])
                    conn = sqlite3.connect(pathtodatabase)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO similiaty (simmilarityid, similitary, sourceid, targetid) \
                        VALUES ( ?, ?, ?, ?)', ( str(uuid.uuid4()), sim, x[0], y[0]) )
                    conn.commit()
                    cur.close()
