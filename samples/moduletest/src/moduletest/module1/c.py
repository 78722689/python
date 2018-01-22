#from .a import A

class C:
    def call_me(self):
        print('C::call_me')
        from .a import A
        o_a = A()
        o_a.call_me2()