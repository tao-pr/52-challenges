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
        longest_pref = ''
        for prefix, cnt in counter.items():
            if cnt > 1:
                longest = len(prefix)
                longest_pref = prefix
        return longest_pref
    

    assert longest_pref(
        "aa1",
        "aa2",
        "aaaa3",
        "a15",
        "ba1uaaaa",
        "aaa5"
    ) == "aaa"

    assert longest_pref(
        "123",
        "abca123",
        "911a",
        ""
    ) == ""

    assert longest_pref(
        "aa",
        "aa",
        "c91111",
        "jaaaa",
        "aa55",
        "c911117",
        "c"
    ) == "c91111"



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
        shortest = min(arr, key=len) # O(N)

        if len(shortest) == 0:
            return ''

        common = ''

        # iterate all combinations of shortest string, find if they occur in all other strings
        for i in range(len(shortest)): # O(S)
            for l in range(1, len(shortest)-i+1): # O(S)
                if len(shortest[i:l])<1 or len(shortest[i:l])<len(common):
                    continue

                print(f'testing: {shortest[i:l]}')

                sub = shortest[i:l]
                # check if sub exists in all other strings
                if all([sub in s for s in arr]):
                    common = sub
                    print(f'yes: {sub}')
                else:
                    # stop here, iterating longer won't beat the common
                    break

        return common


    assert lss(
        "abc",
        "abanau",
        "1111ab"
    ) == "ab"

    assert lss(
        "abccccc",
        "abanauccc",
        "11c11abiccc"
    ) == "ccc"

    assert lss(
        "abc",
        "c71",
        "i9kbc"
    ) == ""


def test_longest_palindrome_substr():
    """
    Given a string, find the longest palindrome inside
    """

    def lps(s):

        if len(s) <= 1:
            return ''

        longest = s[0]
        for i in range(len(s)):
            print(f'Iter @{i}')
            # check if s[i] is a centre of a palindrome

            # [1] with centre
            d = 1
            pal = s[i]
            while i-d >= 0 and i+d < len(s) and s[i-d] == s[i+d]:
                pal = s[i-d] + pal + s[i+d]
                if len(pal) > len(longest):
                    longest = pal
                    print(f'Found new longest with centre: {longest}')
                d += 1

            # [2] without centre
            d = 0
            pal = ''
            while i-d > 0 and i+d+1 < len(s) and s[i-d] == s[i+d+1]:
                pal = s[i-d] + pal + s[i+d+1]
                if len(pal) > len(longest):
                    longest = pal
                    print(f'Found new longest without centre: {longest}')
                d += 1

        return longest if len(longest) > 1 else ''


    assert lps('aaa') == 'aaa'
    assert lps('abcd') == ''
    assert lps('p') == ''
    assert lps('p11151315p') == '51315'
    assert lps('uabccbaabccba7aaa') == 'abccbaabccba' # palindrome in palindrome


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
        if len(ss)>1:
            left = ss.popleft()
            right = ss.pop()
            if left != right:
                # find a sub
                for i, v in enumerate(ss):
                    # dont swap elements which are alreay in place
                    if v == right and ss[len(ss)-i-1] != v:
                        # swap here
                        ss[i] = left
                        return 1 + count_swap(ss)
                
                # if right is unique, no duplicates anywhere to swap with
                # then try swapping right with centre
                print(f'Cant find {right} from {ss}, try centre {ss[len(ss)//2]}')
                if len(ss)%2 == 1 and ss[len(ss)//2] == left:
                    ss[len(ss)//2] = right
                    return 1 + count_swap(ss)
                else:
                    # not possible to make it a panlimdrom
                    return 0
            return count_swap(ss)
        else:
            return 0


                
    assert make_pal('aaa') == 0
    assert make_pal('aba') == 0
    assert make_pal('gbaagb') == 1
    assert make_pal('tkktkk') == 1
    assert make_pal('ababk') == 1


def find_palindrome_words():
    """
    Given a string with white spaces,
    find a word which is a palindrome
    """

    def find_pal(ss):
        # tokenise words
        return next((w for w in ss.split(' ') \
                    if is_pal(deque(w))), '')
    

    def is_pal(word: deque):
        # Complexity: O(N)
        while word > '':
            if word.pop() != word.popleft():
                return False
        return True
    
    """
    Total time complexity = O(L + W*N)
    """
    

    assert find_pal('his cat is nun') == 'nun'
    assert find_pal('the aaa battery is so good') == 'aaa'
    assert find_pal('a cookie is rotten') == ''
    assert find_pal('can hza uuuk hbhbh nac') == 'hbhbh'

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
            while len(expr) > 0 and expr[0] not in {'x','+','-','/'}:
                d *= 10
                d += int(expr[0])
                expr = expr[1:]
            
            tokens.append(d)
            # take an operator
            if len(expr)>0:
                tokens.append(expr[0])
            expr = expr[1:]

        # Evaluate tokens
        return compute(tokens)
        
    def compute(tokens):
        # put operands and operators in brackets,
        # prioritised by operator
        op = []
        num = []
        while len(tokens)>0:
            if isinstance(tokens[0], int):
                num.append(tokens[0])
                tokens = tokens[1:]
            elif tokens[0] == '/': # highest prio
                op = num.pop()
                op2 = tokens[1]
                num.append(op/op2)
                tokens = tokens[2:]
            elif tokens[0] == 'x': # high prio
                op = num.pop()
                op2 = tokens[1]
                num.append(op*op2)
                tokens = tokens[2:]
            else:
                op = num.pop()
                action = tokens[0]
                op2 = tokens[1]
                if action == '+':
                    num.append(op+op2)
                elif action == '-':
                    num.append(op-op2)
                tokens = tokens[2:]
        return num[-1]
    
    assert eval('1+1') == 2
    assert eval('2x3') == 6
    assert eval('16-5+3') == 14
    assert eval('4/2+5') == 7
    assert eval('0+13x2-16') == 10
