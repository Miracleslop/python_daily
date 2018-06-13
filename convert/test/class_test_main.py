# control " from class_test_main import * " import's files
__all__ = ['S1', 'S2', 'AStore', 'AFactory']

# set the file of py's __name__
__name__ = '__test__2'
print('now the __name__ of py is %s' % __name__)


class Cat(object):

    def __init__(self):
        """ 调用父类方法三种方式 """
        # 方式1： object.__init__(self)
        # 方式2： super(Cat, self).__init__()
        super().__init__()  # 方式3

    content = 'hello cat ye!!'

    def show(self):
        """ 实例方法 show() """
        print('object: ' + self.content)
        # 方式2： print('object: ' + Cat.content)

    @classmethod
    def show(cls):
        """ 类方法 show() """
        print('class: ' + cls.content)
        # 方式2： print('class: ' + Cat.content)

    @staticmethod
    def show():
        """ 静态方法 show() """
        print('static: ' + Cat.content)


if __name__ == '__test__1':
    cat_obj = Cat()
    cat_obj.show()
    Cat.show()


# ***********************************************************
# __test__2     factory model


class F1(object):
    def show(self):
        print('F1.show')


class S1(F1):
    def show(self):
        print('S1.show')


class S2(F1):
    def show(self):
        print('S2.show')


if __name__ == '__test__2':
    def func(obj):
        print(obj.show())


    s1_obj = S1()
    func(s1_obj)
    s2_obj = S2()
    func(s2_obj)


class Store(object):

    def __init__(self):
        self.__s = None

    def create(self, type_name):
        pass

    def start(self, type_name):
        self.__s = self.create(type_name)

        if not self.__s:
            return

        # way 1:
        self.__s.show(self.__s)

        # way 2:
        # if hasattr(self.__s, 'show'):
        #     fun = getattr(self.__s, 'show')
        #     fun(self.__s)
        # else:
        #     print('%s has not method show()' % self.__s)


class AFactory(object):
    __range = 'S1S2'
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def work(self, type_name):
        try:
            self.__range.index(type_name)
        except ValueError as msg:
            print('[ValueError] ---- type_name is illegal and error msg is : %s' % msg)
            return None
        return eval(type_name)


class AStore(Store):
    def create(self, type_name):
        return AFactory().work(type_name)


if __name__ == '__test__2':
    atemp = AStore()
    atemp.start('S2')
