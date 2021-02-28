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