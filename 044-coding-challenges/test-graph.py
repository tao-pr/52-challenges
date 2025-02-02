import heapq

def test_warmup_find_longest_chain():
    """
    Given an array of links (value denotes distance)
    find the longest possible chain (sum of distance)

    link shouldn't repeat a node
    """

    def longest(arr):
        # build graph into dict
        G = {}
        for a,b,w in arr: # O(N)
            if a not in G:
                G[a] = {b: w}
            else:
                G[a][b] = w

        # then construct all possible paths
        heap = []
        for a in G:
            traverse(G, a, heap, [a], 0)

        # get longest we traverse so far
        distance, path = heapq.heappop(heap)
        print(distance, path)
        return -distance


    def traverse(G, a, heap, path_prefix, pre_weight):
        """
        DFS, enumerate all deepest possible paths
        """
        if a not in G:
            return
        
        for b in G[a]:
            if b not in path_prefix:
                path = path_prefix + [b]
                w = G[a][b] + pre_weight
                heapq.heappush(heap, (-w, path))
                traverse(G, b, heap, path, w)

    assert longest([
        (1, 2, 10),
        (2, 1, 25),
        (1, 3, 10),
        (1, 4, 1),
        (4, 2, 10)
    ]) == 45 # 4 -> 2 -> 1 ->3 

    assert longest([
        (0, 0, 56),
        (0, 1, 1),
        (1, 0, 61),
        (1, 5, 6),
        (1, 4, 1),
        (4, 5, 3),
        (3, 5, 1),
        (3, 1, 7),
        (5, 0, -1)
    ]) == 68 # 3 -> 1 -> 0 = 7+61 = 68


