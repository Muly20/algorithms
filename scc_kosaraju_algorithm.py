
"""
SCC - Kosaraju algorithm.py
An implementation of Kosaraju's linear-time Algorithm for finding directed graph's strongly-connected components.
implemented both recursive and stacked version (to avoid python's recursive limits).
"""

import time
from collections import deque
import sys

filepath = 'Algorithms/'

def get_file(filepath, n):
  """
  each line in the input file is a directed edge, from the vertex represented 
  in the first number to the vertex represented in the second.
  
  returns two adjacency lists, one "straight" and the other "reversed" (tail<->head)
  """
  
  with open(filepath, 'r') as f:
    file_lines = f.readlines()
  f.close()

  adj_list = {i: [] for i in range(1,n+1)} # adj_list[0] will stay an empty list []
  rev_adj_list = {i: [] for i in range(1,n+1)}

  for line in file_lines:
    line = line.strip('\n')
    edge = line.split(' ')[:2]

    adj_list[int(edge[0])].append(int(edge[1]))
    rev_adj_list[int(edge[1])].append(int(edge[0]))

  return adj_list, rev_adj_list

def DFS_recursive(G, i, leader, reversed):
  """
  G - graph represented by a dict, with keys as nodes and values for each outgoing directed edge from that node
  i - the node from which to search the graph
  leader - the node from which the routine was called
  leaders_dict - a dict with key representing the leader node for each of the graph's SCCs,
                with values of the vertices in the SCC
  explored_list - a list describing which nodes already been explored
  reversed - a boolian flag noting how to read the given edges

  """
  global leaders_dict, explored_list, finishing_time
  # mark node i as explored
  explored_list[i] = True

  # set leader in the 2nd pass
  if reversed==False: leaders_dict[leader].append(i)

  for head in G[i]:
    if not explored_list[head]: DFS(G, head, leader, reversed)
  
  # set finishing time in the 1st pass
  if reversed: finishing_time.append(i)

def DFS_stack(G, i, leader, reversed):
  """
  implementation using stack, instead of recursion. 
  useful to avoid recursive limits in python for large graphs
  """
  global leaders_dict, explored_list, finishing_time
  
  # in order to aboid recursions (for handling "deep" graphs), use a LIFO stack (python list) instead.
  # use faster list: 'deque' from python's 'collections' library, for faster "in and outs"
  stack = deque([i])
  explored_list[i] = True

  while stack:
    v = stack[-1]
    not_explored = [head for head in G[v] if not explored_list[head]]

    if not_explored: # additional deeper nodes
      stack += deque(not_explored)
      for head in not_explored:
        explored_list[head] = True
    
    else: # update finishing time only when exhausted deepest route
      stack.pop()
      if reversed: finishing_time.append(v)
      if reversed==False: leaders_dict[leader].append(v)

def DFSLoop(G, n, order, reversed):
  global leaders_dict, explored_list, finishing_time
  
  # initialize explored_list;
  # in order to avoid O(n) search in sub-routine, should define a static list of 
  # explored nodes (with sorted indices). length n+1 in order to keep indexing simple
  explored_list = [False] * (n+1)
  
  for node in order:
    if not explored_list[node]:
      if reversed==False: leaders_dict[node] = []
      DFS_stack(G, node, leader=node, reversed=reversed)

def ComputeSCC(G, G_rev, n):
  global leaders_dict, finishing_time
  
  # first pass DFS-Loop on reversed graph, in order to compute ordered list of nodes for the 2nd pass
  order = list(range(1, n+1))
  DFSLoop(G_rev, n, order, reversed=True)

  # second pass of DFS-Loop on original graph, with reversed finishing_time order
  order = reversed(finishing_time)
  DFSLoop(G, n, order, reversed=False)

# get files

n = 875714 # number of vertices in 'SCC.txt'
n1 = 9
n2 = 8
n3 = 8
n4 = 8
n5 = 12
test1_adjlist, test1_adjlist_rev = get_file(filepath + 'test1_33300.txt', n1)
test2_adjlist, test2_adjlist_rev = get_file(filepath + 'test2_33200.txt', n2)
test3_adjlist, test3_adjlist_rev = get_file(filepath + 'test3_33110.txt', n3)
test4_adjlist, test4_adjlist_rev = get_file(filepath + 'test4_71000.txt', n4)
test5_adjlist, test5_adjlist_rev = get_file(filepath + 'test5_63210.txt', n5)
SCC_list, SCC_list_rev = get_file(filepath + 'SCC.txt', n)

# SCC main

# defining global variables
explored_list = []
leaders_dict = {} # dictionary with each key represent a Strongly-Connected Component, with values as the nodes within this SCC
finishing_time = [] # a list of nodes with increasing order of finishing time

tic = time.time()

# ComputeSCC(test5_adjlist, test5_adjlist_rev, n5)
ComputeSCC(SCC_list, SCC_list_rev, n)

toc = time.time()

# evaluating running time
t = ((toc - tic)*1000//1)
sec = t/1000

print(f"running time: {sec}s")

# finding largest 5 SCCs
SCC_lengths = [0, 0, 0, 0, 0]

for key in leaders_dict.keys():
  key_len = len(leaders_dict[key])
  if key_len > min(SCC_lengths):
    SCC_lengths.append(key_len)
    SCC_lengths.remove(min(SCC_lengths))
SCC_lengths.sort(reverse=True)
print(SCC_lengths)