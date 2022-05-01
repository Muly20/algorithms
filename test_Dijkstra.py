from Dijksra_ShortestPath import get_file, shortestPath

def test_simple():
    filepath='DijkstraTest.txt'
    adj_list = get_file(filepath)

    assert shortestPath(adj_list) == [-1, 0, 1, 3, 6]

def test_full():
    filepath = 'DijkstraData.txt'
    adj_list = get_file(filepath)

    results = shortestPath(adj_list)
    selected_nodes = [7,37,59,82,99,115,133,165,188,197]
    paths = [results[node] for node in selected_nodes]
    assert paths == [2599,2610,2947,2052,2367,2399,2029,2442,2505,3068]

