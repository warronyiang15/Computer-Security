from Crypto.Util.number import long_to_bytes
from pwn import *

# build table
table = {}
hex_chr = ['0','1','2','3','4','5','6','7','8','9','a','b',
           'c','d','e','f','A','B','C','D','E','F']
for c in hex_chr:
    table[''.join(['T' if chr(ord(c) ^ i) in hex_chr else 'F' for i in range(1, 128)])] = c

print(table)
exit()
r = remote('eof.ais3.org', 10050)
#r = process(['python3', 'chal.py'])
iv_cipher = r.recvline().decode().strip()
iv = iv_cipher[:32]
cipher = iv_cipher[32:]
r.recvline()

token_hex = []
for i in range(16):
    res = []
    for xor in range(1, 128):
        r.recvuntil(b'Exit\n')
        r.sendline(b'1')
        r.recvuntil(b'Message(hex): ')
        new_iv = iv[:i * 2] + long_to_bytes(int(iv[i * 2:i * 2 + 2], 16) ^ xor).hex() + iv[i * 2 + 2:]
        r.sendline((new_iv + cipher).encode())
        res.append('T' if r.recvline().decode().strip() == 'Well received' else 'F')
    token_hex.append(table[''.join(res)])

r.recvuntil(b'Exit\n')
r.sendline(b'2')
r.recvuntil(b'Token(hex): ')
r.sendline(''.join(token_hex).encode())
print(r.recvline().decode().strip())
'''
FLAG{OHh...i_FOrG0t_To_remOve_TH3_errOr_Me55AG3}
'''