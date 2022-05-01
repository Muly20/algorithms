import heapq

def get_file(filepath):
    """
    each line in the input file is a list of edges directed from the
    raw-numbered vertex.
    each edge contains a tuple of two numbers: the first is the 'head' vertex
    and the second is the value/weight of the edge.

    returns the adjacency list as a python dict, with keys as the 'source'
    vertices and values as tuples of (head-vertex, weight)
    """

    with open(filepath, 'r') as f:
        file_lines = f.readlines()
    f.close()

    adj_list = {}

    for line in file_lines:
        line = line.strip('\n').split('\t')[:-1]
        s = int(line[0])
        adj_list[s] = []
        for edge in line[1:]:
            adj_list[s].append(tuple(map(int, edge.split(','))))

    return adj_list


def shortestPath(adj_list):
    N = len(adj_list)

    # defining source node index
    source = 1

    # intialize the shortest path list in order to track processed
    # vertices and their shortest path
    processed = [-1 for _ in range(N + 1)]
    # path to source node
    processed[source] = 0

    # this dictionary will map between vertices and 'best' weights found so
    # far, in order to access that info in O(1)
    weights = {}
    # priority queue to sort by next vertex with the shortest path
    frontier = []
    # first, consider only vertices that are directly connected to source node
    for head, weight in adj_list[source]:
        weights[head] = weight
        heapq.heappush(frontier, (weight, head))

    while frontier:
        # take out the node with the smallest Dijkstra's score (=key)
        key, node = heapq.heappop(frontier)

        if processed[node] != -1:
            # node already processed
            continue

        # mark as processed
        processed[node] = key

        # update heap values for all vertices that have edges directed from
        # the processed node
        for head, weight in adj_list[node]:
            if key+weight < weights.get(head, 100000):
                # current path shorter than known before
                weights[head] = key + weight

                # add path to queue with O(log n)
                heapq.heappush(frontier, (key+weight, head))

    return processed

if __name__ == '__main__':
    adj_list = get_file('dijkstraData.txt')

    vertex_scores = shortestPath(adj_list)

    # extract certain nodes:
    nodes = [7,37,59,82,99,115,133,165,188,197]
    out = []
    for node in nodes:
        out.append(vertex_scores[node])

    print(out)
    print(f'results match: {out == [2599,2610,2947,2052,2367,2399,2029,2442,2505,3068]}')


