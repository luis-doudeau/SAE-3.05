import string 
import random
import zlib
def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

tab=  {}
val = bytes(get_random_string(8),"ascii")
while not zlib.crc32(val) in tab:
    tab[zlib.crc32(val)]=val
    val = bytes(get_random_string(8),'ascii')
print(val)
print(zlib.crc32(val))

print(tab[zlib.crc32(val)])
print(zlib.crc32(tab[zlib.crc32(val)]))