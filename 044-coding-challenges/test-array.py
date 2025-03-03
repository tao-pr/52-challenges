from typing import Tuple
from collections import Counter, defaultdict
from heapq import heappush, heappop


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

        if len(arr) <= 1:
            return 0, arr
        else:
            # swap smallest to the leftmost and move on
            smallest = arr[0]
            smallest_index = 0
            for i, a in enumerate(arr[1:]):
                if a < smallest:
                    smallest = a
                    smallest_index = i + 1

            if smallest_index > 0:
                # swap, and move on
                arr[smallest_index], arr[0] = arr[0], arr[smallest_index]
                n, remaining = sortme(arr[1:])
                return n + 1, [arr[0]] + remaining
            else:
                n, remaining = sortme(arr[1:])
                return n, [arr[0]] + remaining

    assert sortme([]) == (0, [])
    assert sortme([1]) == (0, [1])
    assert sortme([2, 2, 2]) == (0, [2, 2, 2])
    assert sortme([1, 2, 5]) == (0, [1, 2, 5])
    assert sortme([1, 5, 2, 5]) == (1, [1, 2, 5, 5])  # 1 swap
    assert sortme([1, 1, 2, 9, 7, 7, 1]) == (2, [1, 1, 1, 2, 7, 7, 9])  # 2 swaps


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

        longest = []  # left side of longest palindrome

        if len(arr) <= 1:
            return arr

        for i in range(len(arr)):
            # check if i-th is the centre of palindrome

            # [1] with arr[i] as centre element
            k = 1
            pal = [arr[i]]
            while i - k >= 0 and i + k < len(arr) and arr[i - k] == arr[i + k]:
                pal.append(arr[i + k])
                pal = [arr[i - k]] + pal
                k += 1

            if len(pal) > 1 and len(longest) < len(pal):
                longest = pal

            # [2] without centre element
            k = 0
            pal = []
            while i - k >= 0 and i + 1 + k < len(arr) and arr[i - k] == arr[i + 1 + k]:
                pal.append(arr[i + 1 + k])
                pal = [arr[i - k]] + pal
                k += 1

            if len(pal) > 1 and len(longest) < len(pal):
                longest = pal

            # stop early, no chance to find longer than the longest we spotted so far
            if len(arr) - i < len(longest):
                return longest

        return longest

    assert lpal([1, 1]) == [1, 1]
    assert lpal([0, 1, 2]) == []
    assert lpal([0, 1, 0]) == [0, 1, 0]
    assert lpal([0, 1, 0, 1]) == [0, 1, 0]
    assert lpal([0, 1, 0, 5, 3, 1]) == [0, 1, 0]
    assert lpal([0, 1, 0, 0, 1, 0, 3]) == [0, 1, 0, 0, 1, 0]


def test_warmup_find_the_triplet_sum_to_zero():
    """
    Given an array of int,
    find a triplet that sums to zero
    """

    def zsum(arr):
        if len(arr) < 3:
            return []

        neg = []  # including zeros
        pos = []
        num_zeros = 0
        counter = Counter(arr)  # O(N)
        for a in arr:  # O(N)
            if a <= 0:
                if a == 0:
                    num_zeros += 1
                neg.append(a)
            else:
                pos.append(a)

        if len(neg) == 0:
            return []
        if num_zeros >= 3:
            return [0, 0, 0]

        # combinations :  1 neg + 2pos
        if len(pos) >= 2 and len(neg) > 0:
            for n in neg:
                for p in pos:
                    wanted = -(n + p)
                    tick = 1 if wanted == p or wanted == n else 0
                    if counter[wanted] > tick:
                        return sorted([n, p, wanted])

        # combinations 2 neg + 1 pos
        if len(neg) >= 2 and len(pos) > 0:
            for i, n1 in enumerate(neg):
                for j, n2 in enumerate(neg):
                    if i == j:
                        continue
                    if counter[-(n1 + n2)] > 0:
                        return sorted([n1, n2, -(n1 + n2)])

        return []

    assert zsum([]) == []
    assert zsum([1, -1, 0]) == [-1, 0, 1]
    assert zsum([1, 1, 5, 1]) == []
    assert zsum([-3, 1, 6, 1]) == []
    assert zsum([-2, 1, 0, -1, 3]) == [-2, -1, 3]


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
        pos = (len(arr1) + len(arr2)) // 2
        stacked = []
        while len(stacked) <= pos:
            if len(arr1) == 0:
                stacked.append(arr2[0])
                arr2 = arr2[1:]
            elif len(arr2) == 0:
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

    assert median([], [1, 2, 3]) == 2
    assert median([1], [1]) == 1
    assert median([1, 5, 5], [1, 2, 3]) == 3
    assert median([1, 7, 9], [1, 2, 2, 2, 7]) == 2


