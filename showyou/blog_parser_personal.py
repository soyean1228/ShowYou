# --*-- coding: utf-8 --*--
import codecs

import re
import pandas as pd
import collections
import requests
import pymongo

from . import mongo_connection

from bs4 import BeautifulSoup


# 에러 리스트 생성 함수
def insert_error(blog_id, error, error_doc):
    for i in error_doc:
        error_log = str(error_doc["page"]) + "page / " + str(error_doc["post_number"]) \
                    + "th post / " + error + " / http://blog.naver.com/PostList.nhn?blogId=" + blog_id + "&currentPage=" + str(error_doc["page"])
    error_list.append(error_log)

def parsing(ID):
    
    total_num = 0
    csvtext = []
    error_list = []
    stop = 'no'

    blog_id = ID
    start_p = 1

    # print("\nCreating File Naver_Blog_Crawling_Result.txt...\n")

    content_text = '초본'
    copy_text = '0'
    num = 1

    global i 
    i = 0

    blog_post_list = []

    # 페이지 단위
    for page in range(start_p, 100):
        if stop == 'yes':
            break

        # print("=" * 50)
        #file.write("=" * 50 + "\n")

        doc = collections.OrderedDict()

        url = "http://blog.naver.com/PostList.nhn?blogId=" + blog_id + "&currentPage=" + str(page)
        r = requests.get(url)
        if (not r.ok):
            print("Page" + page + "연결 실패, Skip")
            continue

        # html 파싱
        soup = BeautifulSoup(r.text.encode("utf-8"), "html.parser")

        #총 게시글 수
        #total_count = soup.find_all("h4",{"class":"category_title pcol2"})

        # 페이지 당 포스트 수 (printPost_# 형식의 id를 가진 태그 수)
        post_count = len(soup.find_all("table", {"id": re.compile("printPost.")}))

        # doc["page"] = page

        blog_post = []

        # 포스트 단위
        for pidx in range(1, post_count + 1):
            # print('-' * 50)

            post = soup.find("table", {"id": "printPost" + str(pidx)})


            # 내용 찾기---------------------------

            content = post.find("div", {"class": "se-component se-text se-l-default"})
                    

            if (content == None):
                
                content = post.find("div", {"id": "postViewArea"})
                
            
                if content_text == copy_text:
                    stop = 'yes'
                    break

                else:
                    copy_text = content_text
                

            if (content != None):
                content_text = content.get_text()
                
                if content_text == copy_text:
                    stop = 'yes'
                    break

                else:
                    copy_text = content_text
                    csvtext.append([])
                    doc["num"]=num
                    num += 1
                    csvtext[total_num].append(doc["num"])
                    doc["content"] = content.get_text()
                    csvtext[total_num].append( doc["content"])
                

            else:
                doc["content"] = "CONTENT ERROR"

            blog_info = {}
            blog_info['post_id'] = i
            blog_info['person_id'] = ID
            blog_info['post'] = content.get_text()
            blog_post += [blog_info] 
            i += 1

            # # doc 출력 (UnicodeError - 커맨드 창에서 실행 시 발생)
            # for i in doc:

            #     str_doc = str(i) + ": " + str(doc[i])
            #     try:
            #         print(str_doc)
            #     except UnicodeError:
            #         print(str_doc.encode("utf-8"))

            #     # 에러 처리
            #     if ("ERROR" in str(doc[i])):
            #         insert_error(blog_id, doc[i], doc)

            # # 전체 수 증가
            total_num += 1
        blog_post_list += blog_post

    print(blog_post_list)
    mongo_connection.post_insert(blog_post_list)
    # data = pd.DataFrame(csvtext,columns=["num","text"])
    # data.to_csv('blog_parsing_new.csv', encoding='utf-8',index=False)

    # print("Total : " + str(total_num))

    error_num = len(error_list)
    print("Error : " + str(error_num))

    # 에러가 있을 경우 출력
    if (error_num != 0):
        print("Error Post : ")
        for i in error_list:
            print(i)