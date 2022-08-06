import requests


def get_request_cookie(loginUrl, body):
    # 创建session
    session = requests.Session()
    session.post(loginUrl, body == map)
    request_cookies = session.cookies.get_dict()
    print(request_cookies)
    return request_cookies


def login(loginUrl, body, headers):
    resp = requests.post(loginUrl, data=body, headers=headers, cookies=get_request_cookie(loginUrl, body),
                         allow_redirects=False)
    cookies = resp.cookies
    return cookies
