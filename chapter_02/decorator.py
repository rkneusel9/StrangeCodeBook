#  function decorators are syntactic sugar

#  a decorator
def mydecorator(f):
    def decorate(*args, **kwargs):
        return "Per your request, the result is " + str(f(*args,**kwargs))
    return decorate

#  applying the decorator
@mydecorator
def afunc(x):
    return x**2 + 3*x + 4

#  which is the same as these two lines
def bfunc(x):
    return x**2 + 3*x + 4

dfunc = mydecorator(bfunc)

