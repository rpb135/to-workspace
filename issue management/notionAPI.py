import requests
import json
import mondayAPI

from dotenv import dotenv_values
from notion_client import Client
from pprint import pprint

def iss_state(st, nt_dict):

    notion_state_confirm = { 0: '기획검토 중', 1: '배정 전', 2: '시작 전', 3: '진행 중', 4: '해결', 5: '배포대기', 6: '완료', 7: '보류/취소', 8: '상태없음' }
    monday_state_confirm = { 0: 'Open', 1: 'Open', 2: 'Open', 3: 'In Progress', 4: 'Resolved', 5: 'Resolved', 6: 'Closed', 7: 'Pending', 8: 'Feedback' }
    
    for key, val in notion_state_confirm.items():
        if val in st:
            nt_dict['is_state'] = monday_state_confirm[key]

    return nt_dict['is_state']


def R_notion():

    nt_dict = {
        'is_title'     :'',
        'is_url'       :'',
        'is_state'     :'',
        'is_type'      :'',
        'is_priority'  :'',
        'is_platform'  :[]
    }

    notion_priority_confirm = { 0: '즉시', 1: '긴급', 2: '높음', 3: '보통', 4: '낮음'}
    monday_priority_confirm = { 0: 'Critical', 1: 'Critical', 2: 'Major', 3: 'Minor', 4: 'Trivial'}

    # request notion-sdk-py
    config = dotenv_values("./issue management/.env")
    notion_secret = config.get('NOTION_TOKEN')
    notion = Client(auth=notion_secret)

    has_more = True
    cursor_id = ''

    # 생성 된 객체 List 모두 요청
    while has_more: 

        if cursor_id == '':
            pages = notion.search(filter={"property": "object", "value": "page"}, page_size=1)
        else:
            pages = notion.search(filter={"property": "object", "value": "page"}, start_cursor=cursor_id, page_size=10)

        for page in pages['results']:

            # parent type : database_id 일 때만 작업 수행
            if page['parent']['type'] == 'database_id':
                 
                 # 영웅배송 유지보수 로드맵 DB id
                if page['parent']['database_id'] == 'cf711923-91d8-47b4-a7bd-5179dcac3ebe':

                    # notion 제목
                    nt_dict['is_title'] = page['properties']['Projects']['title'][0]['plain_text']

                    # 등록 된 이슈 인지 확인
                    if mondayAPI.SR_monday(page['url']):
                        # notion url
                        nt_dict['is_url'] = page['url']
                    else:
                        continue

                    # 상태
                    if page['properties']['상태']['select'] == None:
                        print('상태 없음')
                        nt_dict['is_state'] = 'Feedback'
                    else:
                        nt_dict['is_state'] = iss_state(page['properties']['상태']['select']['name'], nt_dict)

                    # notion : 우선순위, monday : 중요도
                    if page['properties']['우선순위']['select'] == None:
                        if page['properties']['유형']['select'] == None:
                            print('입력 값(중요도, 유형) 없음')
                            nt_dict['is_type'] = 'bug'
                            nt_dict['is_priority'] = 'Major'

                        else:
                            if '작업' in page['properties']['유형']['select']['name']:
                                print('작업')
                                nt_dict['is_type'] = 'work'
                                nt_dict['is_priority'] = 'Major'
                            elif '에픽' in page['properties']['유형']['select']['name']:
                                print('에픽')
                                nt_dict['is_type'] = 'epic'
                                nt_dict['is_priority'] = ''     # 에픽은 중요도를 설정하지 않음
                            elif '배포' in page['properties']['유형']['select']['name']:
                                print('배포')
                                nt_dict['is_type'] = 'release'
                                nt_dict['is_priority'] = ''     # 배포는 중요도를 설정하지 않음
                            else:
                                nt_dict['is_type'] = page['properties']['유형']['select']['name']
                                nt_dict['is_priority'] = 'Major'
                        
                    else:
                        nt_dict['is_type'] = 'bug'
                        nt_dict['is_priority'] 
                        for key, val in notion_priority_confirm.items():
                            if val in page['properties']['우선순위']['select']['name']:
                                nt_dict['is_priority'] = monday_priority_confirm[key]

                    # 플랫폼 값이 없을 때
                    if page['properties']['플랫폼']['multi_select'] == [] :
                        nt_dict['is_platform'] = ''
                    # 플랫폼 값이 있을 때
                    else:
                        plat = []
                        for n in page['properties']['플랫폼']['multi_select']:
                            plat.append(n['name'])

                        nt_dict['is_platform'] = plat
                    
                    pprint(nt_dict)
                    # return 받은 id 값으로 등록 된 이슈인지 찾기
                    mondayAPI.CU_monday(nt_dict)
                    #print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
                else:
                    # 영웅배송 유지보수 로드맵 외 DB id
                    continue
            else:
                # parent type이 database_id 아닐 때 PASS
                print('parent type : ',page['parent']['type'])
                continue
                
        if pages['has_more']:
            cursor_id = pages['next_cursor']

        has_more = pages['has_more']


    '''
    #아래 방법은 API docs 준수 및 postman 활용하는 내용

    # https://www.notion.so/spidor/cf71192391d847b4a7bd5179dcac3ebe?v=0e3d5bc3fab34b05ba041cf19bc1fc88 플랫폼 유지보수 URL
    #notion.pages
    #pprint(page)

    notion_header = {
        "Authorization": notion_secret,
        "Accept": "application/json",
        "Notion-Version": "2022-06-28"
    }

    notion API docs 참조

        "query": "",
        "filter": { 
            "property": "object",  
            "value": "page"
        },
        "page_size": 5

    API 에서 해당 필터 조건으로 요청 한 결과가 notion.search(filter={"property": "object", "value": "page"}, page_size=10) 내용과 동일한 결과를 노출 함

        "query": "플랫폼 유지보수 로드맵",
        "filter": { 
            "property": "object",  
            "value": "database"
        },
        "page_size": 5

    해당 내용으로 요청 시 플랫폼 유지보수 로드맵 database의 속성 및 query 조건으로 검색하는 개념으로 접근 함

    ### Page
    #page_id = 'cf71192391d847b4a7bd5179dcac3ebe'
    #page_id = '0e3d5bc3fab34b05ba041cf19bc1fc88'
    platform_database_id = 'cf71192391d847b4a7bd5179dcac3ebe'    #플랫폼 유지보수 로드맵 Database ID
    #notion_url = 'https://api.notion.com/v1/databases/' + platform_database_id
    notion_url = 'https://api.notion.com/v1/search'

    print(notion_url)
    #notion_url = 'https://api.notion.com/v1/pages/'+ page_id

    ## request URL 
    #res = requests.post(notion_url, headers=notion_header)
    #json_data = json.loads(res.text)
    #pprint(json_data)
    '''