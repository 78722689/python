#!/usr/bin/env python
#coding=utf-8


import gevent
from gevent.queue import Queue
from gevent.lock import BoundedSemaphore
from abc import ABC, ABCMeta, abstractmethod
from Crawler.Util.tools import logger
import time

class TaskFactory(object):
    '''
    The factory to manage the Tasks in gevent coroutines. 
    '''
    
    __metaclass__ = ABCMeta
    
    def __init__(self, max_task_queue_size=1024, coroutine_number=1024, start=True):
        self.__manage_queue = Queue(max_task_queue_size)
        self.task_queue = Queue(max_task_queue_size)
        self.__coroutine_number = coroutine_number
        self.__free_workers = 0
        self.__sem = BoundedSemaphore(1)

        if start:
            self.start()
           
    # Start worker routines
    def start(self):
        # DONT JOIN below routines.
        # It will cause 'gevent join block forever', because all the routines will be in waiting when queue.get(),
        # and no more available routines can be switched when gevent scheduling.
        # SO, if you have others routine in implementation and it will not in waiting to ensure gevent schedule successfully, you can join the following routines here.
        # Or, no join here but sleep in main routine to ensure the following routines finishing its job.
        gevent.spawn(self.manager)
        [gevent.spawn(self.worker, i) for i in range(self.__coroutine_number)]

    def wait_for_message(self):
        msg = self.__manage_queue.get()
        return msg

    def put_message(self, msg):
        
        self.__manage_queue.put(msg)

    def put_task(self, task):
        if isinstance(task, Task):
            self.task_queue.put(task)
            #self.__manage_queue.put(task)
        else:
            raise Exception('Input task is not an instance of class Task.')
    
    @abstractmethod
    def manager(self):
        '''
        To manage the tasks.
        '''
        pass
        
    def worker(self, id):
        #print('woker-%d started' % id)

        while True:
            logger.debug('worker-%d, is free currently.', id)
            #self.__free_workers += 1
            task = self.task_queue.get()
            logger.debug('worker-%d, received task [%s].', id, task.name)
            #logger.debug('Routine status, Free workers %d, Busy workers %d', self.__free_workers, (self.__coroutine_number - self.__free_workers))

            #self.__sem.acquire()
            #self.__free_workers -= 1
            #self.__sem.release()

            try:
                t = gevent.spawn(self.__run, id, task)
                t.join(task.timeout)
                
                # Try to re-raise the exception
                t.get()
                logger.debug('worker-%d, task [%s] is done.', id, task.name)
                #self.__run(id, task)
            except Exception as err:
                logger.debug('worker-%d, try to run task fail, %s', id, err)
            
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

class NewTask(Task):
    def __init__(self):
        self.__name = 'NewTask'
        self.__timeout = 0
        
    def my_job(self, id):
        print('Worker-%d, Entry NewTask.' % id)
        gevent.sleep(20)
        print('Worker-%d, Exit NewTask.' % id)

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
        return self.my_job
        
        
# Example
class MyExampleTask(Task):
    def __init__(self, factory, name='', timeout=0):
        self.__factory = factory
        self.__name = name
        self.__timeout = timeout
        #self.__job = self.my_job
        
    def my_job(self, id):
        print('Worker-%d, Entry MyExampleTask' % id)
        for i in range(10):
            nj = NewTask()
            self.__factory.put_task(nj)
        print('Worker-%d, Exit MyExampleTask' % id)
        
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
        return self.my_job
        
    @job.setter
    def job(self, value):
        self.__job = value
        
def task_producer(i, factory):
    #while True:
    factory.put_task(MyExampleTask(factory, 'MyExampleTask', 0))
    time.sleep(120)
    
if __name__ == '__main__':
    f = TaskFactory()
    gevent.joinall([gevent.spawn(task_producer, i, f) for i in range(1)])
