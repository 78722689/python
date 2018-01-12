
class var_sample(object):
    
    # define class member
    var1 = 'aaaa'
    
    def __init__(self):
        # define class instance member
        self.var2 = 'bbbb'
    
    def change_var(self):
        # define class instance member
        self.var1 = 'cccc'
        self.var2='eeeee'
        
        # change class member value
        var_sample.var1 = 'dddd'
        
    # CAN NOT invoke from the instance of this class
    def __internal_fun(self):
        print('__internal_fun call')

if __name__ == '__main__':
    # output 'aaa'
    #
    print('var_sample.var1=%s' % var_sample.var1)
    
    print('-------------------')
    
    vs = var_sample()
    # output 'aaa'
    print('var_sample.var1=%s' % var_sample.var1)
    print('-------------------')
     
    vs.change_var()
    # output 'cccc'
    print('vs.var1=%s' % vs.var1)
    # output 'dddd'
    print('var_sample.var1=%s' % var_sample.var1)
    
    print('-------------------')
    
    vs2 = var_sample()
    # output 'dddd', why???????
    # python looks for member variable var1, but var1 defined in  function 'change_var()' and no invoke it, 
    # so no member variable var1 exist, and then python looks for class member and find out var1, so print the class member value of var1.
    print('vs2.var1=%s' % vs2.var1)
    
    # output 'bbbb', why???
    # var2 defined in constructor '__init__', so python could find out it in class member variable table.
    print('vs2.var2=%s' % vs2.var2)
    # output 'dddd', why???
    # because print var1 via class name not an instance, so var1 is class member.
    # and the class member var1 will be a common variable
    print('var_sample.var1=%s' % var_sample.var1)
    
 