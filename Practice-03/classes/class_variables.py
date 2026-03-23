class Student:
    school = "KBTU"  # class variable

    def __init__(self, name):
        self.name = name  # instance variable

s1 = Student("Dimash")
s2 = Student("Ali")

print(s1.school, s2.school)