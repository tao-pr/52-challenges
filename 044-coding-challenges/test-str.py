from collections import defaultdict, deque


def test_warmup_longest_common_prefixes():
    """
    Given a list of strings,
    find the longest most common prefixes among them
    The common prefix has to be shared by at least 2 strings
    """

    def longest_pref(*slist):
        """
        Time complexity:
            iter1: N
            iter2: <=N
            iter3: <=N
            ..
            iterL: <=N

            ~= O(L*N)
        """

        counter = defaultdict(int)

        slist = list(slist)

        # iterate every string one position at a time
        p = 1
        remains = set(range(len(slist)))
        while len(remains) > 0:
            to_delete = set()
            for i in remains:
                if len(slist[i]) < p:
                    to_delete.add(i)
                else:
                    pref = slist[i][:p]
                    counter[pref] += 1

            for d in to_delete:
                remains.remove(d)

            p += 1

        longest = 0
        longest_pref = ""
        for prefix, cnt in counter.items():
            if cnt > 1:
                longest = len(prefix)
                longest_pref = prefix
        return longest_pref

    assert longest_pref("aa1", "aa2", "aaaa3", "a15", "ba1uaaaa", "aaa5") == "aaa"

    assert longest_pref("123", "abca123", "911a", "") == ""

    assert (
        longest_pref("aa", "aa", "c91111", "jaaaa", "aa55", "c911117", "c") == "c91111"
    )


def test_longest_common_substrings():
    """
    Given an array of strings,
    find the longest substrings that have to occur in every string
    """

    def lss(*arr):
        """
        Time complexity:
            iter1: N * L^2
            ..
            iterS:

            ~= O(N * S * L^2)
        """

        print(arr)
        shortest = min(arr, key=len)  # O(N)

        if len(shortest) == 0:
            return ""

        common = ""

        # iterate all combinations of shortest string, find if they occur in all other strings
        for i in range(len(shortest)):  # O(S)
            for l in range(1, len(shortest) - i + 1):  # O(S)
                if len(shortest[i:l]) < 1 or len(shortest[i:l]) < len(common):
                    continue

                print(f"testing: {shortest[i:l]}")

                sub = shortest[i:l]
                # check if sub exists in all other strings
                if all([sub in s for s in arr]):
                    common = sub
                    print(f"yes: {sub}")
                else:
                    # stop here, iterating longer won't beat the common
                    break

        return common

    assert lss("abc", "abanau", "1111ab") == "ab"

    assert lss("abccccc", "abanauccc", "11c11abiccc") == "ccc"

    assert lss("abc", "c71", "i9kbc") == ""


def test_longest_palindrome_substr():
    """
    Given a string, find the longest palindrome inside
    """

    def lps(s):
        if len(s) <= 1:
            return ""

        longest = s[0]
        for i in range(len(s)):
            print(f"Iter @{i}")
            # check if s[i] is a centre of a palindrome

            # [1] with centre
            d = 1
            pal = s[i]
            while i - d >= 0 and i + d < len(s) and s[i - d] == s[i + d]:
                pal = s[i - d] + pal + s[i + d]
                if len(pal) > len(longest):
                    longest = pal
                    print(f"Found new longest with centre: {longest}")
                d += 1

            # [2] without centre
            d = 0
            pal = ""
            while i - d > 0 and i + d + 1 < len(s) and s[i - d] == s[i + d + 1]:
                pal = s[i - d] + pal + s[i + d + 1]
                if len(pal) > len(longest):
                    longest = pal
                    print(f"Found new longest without centre: {longest}")
                d += 1

        return longest if len(longest) > 1 else ""

    assert lps("aaa") == "aaa"
    assert lps("abcd") == ""
    assert lps("p") == ""
    assert lps("p11151315p") == "51315"
    assert lps("uabccbaabccba7aaa") == "abccbaabccba"  # palindrome in palindrome


