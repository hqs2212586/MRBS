from django.test import TestCase

# Create your tests here.


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class MyClass(Singleton):
    a = 1


one = MyClass()
one.a = 3

two = MyClass()
print(two.a)
print("one", id(one))
print("tow", id(two))
"""
3
one 4362186704
tow 4362186704
"""
