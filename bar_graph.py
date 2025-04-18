import os  # 운영체제 관련 기능을 제공하는 모듈
import re  # 정규 표현식 관련 기능을 제공하는 모듈

import pandas as pd  # 데이터 분석 및 조작을 위한 라이브러리

# 연도별 자격증 합격률 csv 파일 불러오기 ('UTF-8' 인코딩이 아닌 'EUC-KR' 인코딩이라 설정)
pr_df = pd.read_csv('data\passing_rate.csv', encoding='EUC-KR')
# pandas의 read_csv 함수를 사용하여 'data' 폴더 내의 'passing_rate.csv' 파일을 읽어 DataFrame 객체 'pr_df'에 저장합니다.
# encoding='EUC-KR' 파라미터는 파일의 인코딩 방식을 명시적으로 지정합니다.

print("----------------------------------------------------------------")
print(f"pr_df 컬럼들: \n{pr_df.columns}")
# DataFrame 'pr_df'의 컬럼 이름을 출력합니다. 이는 데이터의 구조를 파악하는 데 유용합니다.
# 예상 출력: Index(['종목별', '항목', '단위', '2019 년', '2020 년', '2021 년', '2022 년', '2023 년','Unnamed: 8'], dtype='object')
print("----------------------------------------------------------------")
print("pr_df 길이: {}".format(len(pr_df)))
# DataFrame 'pr_df'의 행의 개수 (길이)를 출력합니다. 이는 전체 데이터의 크기를 나타냅니다.
# 예상 출력: pr_df 길이: 6832

# 'Unnamed: 8'이라는 필요없는 컬럼 drop
pr_df = pr_df.drop(columns='Unnamed: 8')
# DataFrame 'pr_df'에서 'Unnamed: 8'이라는 이름의 컬럼을 제거합니다.
# drop 함수의 columns 파라미터에 제거할 컬럼 이름을 리스트 형태로 전달합니다.

print("----------------------------------------------------------------")
# 데이터 결측치 %로 확인
print("전체데이터 길이: {}".format(len(pr_df)))
# 컬럼 제거 후 DataFrame 'pr_df'의 전체 데이터 길이를 다시 출력합니다.
print()
print(f"19년도 결측치: {pr_df['2019 년'].isnull().sum()/len(pr_df):.04f}")
# '2019 년' 컬럼의 결측치 개수를 전체 데이터 길이로 나누어 결측치 비율을 소수점 4자리까지 출력합니다.
# isnull() 함수는 각 요소가 결측치인지 여부를 True/False로 반환하고, sum() 함수는 True의 개수를 세어 결측치 개수를 얻습니다.
print(f"20년도 결측치: {pr_df['2020 년'].isnull().sum()/len(pr_df):.04f}")
# '2020 년' 컬럼의 결측치 비율을 계산하여 출력합니다.
print(f"21년도 결측치: {pr_df['2021 년'].isnull().sum()/len(pr_df):.04f}")
# '2021 년' 컬럼의 결측치 비율을 계산하여 출력합니다.
print(f"22년도 결측치: {pr_df['2022 년'].isnull().sum()/len(pr_df):.04f}")
# '2022 년' 컬럼의 결측치 비율을 계산하여 출력합니다.
print(f"23년도 결측치: {pr_df['2023 년'].isnull().sum()/len(pr_df):.04f}")
# '2023 년' 컬럼의 결측치 비율을 계산하여 출력합니다.
print("----------------------------------------------------------------")
# 결측치가 약 1%에서 약 2% 사아이기에 결측치를 전부 0으로 대체
pr_df = pr_df.fillna(0)
# DataFrame 'pr_df'의 모든 결측치(NaN) 값을 0으로 채웁니다.
# fillna() 함수는 결측치를 지정된 값으로 채우는 데 사용됩니다.

print()

# 혹시 모르니까 결측값 다시 확인
print(f"전체 결측값: \n{pr_df.isnull().sum()}")
# fillna() 함수 적용 후 DataFrame 'pr_df'의 컬럼별 결측치 개수를 다시 확인하여 결측치가 모두 0으로 대체되었는지 검증합니다.
# 예상 출력:
# 전체 결측값:
# 종목별    0
# 항목      0
# 단위      0
# 2019 년    0
# 2020 년    0
# 2021 년    0
# 2022 년    0
# 2023 년    0
# dtype: int64
print("----------------------------------------------------------------")
print()

# pr_df의 합격 인원만 가져오기
people_pr_df = pr_df.loc[pr_df['단위'] != '%'].reset_index(drop=True)
# DataFrame 'pr_df'에서 '단위' 컬럼의 값이 '%'가 아닌 행들만 선택하여 새로운 DataFrame 'people_pr_df'를 생성합니다.
# loc[] 인덱서를 사용하여 조건에 맞는 행을 선택합니다.
# reset_index(drop=True)는 새로운 DataFrame의 인덱스를 0부터 시작하도록 재설정하고, 이전 인덱스를 삭제합니다.

# pr_df의 합격률만 가져오기
per_pr_df = pr_df.loc[pr_df['단위'] == '%'].reset_index(drop=True)
# DataFrame 'pr_df'에서 '단위' 컬럼의 값이 '%'인 행들만 선택하여 새로운 DataFrame 'per_pr_df'를 생성합니다.
# 이는 합격률 데이터를 분리하는 작업입니다.

# 각 데이터 프레임 길이
print("dataFrame length")
print("people_per_df: {}\nper_pr_df: {}".format(len(people_pr_df), len(per_pr_df)))
# 생성된 'people_pr_df' (합격 인원)와 'per_pr_df' (합격률) DataFrame의 길이를 각각 출력하여 데이터가 올바르게 분리되었는지 확인합니다.

print("----------------------------------------------------------------")