'''
    KWIC (Keyword in context)
    Matt Briggs
    v.1.0.0 2022-6-11
'''

import yaml
import createdatabase as CD
import loaddatabase as LD
import loadcentrality as LC

def main():
    '''
    '''
    with open ("config.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.CLoader)

    print("Start to collecting the keyword in contact in: {}".\
    format(config["Corpustoassess"]))

    corpusmodel = CD.CorpusModel()
    databasepath = corpusmodel.create(config["Databasefolder"])
    parsecorpus = LD.parseCorpus()
    loaddocs = parsecorpus.parse(config["Corpustoassess"], databasepath)
    print(loaddocs)
    loadcontext = LD.loadContext()
    loadcon = loadcontext.find_matching_lines(databasepath)
    print(loadcon)
    getsim = LD.getSimilarity()
    loadsim = getsim.get_similarity(databasepath)
    print(loadsim)
    loadcental = LC.createCentralnodes()
    getcentrality_docs = "0" #loadcental.load_doc_centrality(databasepath)
    getcentrality_entities = loadcental.load_entity_centrality(databasepath)
    print("{} : {}".format(getcentrality_docs, getcentrality_entities))

    print("Completed collecting KWIC.")

if __name__ == "__main__":
    main()