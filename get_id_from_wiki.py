from urllib.request import urlopen
import csv
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

def crawl_id():
    # define url for crawling
    url = 'https://en.wikipedia.org/wiki/Main_Page'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    # newline='' 參數，這是為了讓資料中包含的換行字元可以正確被解析
    with open ('MLB_ID_reference_.csv', 'r', newline='') as csvfile:
        # 讀取 CSV 檔案內容
        # reader = csv.reader(csvfile)
        reader = csv.DictReader(csvfile)
        column = [row['mlb_name'] for row in reader]

    with open('screen_name.csv', 'w') as f:
        writer = csv.writer(f)
        # table=[column,screen_name_str]
        # print(table)
        writer.writerow(['mlb_name', "screen_name"])


    for name in column:
        a = name.replace('.', '._')
        input_keyword=a.replace(' ','_')
        keyword_link = "https://en.wikipedia.org/wiki/"+input_keyword
        # print(keyword_link)
        res = requests.get(keyword_link, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # content = soup.find(name='div', attrs={'id':'mw-content-text'}).find_all(name='a')
        # print(content)

        # html = urlopen("https://en.wikipedia.org/wiki/"+input_keyword)
        # soup = BeautifulSoup(keyword_link,'html.parser')



        # (?!)是不包含:的意思
        regex = re.compile(r"^(https:\/\/twitter\.com\/)((?!:).)*$")
        for link in soup.find('div', {'id': 'mw-content-text'}).find_all('a', href=regex):
            if 'href' in link.attrs:
                screen_name_str=link.attrs['href'].split('/')[-1]

                ppp = re.compile('[0-9]{18}')
                mmm = re.compile('slideshow')
                if bool(ppp.search(screen_name_str)) or bool(mmm.search(screen_name_str)):
                    continue
                # print(screen_name_str,'\n link : ',link)
                print(screen_name_str)

                # writer.writerows(column,screen_name_str)
                columns_to_write =[]
                columns_to_write.append(name)
                columns_to_write.append(screen_name_str)
                print(columns_to_write)
                with open('screen_name.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns_to_write)
                    # print('done')


    return 'screen_name'




crawl_id()