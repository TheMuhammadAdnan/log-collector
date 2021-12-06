import time
from parser import Parser

parser = Parser()

def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line

for line in follow(open("test_file", "r")):
    if line =='':
        continue
    line =  line.rstrip().lstrip()
    parsed = parser.parse(line)
    print(parsed)
