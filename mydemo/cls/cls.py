class A:
    def __init__(self):
        pass

    def say(self, msg):
        print('A: ', msg)

class B:
    def __init__(self):
        pass

    def say(self, msg):
        print('B: ', msg)

class C(B, A):
    pass

c = C()

c.say('a')