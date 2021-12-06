import time
from parser import Parser

parser = Parser()
payload = []

def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    global payload
    while True:
        line = thefile.readline()
        if not line:
            if len(payload) != 0:
                print(payload)
                # send(payload)
                payload = []
            time.sleep(0.1) # Sleep briefly
            continue
        yield line


for line in follow(open("test_file", "r")):
    if line =='':
        continue
    line =  line.rstrip().lstrip()
    parsed = parser.parse(line)
    
    # temp_log_object = {}
    # temp_log_object["logType"] = "syslog"
    # temp_log_object['time'] = parsed['timestamp']

    print(parsed)
