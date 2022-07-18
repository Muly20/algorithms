import random
import heapq

"""
An implementation, using heaps, of Prim's Algorithm (running time O(m log n)
for computing Minimum Cost Spanning Tree of an undirected connected acyclic 
Graph G={V,E}.

Graph G is represented using an Adjacency List.

See also https://en.wikipedia.org/wiki/Prim%27s_algorithm
"""

# construct the adjacency list from file
with open('edges.txt', 'r') as f:
    n, m = list(map(int, f.readline().strip('\n').split(' ')))
    # adjacency list representation of the graph
    A = [None] + [[] for _ in range(n)]
    # set of edges
    E = set()
    for line in f:
        # each raw contains endpoint1, endpoint2 and the edge's cost
        v, w, c = list(map(int, line.strip('\n').split(' ')))

        E.add((c, v, w))
        A[v].append((w, c))
        A[w].append((v, c))

# X - set of processed vertices
X = set()
# T - set of the MST's edges
T = set()
# maintain a fixed array to track vertices not yet in X
V = [False] + [True for _ in range(n)]

# pick first vertex arbitrarily
s = random.randrange(1, 501)
V[s] = False
X.add(s)

# initialize the heap
# each vertex with no edge coming from X will have a priority (cost) of
# +infinity. edges are stored as a tuple of (cost, vertex in V, vertex in X)
heap = [(float('+inf'), v, None) for v in range(1, n+1)]

# run through edges coming out of the first vertex s and add their end
# vertex (not in X) to the heap with their cost as key. O(m log n)
for v, c in A[s]:
    # cost, destination vertex, source vertex
    heap[v] = (c, v, s)

heapq.heapify(heap)

# main while loop
while len(X) < n:
    # extract-min: the lowest cost crossing edge from {X} to {V-X}
    c, v, s = heapq.heappop(heap)
    # make sure not to handle a vertex already in X
    while not V[v]:
        c, v, s = heapq.heappop(heap)

    T.add((c, v, s))
    X.add(v)
    V[v] = False

    for edge in A[v]:
        w, c = edge
        if V[w]:
            # w not in X
            # instead of deleting and re-inserting w from the heap,
            # I'll just add it with its new priority (lower cost key) and
            # consider that when popping item from the heap (above)
            heapq.heappush(heap, (c, w, v))


# count cost of the spanning tree T
cost = sum(c for c, _, _ in T)

print(f'MST cost: {cost}')
