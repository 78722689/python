import gevent
from gevent.queue import Queue
 

class TaskFactory(object):
    def __init__(self, max_task_queue_size=2048, coroutine_number=1024, start=True):
        self.task_queue = Queue(max_task_queue_size)
        if start:
            self.worker()
    def start():
        for i in range(coroutine_number):
            gevent.spawn(self.worker, i)
        
    def worker(self, id):
        print('woker id-%d started' % id)
        
        while True:
            task = self.task_queue.get()
            gevent.spawn(self.run, task).join(task['timeout'])
            
    def run(id, task):
        print('worker id-%d run_task() %s' % (id, task))
        




task = Queue()

def workder(i):
    print('worker %d start' % i)
    t = task.get()
    print('worker %d received task from boss %d' %(i, t))
    
def boss(i):
    print('boss %i start' % i)
    task.put(i)
    print('boss %i end' % i)
    

if __name__ == '__main__':
    gevent.joinall(
        [gevent.spawn(workder, 0),
        gevent.spawn(workder, 1),
        gevent.spawn(workder, 2),
        gevent.spawn(workder, 3),
        gevent.spawn(workder, 4),
        gevent.spawn(workder, 4),
        gevent.spawn(boss, 6),
        gevent.spawn(boss, 7),
        gevent.spawn(boss, 8),
        gevent.spawn(boss, 9),
        ]
    )
    


