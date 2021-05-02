# coding: utf-8

class SingletonInstane:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kargs)
            cls.instance = cls.__getInstance
        return cls.__instance