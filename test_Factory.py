import operator
from nose.tools import *
import Factory

def test_alias():
    assert Factory.Factory is Factory.bind

def test_callable_object():
    class CallMe(object):
        def __init__(self, x):
            self.x = x
        def __call__(self, y):
            return self.x + y
    fac = Factory.Factory(CallMe(1))
    assert fac(1) == 2


def test_missing_attr():
    fac=Factory.Factory(lambda x: x)
    assert_raises(AttributeError, getattr, fac, 'x')
    assert_raises(AttributeError, getattr, fac, 'y')
    fac.x = 'x'
    obj = fac()
    assert obj == 'x'

class A(object):
    """This class doesn't define a cooperative constructor, but it doesn't call
    its super anyway."""
    def __init__(self, x):
        self.x = x

class B(A):
    def __init__(self, y, **kwargs):
        self.y = y
        super(B, self).__init__(**kwargs)

class C(B):
    def __init__(self, z, **kwargs):
        self.z = z
        super(C, self).__init__(**kwargs)


def test_basic_use_with_cooperative_constructors():
    fac = Factory.Factory(C)
    fac.z = 'z'
    fac.y = 'y'
    fac.x = 'x'
    obj = fac()
    assert obj.x == 'x'
    assert obj.y == 'y'
    assert obj.z == 'z'
    fac.bind(x='xx', y='yy')
    obj = fac()
    assert obj.x == 'xx'
    assert obj.y == 'yy'
    assert obj.z == 'z'

class Uncooperative(A):
    def __init__(self, y='Uncooperative'): # Note there's no x=
        super(Uncooperative, self).__init__(x='Uncooperative')
        self.y = 'Uncooperative'

def test_bind_constructor_does_not_use_kwargs():
    fac = Factory.Factory(Uncooperative)
    fac.bind(y='Factory') # This is normal, and should succeed.
    assert_raises(AttributeError, fac.bind, x='Factory')
    assert_raises(AttributeError, setattr, fac, 'x', 'Factory')


def test_bind_varargs():
    def mysum(*args):
        return sum(args)
    fac = Factory.Factory(mysum)
    fac.bind(1, 2, 3)
    fac.bind(4, 5, 6)
    fac.bind(7, 8, 9)
    assert fac() == 45
    assert fac(10) == 55


def test_bind_varargs_preserves_order():
    # Now for a non-commutative operation.
    def join(*args):
        return ''.join(args)
    fac = Factory.Factory(join)
    fac.bind('a', 'b', 'c')
    fac.bind('d', 'e', 'f')
    fac.bind('g', 'h', 'i')
    assert fac() == 'abcdefghi'
    assert fac('j', 'k', 'l') == 'abcdefghijkl'


def test_bind_varargs_fails_when_callee_does_not_support_varargs():
    def add(a, b):
        return a + b
    fac = Factory.Factory(add)
    assert_raises(TypeError, fac.bind, 1, 2)


def test_permits_varkwargs():
    def f(**kwargs):
        return kwargs # This accepts any and all args.
    fac = Factory.Factory(f)
    fac.bind(x='x', y='y')
    assert fac() == {'x': 'x', 'y': 'y'}

    class A(object):
        def __init__(self, **kwargs):
            pass
    class B(A):
        def __init__(self, **kwargs):
            super(B, self).__init__(**kwargs)
    class C(B):
        def __init__(self, b=None):
            super(C, self).__init__({'b': b})
    B_fac = Factory.Factory(B) # Should accept variable kwargs.
    C_fac = Factory.Factory(C) # Should not accept variable kwargs.
    assert B_fac(x=1)
    assert_raises(AttributeError, C_fac.bind, x=1)

def test_builtin_function():    
    assert Factory.Factory(hex, 42)() == '0x2a'

def test_builtin_class():
    fac = Factory.Factory(list)
    fac.bind((1, 2, 3))
    L = fac()
    assert L == [1, 2, 3]

def test_subclass_of_builtin():
    class MyList(list):
        pass
    
    fac = Factory.Factory(MyList)
    fac.bind((1, 2, 3))
    L = fac()
    assert L == [1, 2, 3]
    assert isinstance(L, MyList)

def test_bultin_instancemethod():
    L = [1, 2, 3]
    fac = Factory.Factory(L.append)
    fac(4)
    assert L == [1, 2, 3, 4]
    fac.bind(5)
    fac()
    assert L == [1, 2, 3, 4, 5]
    
def test_delattr():
    def called_with(x='pants'):
        return x
    
    fac = Factory.Factory(called_with)
    fac.x = 'shirt'
    assert fac() == 'shirt'
    del fac.x
    assert fac() == 'pants'

def test_getattr():
    def do_stuff(x, y):
        return x, y
    
    fac = Factory.Factory(do_stuff, x=1)
    assert fac.x == 1
    assert_raises(AttributeError, getattr, fac, 'y')

def test_bunch_equals():
    b = Factory.Bunch(pants="jeans", shirt="dressy")
    c = b.harden()
    assert c is not b
    assert c == b
    c.shirt = "sloppy"
    assert c != b

def test_bunch_repr():
    b = Factory.Bunch(pants="jeans")
    assert repr(b) == """Bunch(pants='jeans')"""

def test_bunch_get(): 
    b = Factory.Bunch(pants="jeans")
    assert b.get('pants', 'foo') == 'jeans'
    assert b.get('nonesuch', 'foo') == 'foo'
    assert b.get('nonesuch') is None
