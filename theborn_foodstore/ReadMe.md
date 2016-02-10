# 더본 코리아 브랜드 및 지역별 매장 분석(백주부)

> 파이썬 언어를 이용하여 더본 코리아 프렌차이즈 웹 사이트 크롤링을 통해 매장 정보 및 지역 정보를 도출하여 브랜드, 매장수, 지역 정보 시각화 

1. 매장 찾기 게시글의 목록과 매장 상세 내용
 * http://www.theborn.co.kr/tb/store_domestic.asp
 * http://www.theborn.co.kr/store_detail.asp?shop_seq=1&amp;st_seoul=&amp;st_region=&amp;shop_seoul=&amp;t_shop_region=&amp;shop_brand_seq=2&amp;str_na="

2. 위도 경도 알기 위해서  Google Maps Geocoding API
 * http://amornatura.tistory.com/84
 
3. 기본 사용한 라이브러리  
 pandas, numpy, matplotlib.pyplot, folium

4. 추가 설치 파이썬 패키지 
```bash
	easy_install pip cssselect
	easy_install pip pycurl
```
