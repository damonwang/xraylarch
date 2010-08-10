def dictplus(a, b):
    '''syntactic sugar for a.update(b), return a'''
    a.update(b)
    return a

def closure(function, *curry, **kwcurry):
    '''syntactic sugar for a closure'''
    return lambda *args, **kwargs: function(*(args + curry),
            **dictplus(kwargs, kwcurry))
