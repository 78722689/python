#!/usr/bin/env python
#coding=utf-8

import gevent
import urllib3
import time

##################################
# Cooperate with gevent_monkey_sample
#import gevent.monkey
#gevent.monkey.patch_socket()
##################################

from gevent.event import Event
from gevent import sleep
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore


class gevent_monkey_sample:
    def __init__(self):
        print('gevent_monkey_sample')
        
    def fetch(self, pid, url):
        print('Process %s: %s start work' % (pid, url))
        flag = None
        status = None
        error_msg = None

        try :
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            gevent.sleep(0)
            result = r.data
            status = r.status
            flag = True
        except Exception as e :
            error_msg = str(e)
            print(error_msg)
            flag = False

        print('Process %s: %s %s' % (pid, url, status))
        return (pid, flag, url, status, error_msg)

    def asynchronous(self):
        i = 0
        jobs = []
        url = 'http://127.0.0.1:8000'
        for i in range(0, 100) : 
            jobs.append(gevent.spawn(self.fetch, i, url))
        gevent.joinall(jobs)
        value = []
        for job in jobs:
     #      print job.value
            value.append(job.value)

# gevent asynchronous works with monkey lib
def gevent_monkey_sample_call():
    start = time.time()
    print('Asynchronous:')
    ge = gevent_monkey_sample()
    ge.asynchronous()
    stop = time.time()
    print('stop-start')
    
    
class gevent_event_sample:
    '''
    Illustrates the usage of events
    '''
    
    def __init__(self, event):
        self.evt = event
        print('gevent_event_sample')

    def setter(self):
        '''After 3 seconds, wake all threads waiting on the value of evt'''
        print('A: Hey wait for me, I have to do something')
        gevent.sleep(3)
        print("Ok, I'm done")
        self.evt.set()

    def waiter(self):
        '''After 3 seconds the get call will unblock'''
        print("I'll wait for you")
        self.evt.wait()  # blocking
        print("It's about time")

def gevent_event_call():
    evt = Event()
    ev = gevent_event_sample(evt)
    gevent.joinall([
        gevent.spawn(ev.setter),
        gevent.spawn(ev.waiter),
        gevent.spawn(ev.waiter),
        gevent.spawn(ev.waiter),
        gevent.spawn(ev.waiter),
        gevent.spawn(ev.waiter)
    ])

class gevent_sem_sample:
    '''
    To understand how the semaphore works in different routines.
    Apply only 1 semaphore to lock the code block. 
    Once one thread acquired the semaphore, others threads will be blocked in acquire request until the acquired semaphore released.
    '''
    def __init__(self):
        self.sem = BoundedSemaphore(1)  # Only 1 code block can run at the same time.
        self.s = 0
     
    def worker1(self, n):
        print('Worker1 %i start' % n)
        self.sem.acquire()
        #gevent.sleep(0)
        print('Worker1 %i acquired semaphore' % n)
        self.s = 1
        print('Worker1 %i s=%d' % (n, self.s))
        sleep(10)
        self.sem.release()
        print('Worker1 %i released semaphore' % n)
     
    def worker2(self, n):
        print('Worker2 %i start' % n)
        
        with self.sem:
            print('Worker2 %i acquired semaphore' % n)
            self.s = 2
            print('Worker2 %i s=%d' % (n, self.s))
            #sleep(0)
        
        print('Worker2 %i released semaphore' % n)
 


def gevent_sem_sample_caller():
    pool = Pool()
    worker  = gevent_sem_sample()
    #pool.map(worker.worker1, range(0,2))
    #pool.map(worker.worker2, range(3,6))
    gevent.joinall([
        gevent.spawn(worker.worker1, 1),
        gevent.spawn(worker.worker2, 2)]
        )

from gevent.pywsgi import WSGIServer
def application(environ, start_response):
    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html')
    ]

    start_response(status, headers)
    yield "<p>Hello"
    yield "World</p>"

import gevent.monkey
gevent.monkey.patch_all(thread=False)
from gevent.queue import Queue
tasks = Queue()
co_queue= Queue()
def worker(n):
    print('Worker %s started' % n)
    try:
        while True:
            task = tasks.get()
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except:
        print('except..........')
    print('Quitting time!')

def boss():
    for i in range(1,25):
        tasks.put_nowait(i)

def co_worker():
    while True:
        time.sleep(1)
        #gevent.sleep(0)
        
if __name__ == '__main__':
    gevent.spawn(boss).join()
    
    #gevent.spawn(co_worker)
    #gevent.joinall([
    gevent.spawn(worker, 'steve')
    gevent.spawn(worker, 'john')
    gevent.spawn(worker, 'nancy')
    #])
    #while True:
    #time.sleep(10)
    #gevent_monkey_sample_call()
    #gevent_event_call()
    #gevent_sem_sample_caller()
    #WSGIServer(('', 8008), application).serve_forever()
    #mystr = '1dc3ef80b85ad13c59dc0'
    #oid = ''
    #for i in mystr:
    #    oid = oid + str(ord(i)) + '.'
    #print(oid)

