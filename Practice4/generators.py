# Iterator example
nums = [1, 2, 3]
it = iter(nums)

print(next(it))
print(next(it))

# Custom iterator
class Count:
    def __init__(self, max):
        self.max = max
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.max:
            val = self.current
            self.current += 1
            return val
        else:
            raise StopIteration

for x in Count(3):
    print(x)

# Generator
def my_gen():
    yield 1
    yield 2
    yield 3

for x in my_gen():
    print(x)

# Generator expression
squares = (x*x for x in range(5))
print(list(squares))