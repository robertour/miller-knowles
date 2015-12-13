import os
import networkx as nx
from matplotlib import pyplot as plt, pylab
import matplotlib.cm as cmx
import matplotlib.colors as colors

from networkx.algorithms.cluster import transitivity, average_clustering
from networkx.algorithms.shortest_paths.generic import \
    average_shortest_path_length

from variables import *
from networkx_to_gephi import *
from sortedcontainers.sortedlist import SortedList
from sortedcontainers.sorteddict import SortedDict


def get_cmaps(N, alpha=None):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    def map_index_to_rgb_color_alpha(index):
        return scalar_map.to_rgba(index, alpha)
    return [map_index_to_rgb_color, map_index_to_rgb_color_alpha]

def get_colormaps(N):
    dark_colors=('blue','red','green','purple','black','darksage',
                 'blueviolet','goldenrod','olive','firebrick')
    light_colors=('skyblue', 'orange','greenyellow', 'magenta','gray','sage',
                  'plum','gold','y','indianred')
    return (dark_colors, light_colors)

def count_coop(sn):
    coop = 0 
    for key, value in sn.g.node.items():
        if value['nst'] == COOP:
            coop += 1
    return coop


def network_structure_calculations(sn):
    g = sn.g

    _transitivity = transitivity(g)
    _average_clustering = average_clustering(g)   
    size_biggest_component = -1
    connected_components = 0
    ave_short_path_biggest = -1
    
    for sg in nx.connected_component_subgraphs(g, False):
        connected_components += 1
        if len(sg) > size_biggest_component:
            size_biggest_component = len(sg)
            ave_short_path_biggest = average_shortest_path_length(sg)
            
    return (_transitivity,_average_clustering,
            connected_components, size_biggest_component,
            ave_short_path_biggest)


def generate_gephi(sn, timedir, folder):
    gephidir = os.path.join(timedir, "gephi", str(sn.treatment), 
                            str(sn.id), folder)
    if not os.path.exists(gephidir):
        os.makedirs(gephidir)
    n2g(sn.g, gephidir)


def generate_graphs(sn, fit, timedir, stage, palette):
    
    graphdir = os.path.join(timedir, "graphs", sn.treatment, str(sn.id))
    if not os.path.exists(graphdir):
        os.makedirs(graphdir)
   
    # this one desn't seem to be very useful
