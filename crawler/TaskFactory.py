#!/usr/bin/env python
#coding=utf-8

import gevent.monkey
gevent.monkey.patch_all()

import gevent
from gevent.queue import Queue
from abc import ABCMeta, abstractmethod
import time

class TaskFactory(object):
    '''
    The factory to run tasks in gevent coroutines. 
    Task format {taskname: 'name', timeout: tm, job:job}
    '''
    
    __metaclass__ = ABCMeta
    
    def __init__(self, max_task_queue_size=2048, coroutine_number=1024, start=True):
        self.task_queue = Queue(max_task_queue_size)
        self.coroutine_number = coroutine_number
        if start:
            self.start()
           
    # Start worker routines
    def start(self):
        print('TaskFactory:start() coroutine_number-%d' % self.coroutine_number)
        
        # DONT JOIN below routines.
        # It will cause 'gevent join block forever', because all the routines will be in waiting when queue.get(),
        # and no more available routines can be switched when gevent scheduling.
        # SO, if you have others routine in implementation and it will not in waiting to ensure gevent schedule successfully, you can join the following routines here.
        # Or, no join here but sleep in main routine to ensure the following routines finishing its job.
        [gevent.spawn(self.worker, i) for i in range(self.coroutine_number)]
        
    def put_task(self, task):
        self.task_queue.put(task)
    
    @abstractmethod
    def manager(self):
        '''
        Define the work flow to pre-process all the task before put into the queue.
        '''
        pass
        
    def worker(self, id):
        print('woker id-%d started' % id)

        while True:
            task = self.task_queue.get()
            try:
                t = gevent.spawn(self.__run, id, task)
                t.join(task['timeout'])
                t.get()
            except Exception as err:
                print('worker id-%d try to run task fail, %s' % (id, err))
            
    def __run(self, id, task):
        task['job'](id)

class Task(object):
    '''
    Define the task interface so that task factory run normally.
    '''
    
    @property
    @abstractmethod
    def name(self):
        pass
        
    @name.setter
    @abstractmethod
    def name(self):
        pass
    
class MyTask(Task):
    @property
    def name(self):
        return self._name
        
    def name(self, value):
        self._name = value
        
# Example
def do_job(id):
    print('in mycb in routine %d' % (id))
def task_producer(i, factory):
    while True:
        t = {'taskname' : 'printer' + str(i), 'timeout': 10, 'job': do_job}
        factory.put_task(t)
        time.sleep(0.5)
    

if __name__ == '__main__':
    #f = TaskFactory()
    #gevent.joinall([gevent.spawn(task_producer, i, f) for i in range(100)])
    task = MyTask()
    task.name = 'lixijiang'
    
    print(task.name)
    
    if isinstance(task, Task):
        print('yes')
    

  
        
    
    


