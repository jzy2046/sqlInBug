import requests

def get_request_cookie(LOGIN_URL,body):
    #创建session
    session = requests.Session()
    session.post(LOGIN_URL,body==map)
    request_cookies = session.cookies.get_dict()
    print(request_cookies)
    return request_cookies

def login(LOGIN_URL,body,headers):
    resp = requests.post(LOGIN_URL,data=body,headers=headers,cookies=get_request_cookie(LOGIN_URL,body),allow_redirects=False)
    cookies = resp.cookies
    return cookies