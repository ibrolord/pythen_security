import os,sys

def filter():
    file="test_rsa.key"

    if os.path.isfile(file):
        with open(file, 'r') as file:
            for line in file.readlines():
                print(line)
    else:
        print(f"{file} not in {os.path.dirname(os.path.realpath(__file__))}")
        

filter()