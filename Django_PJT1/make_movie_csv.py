import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
from datetime import datetime

today = datetime.today().strftime('%Y%m%d')

writer1 = csv.writer(open('make_movie_csv.csv', 'w', encoding='utf-8', newline=''))
writer2 = csv.writer(open('make_related_table_csv.csv', 'w', encoding='utf-8', newline=''))
# writer.writerow(['MovieCd', 'movieName', 'movieNameE', 'pubDate', 'runtime', 'genre', 'director', 'userRating', 'poster_url', 'description'])
# 영화          대표코드(네이버),영화명(국문),영화명(영문),  개봉연도,   상영시간,   장르,      감독,     실관람객평점, ,  포스터,     '줄거리'

# 최근상영영화 중 평점 높은 50개
# url = f'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date={today}'
for page in range(1, 2):

    url = f'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date={today}&page={page}'
    headers = {'User-Agent': ':)'} # 딕셔너리(키, 밸류)

    response = requests.get(url, headers=headers).text
    text = BeautifulSoup(response, 'html.parser')
    rows = text.select('.tit5')
    num = 1
    movie_id = 1
    for row in rows:
        
        # 1. 영화코드 가져오기 >> 네이버 영화 상세 페이지로 가서 다 긁어올 것임
        target = str(row.select_one('div > a'))
        temp = target[37:43]
        if temp[-1] == '\"':
            temp = temp[:-1]
        MovieCd = int(temp)
        print(MovieCd)

        # 영화 상세 페이지로 이동
        url2 = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code={MovieCd}'
        # url2 = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code=176354'
        res = requests.get(url2, headers=headers).text
        text = BeautifulSoup(res, 'html.parser')
        
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
        tempUrl = urlopen(f"https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={MovieCd}")
        tempRes = BeautifulSoup(tempUrl, 'html.parser')
        poster_url = tempRes.find('img', id="targetImage").get('src')
        print(poster_url)

        # 11. description
        d = text.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p').text
        description = d.replace('\r', '').replace('\xa0', ' ')
        # from IPython import embed; embed()
        print(description)
        # print(MovieCd, movieName, movieNameE, pubDate, runtime, genre, director, userRating, poster_url, description)
        writer1.writerow([num, MovieCd, movieName, movieNameE, pubDate, runtime, director, userRating, poster_url, description]) 
        writer2.writerow([num, movie_id, genre_id])
        num+=1
        movie_id+=1