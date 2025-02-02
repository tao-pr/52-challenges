from typing import Tuple
from collections import Counter

def test_warmup_min_shuffle_sorted():
    """
    Given an array of integers,
    find a minimum number of element swaps
    so the final array is sorted ascendingly
    """

    def sortme(arr) -> Tuple[int, list[int]]:
        """
        Greedy swap, iterating left -> right
        for each element, swaps the smallest int to left
        orig: [1,0,0] -> [0,0,1]
        orig: [3,2,1] -> [1,2,3] swap1
        orig: [1,5,2,1] -> [1]+[1,2,5] swap1
        orig: [1,5,7,2] -> [1]+[2,7,5] swap1 ->  -> [1,2]+[5,7] swap2

        Time complexity: 
            for N elements: N + (N-1) + (N-2) .. 1 ~= O(N^2)
        
        Space complexity:
            Call stack size = O(N)
        """

        if len(arr)<=1:
            return 0, arr
        else:
            # swap smallest to the leftmost and move on
            smallest = arr[0]
            smallest_index = 0
            for i, a in enumerate(arr[1:]):
                if a < smallest:
                    smallest = a
                    smallest_index = i+1
            
            if smallest_index > 0 :
                # swap, and move on
                arr[smallest_index], arr[0] = arr[0], arr[smallest_index]
                n, remaining = sortme(arr[1:])
                return n+1, [arr[0]]+remaining
            else:
                n, remaining = sortme(arr[1:])
                return n, [arr[0]]+remaining

    
    assert sortme([]) == (0, [])
    assert sortme([1]) == (0, [1])
    assert sortme([2,2,2]) == (0, [2,2,2])
    assert sortme([1,2,5]) == (0, [1,2,5])
    assert sortme([1,5,2,5]) == (1, [1,2,5,5]) # 1 swap
    assert sortme([1,1,2,9,7,7,1]) == (2, [1,1,1,2,7,7,9]) # 2 swaps


def test_warmpup2_find_longest_palyndrome():
    """
    Given an array of integer,
    find the longest palyndrome inside
    """

    def lpal(arr):
        """
        [1,1,0,1]

        iterate each element,
            - check if it is a centre of palindrome (walk left and right)
            - record longest palindrome
        move next


        Time complexity:
            for N elements:
                iter 1 - k (<N/2)
                iter 2 - k (<N/2)
                ..

                ~= N * (k) = N * (N/2) = O(N^2)
                but technically it should stops as long as it finds palindrome half the size of array
        """

        longest = [] # left side of longest palindrome

        if len(arr)<=1:
            return arr
        
        for i in range(len(arr)):
            # check if i-th is the centre of palindrome
            
            # [1] with arr[i] as centre element
            k = 1
            pal = [arr[i]]
            while i-k >= 0 and i+k < len(arr) and arr[i-k] == arr[i+k]:
                pal.append(arr[i+k])
                pal = [arr[i-k]] + pal
                k += 1

            if len(pal) > 1 and len(longest) < len(pal):
                longest = pal

            # [2] without centre element
            k = 0
            pal = []
            while i-k>=0 and i+1+k < len(arr) and arr[i-k] == arr[i+1+k]:
                pal.append(arr[i+1+k])
                pal = [arr[i-k]] + pal
                k += 1
            
            if len(pal) > 1 and len(longest) < len(pal):
                longest = pal

            # stop early, no chance to find longer than the longest we spotted so far
            if len(arr)-i < len(longest):
                return longest

        return longest
            
    

    assert lpal([1,1]) == [1,1]
    assert lpal([0,1,2]) == []
    assert lpal([0,1,0]) == [0,1,0]
    assert lpal([0,1,0,1]) == [0,1,0]
    assert lpal([0,1,0,5,3,1]) == [0,1,0]
    assert lpal([0,1,0,0,1,0,3]) == [0,1,0,0,1,0]


def test_warmup_find_the_triplet_sum_to_zero():
    """
    Given an array of int,
    find a triplet that sums to zero
    """

    def zsum(arr):

        if len(arr)<3:
            return []

        neg = [] # including zeros
        pos = []
        num_zeros = 0
        counter = Counter(arr) # O(N)
        for a in arr: # O(N)
            if a<=0:
                if a ==0:
                    num_zeros += 1
                neg.append(a)
            else:
                pos.append(a)

        if len(neg)==0:
            return []
        if num_zeros >= 3:
            return [0,0,0]
        
        # combinations :  1 neg + 2pos
        if len(pos)>=2 and len(neg)>0:
            for n in neg:
                for p in pos:
                    wanted = -(n+p)
                    tick = 1 if wanted == p or wanted == n else 0
                    if counter[wanted]>tick:
                        return sorted([n, p, wanted ])

        # combinations 2 neg + 1 pos
        if len(neg) >= 2 and len(pos)>0:
            for i, n1 in enumerate(neg):
                for j, n2 in enumerate(neg):
                    if i == j:
                        continue
                    if counter[-(n1+n2)]>0:
                        return sorted([n1, n2, -(n1+n2)])
        
        return []
    
    assert zsum([]) == []
    assert zsum([1,-1,0]) == [-1,0,1]
    assert zsum([1,1,5,1]) == []
    assert zsum([-3,1,6,1]) == []
    assert zsum([-2,1,0,-1,3]) == [-2,-1,3]


