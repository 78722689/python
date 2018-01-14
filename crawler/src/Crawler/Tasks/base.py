#!/usr/bin/env python
#coding=utf-8

import gevent.monkey
gevent.monkey.patch_all()

import gevent
from gevent.queue import Queue
from abc import ABC, ABCMeta, abstractmethod
import time

class TaskFactory(object):
    '''
    The factory to manage the Tasks in gevent coroutines. 
    '''
    
    __metaclass__ = ABCMeta
    
    def __init__(self, max_task_queue_size=2048, coroutine_number=1024, start=True):
        self.task_queue = Queue(max_task_queue_size)
        self.coroutine_number = coroutine_number
        if start:
            self.start()
           
    # Start worker routines
    def start(self):
        # DONT JOIN below routines.
        # It will cause 'gevent join block forever', because all the routines will be in waiting when queue.get(),
        # and no more available routines can be switched when gevent scheduling.
        # SO, if you have others routine in implementation and it will not in waiting to ensure gevent schedule successfully, you can join the following routines here.
        # Or, no join here but sleep in main routine to ensure the following routines finishing its job.
        gevent.spawn(self.manager())
        [gevent.spawn(self.worker, i) for i in range(self.coroutine_number)]
        
    def put_task(self, task):
        if isinstance(task, Task):
            self.task_queue.put(task)
        else:
            raise Exception('Input task is not an instance of class Task.')
    
    @abstractmethod
    def manager(self):
        '''
        Define the work flow to pre-process all the Tasks before put them into the queue.
        '''
        pass
        
    def worker(self, id):
        print('woker id-%d started' % id)

        while True:
            print('worker id-%d is free currently.' % id)
            task = self.task_queue.get()
            print('worker id-%d received task [%s]' % (id,task.name))
            try:
                t = gevent.spawn(self.__run, id, task)
                t.join(task.timeout)
                
                # Try to re-raise the exception
                t.get()
            except Exception as err:
                print('worker id-%d try to run task fail, %s' % (id, err))
            
    def __run(self, id, task):
        return task.job(id)

class Task(ABC):
    '''
    Define the task interface so that task factory run normally.
    
    All the customized tasks should inherit from this class.
    '''

    @property
    @abstractmethod
    def name(self):
        '''
        Getter to get the task name
        '''
        pass
        
    @name.setter
    @abstractmethod
    def name(self, value):
        '''
        Setter to set the task name
        
        value: string
        '''
        pass
    
    @property
    @abstractmethod
    def timeout(self):
        '''
        Getter to get the timeout of this task
        '''
        pass
        
    @name.setter
    @abstractmethod
    def timeout(self, value):
        '''
        Setter to set the timeout of this task
        
        value: integer
        '''
        pass
    
    @property
    @abstractmethod
    def job(self):
        '''
        Getter to get the timeout of this task
        '''
        pass
        
    @name.setter
    @abstractmethod
    def job(self, value):
        '''
        Setter to set the timeout of this task
        
        value: function(id)
        '''
        pass

# Example
class MyExampleTask(Task):
    def __init__(self, name='', timeout=0):
        self.__name = name
        self.__timeout = timeout
        self.__job = self.my_job
        
    def my_job(self, id):
        print('Entry my_job %d' % id)
        #raise Exception('my_job exception')
        return '========My job is done==========='
        
    @property
    def name(self):
        return self.__name
        
    @name.setter
    def name(self, value):
        self.__name = value
        
    @property
    def timeout(self):
        return self.__timeout
        
    @timeout.setter
    def timeout(self, value):
        self.__timeout = value
        
    @property
    def job(self):
        return self.__job
        
    @job.setter
    def job(self, value):
        self.__job = value
        
def task_producer(i, factory):
    while True:
        factory.put_task(MyExampleTask('example_task', 0))
        time.sleep(0.5)
    
if __name__ == '__main__':
    f = TaskFactory()
    gevent.joinall([gevent.spawn(task_producer, i, f) for i in range(10)])
    
    

  
        
    
    


