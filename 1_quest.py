import requests

from pprint import pprint

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.4.731 Yowser/2.5 Safari/537.36'}

params = {'user_id': '***',
          'access_token': '***',
          'extended': '1'}

url = 'https://api.vk.com/method/groups.get?user_id=***&v=5.131'
response = requests.get(url, params=params, headers=headers)

j_data = response.json()

#pprint(j_data)
groups = []

for i in j_data['response']['items']:
    groups.append(i['name'])

print(groups, sep='\n')

with open('HW1.html', 'w', encoding='UTF-8') as f:
    f.write(response.text)



