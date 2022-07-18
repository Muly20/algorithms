# algorithms

This is a collection of my implementation of some useful algorithms.

1. Dijkstra's shortest path. A greedy algorithm, a generalization of BFS (breadth-first search), to include non-zero weighted edges, in a directed acyclic graph model for finding the shortest path between a given source node and every other connected node in the graph. Implemented using a heap data structure. Running time complexity: O(m log n), m-number of edges, n-number of nodes. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
2. Closest pair (2D): A recursive algorithm for finding the closest pair of points in 2D in O(n log n) time. https://en.wikipedia.org/wiki/Closest_pair_of_points_problem
3. Kosaraju's SCC: A linear time algorithm for finding directed graph's strongly-connected components by running through the graph twice: first in reversed order than on original order. Implemented both recursive and stacked version (to avoid python's recursive limits). Running time complexity: O(m+n), m-edges, n-nodes. https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
4. Harris corner detection: Corner detection in images, using gradients, Harris' response function and non-max suppression. Using native python libraries. https://en.wikipedia.org/wiki/Harris_corner_detector
5. Prim's Algorithm: an implementation of Prim's Algorithm of finding Minimum-Cost Spanning Tree of an undirected, connected, acyclic Graph. The Graph is represented using an Adjacency List and the algorithm is implemented using heap data structure for running time of O(m log n). (m- number of edges, n- number of vertices.) Test data in 'edges.txt'. https://en.wikipedia.org/wiki/Prim%27s_algorithm
