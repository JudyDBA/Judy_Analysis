#!/usr/bin/env python3

import json
import time
import requests
import pandas as pd
import random
import os
import pprint
from urllib.parse import urlparse, parse_qs
import pycurl
import re

from datetime import datetime
from dateutil import parser
from lxml import html

pp = pprint.PrettyPrinter(indent=4)

AGENT = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
]

CONTENT_TYPE = "application/x-www-form-urlencoded; charset=UTF-8"
ACCEPT = "application/json, text/javascript, */*; q=0.01"
REFERER = 'http://www.theborn.co.kr'

l = []          ## 매장 목록
max_pages = 55    # 글어올 최대 페이지

## 매장 목록을 얻어 온다.
def LoadShopList():
    global l, max_pages

    if os.path.exists('shopInfo.json') :
        with open('shopInfo.json', encoding='utf-8') as f:
            ##print('file read')
            l = json.load(f)
            return

    # 매장 정보
    url = 'http://www.theborn.co.kr/tb/store_domestic.asp?page={}&pagesize=20'

    # 게시판 주소를 요청할 세션 생성
    session = requests.Session()
    session.headers.update({
        'User-Agent': random.choice(AGENT),
        'Referer': REFERER,
        'Content-Type': CONTENT_TYPE,
        'Accept': ACCEPT
    })

    i = 0
    subUrl = ''
    for p in range(1, max_pages+1):
        print('page : {}'.format(p))

        # 해당 페이지의 자유게시판 주소를 GET 메서드로 요청
        resp = session.get(url.format(p))
        resp.encoding = 'euc-kr'

        text = resp.text # Response 객체에서 text 필드만 따로 참조
        elem = html.fromstring(text) # lxml.html을 이용해서 html문서를 파싱

        # 구글 개발자 도구(F12)을 이용하여  내가 원하는 데이타 찾아 Copy>Copy Selector의 값을 copy 한다.
        # body > table > tbody > tr:nth-child(7) > td > center > table > tbody > tr:nth-child(4) > td.Brdbox.ali_Top > table:nth-child(2) > tbody > tr:nth-child(4)
        tagstors = elem.cssselect('td.Brdbox.ali_Top table')[2]

        for k in tagstors.cssselect('table tr')[3:]:
            td = k.cssselect('td')
            i=i+1
            if (i%2) <= 0 :
                continue

            #print(td[0].text_content().strip(), td[1].text_content().strip(), td[2].text_content().strip(), td[3].text_content().strip(), td[4].text_content().strip(), i)
            shop_url = td[2].cssselect('a')[0].get('href')
            params = urlparse(shop_url)
            query = parse_qs(params.query)

            ## 매장 상세 정보 얻어온다.
            subUrl = 'http://www.theborn.co.kr/tb' + shop_url[1:]+'&page={}&pagesize=20'
            subresp = session.get(subUrl.format(p))
            subresp.encoding = 'euc-kr'

            subtext = subresp.text
            subelem = html.fromstring(subtext)

            ## body > table > tbody > tr:nth-child(5) > td > center > table > tbody > tr:nth-child(4) > td:nth-child(3) > table.StoreBox > tbody > tr:nth-child(3) > td
            subdetails = subelem.cssselect('td.StoreInfo.ali_Top table tr')

            d = {'area':td[0].text_content().strip(),
                 'brand':td[1].text_content().strip(),
                 'shop_nm':td[2].text_content().strip(),
                 'shop_addr':td[3].text_content().strip(),
                 'shop_number':td[4].text_content().strip(),
                 'shop_seq': int(query['shop_seq'][0]),
                 'brand_seq': int(query['shop_brand_seq'][0]),
                 'shop_url':shop_url,
                 'locate':subdetails[1].text_content().strip(),
                 'openning_hr': subdetails[3].text_content().strip(),
                 'holiday':subdetails[4].text_content().strip(),
                 'Seats_num':subdetails[5].text_content().strip(),
                 'parking':subdetails[6].text_content().strip(),
                 'coord':shopCoord( td[3].text_content().strip() ),
                 }

            print(d)
            #exit()
            l.append(d)

    ## 중복으로 읽히지 않도록 파일의 내용을 저장 한다.
    with open('shopInfo.json', 'w', encoding='utf-8') as fw:
        js = json.dumps(l , indent=4, ensure_ascii=False)
        fw.write(js)


## 매장 위도와 경도 추출
## http://chongmoa.com/webtool/2667
## https://developers.google.com/maps/documentation/geocoding/intro
def shopCoord(addr):
    apiURL = 'http://maps.googleapis.com/maps/api/geocode/json??sensor=false&language=ko&address={0}'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    ##addr = "경기도 용인시 기흥구 마북동 연원마을 현대 아파트 101동 302호"
    ## req = requests.post(apiURL.format(addr), headers=headers)
    response  = requests.get(apiURL.format(addr), headers=headers, verify=True)

    # Check for HTTP codes other than 200
    if response .status_code != 200:
        print('Status:', response .status_code, 'Problem with the request. Exiting.')
        exit()

    data = response.json()
    ## print(data);

    ## 위도 경도 정보
    #print( data['results'][0]['geometry']['location'] )
    print (addr)
    d = {}

    if data['status'] == "ZERO_RESULTS" :
        d = [-1,-1]
    else :
        d = [data['results'][0]['geometry']['location']['lng'], data['results'][0]['geometry']['location']['lat'] ]

    return d


    '''
    c = pycurl.Curl()
    c.setopt(c.URL, apiURL)
    c.setopt(c.HTTPHEADER, {
        'User-Agent': random.choice(AGENT),
        'Referer': REFERER,
        'Content-Type': CONTENT_TYPE,
        'Accept': ACCEPT
    })
    c.setopt(c.POSTFIELDS, data)
    c.setopt(c.VERBOSE, True)
    c.perform()
    '''
    
def LoadShop():
    global l
    LoadShopList()
    return l


def main():
    LoadShopList()
    pp.pprint(l)
    # df = pd.DataFrame(l)
    # print(df)
    ##print(df.index)
    # print(df.columns)
    # print(df['Seats_num'])

    # http://chrisalbon.com/python/pandas_create_column_with_loop.html
    ##좌석수의 문자열 정보를 숫자로 변환해서 저장 한다.
    ##seacount = []
    ##for seas in df['Seats_num']:
    ##    seacount = re.compile('(\d+)석').search(seas).group(0)
    ##
    ##print(seacount)

    '''
    print('Analyze')
    print( df.head() )
    print('')
    print('총 매장수 : ' , df['Seats_num'].count() )
    brand_cnt = df['brand'].unique()
    print('총 브랜드 수: ', len(brand_cnt))
    print('')
    print('=========================')
    print('총 브랜드 별 매장 수')
    print('')
    print(df['brand'].value_counts())
    print('=========================')
    print('지점별 매장수')
    print(df['shop_nm'].value_counts())
    '''

    ## 총 매장수
    ## 브랜드 갯수
    ## 지점 갯수
    ## 브랜드별 매장수 및 가장 많이 매장을 보유한 브랜드?
    ## 최대 군집된 지역(시각화)
    ## 최대 매장(판단 근거 좌석수) -->  좌석수 산정... reg 체크 하자.
    ## 각 매장별 음식맛 성공/실패?? --> 텍스트 마이닝

if __name__ == "__main__":
    main()

