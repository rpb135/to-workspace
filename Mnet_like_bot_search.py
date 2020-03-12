import requests, json
import re

from bs4 import BeautifulSoup as bs
from selenium import webdriver

driver = webdriver.Chrome('C:/Python/chromedriver')

header = {
    'Origin' : 'https://user.interest.me4',
    'Referer': 'https://user.interest.me/common/cookie/cookieRedirect.html',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Accept-Encoding' : 'gzip, deflate, kr',
    'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

LOGIN_INFO = {
    'siteCode'  : 'S20',
    'id'        : 'mgen2@yopmail.com', #변동 값
    'token'     : '9R8cz19FAIe3yHJ4B4GqFko25PQdH0X8F0w0', #변동 값
    'isSSO'     : 'N',
    'ssLogin'   : 'N',
    #변동 값
    'userInfo'  : 'EQvipQhNwGwIXzbFq5SO4853fUliu2kd9qvh2bICyVNfL0jjvS9jRPpHdOPgfBq5fNPmLwk%2Fp%2F0t%0A8tfIetQPgpqjjexdAqSsiO2cr9bSrW12HigRuoCc%2FDf8ENLEP%2Byk%2FYU%2BGGn0InD0JvVT1K5Z1qrW%0AuFnZayizRB1U75uqZuZ18AkvRtUV9KyUM9VsY9TV9o6FKJkIo%2FwsOY8YU5mY9kMJiS%2BCvprDqRqp%0AKZp6zebEo18AJN9tQeB%2Fjzg9HfAV7HInQvQGnRAnq3A6wCMVG4Qkkm5e9y6mVqKtYdGgN6HVFlGu%0AOZhrqHc0B682nRECYiw%2B7Mk1TmKbfsowQBqIOLDIr2fQBcSkV85j0KOKM%2FPt4VkWCvwhhhsWNRJ3%0A3P6oydxvN9fyxQMES5MPSTf5mr756iiq1E4B4dsYNcBNWmNxWw%2BfhxH3x%2BYAVzj4styzW2t9i2BM%0AtmgrIVefp%2BcgEfq8Q36%2FpmsQK4c7kj20mF0MLvcYZKdtozEqKG4pNsoEtOwa7nAUu77tI3bd8AmJ%0AfPRELU2IF%2BJ00GRFYngB0jfaO481wVsnvAYCI5Oy7xgYUHHIQSJ0jv%2Bmk98IkriLoQQ6b0pzauGX%0ALI2pgZlieCXiOgx%2BW29YYP6UtqVl%2FeBuxP%2FfnZv2bBAkEvxcjxPfboH8ehQU%2BVJrgR4KNE%2F2sAsS%0A4OPDOZvM5Btad6yLDeo3RVNRmtZJaqQfcZwiKNFEYyno9w9%2BGVb60YDzGXup%2FnorOwi1zOERXR%2F6%0AajkqAM3LLQ3TZRfOyVkXIymSo3OPu%2Fqx8OK0KBDH%2BmkQUvVkDVcTcytvSPmlTfthH%2BFwzLrLjw3S%0ABcGAIaVl8m3eU4%2BVi8jAuEiJZd0669YMNBPv4Bvt8HArompYebpYjg%2BylYqSuU9cRGtTpBXFFgCx%0Aw%2B6LFC3CIjfGIJoUEu3yWBvkIlw%3D'
}

# Session 생성
with requests.Session() as s:

    res_req = s.post('https://mid.mnet.com/web/login.asp', data=LOGIN_INFO)
    res = s.get('http://www.mnet.com/my/music/like.asp')
    # 인코딩 에러 시 인코딩
    # res.encoding = 'utf-8'

    soup = bs(res.text,'html.parser')
    he_coin = soup.select_one('#container5 > div.sideArea > div.photoBox > div.name')
    #로그인 유무 확인
    print ('mileage is', he_coin.get_text())

    artist = '방탄소년단'
    
    driver.get('http://search.mnet.com/search/artist.asp?q=' + artist)
    #driver.get('http://www.mnet.com/artist/181250/tracks?gcode=1&otype=1&pNum=' + 1)
    # song.asp? > 곡 검색 결과 
    # album.asp? > 앨범 검색 결과
    # artist.asp? > 아티스트 검색 결과
    # vod.asp? > 영상 검색결과 > 뮤직비디오 탭에서 한번더 필터링 필요

    html = driver.page_source
    soup = bs(html, "html.parser")
    artist_attr = soup.find('a', attrs={'class': 'search_link ng-binding'})
    
    for i in range(1, 50, 1):

        # 아티스트 주소
        # 곡 좋아요
        # artist_url = artist_attr.get('href') + '/tracks?gcode=1&otype=1&pNum=' + str(i)
        # 앨범 좋아요
        artist_url = artist_attr.get('href') + '/albums?gcode=1&otype=1&pNum=' + str(i)
        driver.get(artist_url)
        print(artist_url)

        html = driver.page_source
        soup = bs(html, "html.parser")
        # 곡 찾기
        #song_attr = soup.find_all('a', attrs={'class': 'MMLI_SongInfo'})
        # 앨범 찾기
        song_attr = soup.find_all('a', attrs={'class': 'b'})

        #곡 조건 문
        #if soup.find('a', attrs={'class': 'MMLI_SongInfo'}):

        # 앨범 조건문
        if soup.find('a', attrs={'class': 'b'}):
            print(" 값 있음 ")

            # 곡 조건
            # for song_attr in soup.find_all('a', attrs={'class': 'MMLI_SongInfo'}):
            # 앨범 조건
            for song_attr in soup.find_all('a', attrs={'class': 'b'}):
                songNum_index = song_attr.get('href')
                print(songNum_index)

                #곡 조건 분류
                #numbering = songNum_index.split('/track/')
                #앨범 조건 분류
                numbering = songNum_index.split('/album/')
                #numbering = filter(songNum_index.isdigit,songNum_index)
                # 곡
                # send_url = 'http://api.mnet.com/v1/like/0203/' + str(numbering[1])
                # 앨범
                send_url = 'http://api.mnet.com/v1/like/0202/' + str(numbering[1])
                print(send_url)

                send_data = {
                    # 0201 : 아티스트
                    # 0202 : 앨범
                    # 0203 : 곡
                    # 0209 : 영상
                    'url' : send_url,
                    'pnm' : 'titleMain,titleSub,location,imageUrl',
                    'titleMain': '-1',
                    'titleSub' : '-1',
                    'location' : '-1',
                    'imageUrl' : '-1'
                }

                #좋아요 데이터 전송
                res = s.post('http://www.mnet.com/common/proxy_social.asp', data=send_data)

        else:
            print(" 값 없음 ")
            break

#print(send_data)