from moduletest.module2.b import *
from .c import C

class A:
    def call_me1(self):
        print('A::call_me1')
        o_b =B()
        o_b.call_me()
        o_c =C()
        o_c.call_me()
    def call_me2(self):
        print('A::call_me2')