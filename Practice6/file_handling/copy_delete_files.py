import shutil
import os

shutil.copy("example.txt", "copy.txt")

os.remove("copy.txt")