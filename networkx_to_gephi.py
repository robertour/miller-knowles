import csv
from os.path import join


def n2g(g, directory):
        
    nodeslist = []
    for key, atts in g.nodes(data=True):
        line = [key]
        line.extend (list(atts.values()))
        nodeslist.append(line)
    
    with open( join(directory,'nodes.csv'), 'w', newline='') as nodefile:
        nodewriter = csv.writer(nodefile, delimiter=',')
        firstline = ['Id']
        firstline.extend(list(atts.keys()))
        nodewriter.writerow(firstline)
        nodewriter.writerows(nodeslist)
    
    
    edgeslist = [] 
    # this should be possible to implement in the main file
    for e0, e1, atts in g.edges(data=True):
        line = [e0, e1]
        line.extend (list(atts.values()))
        edgeslist.append(line)
    
    with open( join(directory,'edges.csv'), 'w', newline='') as edgefile:   
        edgewriter = csv.writer(edgefile, delimiter=',')
        firstline = ['Source','Target']
        firstline.extend(list(atts.keys()))
        edgewriter.writerow(firstline)
        edgewriter.writerows(edgeslist)