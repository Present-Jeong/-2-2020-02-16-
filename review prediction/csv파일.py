from selenium import webdriver
import time
import pandas as pd
keyword = input("데이터를 얻고 싶은 강의의 학수번호를 입력하시오.")
professor = input("데이터를 얻고 싶은 교수명을 입력하시오.")

driver = webdriver.Chrome("C:/chromedriver_win32/chromedriver.exe")

url = 'http://klue.kr/'
driver.get(url)
time.sleep(2)

f = open(keyword + '.csv', 'w')
f.write("과목명, 교수님명, 평점\n")

reviews = driver.find_elements_by_css_selector('span.index-menubar-detail')
review=reviews[1]
review.click()
info = driver.find_elements_by_css_selector('input.modal-login-input')
id = info[0]
id.send_keys("kree0920")
pw = info[1]
pw.send_keys("aa0920@@")

btn = driver.find_element_by_css_selector("button.modal-login-submit").click()
time.sleep(1)
btn1 = driver.find_element_by_css_selector("li.index-menubar-detail").click()
time.sleep(1)

searchbar = driver.find_element_by_css_selector("input.lecture-search-content-context-text")
searchbar.send_keys(keyword)
btn2 = driver.find_element_by_css_selector("img.lecture-search-content-context-btn").click()



SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    time.sleep(3)
    container = driver.find_elements_by_css_selector("div.lecture-search-result")
    length = len(container)
    for cont in container:
        lecture_names = cont.find_element_by_css_selector("span.lecture-search-result-code").text
        professor_names = cont.find_element_by_css_selector("div.lecture-search-result-professor span").text
        whole = cont.find_elements_by_css_selector("span.lecture-search-result-rate")

        f.write(lecture_names + "," + professor_names + ",")
        for wh in whole:
            if (float(wh.text[2:])) == 0.00:
                f.write('' + '\n')
            else:
                f.write(wh.text[2:] + '\n')



    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    for i in range(length):
        driver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, container[i])
f.close()

driver.close()
# ----------------------------------------------수정님 코드 ---------------------------------------------------------------------------------
# 파일 변환
# 두분 파일 결합하기! (pandas를 이용해서 두 파일 병합)
file_name = str(keyword) + '.csv'
csv_data = pd.read_csv(file_name, encoding='CP949', error_bad_lines=False)
df = pd.read_csv('kupid.csv', encoding='CP949', error_bad_lines=False)
# 혜성님 파일 pandas로 해석하기
df2 = df.drop_duplicates('과목명')
# 과목에서 중복되는 학수번호 먼저 삭제
df3 = pd.merge(df2, csv_data, on='과목명')
# 두 파일 병합하기 merge이용
df4 = df3.drop(df3.columns[1], axis='columns')
# 필요없는 1번째 열 column 삭제
print(df4)
# 최종 파일로 완성! (수정님꺼랑 거의 비슷한데 폐강강의가 사라지고 실시간 업데이트된 kupid 파일 이용가능

#-----------------------------최종 만든 csv 파일로 머신러닝하기----------------------------------------------------------
#recommend 멘토님 파일에서 우리 버전에 맡게 변수랑 데이터 수정

from surprise import SVD
from surprise.model_selection import cross_validate

from surprise import Dataset
from surprise import Reader

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df4, reader)

r_system = SVD()

data = Dataset.load_from_df(df4, reader)
r_system.fit(data.build_full_trainset())

def get_rec_point(name, movie):
    return r_system.predict(name, movie).est

keyword2 = str(keyword)
professor2 = str(professor)
expect1 = get_rec_point(keyword2, professor)

print('입력한 학수번호와 교수 수업의 예상 평점은?', expect1)
# 예상 평점이 나옴!

#-----------------------------최종 만든 csv 파일로 웹페이지 만들기----------------------------------------------------------
# 여기는 잘 몰라서 그냥 recommend 복붙, 수정 필요 ㅠ

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/<name>/<movie>')
def first(subject_code, professor_):
    grade = round(get_rec_point(subject_code, professor_), 2)
    return render_template('index.html', grade=grade, subject_code=subject_code, professor_=professor_)


if __name__ == '__main__':
    app.run()

print('http://127.0.0.1:5000/')
