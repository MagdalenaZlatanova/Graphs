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
            friendliness_A.put((friendliness_nodes[node],node))
        else:
            friendliness_nodes[node]=calculate_friendliness(node,adj_list[node],B)
            friendliness_B.put((friendliness_nodes[node],node))

def swap_two_worst_ones():
    #find the worst nodes in each section
    worst_A = friendliness_A.get()
    while (True):
        #if indeed everything is up to date with your node, proceed
        if (worst_A[1] in A and friendliness_nodes[worst_A[1] ]== worst_A[0]):
            break
        worst_A=friendliness_A.get()

    worst_B = friendliness_B.get()
    while (True):
        #if indeed everything is up to date with your node, proceed
        if (worst_B[1] in B and friendliness_nodes[worst_B[1]] == worst_B[0]):
            break
        worst_B=friendliness_B.get()

    node_A=worst_A[1]
    node_B=worst_B[1]

    #do the swapping of the nodes
    A.remove(node_A)
    B.remove(node_B)
    A.add(node_B)
    B.add(node_A)
    #update swapped nodes friendliness
    friendliness_nodes[node_A]=calculate_friendliness(node_A,adj_list[node_A],B)
    friendliness_B.put((friendliness_nodes[node_A],node_A))
    friendliness_nodes[node_B]=calculate_friendliness(node_B,adj_list[node_B],A)
    friendliness_A.put((friendliness_nodes[node_B],node_B))
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
    friendliness_A=PriorityQueue()
    friendliness_B=PriorityQueue()

    #just to store the neighbourhoods of the nodes
    adj_list=dict()

    for node in er.adjacency():
        if(node[0] in A):
            node_belongs_to=A
        else:
            node_belongs_to=B

        neighbourhood=list(node[1].keys())
        adj_list[node[0]]=neighbourhood
        friendliness=calculate_friendliness(node[0],neighbourhood,node_belongs_to)

        if(node[0] in A):
            friendliness_A.put((friendliness, node[0]))
        else:
            friendliness_B.put((friendliness, node[0]))
        friendliness_nodes[node[0]]=friendliness

    progress_list=[]
    num_iterations=100
    for i in range (0,num_iterations):
        progress_list.append(sum(friendliness_nodes.values()))
        swap_two_worst_ones()

    plt.plot([i for i in range (0, num_iterations)], progress_list)
    plt.xlabel=('iteration number')
    plt.ylabel=('total frienliness')
    plt.show()

    print(friendliness_nodes)