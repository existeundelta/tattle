# Ben cipher caesar
plaintext = 'The cat sat on the very fine mat she did.'
alphabet = 'abcdefghijklmnopqrstuvwxyz'
code = 'nopqrstuvwxyzabcdefghijklm' # ROT13

i, secret = 0, ''
for letter in plaintext:
    k = (alphabet.find(letter.lower())+i)%len(alphabet)
    secret += code[k]
    i += 1

''.join(secret)
