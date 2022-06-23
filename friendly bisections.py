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
            update_friendliness_node(node,friendliness_A,A)
        else:
            update_friendliness_node(node,friendliness_B,B)

def get_worst(from_section, set):
    worst=from_section.get()
    while(True):
        #this is the least friendly up to date element, stop looking
        if(worst[1] in set and friendliness_nodes[worst[1]]==worst[0]):
            break
        worst=from_section.get()
    return worst

def get_alpha_n(alpha_n, from_section,set):
    worsts=list()
    for i in range (0, alpha_n):
        worst=get_worst(from_section,set)
        #this is not a very elegant solution, somewhere in update_friendliness the same entry is added more than once
        #correct this
        while(worst in worsts):
            worst=get_worst(from_section,set)
        worsts.append(worst)
    return worsts

def remove_from_set(nodes, from_set, to_set):
    for node in nodes:
        from_set.remove(node)
        to_set.add(node)

def update_friendliness_node(node, friendliness_queue, set):
    friendliness_nodes[node]=calculate_friendliness(node, adj_list[node],set)
    friendliness_queue.put((friendliness_nodes[node],node))

def update_friendliness(nodes,friendliness_queue, set):
    for node in nodes:
        update_friendliness_node(node, friendliness_queue,set)

def swap_two_worst_ones( alpha_n):
    #find the worst alpha_n nodes in each section
    worst_As=get_alpha_n(alpha_n,friendliness_A,A)
    worst_Bs=get_alpha_n(alpha_n,friendliness_B,B)

    #remove the least friendly from each set and add them to the other one
    remove_from_set([worst_A[1] for worst_A in worst_As],A,B)
    remove_from_set([worst_B[1] for worst_B in worst_Bs],B,A)

    #update friendliness of swapped nodes
    update_friendliness([worst_A[1] for worst_A in worst_As],friendliness_B,B)
    update_friendliness([worst_B[1] for worst_B in worst_Bs],friendliness_A,A)

    affected_nodes=set()

    #update neighbourhoods of swapped nodes
    for node_A in [worst_A[1] for worst_A in worst_As]:
        affected_nodes.add(node_A)
    for node_B in [worst_B[1] for worst_B in worst_Bs]:
        affected_nodes.add(node_B)
    update_neighbourhood(list(affected_nodes))

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
        swap_two_worst_ones(4)

    plt.plot([i for i in range (0, num_iterations)], progress_list)
    plt.xlabel=('iteration number')
    plt.ylabel=('total frienliness')
    plt.show()

    print(friendliness_nodes)