'''
Create the relational datamodel of a corpus.
v.1.0.0 2022.2.10
'''

import os
import sqlite3

class CorpusModel():
    '''The corpus model creator creates a set of tables in a datbase for the coprus model.'''

    def __init__(self):
        pass

    def create(self, inpath):
        '''With an incoming path, create an empty sqldatabase.'''

        if os.path.isdir(inpath):
            fullpath = inpath + "\\corpusdata.db"
            try:
                sqliteConnection = sqlite3.connect(fullpath)
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                with open('C:\git\mb\KWIC\KWIC2\corpus.sql', 'r') as sqlite_file:
                    sql_script = sqlite_file.read()
                cursor.executescript(sql_script)
                print("SQLite script executed successfully")
                cursor.close()

            except sqlite3.Error as error:
                print("Error while executing sqlite script", error)
            return fullpath

        else:
            raise TypeError("Use a path to the directory.")


databasefolder = "C:\\data\\20220210corpus"
corpusmodel = CorpusModel()
databasepath = corpusmodel.create(databasefolder)