header1 = {'accept': 'application/json, text/plain, */*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
'cookie': '_ga=GA1.3.954869399.1628166441; _gid=GA1.3.1157128705.1628166441; _gat=1',
'referer': 'https://ppdb.jogjaprov.go.id/',
'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
'sec-ch-ua-mobile': '?0',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
'x-requested-with': 'XMLHttpRequestppdb.jogjaprov.go.id'}

import requests as rq

print(rq.get(f'https://ppdb.jogjaprov.go.id/seleksi/reguler/sma/1-32040009-1000.json', headers=header1, verify=False).json()['data'][0][5])

