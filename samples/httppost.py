#!/usr/bin/env python
#coding=utf-8

import urllib3
from bs4 import BeautifulSoup as bs

#http = urllib3.ProxyManager('http://10.144.1.10:8080/', maxsize=1024)
http = urllib3.PoolManager(num_pools=(1024*3), maxsize=1024)

from urllib import parse

def byte_2_str(data, encoding=[]):
    charsets = ['gb2312', 'utf8','gbk', 'ansi']
    for item in encoding:
        try:
            result = data.decode(item, 'ignore')
            return result
        except:
            logger.error('Decoding content fail.')
    
    
url = 'http://www.baidu.com/s?wd=inur:asp?=&rsv_spt=1&rsv_bp=0&ie=utf-8&tn=baiduhome_pg' #&pn=1
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
with http.request('GET', url, headers=header, timeout = 20, preload_content=False, decode_content=True) as resp:
    #print(resp.status)
    if resp.status != 200:exit
    page = byte_2_str(resp.data, ['utf8'])
    with open('d:/baidu-all.html', 'w+', encoding='utf-8') as f:
        print(page, file=f)
    
    soup = bs(page, 'lxml')
    links = soup.find_all('a')
    for link in links:
        if link.get('data-click') is None: continue
        target_url = link.get('href')
        if target_url is not None and 'link?url=' in target_url:
            print('found url %s' % target_url)
            with http.request('GET', target_url, headers=header, timeout = 20, redirect=True, preload_content=False, decode_content=True) as resp:
                #if resp.status != 200: continue
                print(resp.headers)
                with open('d:/baidu.html', 'w+') as f:
                    content = byte_2_str(resp.data, ['gb2312'])
                    print(content, file=f)

                break

            #break
            