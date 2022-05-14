import requests
import pandas as pd

from bs4 import BeautifulSoup as bs

api_url = 'http://biz.epost.go.kr/KpostPortal/openapi2'
reg_key = '1217e48a021887fc41641993401785'

df = pd.read_excel('C:\workspace\company_work\고용보험_지사정보.xlsx', engine='openpyxl')
jibon = df['지번주소']
doro = df['도로명주소']

print(jibon)

addr = '서울시 관악구 남부순환로 247다길 48'

value = dict(regkey=reg_key, target='postNew', query=addr.encode('utf-8'))
#res = requests.post(api_url, data=value)
#print(res.text)