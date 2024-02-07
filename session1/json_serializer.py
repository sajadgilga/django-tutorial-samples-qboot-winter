import json
from typing import List


class Person:
    def __init__(self, name, age, friends):
        self.name = name
        self.age = age
        self.friends = friends


class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age, "friends": obj.friends}
        return super().default(obj)


def person_encoder(obj):
    if isinstance(obj, Person):
        return {"name": obj.name, "age": obj.age}
    return obj


def person_decoder(dct):
    return Person(dct["name"], dct["age"], [])


p1 = Person("ahmad", 20, [])
p2 = Person("ali", 20, [p1])
data = {
    "profile": p2,
    "number": 100.10
}

json_data = json.dumps(p2, default=person_encoder)

# print(json_data, type(json_data))

p2_data = json.loads(json_data, object_hook=person_decoder)


# print(p2_data, type(p2_data))


class Book:
    name: str
    author: str

    def __init__(self, name, author):
        self.name = name
        self.author = author

    @staticmethod
    def decode(dct):
        return Book(dct['name'], dct['author'])


class Library:
    books: List[Book]
    capacity: int

    def __init__(self, capacity, books):
        self.books = books
        self.capacity = capacity

    @staticmethod
    def decode(dct):
        print('DECODE: ', dct)
        if 'books' in dct:
            books = [Book.decode(book_data) for book_data in dct['books']]
            return Library(dct['capacity'], books)
        return dct


class LibEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Library):
            return obj.__dict__
        if isinstance(obj, Book):
            return obj.__dict__
        return super().default(obj)


lib = Library(10, [Book(f"book {i}", f"author {i}") for i in range(1, 4)])
json_data = json.dumps(lib, cls=LibEncoder)

print(json_data)


def lib_decoder(dct):
    if 'books' in dct:
        return Library(dct['capacity'], [Book(book_data['name'], book_data['author']) for book_data in dct['books']])
    return dct


lib2 = json.loads(json_data, object_hook=Library.decode)
print(lib2)
