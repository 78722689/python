#!/usr/bin/env python
#coding=utf-8

import urllib3

#http = urllib3.ProxyManager('http://10.144.1.10:8080/', maxsize=1024)
http = urllib3.PoolManager(num_pools=(1024*3), maxsize=1024)
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
try:
    with http.request('GET', 'http://www.qujiang.com.cn', headers=header, timeout = 20, preload_content=False, decode_content=True) as r:
        print(r.data)
        print(r.status)
except Exception as err:
    print(err)