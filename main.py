import time
from parser import Parser

parser = Parser()
payload_collector = []

def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    global payload_collector
    while True:
        line = thefile.readline()
        if not line:
            if len(payload_collector) != 0:
                print(payload_collector)
                # send(payload)
                payload_collector = []
            time.sleep(0.1) # Sleep briefly
            continue
        yield line


for line in follow(open("test_file", "r")):
    if line =='':
        continue
    line =  line.rstrip().lstrip()
    payload = parser.parse(line)
    payload_collector.append(payload)
