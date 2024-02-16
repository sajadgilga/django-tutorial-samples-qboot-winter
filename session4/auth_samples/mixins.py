class Logger:
    def log(self):
        print(f"My name is {self.name}")


class Person:
    def __init__(self, name):
        self.name = name

def add_mixin_to_object(obj, mixin):
    class MixedInClass(obj.__class__, mixin):
        pass
    obj.__class__ = MixedInClass

p = Person("Ali")
add_mixin_to_object(p, Logger)
p.log()

