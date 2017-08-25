import re

with open("big.txt","r") as f:
    words = set(re.findall('[a-z]+', f.read().lower())) 

def encrypt(word,password):
   add_letters = lambda x,y:chr((ord(x)+ord(y)-2*ord('a'))%26 + ord('a'))
   return "".join(add_letters(*i) for i in zip(word.lower(),password.lower()))

def decrypt(word,password):
   sub_let = lambda x,y:chr((ord(x)-ord(y)+26)%26 + ord('a'))
   return "".join(sub_let(*i) for i in zip(word.lower(),password.lower()))


def crack(a,b):
    assert(len(a) == len(b))
    w = (i for i in words if len(i) == len(a))
    for i in w:
        password = decrypt(a,i)
        b_plain= decrypt(b,password)
        if b_plain in words:
            print(i,b_plain,password)

password = "haha"
a="bomb"
b="love"

a_cyper=encrypt(a,password)
b_cyper=encrypt(b,password)

print("cyper",a_cyper,b_cyper)

crack(a_cyper,b_cyper)
