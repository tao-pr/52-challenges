import heapq
from collections import defaultdict

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


def test_find_all_meeting_crashes():
    """
    Given a list of meeting time (begin - end),
    find all overlapping meetings
    """

    def find_crashes(meetings):
        times = sorted(meetings, key=lambda x: x[0]) # O(N log N)
        crashes = set()
        clock = times[0][0] # earliest time
        prev = None
        while len(times) > 0:
            t = times[0]
            if t[0] < clock:
                # crashes
                crashes.add(t)
                crashes.add(prev)
            
            clock = max(t[1], clock) # keep tracking the furthest `to`
            times = times[1:]
            prev = t

        return crashes


    assert find_crashes([
        (1100, 1159),
        (1200, 1330),
        (1520, 1550),
        (1525, 1600)
    ]) == {(1520, 1550), (1525, 1600)}

    assert find_crashes([
        (830, 900),
        (900, 1130),
        (930, 1145),
        (730, 800)
    ]) == {(900, 1130), (930, 1145)}


def test_longest_ascending_path_matrix():
    """
    Given a matrix of depth values,
    find the longest ascending path
    """

    def lap(mat):
        # create dict of connected values : O(NxM)
        G = defaultdict(set)
        for n in range(len(mat)):
            for m in range(len(mat[0])):
                v = mat[n][m]
                # add edges to neighbour ascending values
                for dx, dy in [[0,-1], [1,0], [0,1], [-1,0]]:
                    if dx+n >= 0 and dx+n < len(mat) and dy+m >= 0 and dy+m < len(mat[0]):
                        if mat[n+dx][m+dy] > v:
                            G[(n, m)].add((n+dx, m+dy))
        
        # now iterate DFS
        longest = []
        for n, m in G:
            path = find_longest(G, (n, m), [(n, m)])
            longest = longest if len(longest) > len(path) else path

        print(G)
        return [mat[n][m] for n,m in longest]

    
    def find_longest(G, _from, prev):
        # DFS
        longest = prev
        if _from in G:
            for n, m in G[_from]:
                path = find_longest(G, (n, m), prev + [(n, m)])
                longest = longest if len(longest) > len(path) else path
        # end of route
        return longest

    assert lap([
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]) == []

    assert lap([
        [0,0,0],
        [1,2,3],
        [0,0,0]
    ]) == [0,1,2,3]

    assert lap([
        [2,0,0,0],
        [1,3,0,0],
        [0,0,0,5]
    ]) == [0,1,2]

