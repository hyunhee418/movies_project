import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from datetime import datetime

writer1 = csv.writer(open('add_movie_csv.csv', 'w', encoding='utf-8', newline=''))
writer2 = csv.writer(open('add_related_table_csv.csv', 'w', encoding='utf-8', newline=''))
code_li = [36732, 179482, 182205, 49336, 34521, 68695, 92075, 149236, 45290, 143435, 121788, 62586, 88669, 47370, 122489, 91031, 146480, 88426, 52515, 66464, 66440, 34501, 38899, 118955, 152656, 51282, 52515, 39440, 136869, 163788, 17170, 109905, 38444, 62266, 129049, 34522, 47152, 17773, 82473, 39841, 35901, 154222, 107370, 47229, 10016, 57723, 77768, 130013, 167651, 11119, 32686, 89755, 50869, 73372, 92823, 63513, 106360, 52962, 80707, 164932, 136873, 42809, 123386, 123277, 181414, 101966, 39427, 73398, 38898, 121051, 150198, 34324, 115298, 180390, 167613, 130850, 134963, 154449, 52120, 120157, 31726, 76667, 165461, 94775, 42842, 102875, 151728, 175322, 51143, 77855]
num = 51
movie_id = 51

for code in code_li:
    
    headers = {'User-Agent': ':)'} # 딕셔너리(키, 밸류)
    url = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code={code}'
    response = requests.get(url, headers=headers).text
    text = BeautifulSoup(response, 'html.parser')
    # #content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)
    # 2. movieName(영화명-국문)
    movieName = text.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
    print(movieName)

    # 3. movieNameE(영화명-영문) / pubDate(개봉연도)
    e = text.select_one('#content > div.article > div.mv_info_area > div.mv_info > strong').text.split(',')
    print(e)
    try:
        if len(e) == 3:
            movieNameE = ', '.join([e[0], e[1]])
            pubDate = int(e[2][1:])
        elif len(e) == 2:        
            movieNameE = e[0]
            pubDate = int(e[1][1:])
    except ValueError:
        pubDate = 0
    print(movieNameE)
    print(pubDate)

    # # 4. watch_grade(관람등급)
    # # watch_grade = text.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a').text:
    # if '#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a' in text:
    #     #content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(1)
    #     print('yes')
    # else:
    #     print('no')
    # # print(watch_grade)

    # 5. runtime(상영시간)
    runtime = text.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(3)').text[:-1]
    print(runtime)

    # 6. genre(장르)
    # 장르가 2개인 경우는 추후에 보완하도록 하자! 없으면 None 이 나오기 때문에 있을 때만 genre_id에 추가하면 됨. pjt10에서처럼 json 파일에 [1, 5] 이런 식으로....?
    # genreId2 = str(text.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a:nth-child(2)'))
    try:
        genre_id = str(text.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p > span:nth-child(1) > a'))[46:48]
        if genre_id[-1] == '\"':
            genre_id = genre_id[:-1]
        genre_id = int(genre_id)
        print(genre_id)
    except ValueError:
        genre_id = 0
    
    # 7. director(감독)
    director = text.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a').text
    print(director)

    # 8. userRating
    
    u = round(float(str(text.select_one('#pointNetizenPersentBasic > span')).split('width:')[1].split('%')[0]) / 10, 2)
    if u == '없음':
        userRating = 0.0
    else:
        userRating = float(u)
    print(userRating)

    # 9. audience
    # what = text.select_one('')
    # print(what)

    # 10. poster_url(포스터)
    tempUrl = urlopen(f"https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={code}")
    tempRes = BeautifulSoup(tempUrl, 'html.parser')
    poster_url = tempRes.find('img', id="targetImage").get('src')
    print(poster_url)

    # 11. description
    d = text.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text
    description = d.replace('\r', '').replace('\xa0', ' ')
    # from IPython import embed; embed()
    print(description)
    # print(MovieCd, movieName, movieNameE, pubDate, runtime, genre, director, userRating, poster_url, description)
    writer1.writerow([num, code, movieName, movieNameE, pubDate, runtime, director, userRating, poster_url, description]) 
    writer2.writerow([num, movie_id, genre_id])
    num+=1
    movie_id+=1