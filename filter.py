import re
from sys import argv


def get_all_libs(file):
    libs = []
    with open(file, 'rb') as f:
        for line in f:

            libs.append(re.findall(r'"(.*?)"', line))
    print(libs)


get_all_libs(argv[1])
