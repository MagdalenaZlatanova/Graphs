import networkx as nx
import numpy as np
import random
from queue import PriorityQueue
import matplotlib.pyplot as plt
size_of_graph=100
d=5

def difference(a):
    #method returns complement of a set
    U=set([i for i in range(0,size_of_graph)])
    return U-a
def calculate_fitness(neighbourhood, node_belongs_to):
    fitness=0
    for neighbour in neighbourhood:
         if neighbour not in node_belongs_to:
             fitness=fitness-1
    return fitness*0.5

def calculate_cost()  :
    return -sum(fitness_nodes.values())

def create_adj_list():
    adj_list=dict()
    for node in d_regular.adjacency():
        adj_list[node[0]]=list(node[1].keys())
    return adj_list

def update_neighbourhood(node):
    neighbourhood=adj_list[node]
    for neighbour in neighbourhood:
        if neighbour in A:
            update_node(neighbour,A)
        else:
            update_node(neighbour,B)
def update_node(node,new_set):
    fitness_nodes[node] = calculate_fitness(adj_list[node], new_set)
    fitness_queue.put((fitness_nodes[node],node))

def get_worst():
    worst_node=fitness_queue.get()
    while(True):
        if fitness_nodes[worst_node[1]]==worst_node[0]:
            break
        else:
            worst_node=fitness_queue.get()
    return worst_node
def swap():

    worst_node=get_worst()
    if(worst_node[1] in A):
        worst_set=A
        other_set=B
    else:
        worst_set=B
        other_set=A

    other_node=other_set.pop()
    worst_set.remove(worst_node[1])
    worst_set.add(other_node)
    other_set.add(worst_node[1])

    update_node(worst_node[1],other_set)
    update_node(other_node,worst_set)

    update_neighbourhood(worst_node[1])
    update_neighbourhood(other_node)


if __name__ == '__main__':
    d_regular=nx.random_regular_graph(d, size_of_graph)

    #randomly init A and B
    A=set(random.sample(d_regular.nodes,int(size_of_graph/2)))
    B=difference(A)

    #Init of S_best
    A_best=A.copy()
    B_best=B.copy()

    #add all nodes with their fitness in fitness_nodes- this will be our up to date storage
    #fitness_queue is just a min heap to help us get the least fit node, all entries may not be correct but we still have a way to check
    fitness_nodes=dict()
    adj_list=create_adj_list()
    fitness_queue=PriorityQueue()
    for node in adj_list.keys():
        if node in A:
            fitness_nodes[node]=calculate_fitness(adj_list[node],A)
        else:
            fitness_nodes[node]=calculate_fitness(adj_list[node],B)
        fitness_queue.put((fitness_nodes[node], node))

    cost_now=calculate_cost()
    cost_best=cost_now

    num_iterations=200
    costs=[]
    for i in range(0, num_iterations):
        swap()
        cost_now=calculate_cost()
        if cost_now<cost_best:
            A_best=A.copy()
            B_best=B.copy()
            cost_best=cost_now
        costs.append(cost_now)
    plt.plot([i for i in range (0, num_iterations)], costs)
    plt.xlabel=('iteration number')
    plt.ylabel=('total frienliness')

    plt.show()



