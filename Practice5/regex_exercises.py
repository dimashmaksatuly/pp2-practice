import re

# 'a' followed by zero or more 'b'
print("Task 1:")
print(re.findall(r"ab*", "a ab abb abbb ac"))
print()

# 'a' followed by two to three 'b'
print("Task 2:")
print(re.findall(r"ab{2,3}", "ab abb abbb abbbb"))
print()

# lowercase letters joined with underscore
print("Task 3:")
print(re.findall(r"[a-z]+_[a-z]+", "hello_world test_case wrong-Case"))
print()

# one uppercase followed by lowercase letters
print("Task 4:")
print(re.findall(r"[A-Z][a-z]+", "Hello world Test Regex ABC"))
print()

# 'a' followed by anything, ending in 'b'
print("Task 5:")
print(re.findall(r"a.*b", "a123b axxb acb"))
print()

# replace space, comma, or dot with colon
print("Task 6:")
text = "Hello, world. Python is cool"
print(re.sub(r"[ ,\.]", ":", text))
print()

# snake_case to camelCase
print("Task 7:")
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))
print()

# split at uppercase letters
print("Task 8:")
print(re.split(r"(?=[A-Z])", "HelloWorldTest"))
print()

# insert spaces before capital letters
print("Task 9:")
print(re.sub(r"([A-Z])", r" \1", "HelloWorldTest").strip())
print()

# camelCase to snake_case
print("Task 10:")
def camel_to_snake(text):
    return re.sub(r"([A-Z])", r"_\1", text).lower().lstrip("_")

print(camel_to_snake("HelloWorldTest"))