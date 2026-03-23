class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hi, I'm {self.name}"

p = Person("Dimash")
print(p.greet())