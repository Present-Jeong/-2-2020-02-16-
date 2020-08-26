import pandas as pd
from selenium import webdriver
from csv import reader
import time

print('2020년 공공기관 채용계획')

# month = input('원하는 인턴 모집 시기를 입력하세요:')
# month2 = input('상반기 또는 하반기를 선택하세요:')
area = input('원하는 근무지를 입력하세요:')
pay = input('원하는 연봉을 입력하세요:')
pay = int(pay)
csv_data = pd.read_csv('corrected.csv', encoding='CP949', error_bad_lines=False)
reader = reader(csv_data)
csv_data1 = csv_data[' 연봉']
csv_data2 = csv_data[' 근무지']
f = open('fit.csv','w')
f.write('회사명,페이지,연봉,성과금 포함,근무지,인턴 모집 시기,모집 인원,직무 내용\n')

#  연봉
# for A in range(1,141):
#     df = csv_data.loc[A].values
#     list2 = list(df)
#     df2 = csv_data.loc[A,[' 연봉']]
#     df3 = csv_data.loc[A,' 근무지']
#     if int(df2) > pay:
#         f.write(str(list2)+'\n')
#     else :
#         pass
#--------------------------------------------------------------------------------
# 근무지
for A in range(1,141):
    df = csv_data.loc[A].values
    list2 = list(df)
    df2 = csv_data.loc[A,[' 연봉']]
    df3 = csv_data.loc[A,' 근무지']
    if area in df3:
        f.write(str(list2)+'\n')
    else:
        pass
#--------------------------------------------------------------------------------
#  인턴 모집 시기
# for A in range(1,141):
#     df = csv_data.loc[A].values
#     list2 = list(df)
#     df4 = csv_data.loc[A,' 인턴 모집 시기']
#     if month in df4 or month2 in df4:
#         f.write(str(list2)+'\n')
#     else :
#         pass
#------------------------------------------------------------------------------
f.close()
fit_data = pd.read_csv('fit.csv', encoding='CP949', error_bad_lines=False)
fit_data2 = fit_data.replace("'",'',regex = True)
fit_data2 = fit_data2.replace(['\[','\]'],'',regex = True)
fit_data2.to_csv('fit.csv',encoding='CP949',index = False)

name = input('원하는 회사 이름:')
driver = webdriver.Chrome('chromedriver')
url = 'https://www.naver.com'
driver.get(url)
driver.find_element_by_css_selector('input#query.input_text').send_keys(name)
driver.find_element_by_css_selector('button#search_btn.sch_smit').click()
time.sleep(0.5)
driver.find_element_by_css_selector('a.url').click()
driver.close()
