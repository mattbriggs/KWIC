'''
Create KWIC

v. 1.0.0 2022-2-11
'''

import createdatabase as CD
import loaddatabase as LD
import loadcentrality as LC

databasefolder = "C:\\data\\20220210corpus"
corpustoassess = r"C:\git\ms\azure-stack-docs-pr\azure-stack\aks-hci"

print("Start in collecting KWIC.")

corpusmodel = CD.CorpusModel()
databasepath = corpusmodel.create(databasefolder)
parsecorpus = LD.parseCorpus()
loaddocs = parsecorpus.parse(corpustoassess, databasepath)
print(loaddocs)
loadcontext = LD.loadContext()
loadcon = loadcontext.find_matching_lines(databasepath)
print(loadcon)
getsim = LD.getSimilarity()
loadsim = getsim.get_similarity(databasepath)
print(loadsim)
loadcental = LC.createCentralnodes()
getcentrality = loadcental.load_doc_centrality(databasepath)
print(getcentrality)

print("Completed collecting KWIC.")