def test_rotational_cipher():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=238827593802550

  def rotationalCipher(input, rotation_factor):
    cz = []
    for c in input:
      if ord('0') <= ord(c) <= ord('9'):
        cz.append(encode_letter(c, '0', '9', rotation_factor))
      elif ord('A') <= ord(c) <= ord('Z'):
        cz.append(encode_letter(c, 'A', 'Z', rotation_factor))
      elif ord('a') <= ord(c) <= ord('z'):
        cz.append(encode_letter(c, 'a', 'z', rotation_factor))
      else:
        cz.append(c)
    return ''.join(cz)

  def encode_letter(c, min_c, max_c, step):
    n0 = ord(c) - ord(min_c)
    K = ord(max_c) - ord(min_c) + 1
    n = (n0 + step) % K
    return chr(n + ord(min_c))

  assert encode_letter('a', 'a', 'z', 5) == 'f'
  assert encode_letter('Z', 'A', 'Z', 3) == 'C'
  assert rotationalCipher("Zebra-493?", 3) == "Cheud-726?"
  assert rotationalCipher("abcdefghijklmNOPQRSTUVWXYZ0123456789", 39) == "nopqrstuvwxyzABCDEFGHIJKLM9012345678"


def test_string_to_number():
  def str_to_num(q):
    tokens = q.split(' ')
    return parse(tokens)

  def parse(tokens, prev=None):
    if len(tokens)==0:
      return 0
    tk = tokens[-1]
    digits = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirten']
    dec = ['zero','ten','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninty']
    
    n = 1
    if prev == 'hundred':
      n = 100

    if tk in digits:
      return digits.index(tk)*n + parse(tokens[:-1])
    elif tk == 'twenty':
      return 20*n + parse(tokens[:-1])
    elif tk == 'fifteen':
      return 15*n + parse(tokens[:-1])
    elif 'teen' in tk:
      return digits.index(tk.replace('teen',''))*n + parse(tokens[:-1])
    elif tk in dec:
      return dec.index(tk)*n*10 + parse(tokens[:-1])
    elif 'hundred' == tk:
      return parse(tokens[:-1], 'hundred')
    else:
      return 0

  assert str_to_num("fourty four") == 44
  assert str_to_num("two hundred eleven") == 211
  assert str_to_num("seven hundred thirty five") == 735
  assert str_to_num("five hundred fifteen") == 515


def test_string_compression():
  # REF: https://leetcode.com/problems/string-compression/

  def compress(s):
    ctr = ""
    cnt = 0
    for c in s + ' ':
      if len(ctr)==0:
        ctr = c
      
      if ctr[-1]==c:
        # repeating
        cnt += 1
      else:
        # change of alpha
        # conclude the old char
        if cnt>1:
          ctr += str(cnt)
        
        # End marker
        if c != ' ':
          ctr += c
          cnt = 1
    return ctr

  assert compress("aabbcc") == "a2b2c2"
  assert compress("aaabccc") == "a3bc3"


def test_tree_parser():
  """
  Given string of following format:
    (a)ab(b(c))(((c))) 
  Create an output string showing the nested depth as follows
    1a0a0b1b2c3c
  """
  def depth(str1):
    out = ""
    d = 0
    for s in str1:
      if s=='(':
        d += 1
      elif s==')':
        d -= 1
      else:
        out += str(d) + s
    return out
  
  assert depth("abc") == "0a0b0c"
  assert depth("a(b)c") == "0a1b0c"
  assert depth("a(b(c(d((d))e)))") == "0a1b2c3d5d3e"


def test_byte_pair_encode():
  """
  BPE: A technique to encode a string with replacing 
  most two frequent symbols with a single alpha,
  and keep repeating until the remaining symbols are singular
  """

  def bpe(s):
    from collections import Counter
    freq = []
    for a,b in zip(s,s[1:]):
      freq.append(a+b)
    freq = Counter(freq)
    z = 'Z'
    for mc,f in freq.most_common():
      if f>1:
        s = s.replace(mc, z)
        z = chr(ord(z)-1)
    return s

  assert bpe("hey") == "hey"
  assert bpe("foofoo") == "ZoZo"
  assert bpe("quick squad and duck or chicken") == "YiZ sYaVanVduZ or chiZen"