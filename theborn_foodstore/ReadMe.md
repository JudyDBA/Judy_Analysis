# 더본 코리아 브랜드 및 지역별 매장 분석(백주부)

> 프로젝트 시작 동기 : 시댁 근처에서 이동중 백주부 프렌차이즈 지점이 4곳이 넘더라… 백주부 아저씨 얼마나 많은 매장을 갖고 있는 거야? 라는 궁굼함이...
> 데이터 수집 방법 : http://www.theborn.co.kr/tb/store_domestic.asp?page={}&pagesize=20 매장정보 파이썬 스크립트로 크롤링

1. 매장 찾기 게시글의 목록과 매장 상세 내용
http://www.theborn.co.kr/tb/store_domestic.asp
http://www.theborn.co.kr/store_detail.asp?shop_seq=1&amp;st_seoul=&amp;st_region=&amp;shop_seoul=&amp;t_shop_region=&amp;shop_brand_seq=2&amp;str_na="

2. 위도 경도 알기 위해서 네이버 개발자 센터키를 등록해서 가져오자.
http://amornatura.tistory.com/84

3. 추가 설치 파이썬 패키지 
```bash
	easy_install pip cssselect
	easy_install pip pycurl
```
