'''
Create KWIC

v. 1.0.0 2022-2-11
'''

import createdatabase as CD
import loaddatabase as LD

databasefolder = "C:\\data\\20220210corpus"
corpustoassess = r"C:\git\ms\azure-stack-docs-pr\azure-stack\aks-hci"

print("Start")

corpusmodel = CD.CorpusModel()
databasepath = corpusmodel.create(databasefolder)
parsecorpus = LD.parseCorpus()
finish = parsecorpus.parse(corpustoassess, databasepath)
print(finish)

print("End")