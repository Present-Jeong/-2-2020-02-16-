import pandas as pd
import csv
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
matrix = []
f = open('kupid.csv', 'r')
csvReader = csv.reader(f)

for row in csvReader:
    matrix.append(row)
f.close()

f_2 = open('klue.csv', 'w')
f_2.write("교양과목, 교수님\n")

for i in range (0,len(matrix)+1) :
    keyword = matrix[i+1][0] + ' ' + matrix[i+1][1]
    print(keyword)

    driver = webdriver.Chrome('C:/chromedriver_win32/chromedriver')

    url = 'http://klue.kr/'
    driver.get(url)
    time.sleep(2)



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
                    f_2.write('' + '\n')
                else:
                    f_2.write(wh.text[2:] + '\n')


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
    driver.close()

f_2.close()
# ----------------------------------------------수정님 코드 ---------------------------------------------------------------------------------
# 파일 변환
file_name = 'klue.csv'
csv_data = pd.read_csv(file_name, encoding='CP949', error_bad_lines=False)
#-----------------------------최종 만든 csv 파일로 머신러닝하기----------------------------------------------------------
#recommend 멘토님 파일에서 우리 버전에 맡게 변수랑 데이터 수정

from surprise import SVD
from surprise.model_selection import cross_validate

from surprise import Dataset
from surprise import Reader

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(csv_data, reader)

r_system = SVD()

r_system.fit(data.build_full_trainset())

def get_rec_point(name, movie):
    return r_system.predict(name, movie).est

keyword = input("데이터를 얻고 싶은 강의의 학수번호를 입력하시오.")
professor = input("데이터를 얻고 싶은 교수명을 입력하시오.")

keyword2 = str(keyword)
professor2 = str(professor)

expect1 = get_rec_point(keyword2, professor)

print('입력한 학수번호와 교수 수업의 예상 평점은?', expect1)
# 예상 평점이 나옴!
