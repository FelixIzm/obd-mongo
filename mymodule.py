import requests
import sys
import json, re
import pymongo
from pymongo import MongoClient
import urllib.parse
import random

def hello():
    print('Hello, world!')

def fib(n):
    a = b = 1
    for i in range(n - 2):
        a, b = b, a + b
    return b

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",\
                "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",\
                "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"\
                ]
    return random.choice(uastrings)


def main():
    global JSESSIONID_value, secret_cookie,secret_cookie_value, countPages, headers, cookies

    with open('dictionary.json') as f:
        data = f.read()
    js = json.loads(data)

    myclient = pymongo.MongoClient(js['connect'])
    #print(js['ip'],js['port'],js['db_name'])
    mydb = myclient[js['db_name']]
    _set = mydb['settings']
    _pgs = mydb['pages']
    if _set.drop():
        _set = mydb['settings']
    if _pgs.drop():
        _pgs = mydb['pages']

    sys.tracebacklimit = None
    cookies = {}
    headers={}
    secret_cookie = "3fbe47cd30daea60fc16041479413da2"
    secret_cookie_value = ''
    JSESSIONID_value = ''
    countPages = ''
    headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': GET_UA(),
        }
    )
    url3=js['url3']+'&ps=200'
    URL = 'https://obd-memorial.ru/html'
    URL_search = URL + '/search.htm?'+url3
    print(URL_search)
    s = requests.get('https://obd-memorial.ru/html/advanced-search.htm',headers=headers)
    print(s.status_code)
    if(s.status_code==307 or s.status_code==200):
        secret_cookie_value = s.cookies[secret_cookie]
        cookies = { secret_cookie:secret_cookie_value}
        cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
        headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
        headers['cookie']=secret_cookie+"="+secret_cookie_value+'; request='+urllib.parse.quote(url3)
        headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
        headers['authority'] = 'obd-memorial.ru'
        headers['User-Agent']= GET_UA() #'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests']='1'
        headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
        print("1")
        r1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if('JSESSIONID' in r1.cookies.keys()):
            JSESSIONID_value =  r1.cookies["JSESSIONID"]
            cookies = {'JSESSIONID': JSESSIONID_value, secret_cookie:secret_cookie_value}
            cookies['request']=urllib.parse.quote(url3)
            cookies['showExtendedParams']='false'
            headers['JSESSIONID'] = JSESSIONID_value
            headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
            headers['authority'] = 'obd-memorial.ru'
            headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
            headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
            headers['Accept-Encoding'] = 'gzip, deflate, br'
            headers['Connection'] = 'keep-alive'
            headers['cookie']=secret_cookie+"="+secret_cookie_value+'; request='+urllib.parse.quote(url3)+'; JSESSIONID='+JSESSIONID_value
            headers['Upgrade-Insecure-Requests']='1'
            headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
            print("2")

            r2 = requests.get(URL_search,cookies=cookies,headers=headers)
            match = re.search(r'countPages = \d+',r2.text)
            if match:
                m1=re.search(r'\d+',match[0])
                countPages = (m1[0])
            if(countPages==''):
                raise ValueError('Не определилось число страниц!')

            _set.insert_one({'headers':headers, 'cookies':cookies, 'countPages':countPages})
            print("Done")
            # Для обработки страниц по 200 записей - записываем в коллекцию
            # это позволит возобновить обработку с прерванного места
            _r = [*range(1, int(countPages)+1)]
            for rec in _r:
                _pgs.insert_one({'id':str(rec),'processed':False})
        else:
            print('else+++')
            raise ValueError('JSESSIONID not')
    else:
        print(s.status_code)
        print("www")


if __name__ == "__main__":

    main()
