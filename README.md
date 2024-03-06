# 영화 추천 및 예매 시스템

## 프로젝트 개요
이 프로젝트는 PostgreSQL을 사용한 사용자 기반 협업 필터링 알고리즘 기반 영화 추천 및 예매 시스템을 개발합니다. 사용자 맞춤형 영화 추천 기능을 제공하며, Tkinter를 사용한 사용자 친화적 인터페이스를 통해 쉽게 영화를 검색하고 예매할 수 있습니다.

## 기술 스택
- 언어: Python
- 라이브러리: psycopg2, tkinter, tkcalendar, string, hashlib, pandas, numpy, scikit-learn

## 주요 기능
- 사용자별 맞춤 영화 추천
- 영화 검색 및 예매
- 예매 정보 조회 및 평점 작성
- 광고 시스템을 통한 수익 창출

## 사용자 역할
- 고객: 영화 검색, 추천 영화 이용, 영화 예매, 예매 정보 조회 및 평점 작성
- 관리자: 상영관 정보 등록 및 관리, 상영 시간표 등록 및 관리, 사용자 관리
- 배급사: 영화 등록 및 관리, 광고 등록 및 삭제, 예매율 조회

## 프로그램 실행 전 준비 사항
database 폴더의 databaseManager.py 파일을 열어 line 7의 db_config 변수를 사용자 환경에 맞는 DB 계정 정보로 작성하면 된다.
사용한 db_config 변수는 다음과 같다:
        self.db_config = {
            'dbname': 'db_movie',
            'user': 'du_movie',
            'password': '4510471',
            'host': '::1',
            'port': '4510'
        }

이후, makeTable.py를 실행시켜 Table을 생성하고, makeTestData.py를 실행시켜 테스트 데이터를 생성한다.

테스트 데이터 생성 시, admin, customer, distributor 권한이 부여된 ‘관리자 산지니’, ‘사용자 산지니’, ‘배급사 산지니’가 생성된다. 이들의 아이디 및 비밀번호는 각각 admin, customer, distributor 이다.

모든 데이터가 생성이 완료되면, main.py를 실행하여 프로그램을 시작하면 된다.
