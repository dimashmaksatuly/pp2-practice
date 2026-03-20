import os

os.mkdir("test_folder")

os.makedirs("parent/child/grandchild")

print(os.listdir("."))

print(os.getcwd())