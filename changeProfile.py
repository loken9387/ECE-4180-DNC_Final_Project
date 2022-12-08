import re
import os
import time

def dylan():
    with open('/home/loken9387/MagicMirror/config/config.js', 'r') as f:
        lines = f.readlines()
        
    with open('/home/loken9387/MagicMirror/config/config.js', 'w') as f:
        for line in lines:
            if re.search('Najaah', line):
                line = re.sub('Najaah', 'Dylan', line)
            if re.search('calendar.google', line):
                line = re.sub('https://calendar.google.com/calendar/ical/benachambliss%40gmail.com/private-a91ad467dc68fdce59f817718f2444cb/basic.ics', 'https://calendar.google.com/calendar/ical/fraustolimited%40gmail.com/private-3671629132c86d711515099fd0a00c01/basic.ics', line)
            f.write(line)
    os.system("""curl -X POST http://172.20.10.13:8080/api/module/module_1_alert/showalert   -H 'content-type: application/json'   -d '{ 
    "title": "Hello Dylan!", 
    "message": "Hope your day is good!", 
    "timer": 3000
    }'""")
    
    time.sleep(.5)
    os.system("curl -X GET 'http://172.20.10.13:8080/api/refresh'")
        
def najaah():
    with open('/home/loken9387/MagicMirror/config/config.js', 'r') as f:
        lines = f.readlines()
        
    with open('/home/loken9387/MagicMirror/config/config.js', 'w') as f:
        for line in lines:
            if re.search('Dylan', line):
                line = re.sub('Dylan', 'Najaah', line)
            if re.search('calendar.google', line):
                line = re.sub('https://calendar.google.com/calendar/ical/fraustolimited%40gmail.com/private-3671629132c86d711515099fd0a00c01/basic.ics', 'https://calendar.google.com/calendar/ical/benachambliss%40gmail.com/private-a91ad467dc68fdce59f817718f2444cb/basic.ics', line)
            f.write(line)
    os.system("""curl -X POST http://172.20.10.13:8080/api/module/module_1_alert/showalert   -H 'content-type: application/json'   -d '{ 
    "title": "Hello Najaah!", 
    "message": "Your are awesome!", 
    "timer": 3000
    }'""")
    
    time.sleep(.5)
    os.system("curl -X GET 'http://172.20.10.13:8080/api/refresh'")