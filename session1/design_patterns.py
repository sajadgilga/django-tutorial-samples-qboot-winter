import random

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class X:
    def __init__(self, *args, **kwargs):
        print(*args)
        self.value = random.randint(1, 100)


x1 = X(3, 5, 6)
x2 = X(9, 10, 8)

#print(x1.value, x2.value)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Y(metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        print("y constructor called")
        self.value = random.randint(1, 100)

y1 = Y()
y2 = Y()

#print(y1.value, y2.value)


class Person:
    age: int
    name: str

    def __init__(self, name, age):
        self.age = age
        self.name = name
    
    def talk(self):
        pass
 
    def __str__(self):
        return f'Person {self.name}:{self.age}'

    @classmethod
    def create_from_dict(cls, data):
        if data['age'] < 18:
            raise Exception('Not allowed')
        return Person(data['name'], data['age'])

    @staticmethod
    def sample_job(*args, **kwargs):
        pass

data = {'name': 'ahmad', 'age': 20}

p1 = Person('ali', 10)
p2 = Person.create_from_dict(data)


class Subscriber:
    def update(self, data):
        pass


class HotPublisher:
    subscribers = []

    def subscribe(self, s):
        # validation if needed
        self.subscribers.append(s)

    def notify_subscribers(self, data):
        for s in self.subscribers:
            s.update(data)

    def unsubscribe(self, s):
        pass


class SampleSubscriber(Subscriber):
    def update(self, data):
        print(f'sample subscriber got data {data}')


class Sample2Subscriber(Subscriber):
    counter = 0
    def update(self, data):
        self.counter += 1
        print(f'sample 2 subscriber got data {data} -- {self.counter}')



s1 = SampleSubscriber()
s2 = Sample2Subscriber()
s3 = Sample2Subscriber()
p = Publisher()

p.subscribe(s1)
p.notify_subscribers('notify 1!')

p.subscribe(s2)
p.notify_subscribers('notify 2!')
p.notify_subscribers('notify 3!')
p.notify_subscribers('notify 4!')

p.subscribe(s3)
p.notify_subscribers('notify 5!')
p.notify_subscribers('notify 6!')
