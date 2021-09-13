# 필요 패키지들 import 하기

#from urllib.request import urlopen # 인터넷 url를 열어주는 패키지
from urllib.parse import quote_plus # 한글을 유니코드 형식으로 변환해줌
from bs4 import BeautifulSoup 
from selenium import webdriver # webdriver 가져오기
import time # 크롤링 중 시간 대기를 위한 패키지
import warnings # 경고메시지 제거 패키지
from urllib.request import urlopen, Request
import warnings
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys
import pandas as pd

import pymongo
from . import mongo_connection

def parsing(id):
    warnings.filterwarnings(action='ignore') # 경고 메세지 제거
    # 인스타 그램 url 생성
    baseurl = "https://www.instagram.com/"
    plusUrl = id
    url = baseurl + quote_plus(plusUrl) + '/?hl=ko'

    driver = webdriver.Chrome(
        executable_path="/Users/soyean/Desktop/capston/chromedriver.exe"
    )
    driver.get(url)

    time.sleep(3)

    # 로그인 하기
    login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
    driver.find_element_by_xpath(login_section).click()
    time.sleep(2)


    elem_login = driver.find_element_by_name("username")
    elem_login.clear()
    elem_login.send_keys('****@gmail.com') //email 삭제 

    elem_login = driver.find_element_by_name('password')
    elem_login.clear()
    elem_login.send_keys('****')//password 삭제 

    time.sleep(1)

    xpath = """//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button"""
    driver.find_element_by_xpath(xpath).click()

    time.sleep(4)

    SCROLL_PAUSE_TIME = 1.0
    reallink = []

    stop_signal = 0
    
    
    while True:
        
        
        pageString = driver.page_source
        bsObj = BeautifulSoup(pageString, 'lxml')

        for link1 in bsObj.find_all(name='div', attrs={"class":"Nnq7C weEfm"}):
            if stop_signal >0 :
                break
           
            try: 
                for i in range(3):
                  if len(reallink) >= 10:
                       stop_signal += 1
                       break
                  title = link1.select('a')[i]
                  real = title.attrs['href']
                  reallink.append(real)
                  reallink = list(set(reallink))
                      
            except IndexError:
               print('Hello Error!')
        
        if stop_signal > 0 :
            break
            
        #과거의 높이
        
        last_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")


        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue

    same = []
    count = 0

 

    


    num_of_data = len(reallink)
    

    print('총 {0}개의 데이터를 수집합니다.'.format(num_of_data))
    csvtext = []
    result = []
    num =1

    for i in tqdm(range(num_of_data)):

        instagram_info = {}
        csvtext.append([])
        instagram_info['post_id']=num
        req = Request("https://www.instagram.com/p"+reallink[i], headers={'User-Agent': 'Mozila/5.0'})

        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8')
        soup1 = soup.find('meta', attrs={'property':"og:description"})

        reallink1 = soup1['content']
        reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
        reallink1 = reallink1[:20]

        if reallink1 == '':
            reallink1 = "Null"
        # csvtext[i].append(reallink1)
        instagram_info['person_id'] = reallink1

        result_text=""
        for reallink2 in soup.find_all('meta', attrs={'property':"instapp:hashtags"}):
            hashtags = reallink2['content'].rstrip(',')
            csvtext[i].append(hashtags)
            result_text += (hashtags+" ")
            
        # result_text = ""
        # for i in csvtext[i]:
        #     result_text += (i+" ")
           
        #result_text = result_text.strip()

        instagram_info['post'] = result_text
        result += [instagram_info]
        num+=1
    
    
    
    mongo_connection.post_insert(result)

    # csv로 저장

    # data = pd.DataFrame(result)
    # data.to_csv('insta.csv', encoding='utf-8')
    

    driver.close()
