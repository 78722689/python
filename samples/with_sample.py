#!/usr/bin/env python
#coding=utf-8
'''
with 语句是从 Python 2.5 开始引入的一种与异常处理相关的功能（2.5 版本中要通过 from __future__ import with_statement 导入后才可以使用），
从 2.6 版本开始缺省可用（参考 What's new in Python 2.6? 中 with 语句相关部分介绍）。with语句适用于对资源进行访问的场合，
确保不管使用过程中是否发生异常都会执行必要的“清理”操作，释放资源，比如文件使用后自动关闭、线程中锁的自动获取和释放等。

使用：
语句体（with-body）：with 语句包裹起来的代码块，在执行语句体之前会调用上下文管
理器的 __enter__() 方法，执行完语句体之后会执行 __exit__() 方法。
基本语法和工作原理

with 语句的语法格式如下：
with context_expression [as target(s)]:
    with-body
    
这里 context_expression 要返回一个上下文管理器对象，该对象并不赋值给 as 子句中的 target(s) ，如果指定了 as 子句的话，
会将上下文管理器的 __enter__() 方法的返回值赋值给 target(s)。target(s) 可以是单个变量，或者由“()”括起来的元组（不能是仅仅由“,”分隔的变量列表，必须加“()”）。
'''



class with_sample:
    '''
    示例实现上下文管理协议，并使用with 关键字分别处理带异常和不带异常的情况。
    '''
    def __init__(self, tag):
        self.tag = tag
        print('Resource [%s]' % tag)
    def __enter__(self):
        print('[Enter %s]: Allocate resource.' % self.tag)
        return self # 可以返回不同的对象
    def __exit__(self, exc_type, exc_value, exc_tb):
        print('[Exit %s]: Free resource.' % self.tag)
        if exc_tb is None:
            print('[Exit %s]: Exited without exception.' % self.tag)
        else:
            print('[Exit %s]: Exited with exception raised.' % self.tag)
            return True # True-不会把捕获到的异常抛出给外现在调用程序;False-抛出捕获到的异常, 可以省略返回值False，缺省的None也是被看做是False

            
from contextlib import contextmanager
@contextmanager
def contextmanager_sample():
    '''
    contextmanager为上下文管理协议的一个装饰器，用于函数在使用with关键字时的上下文管理,不必创建一个类或单独指定__enter__() 和 __exit__() 方法.
    示例实现函数demo在用contextmanager装饰后成为一个上下文管理器，使之能满足with的使用，以及使用yield调用with里的body代码块。
    '''
    
    #相当于__enter__
    print('[Allocate resources]')
    print('Code before yield-statement executes in __enter__')
    
    #相当于调用with的body代码
    try:
        # 调用with里的body部分代码, 括号里的相当于返回值用于赋值给with后的as变量。 
        # 1个函数只能yield 1次
        yield('*** contextmanager demo ***')
    except Exception as err :
        print('error===============')
    finally :
        print('exit')
    
    #相当于__exit__
    print('Code after yield-statement executes in __exit__')
    print('[Free resources]')

from contextlib import closing
class ClosingDemo(object):
    '''
    closing 上下文管理器包装起来的对象必须提供 close() 方法的定义，否则执行时会报 AttributeError 错误。
    '''
    def __init__(self):
        self.acquire()
    def acquire(self):
        print('Acquire resources.')
    def free(self):
        print('Clean up any resources acquired.')
    def close(self):
        self.free()
            
if __name__ == '__main__':
    #
    #上下文管理协议实现演示
    #with with_sample('Normal'):
    #    print('[with-body] Run without exceptions.')

    # Body to raise the exception.
    #with with_sample('With-Exception'):
    #    print('[with-body] Run with exception.')
    #    raise Exception
    #    print('[with-body] Run with exception. Failed to finish statement-body!')

    #
    #contextmanager 示例演示
    with contextmanager_sample() as c:
        print('WITH BLOCK ========== %s' % c)
        #试着raise一个异常给contextmanager处理.
        raise Exception('My exception')
        
    with closing(ClosingDemo()):
        print('Using resources')
        
    