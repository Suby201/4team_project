import os
import re

import pandas as pd

# 연도별 자격증 합격률 csv 파일 불러오기 ('UTF-8'인코딩이 아닌 'EUC-KR' 인코딩이라 설정)
pr_df = pd.read_csv('data\passing_rate.csv', encoding='EUC-KR')
print("----------------------------------------------------------------")
print(f"pr_df 컬럼들: \n{pr_df.columns}") # Index(['종목별', '항목', '단위', '2019 년', '2020 년', '2021 년', '2022 년', '2023 년','Unnamed: 8'],dtype='object')
print("----------------------------------------------------------------")
print("pr_df 길이: {}".format(len(pr_df))) # pr_df 길이: 6832


# 'Unnamed: 8'이라는 필요없는 컬럼 drop
pr_df = pr_df.drop(columns='Unnamed: 8')
print("----------------------------------------------------------------")
# 데이터 결측치 %로 확인
print("전체데이터 길이: {}".format(len(pr_df)))
print()
print(f"19년도 결측치: {pr_df['2019 년'].isnull().sum()/len(pr_df):.04f}")
print(f"20년도 결측치: {pr_df['2020 년'].isnull().sum()/len(pr_df):.04f}")
print(f"21년도 결측치: {pr_df['2021 년'].isnull().sum()/len(pr_df):.04f}")
print(f"22년도 결측치: {pr_df['2022 년'].isnull().sum()/len(pr_df):.04f}")
print(f"23년도 결측치: {pr_df['2023 년'].isnull().sum()/len(pr_df):.04f}")
print("----------------------------------------------------------------")
# 결측치가 약 1%에서 약 2% 사아이기에 결측치를 전부 0으로 대체
pr_df = pr_df.fillna(0)

print()

# 혹시 모르니까 결측값 다시 확인
print(f"전체 결측값: \n{pr_df.isnull().sum()}") # 없음
print("----------------------------------------------------------------")
print()

# pr_df의 합격 인원만 가져오기
people_pr_df = pr_df.loc[pr_df['단위'] != '%'].reset_index(drop=True)

# pr_df의 합격률만 가져오기
per_pr_df = pr_df.loc[pr_df['단위'] == '%'].reset_index(drop=True)

# 각 데이터 프레임 길이
print("dataFrame length")
print("people_per_df: {}\nper_pr_df: {}".format(len(people_pr_df), len(per_pr_df)))

print("----------------------------------------------------------------")
# str_param = ("정보처리기  사").replace(' ','')

# pr_df.loc[
#         (pr_df['종목별'].str.contains(str_param))
#         &(pr_df['단위']=='%') 
#         &(pr_df['2019 년']!=100)&(pr_df['2020 년']!=100)&(pr_df['2021 년']!=100)
#         &(pr_df['2019 년']!=0)&(pr_df['2020 년']!=0)&(pr_df['2021 년']!=0)
#         ,
#         '종목별':'2021 년' # 이거 대신 ['종목별','항목 ','2019 년','2020 년','2021 년'] 이거도 가능 # 이거 안쓰면 전체 컬럼 값 출력
# ].sort_values(by='2019 년', ascending=True).reset_index(drop=True)
print("----------------------------------------------------------------")