def test_zeroes_to_zeroes_with_minimal_flights():
    """
    Given a matrix of integers denoting the height of terrain,
    find a path from zeros to zeros which yields
    the minimum flights
    """

    def min_flight(mat):
        # find all zeros
        # also generate graph (adjacency mat)
        zero = []  # indices of zeros
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
                if i == j:
                    continue

                # for any pair of zeros,
                # find an easiest path without climbing up/down
                flight, path = walk(zero[i], zero[j], mat)
                if flight < best_flight:
                    best_flight = flight
                    best = path

        print(f"best = {best}")
        return [mat[i][j] for i, j in best]

    def walk(pos1, pos2, mat):
        # greedy walk
        i0, j0 = pos1
        path = [pos1]

        visited = set(pos1)

        print("START")

        # Walks from pos1 until reaches pos2
        rounds = 0
        total_climb = 0
        while path[-1] != pos2:
            best_step = 1e10
            best = None
            for dx, dy in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
                # Just finish if can
                if i0 + dx == pos2[0] and j0 + dy == pos2[1]:
                    path.append((i0 + dx, j0 + dy))
                    return total_climb, path

                # Ignore OOB
                if dx == 0 and dy == 0:
                    continue

                if i0 + dx < 0 or i0 + dx >= len(mat):
                    continue

                if j0 + dy < 0 or j0 + dy >= len(mat[0]):
                    continue

                # ignore visited
                if (i0 + dx, j0 + dy) in visited:
                    continue

                # choose next cell with least flight climb
                d = abs(mat[i0][j0] - mat[i0 + dx][j0 + dy])
                if d < best_step:
                    best_step = d
                    best = (i0 + dx, j0 + dy)
                    visited.add((i0 + dx, j0 + dy))

            path.append(best)
            i0, j0 = best
            total_climb += best_step
            print(best)

        return total_climb, path

    assert min_flight([[1, 1, 0], [0, 5, 1], [0, 1, 3]]) == [0, 0]

    assert min_flight([[1, 1, 0], [1, 5, 1], [0, 1, 3]]) == [0, 1, 1, 1, 0]
    assert min_flight([[1, 3, 0], [5, 2, 1], [2, 1, 3]]) == []

    assert min_flight([[1, 3, 0, 7], [5, 2, 1, 1], [0, 1, 3, 5]]) == [0, 1, 2, 3, 0]


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
        while len(arr) > 0:
            if prev + 1 < arr[0]:
                num_miss += arr[0] - prev - 1
            prev, arr = arr[0], arr[1:]
        return num_miss

    assert missing([]) == 0
    assert missing([1]) == 0
    assert missing([1, 2, 3, 4, 5]) == 0
    assert missing([1, 1, 2, 6]) == 3
    assert missing([5, 6, 9, 11, 16, 27, 29]) == 18


def test_merge_intervals():
    """
    Given a list of intervals, merge them
    """

    def merge(*intervals):
        merged = []
        # O(NlogN)
        intervals = sorted(intervals, key=lambda x: x[0])
        # + O(N)
        for a, b in intervals:
            if len(merged) == 0:
                merged.append([a, b])
            else:
                # Check if this interval [a,b] overlaps with last merged interval
                # [m0,   m1]
                #    ..b]
                #     a ....b]
                m0 = merged[-1][0]
                m1 = merged[-1][1]

                if a <= m1:  # mergeable
                    merged[-1] = [m0, max(m1, b)]
                else:  # not mergable
                    merged.append([a, b])

        return merged

    assert merge([1, 15], [1, 15]) == [[1, 15]]
    assert merge([1, 15], [2, 5], [7, 10], [12, 15]) == [[1, 15]]
    assert merge([1, 7], [7, 9], [10, 11], [10, 25]) == [[1, 9], [10, 25]]
    assert merge([0, 0], [4, 5], [3, 5], [8, 10]) == [[0, 0], [3, 5], [8, 10]]


