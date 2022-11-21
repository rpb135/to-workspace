import requests
import json

from pprint import pprint

def CU_monday(nt_dict):

    monday_apiKey = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE3OTA4NzkzMSwidWlkIjoyOTExOTA0OCwiaWFkIjoiMjAyMi0wOS0wNVQwNjozMjowMC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTA1MzU4MTMsInJnbiI6InVzZTEifQ.xBVcurfDt-aMx_jY0OrzrD-CceG3GEPnGtVkQvfixJI'
    monday_apiUrl = 'https://api.monday.com/v2'
    headers = {'Authorization' : monday_apiKey}

    notion_platform = {0: '가맹점PC', 1: '가맹점App', 2: '기사App', 3: '대리점PC', 4: '대리점APP', 5: '백엔드', 6: 'API연동', 7: '백오피스', 8: 'DB'}
    monday_platform = {0: 'SP', 1: 'SA', 2: 'RA', 3: 'CP', 4: 'CA', 5: 'BackEnd', 6: 'API', 7: 'B.O', 8: 'DB'}

    for plat_len in range(len(nt_dict['is_platform'])):
        for key, val in notion_platform.items():
            if nt_dict['is_platform'][plat_len] in val:
                nt_dict['is_platform'][plat_len] = monday_platform[key]

    # query_sample = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id:2872172460, item_name:$myItemName, column_values:$columnVals) { id } }'
    # query2 = 'mutation { create_item (board_id: 2872172460, group_id: "group_title", item_name: "new issue create test", column_values: "{\"status\" : {\"label\" : \"Medium\"}}") { id } }'
    # query2 = '{ boards (ids:2872172460) { groups {id title} } }'
    #data = {'query' : query2}
    
    # groups id : ____13921 Crawling Page
    query1 = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id: 2872172460, group_id: "____13921", item_name: $myItemName, column_values:$columnVals) { id } }'
    vars = {
        'myItemName' : nt_dict['is_title'],
        'columnVals' : json.dumps({
            'status' : {'label' : nt_dict['is_priority']},  # 중요도
            #'__0' : {'label' : nt_dict['is_state']},       # 버그로 추정 됨. 생성 시 값이 롤백 됨
            '___12' : {'label' : nt_dict['is_state']},      # 상태
            '__' : {'url' : nt_dict['is_url'], 'text' : nt_dict['is_title']}, # 상세 링크
            '___3' : {'labels' : nt_dict['is_platform'] }   # 플랫폼
        })
    }
    monday_data = {'query' : query1, 'variables' : vars}
    # 생성 된 Object 로 부터 ticket ID 값을 return 시킴
    monday_res = requests.post(url=monday_apiUrl, json=monday_data, headers=headers)
    pprint(monday_res.json())

    #return monday_res
    
def SR_monday(idx):

    monday_apiKey = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE3OTA4NzkzMSwidWlkIjoyOTExOTA0OCwiaWFkIjoiMjAyMi0wOS0wNVQwNjozMjowMC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTA1MzU4MTMsInJnbiI6InVzZTEifQ.xBVcurfDt-aMx_jY0OrzrD-CceG3GEPnGtVkQvfixJI'
    monday_apiUrl = 'https://api.monday.com/v2'
    headers = {'Authorization' : monday_apiKey}

    query1 = '{ boards (ids:2872172460) { groups (ids:____13921) { items { name id column_values(ids:__) { text } } } } }'
    monday_data = {'query' : query1}
    monday_res = requests.post(url=monday_apiUrl, data=monday_data, headers=headers)
    monday_json_data = monday_res.json()
    #pprint(monday_json_data)
    #print(monday_json_data['data']['boards'][0]['groups'][0]['items'][0]['column_values'])
    #print(monday_json_data['data']['boards'][0]['groups'][0]['items'][1]['id'])
    for i in monday_json_data['data']['boards'][0]['groups'][0]['items']:
        i['column_values'][0]['text']
        url_text = i['column_values'][0]['text'].split('https://www.notion.so/')
        if url_text[1] in idx:
            print(idx)
            print(url_text[1])
            print('존재 하는 이슈')
            return False
        else:
            print('존재 하지 않는 이슈 인지 찾는 중')
            continue
    
    print('존재 하지 않는 이슈 등록')
    return True
    #obj = monday_json_data['data']['boards'][0]['groups'][0]['items'][0]['column_values'][0]['text']