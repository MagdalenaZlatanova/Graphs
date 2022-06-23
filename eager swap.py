import networkx as nx
import numpy as np
import random
from queue import PriorityQueue
import matplotlib.pyplot as plt
size_of_graph=100
def update_neighbourhood(node_neighbourhood):

    #method to update the neighbourhoods of the the nodes that were swapped
    for node in node_neighbourhood:
        if node in A:
            friendliness_nodes[node]=calculate_friendliness(node,adj_list[node],A)
            if(friendliness_nodes[node]<0):
                unfriendly_A.add(node)
        else:
            friendliness_nodes[node]=calculate_friendliness(node,adj_list[node],B)
            if(friendliness_nodes[node]<0):
                unfriendly_B.add(node)

def swap_two_worst_ones():

    #get a dissasortative element from each A and B
    node_A=unfriendly_A.pop()
    node_B=unfriendly_B.pop()

    #do the swapping of the nodes
    A.remove(node_A)
    B.remove(node_B)
    A.add(node_B)
    B.add(node_A)

    #update swapped nodes friendliness
    friendliness_nodes[node_A]=calculate_friendliness(node_A,adj_list[node_A],B)
    if(friendliness_nodes[node_A]<0):
        unfriendly_B.add(node_A)
    friendliness_nodes[node_B]=calculate_friendliness(node_B,adj_list[node_B],A)
    if(friendliness_nodes[node_B]<0):
        unfriendly_A.add(node_B)

    #update neighbourhoods of swapped nodes
    update_neighbourhood(adj_list[node_A])
    update_neighbourhood(adj_list[node_B])

def difference(a):
    #method returns complement of a set
    U=set([i for i in range(0,size_of_graph)])
    return U-a

def calculate_friendliness(node, neighborhood, belongs_to):

    friendliness=0
    #iterate over all neighbors of the node and if they are in the same section increase friendliness, else decrease
    for neighbor in neighborhood:
        if neighbor in belongs_to:
            friendliness=friendliness+1
        else:
            friendliness=friendliness-1
    return friendliness


if __name__ == '__main__':
    # init the er graph
    er = nx.erdos_renyi_graph(size_of_graph, 0.5)

    #randomly select A
    A=set(random.sample(er.nodes,int(size_of_graph/2)))

    #assign the rest to B
    B=difference(A)

    #calculate friendliness
    #this is our most up to date place to look up friendliness
    friendliness_nodes=dict()

    """keep the friendliness of the the nodes in a min priority queue so it is easy to retrieve them
    friendliness_A and frienliness_B will also contain not up-to-date values, but everytime i pop from them I also check with the
    friendliness_nodes dict and the corresponding sets to check validity
    """
    unfriendly_A=set()
    unfriendly_B=set()

    #just to store the neighbourhoods of the nodes
    adj_list=dict()

    #calculate the initail friendliness
    for node in er.adjacency():
        if(node[0] in A):
            node_belongs_to=A
        else:
            node_belongs_to=B

        neighbourhood=list(node[1].keys())
        adj_list[node[0]]=neighbourhood
        friendliness=calculate_friendliness(node[0],neighbourhood,node_belongs_to)

        #if it is unfriendly, add it to the appropriate set, so that maybe in the future you can choose to swap it
        if(friendliness<0):
            if(node[0] in A):
                unfriendly_A.add(node[0])
            else:
                unfriendly_B.add(node[0])

        friendliness_nodes[node[0]]=friendliness

    progress_list=[]
    num_iterations=100000
    for i in range (0,num_iterations):
        progress_list.append(sum(friendliness_nodes.values()))
        swap_two_worst_ones()

    plt.plot([i for i in range (0, num_iterations)], progress_list)
    plt.xlabel=('iteration number')
    plt.ylabel=('total frienliness')
    plt.show()

    print(friendliness_nodes)