def test_median_of_dedup_arrays():
    """
    Given a list of sorted arrays,
    find the median of these arrays combined after deduplications!
    """

    def median(arrs):
        # O(N) -> iterate all arrays, combine, and dedup
        combined = []
        for arr in arrs:
            for a in arr:
                if len(combined) == 0:
                    combined.append(a)
                elif combined[-1] < a:
                    combined.append(a)

        # Now find median
        if len(combined) == 1:
            return combined[0]
        elif len(combined) % 2 == 0:
            print(combined)
            return (
                combined[len(combined) // 2] + combined[len(combined) // 2 - 1]
            ) / 2.0
        else:
            return combined[len(combined) // 2]

    assert median([[1, 1, 1], [1, 1]]) == 1

    assert (
        median(
            [  # 1,5,16,50 -> 5+16 / 2 = 10.5
                [1, 1, 1, 5],
                [1, 16, 50],
            ]
        )
        == 10.5
    )

    assert median(
        [  # 1,3,5,7,15 -> 5
            [1],
            [3, 3, 5, 7],
            [3, 5, 15],
            [1, 1, 7],
        ]
    )


def test_wait_warmer_temp():
    """
    Given an array of daily temperatures (int),
    return an array containing number of days to wait
    until the weather is warmer
    """

    def wait(dailies):
        still_waits = set()
        daywait = [0 for _ in range(len(dailies))]  # materialized
        for index, temp in enumerate(dailies):
            if len(still_waits) > 0:
                # check prev days stil waiting
                buff = set()
                for wait_index in still_waits:
                    daywait[wait_index] += 1
                    if dailies[wait_index] >= temp:
                        # still wait more
                        buff.add(wait_index)
                still_waits = buff
            still_waits.add(index)

        # replace still waits with zeros
        for i in still_waits:
            daywait[i] = 0

        return daywait

    assert wait([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert wait([15, 15, 15, 15]) == [0, 0, 0, 0]
    assert wait([0, 1, 1, 5]) == [1, 2, 1, 0]
    assert wait([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_product_of_arrays_except_self():
    """
    Given an array of integers, can have duplicates
    find an array of products of all other elements except self
    """

    def product(arr):
        if len(arr) == 1:
            return [0]

        # find product of all elements (except zeros)
        p = 1
        zeros = set()
        for i, a in enumerate(arr):  # O(N)
            if a == 0:
                zeros.add(i)
            else:
                p *= a

        if len(zeros) > 1:
            return [0 for _ in range(len(arr))]

        if len(zeros) == 1:
            return [0 if i not in zeros else p for i, a in enumerate(arr)]

        return [p // a for i, a in enumerate(arr)]

    assert product([1, 15, 3]) == [45, 3, 15]
    assert product([1]) == [0]
    assert product([25, 0, 5]) == [0, 125, 0]
    assert product([0, 0, 15, 1]) == [0, 0, 0, 0]
    assert product([1, 3, 3, 5, 1]) == [45, 15, 15, 9, 45]


def test_largest_sliding_window_with_largest_sum():
    """
    Given an array of integers,
    find the largest sliding window which yields a largest sum amongs all
    """

    def lsum(arr):
        longest = []
        sum_longest = -999
        # 0 1 2 3 (L-1=4)
        for n in range(len(arr)):
            for m in range(1, len(arr) + 1):
                part = arr[n:m]
                sum_part = sum(part)
                if sum_part > sum_longest or (
                    sum_part == sum_longest and len(longest) < m - n
                ):
                    longest = arr[n:m]
                    sum_longest = sum_part
        return longest

    assert lsum([1, -1, -5, 0, 3, 5, 25, -1, 25, -29]) == [0, 3, 5, 25, -1, 25]
    assert lsum([3, 5, 6]) == [3, 5, 6]
    assert lsum([-10, 3, -20, 5, 3, 50, -5, 10, 0, -1]) == [5, 3, 50, -5, 10, 0]
    assert lsum([7, 0, 7, -6, 5, 3, -1]) == [7, 0, 7, -6, 5, 3]
    assert lsum([3, 3, 3, -9, 5, 2, -6, 1]) == [3, 3, 3]


def test_closest_sum():
    """
    Given an set of integer and a target number,
    find the subset that sums into the closest to the target number
    """

    # Complexity: O(N!)
    def _closest_sum(coll, target, candi=[], chain=[]):
        coll = coll if isinstance(coll, list) else list(coll)
        for i in range(len(coll)):
            c = coll[i]
            others = coll[i + 1 :]
            diff = abs(target - c)
            heappush(candi, (diff, [c] + chain))
            if diff > 0:
                _closest_sum(others, target - c, candi, [c] + chain)

        return candi

    def closest_sum(coll, target):
        cands = []
        _closest_sum(coll, target, cands)
        diff, chain = heappop(cands)
        print(f"diff = {diff}, chain = {chain}")
        return set(sorted(chain))

    assert closest_sum(set([1, 5, 6]), 20) == set([1, 5, 6])
    assert closest_sum(set([1, 5, 6, 10]), 16) == set([1, 5, 10])
    assert closest_sum(set([1, 5, 6, 10]), 4) == set([5])
    assert closest_sum(set([1, 5, 6, 10]), 17) == set([1, 6, 10])


def test_drop_water():
    """
    Given a matrix describing how deep the groun at (i,j) is,
    find a final matrix if we drop water into (i,j) position until
    it reaches certain level
    """

    def drop(mat, pos, level):
        # expand all connectivities from pos (8-directions) until no
        # level is below {level}
        visited = set()
        expand(mat, pos, level, visited)
        return mat

    def expand(mat, pos, level, visited):
        # iterate 8 directions from pos
        a, b = pos
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= a + i < len(mat) and 0 <= b + j < len(mat[0]):
                    if (
                        i != j
                        and (a + i, b + j) not in visited
                        and mat[a + i][b + j] < level
                    ):
                        mat[a + i][b + j] = level
                        visited.add((a + i, b + j))
                        # DFS
                        expand(mat, [a + i, b + j], level, visited)

    assert drop(
        [[1, 1, 3, 1], [2, 3, 5, 1], [2, 0, 1, 1], [3, 1, 5, 5]], [2, 2], 2
    ) == [[1, 1, 3, 2], [2, 3, 5, 2], [2, 2, 2, 2], [3, 2, 5, 5]]

    assert drop(
        [[4, 1, 3, 1], [5, 2, 2, 1], [3, 0, 6, 4], [3, 4, 5, 0]], [0, 1], 4
    ) == [[4, 4, 4, 4], [5, 4, 4, 4], [4, 4, 6, 4], [4, 4, 5, 0]]


def test_phone_number_lookup():
    """
    Given a list of telephone numbers,
    write a fast program to lookup as the user is typing first N letters
    """

    def build_trie(numbers):
        trie = {}
        trie_ptr = trie
        for num in numbers:
            print(f"Adding {num} to trie: root keys {trie_ptr.get('0')}")
            for n in num:
                if n not in trie_ptr:
                    trie_ptr[n] = {}
                trie_ptr = trie_ptr[n]
            # enclose the number
            trie_ptr[None] = {}
            # reset pointer
            trie_ptr = trie
        return trie

    def lookup(numbers, initial):
        """
        0891112223
        0915552223
        0891150000
        0690000000
        0950000000
        """

        trie = build_trie(numbers)

        print(trie)

        # walk the trie until end of typing
        pt = trie
        for n in initial:
            if n in pt:
                pt = pt[n]
            else:
                return []  # no match

        print(f"initial: {initial}, next keys: {pt.keys()}")

        # enumerate all children in the current position of trie pointer
        outcome = []
        for p in pt:
            walk_into(pt[p], outcome, initial + p)
        return outcome

    def walk_into(trie, outcome, prefix):
        # walk DFS until it hits None key (denotes end of numbers)
        # {n1: {..}, n2: {...}, None: {}}

        for n in trie:
            if n:
                walk_into(trie[n], outcome, prefix + n)
            else:
                # end of number
                outcome.append(prefix)

    assert sorted(
        lookup(
            ["0891112223", "0915552223", "0891150000", "0690000000", "0950000000"], "0"
        )
    ) == sorted(["0891112223", "0915552223", "0891150000", "0690000000", "0950000000"])

    assert sorted(
        lookup(
            ["0891112223", "0915552223", "0891150000", "0690000000", "0950000000"], "08"
        )
    ) == sorted(
        [
            "0891112223",
            "0891150000",
        ]
    )

    assert sorted(
        lookup(
            ["0891112223", "0915552223", "0891150000", "0690000000", "0950000000"],
            "099",
        )
    ) == sorted([])

    assert sorted(
        lookup(
            ["0891112223", "0915552223", "0891150000", "0690000000", "0950000000"],
            "0891",
        )
    ) == sorted(
        [
            "0891112223",
            "0891150000",
        ]
    )


def test_pascal_row():
    """
    Find all numbers inside the row N of a Pascal triangle
    """

    cache = defaultdict(int)

    def pascal_row(n):
        """
        1
        1 1
        1 2 1
        1 3 3 1 ..... C[n] = C[L-1-n]
        1 4 6 4 1 .... row=4 ... start mirror from row//2+1
        ...

        row N = N numbers
        """

        row = []
        for i in range(n):
            row.append(cell(n, i))
        return row
    
    def cell(row, pos):
        if pos == 0 or pos == row-1:
            return 1
        else:
            if (row,pos) in cache:
                return cache[(row,pos)]
            # mirror
            # R[r][i] = R[r][r-1-i]
            elif row >=3 and pos >= row//2+1:
                return cell(row, row-1-pos)
            else:
                v = cell(row-1, pos) + cell(row-1, pos-1)
                cache[(row, pos)] = v
                return v

    assert pascal_row(1) == [1]
    assert pascal_row(23) == [
        1,
        22,
        231,
        1540,
        7315,
        26334,
        74613,
        170544,
        319770,
        497420,
        646646,
        705432,
        646646,
        497420,
        319770,
        170544,
        74613,
        26334,
        7315,
        1540,
        231,
        22,
        1,
    ]


def test_min_max_sell():
    """
    Given a times-series sequence of stock price,
    find the best time to buy and sell to maximise the profit.
    """

    def minmax(seq):
        # find max possible values to the right 
        # of every element
        # [1,5,5,3]

        """
        3
        5 -> None
        5 -> None
        1 -> 5
        """
        n = len(seq)-2
        mx = seq[-1]
        index_max = len(seq)-1
        offset = {}
        biggest_offset = 0
        biggest_offset_pair = None
        while n>=0:
            if mx > seq[n]:
                offset[n] = mx - seq[n]
                if offset[n] > biggest_offset:
                    biggest_offset = offset[n]
                    biggest_offset_pair = (n, index_max)
            if seq[n] > mx:
                # find a new max
                mx = seq[n]
                index_max = n
            n -= 1

        if biggest_offset_pair:
            return [biggest_offset_pair[0], biggest_offset_pair[1]]


    assert minmax([
        1,5,5,3,5,4,1,1,5
    ]) == [7,8]

    assert minmax([
        7,7,8,6,6,4,4,3,1,5,3,5,7
    ]) == [8,12]


def test_split_array_min_avg():
    """
    Split an array so the average value of each subarrays
    are closest
    """

    def split(arr):
        arr1, arr2 = arr[:1], arr[1:]
        avg1 = arr1[0]
        avg2 = sum(arr2)/float(len(arr2))
        smallest_avg = abs(avg1 - avg2)
        smallest = [arr1, arr2]
        """
        arr = [1] [3 5 7]
        avg = 1 5
        """
        while len(arr2)>1:
            N1 = len(arr1)
            N2 = len(arr2)
            v = arr2[0]
            arr1 = arr1 + [v]
            arr2 = arr2[1:]
            # update avg values
            avg1 = ((avg1 * N1) + v) / (N1 + 1)
            avg2 = ((avg2 * N2) - v) / (N2 - 1)
            print(f'{arr1} - {arr2} -> diff avg = {abs(avg1 - avg2)}, min was = {smallest_avg}')
            if abs(avg1 - avg2) < smallest_avg:
                print(f'New: {avg1}, {avg2} => {arr1}, {arr2}')
                smallest_avg = abs(avg1 - avg2)
                smallest = [arr1, arr2]
        return smallest


    assert split([1,1]) == [[1], [1]]
    assert split([1,3,5,4]) == [[1,3,5],[4]]
    assert split([3,3,3,1,11]) == [[3], [3,3,1,11]]

    

