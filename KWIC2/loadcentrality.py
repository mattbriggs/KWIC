# pip install networkx[default]
# plt.figure(figsize =(15, 15))
# nx.draw_networkx((G))
# plt.savefig("centralitygraph.png")
# deg_centrality = nx.degree_centrality(G)
# print(deg_centrality)

import networkx as nx
import matplotlib.pyplot as plt
import sqlite3

class createCentralnodes():
    ''' '''
    def __init__(self):
        pass

    def load_doc_centrality(self, pathtodabase):
        '''With a list of similar documents, find the most centrally
        similar documents using a centrality score in a the similarity network.
        Update the document table.'''

        conn = sqlite3.connect(pathtodabase)
        cur = conn.cursor()
        edges = list(cur.execute('SELECT sourceid, targetid FROM \
            similiaty WHERE similitary > 0.33'))
        cur.close()

        nodes_a = []
        for i in edges:
            nodes_a.append(i[0])
            nodes_a.append(i[1])
        nodes = list(set(nodes_a))

        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)

        for i in deg_centrality.keys():
            conn = sqlite3.connect(pathtodabase)
            cur = conn.cursor()
            sqlstring = 'UPDATE document SET centrality = "{}" WHERE \
                documentid = "{}";'.format(float(deg_centrality[i]), str(i))
            cur.execute(sqlstring)
            conn.commit()
            cur.close()
        
        return("Added centrality for documents.")