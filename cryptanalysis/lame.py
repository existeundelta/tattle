def dcode(data):
key = 20
newdata = ''
for i in data:
i=ord(i)
if i< key:
i = 256 + (1)
newdata += chr(i-key)
return newdata
def ncode(data):
newdata = ''
key = 20
for i in data:
i = ord(i)
if i + key >= 256:
i = i - (256)
newdata += chr(i+key)
return newdata