def test_median_of_two_sorted_arrays():
    """
    Given 2 sorted arrays
    find the median
    """

    def median(arr1, arr2):
        """
        Find the position of the median "IF" two arrays combine (mid point)

        Only iterate halfway
        Keep adding smallest leftmost to the stack until 
        it reaches the median point.
        Report that last position
        """
        pos = (len(arr1) + len(arr2))//2
        stacked = []
        while len(stacked) <= pos:

            if len(arr1)==0:
                stacked.append(arr2[0])
                arr2 = arr2[1:]
            elif len(arr2)==0:
                stacked.append(arr1[0])
                arr1 = arr1[1:]
            elif arr1[0] < arr2[0]:
                stacked.append(arr1[0])
                arr1 = arr1[1:]
            else:
                stacked.append(arr2[0])
                arr2 = arr2[1:]

            print(pos, stacked)
        return stacked[-1]
    

    assert median([], [1,2,3]) == 2
    assert median([1], [1]) == 1
    assert median([1,5,5], [1,2,3]) == 3
    assert median([1,7,9], [1,2,2,2,7]) == 2

def test_zeroes_to_zeroes_with_minimal_flights():
    """
    Given a matrix of integers denoting the height of terrain,
    find a path from zeros to zeros which yields 
    the minimum flights
    """

    def min_flight(mat):
        
        # find all zeros
        # also generate graph (adjacency mat)
        zero = [] # indices of zeros
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] == 0:
                    zero.append((i, j))
        
        if len(zero) <= 1:
            return []
        

        best_flight = 1e6
        best = []
        for i in range(len(zero)):
            for j in range(len(zero)):
                if i==j:
                    continue

                # for any pair of zeros,
                # find an easiest path without climbing up/down
                flight, path = walk(zero[i], zero[j], mat)
                if flight < best_flight:
                    best_flight = flight
                    best = path
        
        print(f'best = {best}')
        return [mat[i][j] for i,j in best]
    

    def walk(pos1, pos2, mat):
        # greedy walk
        i0, j0 = pos1
        path = [pos1]

        visited = set(pos1)

        print('START')

        # Walks from pos1 until reaches pos2
        rounds = 0
        total_climb = 0
        while path[-1] != pos2:
            best_step = 1e10
            best = None
            for dx, dy in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
                
                # Just finish if can
                if i0+dx == pos2[0] and j0+dy == pos2[1]:
                    path.append((i0+dx, j0+dy))
                    return total_climb, path

                # Ignore OOB
                if (dx==0 and dy==0):
                    continue

                if i0+dx < 0 or i0+dx >= len(mat):
                    continue

                if j0+dy < 0 or j0+dy >= len(mat[0]):
                    continue

                # ignore visited
                if (i0+dx, j0+dy) in visited:
                    continue
                
                # choose next cell with least flight climb
                d = abs(mat[i0][j0] - mat[i0+dx][j0+dy])
                if d < best_step:
                    best_step = d
                    best = (i0+dx, j0+dy)
                    visited.add((i0+dx, j0+dy))
            
            path.append(best)
            i0, j0 = best
            total_climb += best_step
            print(best)

        return total_climb, path
    

    assert min_flight([
        [1, 1, 0],
        [0, 5, 1],
        [0, 1, 3]
    ]) == [0,0]

    assert min_flight([
        [1, 1, 0],
        [1, 5, 1],
        [0, 1, 3]
    ]) == [0,1,1,1,0]
    assert min_flight([
        [1, 3, 0],
        [5, 2, 1],
        [2, 1, 3]
    ]) == []

    assert min_flight([
        [1, 3, 0, 7],
        [5, 2, 1, 1],
        [0, 1, 3, 5]
    ]) == [0,1,2,3,0]


def test_inverse_lego():
    """
    Given a sorted array,
    locate total number of missing elements

    eg
    [1,2,6,7,9] => missing 3,5,8 => 3 numbers
    """

    def missing(arr):
        if len(arr) <= 1:
            return 0
        
        num_miss = 0
        prev, arr = arr[0], arr[1:]
        while len(arr)>0:
            if prev+1 < arr[0]:
                num_miss += arr[0] - prev - 1
            prev, arr = arr[0], arr[1:]
        return num_miss
    
    assert missing([]) == 0
    assert missing([1]) == 0
    assert missing([1,2,3,4,5]) == 0
    assert missing([1,1,2,6]) == 3
    assert missing([5,6,9,11,16,27,29]) == 18

