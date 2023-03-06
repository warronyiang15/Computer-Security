from Crypto.Cipher import AES
from hashlib import sha256
from math import gcd
from sympy.ntheory.modular import crt

DEGREE = 128

def polyeval(poly, x):
    return sum([a * x**i for i, a in enumerate(poly)])

shares = eval(input())
cipher = eval(input())
nonce = eval(input())

# find proper shares to solve CRT
x = []
y = []
for i in range(len(shares)):
    for j in range(i + 1, len(shares)):
        if gcd(shares[i][0], shares[j][0]) != 1:
            break
    else:
        x.append(shares[i][0])
        y.append(shares[i][1])

print(x)
# use CRT to solve coefficients
poly = []
for i in range(DEGREE + 1):
    a = [y[i] % x[i] for i in range(len(x))]
    coef = crt(x, a)[0]
    poly.append(coef)
    for i in range(len(x)):
        y[i] -= coef
        y[i] //= x[i]

secret = polyeval(poly, 0x48763)
key = sha256(str(secret).encode()).digest()[:16]
aes = AES.new(key, AES.MODE_CTR, nonce=nonce)
print(aes.decrypt(cipher))