def test_minimum_swap_to_make_palindrom():
    """
    Do minimum number of letter swaps,
    so that the final string becomes a palindrome
    """

    def make_pal(ss) -> int:
        """
        iterate left to right until reach centre, and swap out-of-place tokens
        """
        return count_swap(deque(ss))

    def count_swap(ss):
        if len(ss) > 1:
            left = ss.popleft()
            right = ss.pop()
            if left != right:
                # find a sub
                for i, v in enumerate(ss):
                    # dont swap elements which are alreay in place
                    if v == right and ss[len(ss) - i - 1] != v:
                        # swap here
                        ss[i] = left
                        return 1 + count_swap(ss)

                # if right is unique, no duplicates anywhere to swap with
                # then try swapping right with centre
                print(f"Cant find {right} from {ss}, try centre {ss[len(ss) // 2]}")
                if len(ss) % 2 == 1 and ss[len(ss) // 2] == left:
                    ss[len(ss) // 2] = right
                    return 1 + count_swap(ss)
                else:
                    # not possible to make it a panlimdrom
                    return 0
            return count_swap(ss)
        else:
            return 0

    assert make_pal("aaa") == 0
    assert make_pal("aba") == 0
    assert make_pal("gbaagb") == 1
    assert make_pal("tkktkk") == 1
    assert make_pal("ababk") == 1


def find_palindrome_words():
    """
    Given a string with white spaces,
    find a word which is a palindrome
    """

    def find_pal(ss):
        # tokenise words
        return next((w for w in ss.split(" ") if is_pal(deque(w))), "")

    def is_pal(word: deque):
        # Complexity: O(N)
        while word > "":
            if word.pop() != word.popleft():
                return False
        return True

    """
    Total time complexity = O(L + W*N)
    """

    assert find_pal("his cat is nun") == "nun"
    assert find_pal("the aaa battery is so good") == "aaa"
    assert find_pal("a cookie is rotten") == ""
    assert find_pal("can hza uuuk hbhbh nac") == "hbhbh"


def test_evaluate_math_expr():
    """
    Given a string containing mathemetical expression,
    calculate the output
    """

    def eval(expr):
        # convert expr string into tokens: O(L)
        tokens = []
        while len(expr) > 0:
            # iterate until find an operator
            d = int(expr[0])
            expr = expr[1:]
            while len(expr) > 0 and expr[0] not in {"x", "+", "-", "/"}:
                d *= 10
                d += int(expr[0])
                expr = expr[1:]

            tokens.append(d)
            # take an operator
            if len(expr) > 0:
                tokens.append(expr[0])
            expr = expr[1:]

        # Evaluate tokens
        return compute(tokens)

    def compute(tokens):
        # put operands and operators in brackets,
        # prioritised by operator
        op = []
        num = []
        while len(tokens) > 0:
            if isinstance(tokens[0], int):
                num.append(tokens[0])
                tokens = tokens[1:]
            elif tokens[0] == "/":  # highest prio
                op = num.pop()
                op2 = tokens[1]
                num.append(op / op2)
                tokens = tokens[2:]
            elif tokens[0] == "x":  # high prio
                op = num.pop()
                op2 = tokens[1]
                num.append(op * op2)
                tokens = tokens[2:]
            else:
                op = num.pop()
                action = tokens[0]
                op2 = tokens[1]
                if action == "+":
                    num.append(op + op2)
                elif action == "-":
                    num.append(op - op2)
                tokens = tokens[2:]
        return num[-1]

    assert eval("1+1") == 2
    assert eval("2x3") == 6
    assert eval("16-5+3") == 14
    assert eval("4/2+5") == 7
    assert eval("0+13x2-16") == 10


def test_bracket_parser():
    """
    Given a string containg nested brackets,
    convert it into nested array.

    example:
        "{a{b{c}d}{e}} -> [a,[b,[c], d], [e]]
    """

    # O(N)
    def parse(ss):
        stack = []  # last element is the inner-most layer
        while len(ss) > 0:
            if ss[0] == "{":
                # create a new empty list
                stack.append([])
            elif ss[0] == "}":
                # list finishes
                inner = stack.pop()
                # append it to the previous layer
                if len(stack) > 0:
                    stack[-1].append(inner)
                else:
                    stack.append(inner)
            else:
                # add it to the last element (inner-most)
                stack[-1].append(ss[0])

            ss = ss[1:]
        return stack.pop()

    assert parse("{}") == []
    assert parse("{c}") == ["c"]
    assert parse("{e{}}") == ["e", []]
    assert parse("{{{e}}}") == [[["e"]]]
    assert parse("{{}{a}{b}}") == [[], ["a"], ["b"]]
    assert parse("{a{bcd}{e}}") == ["a", ["b", "c", "d"], ["e"]]
    assert parse("{a{b{c}d}{e}}") == ["a", ["b", ["c"], "d"], ["e"]]


def test_longest_matched_pattern():
    """
    Given a pattern string containing * for any letters,
    find the longest matched strings
    """

    def longest_match(pattern, cands):
        if pattern == "*":
            return max(cands, key=len)

        match = ""

        pattern = pattern.split("*")

        # check each candidate (stop early if not possible to become a longest)
        while len(cands) > 0:
            cand = cands[0]
            if len(cand) < len(match):
                cands = cands[1:]
                continue

            # match pattern
            if is_match(cand, pattern[:]) and len(cand) > len(match):
                match = cand

            cands = cands[1:]

        return match

    def is_match(cand, pattern):
        "prune candidate until all pattern parts are matched"
        # wildcard
        if pattern == [""]:
            return True
        # all matched
        if pattern == [] and cand == "":
            return True
        # remaining unmatchables
        if (pattern == [] and cand > "") or (len(pattern) > 0 and cand == ""):
            return False
        if pattern[0] == "":
            # wildcard, skip until we find next exact match (pattern[1])
            while cand > "":
                if cand.startswith(pattern[1]):
                    return is_match(cand.lstrip(pattern[1]), pattern[2:])
                cand = cand[1:]
            # not found a match
            return False

        else:
            # exact match
            if cand.startswith(pattern[0]):
                return is_match(cand.lstrip(pattern[0]), pattern[1:])
            else:
                return False

    assert longest_match("*", ["abc", "", "ayaaaaaa", "ii"]) == "ayaaaaaa"

    assert longest_match("*d", ["aaaaaaaaaaaaaaaa", "aad", "d", "ddddda"]) == "aad"


def test_edit_distance():
    """
    Find the minimum number of edits between 2 strings
        - insertion
        - deletion
        - replacement
    """

    def edit(str1, str2):
        # longer first
        if len(str2) >= len(str1):
            str1, str2 = str2, str1

        return edistance(str1, str2)

    def edistance(str1, str2):
        if str2 == "":
            return len(str1)
        else:
            if len(str1) == len(str2):
                # check how many diff
                print(f"diff: {str1} v {str2}")
                return sum(1 if a != b else 0 for a, b in zip(str1, str2))
            else:
                # prefix: abcd ~~ bcd
                if str1[0] != str2[0]:
                    print(f"prefix: {str1} v {str2}")
                    return 1 + edistance(str1[1:], str2)
                # suffix: abcd ~~ abc
                else:
                    # iterate until no match
                    print(f"suffix: {str1} v {str2}")
                    return edistance(str1[1:], str2[1:])

    assert edit("abc", "abc") == 0
    assert edit("abc", "abbc") == 1
    assert edit("abc", "acb") == 2
    assert edit("", "ab") == 2
    assert edit("aa", "abab") == 2
    assert edit("abc", "1abc") == 1
    assert edit("abc", "jjj") == 3


def test_bracketize_expression():
    """
    Given a string of mathematical expression
        eg. 1+15/25/5+1*4

    Put a bracket by priority of operations / > * > + -
    """

    def bracket(expr):
        """
        1+1*5+1

        [1] +1*5
        [1,+,] 1*5
        [1,+,1] *5
        [1,+,] [1*] 5
        [1,+,] [1*5] +1
        [1,+,] [[1*5]+ ] 1
        [1,+,] [[1*5]+1 ]

        then parse from right to left (inner to outer shell)
        """

        stack = []
        prio = {None: 0, "+": 0, "-": 0, "*": 1, "/": 2}

        def append_stack(s):
            if len(stack) == 0:
                stack.append([s])
            else:
                stack[-1].append(s)

        def get_last_op():
            if len(stack) == 0:
                return 0
            else:
                n = -1
                # iterate from the back of stack,
                # until we find the last op
                op = next(
                    (a for a in stack[-1] if isinstance(a, str) and a in prio), None
                )
                print(f"prev op = {op}")
                return prio[op]

        for e in expr:
            if e.isnumeric():
                append_stack(e)
            else:
                # operator
                # check if last element in stack already has operator?
                prev_op = get_last_op()
                if (
                    prio[e] > prev_op
                ):  # find a higher prio op, take the last operand out
                    last_operand = stack[-1].pop()
                    stack.append([last_operand, e])
                elif prio[e] < prev_op:  # time to enclose last expression block
                    stack[-1] = [stack[-1]]  # enclose last expression with bracket
                    stack[-1].append(e)
                else:
                    stack[-1].append(e)

        # now parse the stack
        print(expr)
        print(stack)
        return render(stack)

    def render(stack):
        # [[], [['1', '*', '5'], '+', '2', '+'], ['5', '/', '3']]
        r = ""
        for block in stack[::-1]:  # render rightmost first (as innermost)
            br = render_block(block)
            # ['5', '/', '3'] --> "5/3"
            r = br + "{" + r + "}" if r > "" else br
        return r

    def render_block(block):
        br = ""
        for el in block:
            if isinstance(el, list):
                br += "{" + render_block(el) + "}"
            else:
                br += el
        return br

    assert bracket("1+1") == "1+1"
    assert bracket("1+5+3") == "1+5+3"
    assert bracket("1*5+2+5/3") == "{{1*5}+2+{5/3}}"
    assert bracket("5/4/3/2") == "{5/4/3/2}"
    assert bracket("5/4/3/2+1") == "{{5/4/3/2}+1}"


def test_word_break():
    """
    Given a dictionary of words,
    break a given string into array of words and other unknown words
    """

    def wbreak(worddict, text):
        # build a nested dict containing all words in the dict
        # the, there, cat
        # {t -> h -> e -> NULL,  r -> e -> NULL, c -> a -> t -> NULL}
        tree = {}
        for word in worddict:
            add_to_tree(tree, word)
        print(tree)
        return run_wbreak(tree, text)

    def add_to_tree(tree, word):
        if len(word) == 1:
            # add last letter with NULL terminating
            if word[0] in tree:
                tree[word[0]][None] = None
            else:
                tree[word[0]] = {None: None}  # still needs to remain a dict
        else:
            if word[0] in tree:
                add_to_tree(tree[word[0]], word[1:])
            else:
                tree[word[0]] = {}
                add_to_tree(tree[word[0]], word[1:])

    def run_wbreak(tree, text):
        result = []
        last_cand = ""

        tree_ptr = tree
        for t in text:
            if t in tree_ptr:
                print(f"{t} in tree")
                last_cand += t
                tree_ptr = tree_ptr[t]  # iterate deeper into the tree
            else:
                # end of word
                # check if the word is recognised in the tree
                if None in tree_ptr and last_cand > "":
                    result.append(last_cand)

                # check if t could be a beginning of a new word?
                tree_ptr = tree  # reset pointer to the root
                last_cand = ""

                if t in tree_ptr:
                    last_cand = t
                    tree_ptr = tree_ptr[t]

        # check if last word also ends?
        if last_cand > "":
            print(last_cand)
            if None in tree_ptr:
                result.append(last_cand)
        return result

    assert wbreak(set(["the", "is", "there", "cat"]), "thereisthecat") == [
        "there",
        "is",
        "the",
        "cat",
    ]
    assert wbreak(set(["ben", "net", "been"]), "beennetbenetben") == [
        "been",
        "net",
        "ben",
        "ben",
    ]


def test_concat_words():
    """
    Given a list of untokenised words,
    find a combination of shortest unique words

    eg.
    inputs: [ant, anti, santi, eat]
    output: [anteat]

    inputs: [car, cart, fast, tart, start]
    output: [carfasttart]
    """

    def concat(inputs):
        # sort words, shorter first
        # ant, eat, anti, santi
        words = sorted(inputs, key=len) # O(N logN)
        bag = set()
        for word in words:
            # see ant --> check if any existing words already contain ant
            if any(b for b in bag if b in word):
                continue
            bag.add(word)
        
        print(bag)
        return "".join(sorted(bag))

    assert concat(["ant", "anti", "santi", "eat"]) == "anteat"
    assert concat(["car", "cart", "fast", "scar", "tart", "start"]) == "carfasttart"
