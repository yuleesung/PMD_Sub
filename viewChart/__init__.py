# RUN은 start_server.py 에서 !!!!!!!

from flask import Flask
from flask import request
from flask_cors import CORS
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import pandas as pd
from pandas import Series, DataFrame
import datetime


#크로스 도메인 오류를 해결하기 위해 
# flask-cors패키지를 설치해 둬야 한다.
app = Flask(__name__)
CORS(app)






# 맵 차트 영역
@app.route("/mapChart", methods=['POST']) #post방식
#@app.route("/mapChart") #get방식
def mapChart():
    '''
    <<< hrd 지역 값 >>>
    11' : 서울, '26' : 부산, '27' : 대구, '28' : 인천 '29' : 광주, '30' : 대전, '31' : 울산, '36' : 세종, 
    41' : 경기, '42' : 강원, '43' : 충북, '44' : 충남, '45' : 전북, '46' : 전남, '47' : 경북, '48' : 경남, '50' : 제주
    '''
    
    # 날짜 구하기
    now = datetime.datetime.now()
    after = now + datetime.timedelta(days=365)

    now1 = str(now)[0:10]
    after1 = str(after)[0:10]
    now2 = now1.split('-')
    after2 = after1.split('-')
    
    now3 = ''
    after3 = ''
    
    for i in now2:
        now3 += i
        
    for i in after2:
        after3 += i
    
    
    # 지역 값을 list에 저장
    loc = ['11','26','27','28','29','30','31','36','41','42','43','44','45','46','47','48','50']
    
    # 결과값을 담을 공간
    row = [] 
    
    for url in loc:
        # 지역별 url 생성
        spec = "http://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=XML&authKey=Aflc7YIke55KR8qliEbmLwJGWIpsH2DL&pageNum=1&pageSize=100&srchTraStDt="+now3+"&srchTraEndDt="+after3+"&outType=1&sort=ASC&sortCol=TR_STT_DT&srchTraArea1="+url
        
        # row에 담을 지역 값
        city = '' 
        name = ''
        if(url == '11'):
            city = "KR-11" # 차트에 들어갈 지역코드
            name = "서울"
        if(url == '26'):
            city = "KR-26"
            name = "부산"
        if(url == '27'):
            city = "KR-27"
            name = "대구"
        if(url == '28'):
            city = "KR-28"
            name = "인천"
        if(url == '29'):
            city = "KR-29"
            name = "광주"
        if(url == '30'):
            city = "KR-30"
            name = "대전"
        if(url == '31'):
            city = "KR-31"
            name = "울산"
        if(url == '36'):
            city = "KR-50"
            name = "세종"
        if(url == '41'):
            city = "KR-41"
            name = "경기"
        if(url == '42'):
            city = "KR-42"
            name = "강원"
        if(url == '43'):
            city = "KR-43"
            name = "충북"
        if(url == '44'):
            city = "KR-44"
            name = "충남"
        if(url == '45'):
            city = "KR-45"
            name = "전북"
        if(url == '46'):
            city = "KR-46"
            name = "전남"
        if(url == '47'):
            city = "KR-47"
            name = "경북"
        if(url == '48'):
            city = "KR-48"
            name = "경남"
        if(url == '50'):
            city = "KR-49"
            name = "제주"


        res = urlopen(spec).read().decode('euc-kr')  # 파일 읽기전용   #.decode('euc-kr')
        xmlDoc = ET.fromstring(res) #xml문서화
    
        cnt = xmlDoc.find('scn_cnt').text # 지역별 훈련과정 갯수
        
        row.append({'value':cnt,'id':city, 'name':name}) # 지역, 갯수를 row에 추가
    
    df = DataFrame(row) 
    
    json = df.to_json(orient='records') # 결과 값을 json으로 변환
    
    
    return json




# 스택형차트 영역
@app.route("/stackChart", methods=['POST']) #post방식
#@app.route("/stackChart") #get방식
def stackChart():
    
    # 날짜 구하기
    now = datetime.datetime.now()
    after = now + datetime.timedelta(days=365)
    
    now1 = str(now)[0:10]
    after1 = str(after)[0:10]
    now2 = now1.split('-')
    after2 = after1.split('-')
    
    now3 = ''
    after3 = ''
    
    for i in now2:
        now3 += i
        
    for i in after2:
        after3 += i
    
    
    # 결과값을 담을 공간
    row_stack = []
    
    name="" # 자바에서 받은 파라미터 값 담을변수
 
    if request.method == 'POST':  #POST방식으로 get
        name = request.form.get("srchKeco1")
    
    cod_val = name #spec에 넣을 코드값
    
    spec = "http://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=XML&authKey=Aflc7YIke55KR8qliEbmLwJGWIpsH2DL&pageNum=1&pageSize=100&srchTraStDt="+now3+"&srchTraEndDt="+after3+"&outType=1&sort=ASC&sortCol=TR_STT_DT&srchKeco1="+cod_val
    res = urlopen(spec).read().decode('euc-kr')
    xmlDoc = ET.fromstring(res)
    
    
    scn_cnt = xmlDoc.find('scn_cnt').text # 유형별 훈련과정 갯수
    page_val = (int(scn_cnt)/100)+1  # 페이지 값
    
    nowPage = 1 #url에 넣을 페이지값
    while nowPage<=page_val:
        # 각 유형별 페이지만큼 반복문으로 교육기관 주소를 가져오는 목적 
        spec2 = "http://www.hrd.go.kr/jsp/HRDP/HRDPO00/HRDPOA60/HRDPOA60_1.jsp?returnType=XML&authKey=Aflc7YIke55KR8qliEbmLwJGWIpsH2DL&pageNum="+str(nowPage)+"&pageSize=100&srchTraStDt="+now3+"&srchTraEndDt="+after3+"&outType=1&sort=ASC&sortCol=TR_STT_DT&srchKeco1="+cod_val
        res2 = urlopen(spec2).read().decode('euc-kr')
        xmlDoc2 = ET.fromstring(res2)
        
        srchList = xmlDoc2.find('srchList')
        
        for node in srchList:
            address = node.find('address').text # 지역 값
            row_stack.append({'address':address}) # 배열에 추가
           
        nowPage += 1
    
    df = DataFrame(row_stack)

    df_res = df.address.value_counts().rename_axis('address').reset_index(name='counts')
    
    df_city = df_res.address.str.split(' ', expand=True)[0]
    df_loc = df_res.address.str.split(' ', expand=True)[1]
    
    df_res['city'] = df_city
    df_res['location'] = df_loc
    
    del df_res['address']
    
    json = df_res.to_json(orient='records')
    
    return json









