import collections

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ETAOIN = 'etaoinshrdlcumwfgypbvkjxqz'

def generate_caesar_key(offset):
    dictionary = {}
    index = 0
    for letter in ALPHABET:
        if index+offset >= 26:
            index -= 26
        dictionary.update({letter:ALPHABET[index+offset]})
        index += 1
    return dictionary

def switch_encode(string, key):
    encoded = ""
    for letter in string.lower():
        if letter in key.keys():
            encoded += key[letter]
        else:
            encoded += letter
    return encoded

def switch_decode(string, key):
    key = dict(zip(key.values(),key.keys()))
    decoded = ""
    for letter in string.lower():
        if letter in key.keys():
            decoded += key[letter]
        else:
            decoded += letter
    return decoded

def switch_crack(string):
    key = {}
    frequent_letters = collections.Counter(string).most_common()
    index = 0
    for letter in frequent_letters:
        if letter[0] in ALPHABET:
            key[ETAOIN[index]] = letter[0]
            index += 1
    return key
