# unique 
_my = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJK'
# enc
_enc = 'SnjGF3gsbHvOecDwuaiImxdfklQyJUqrY0t2KpPhT765z8A914WERo'
# _enc_flag
_enc_flag = '6ct69GHt_A00utACToohy_0u0rb_9c5byF3A}G515buR11_kL{3rp_'

my = [i for i in _my]
enc = [i for i in _enc]
enc_flag = [i for i in _enc_flag]

print(len(my))
print(len(enc))
print(len(enc_flag))

# Make sure all chars are unique
for i in range(len(my)):
	for j in range(len(my)):
		if my[i] == my[j] and i != j:
			print('no')

mp = dict()

for i in range(len(enc)):
	found = False
	for j in range(len(my)):
		if enc[i] == my[j]:
			if mp.get(j) == None:
				mp[j] = i 
			else:
				print('wtf')


s = ''
for i in range(len(enc_flag)):
	print(enc_flag[mp[i]],end ='')