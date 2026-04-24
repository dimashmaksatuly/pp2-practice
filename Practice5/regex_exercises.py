import re


print("Task 1:")
print(re.findall(r"ab*", "a ab abb abbb ac"))
print()

print("Task 2:")
print(re.findall(r"ab{2,3}", "ab abb abbb abbbb"))
print()

print("Task 3:")
print(re.findall(r"[a-z]+_[a-z]+", "hello_world test_case wrong-Case"))
print()

print("Task 4:")
print(re.findall(r"[A-Z][a-z]+", "Hello world Test Regex ABC"))
print()

print("Task 5:")
print(re.findall(r"a.*b", "a123b axxb acc"))
print()

print("Task 6:")
text = "Hello, world. Python is cool"
print(re.sub(r"[ ,\.]", ":", text))
print()

print("Task 7:")
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(snake_to_camel("hello_world_test"))
print()

print("Task 8:")
print(re.split(r"(?=[A-Z])", "HelloWorldTest"))
print()

print("Task 9:")
print(re.sub(r"([A-Z])", r" \1", "HelloWorldTest").strip())
print()

print("Task 10:")
def camel_to_snake(text):
    return re.sub(r"([A-Z])", r"_\1", text).lower().lstrip("_")

print(camel_to_snake("HelloWorldTest"))