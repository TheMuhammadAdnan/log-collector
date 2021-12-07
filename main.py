import time
from parser import Parser
import requests

url = 'http://127.0.0.1:8080'
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
                requests.get(url=url, params={'payload_collector':payload_collector})
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
