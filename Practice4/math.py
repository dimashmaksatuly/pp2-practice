import math
import random

# built-in
print(min(1, 5, 3))
print(max(1, 5, 3))
print(abs(-10))
print(round(3.6))
print(pow(2, 3))

# math module
print(math.sqrt(16))
print(math.ceil(2.3))
print(math.floor(2.7))
print(math.pi)

# random
nums = [1, 2, 3, 4]

print(random.randint(1, 10))
print(random.choice(nums))

random.shuffle(nums)
print(nums)