#         sn.figcdf = fit.plot_cdf(color='000', linewidth=2)
#         fit.power_law.plot_cdf(color='deepskyblue', linewidth=2, 
#                                linestyle='--', ax=sn.figcdf)
#         plt.savefig('plot_cdf.eps', bbox_inches='tight')
    
    if stage == INITIAL_STAGE:
        dark = 'blue'
        light = 'lightblue'
    elif stage == FINAL_STAGE:
        dark = 'red'
        light = 'orange'
   
    # INITIAL AND FINAL INDIVIDUAL PDF 
    fig = plt.figure(PDF)
    #fig_pdf_ccdf.set_ylabel(r"$p(X)$,  $p(X\geq x)$")
    #fig_pdf_ccdf.set_xlabel(r"Node Degree")
    fig_pdf_ccdf = fit.plot_pdf(color=dark, linewidth=2)
    fit.power_law.plot_pdf(color=light, linestyle='--', ax=fig_pdf_ccdf)
    if stage == FINAL_STAGE:
        #pylab.ylim([0.000001,1])
        pylab.xlim([0,1000])
        filename = os.path.join(graphdir, sn.signature+'_pdf.eps')
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)
    
    # INITIAL OR FINAL TREATMENT PDF
    if stage == INITIAL_STAGE:
        fig = plt.figure(PDF_INITIAL)
    elif stage == FINAL_STAGE:
        fig = plt.figure(PDF_FINAL)  
    fig_pdf = fit.plot_pdf(color=palette[0][sn.rep], linewidth=1)
    fit.power_law.plot_pdf(color=palette[1][sn.rep], 
                           linestyle='--', ax=fig_pdf)
    

    
    # INITIAL AND FINAL INDIVIDUAL CCDF
    fig = plt.figure(CCDF)
    #fig_pdf_ccdf.set_ylabel(r"$p(X)$,  $p(X\geq x)$")
    #fig_pdf_ccdf.set_xlabel(r"Node Degree")
    figccdf = fit.plot_ccdf(color=dark, linewidth=2)
    fit.power_law.plot_ccdf(color=light, linestyle='--', ax=fig_pdf_ccdf)
    if stage == FINAL_STAGE:
        #pylab.ylim([0.0001,1])
        pylab.xlim([0,1000])
        filename = os.path.join(graphdir, sn.signature+'_ccdf.eps')
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)
    
    # INITIAL OR FINAL TREATMENT CCDF
    if stage == INITIAL_STAGE:
        fig = plt.figure(CCDF_INITIAL)
    elif stage == FINAL_STAGE:
        fig = plt.figure(CCDF_FINAL)
    fig_ccdf = fit.plot_ccdf(color=palette[0][sn.rep], linewidth=1)
    fit.power_law.plot_ccdf(color=palette[1][sn.rep], 
                            linestyle='--', ax=fig_ccdf)
    
    
    
    
    sd = SortedDict()
    for value in sn.degrees:
        if value in sd:
            sd[value] += 1
        else:
            sd[value] = 1
    
    degree_x = []
    freq_y = []
    for x,y in sd.items():
        degree_x.append(x)
        freq_y.append(y)

    # INITIAL AND FINAL INDIVIDUAL DFD
    fig = plt.figure(DFD)
    # plt.xlabel("Degree")
    # plt.ylabel("Frequency")
    # plt.figure(str('Log Log Plot Degree Frequencies Distribution'),figsize=(10.5,9))
    plt.loglog(degree_x,freq_y,linestyle='-', marker='', 
               color=dark)
    if stage == FINAL_STAGE:
        pylab.ylim([0,1000])
        pylab.xlim([0,1000])
        filename = os.path.join(graphdir, sn.signature+'_dfd.eps')
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)
    
    # INITIAL OR FINAL TREATMENT DFD
    if stage == INITIAL_STAGE:
        fig = plt.figure(DFD_INITIAL)
    elif stage == FINAL_STAGE:
        fig = plt.figure(DFD_FINAL)
    plt.loglog(degree_x,freq_y,linestyle='-', marker='', 
               color=palette[1][sn.rep]) 

    
    #  INITIAL AND FINAL INDIVIDUAL DR
    fig = plt.figure(DR)
    # plt.title("Degree rank plot")
    # plt.ylabel("degree")
    # plt.xlabel("rank")
    degree_sequence = sorted(sn.degrees,reverse=True)
    plt.loglog(degree_sequence,ls='-',color=dark,marker='.')
    if stage == FINAL_STAGE:
        pylab.ylim([0,1000])
        pylab.xlim([0,1000]) 
        filename = os.path.join(graphdir, sn.signature+'_dr.eps')
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)
    
    if stage == INITIAL_STAGE:
        fig = plt.figure(DR_INITIAL)
    elif stage == FINAL_STAGE:
        fig = plt.figure(DR_FINAL)
    plt.loglog(degree_sequence,ls='-',color=palette[1][sn.rep],marker='.')

    
    
    
def save_figures(sn, palette, timedir):
    graphdir = os.path.join(timedir, "graphs", str(sn.treatment))
    if not os.path.exists(graphdir):
        os.makedirs(graphdir)
    
    fig = plt.figure(PDF_INITIAL)
    pylab.ylim([0.000001,1])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "pdf_initial.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
    
    fig = plt.figure(CCDF_INITIAL)
    pylab.ylim([0.0001,1])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "ccdf_initial.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)    
    
    fig = plt.figure(DR_INITIAL)
    pylab.ylim([0,1000])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "dr_initial.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
    
    fig = plt.figure(DFD_INITIAL)
    pylab.ylim([0,1000])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "dfd_initial.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
    
    
    fig = plt.figure(PDF_FINAL)
    pylab.ylim([0.000001,1])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "pdf_final.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)    
    
    fig = plt.figure(CCDF_FINAL)
    pylab.ylim([0.0001,1])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "ccdf_final.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
        
    fig = plt.figure(DR_FINAL)
    pylab.ylim([0,1000])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "dr_final.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
    
    fig = plt.figure(DFD_FINAL)
    pylab.ylim([0,1000])
    pylab.xlim([0,1000])
    filename = os.path.join(graphdir, "dfd_final.eps")
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)        

def draw_random(sn):
    nx.draw(sn.g)
    plt.show()

    
def draw(sn):
    G=sn.g
    # find node with largest degree
    node_and_degree=G.degree()
    (largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]
    # Create ego graph of main hub
    hub_ego=nx.ego_graph(G,largest_hub)
    # Draw graph
    pos=nx.spring_layout(hub_ego)
    nx.draw(hub_ego,pos,node_color='b',node_size=50,with_labels=False)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego,pos,nodelist=[largest_hub],node_size=300,node_color='r')
    plt.savefig('ego_graph.png')
    plt.show()
    
    
    
def plot_degree_distribution(G):

    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)
    
    plt.loglog(degree_sequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")
    
    # draw graph in inset
#         plt.axes([0.45,0.45,0.45,0.45])
#         Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
#         pos=nx.spring_layout(Gcc)
#         plt.axis('off')
#         nx.draw_networkx_nodes(Gcc,pos,node_size=20)
#         nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
    
    plt.savefig("degree_histogram.png")
    plt.show()