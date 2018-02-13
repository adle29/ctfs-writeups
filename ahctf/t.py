#nc 54.186.65.159 20002
#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import hashlib 
from time import sleep
import re
        # Create a socket object
host = "54.186.65.159"  #    Get local machine name
port = 20005                # Reserve a port for your service.
s = socket.socket()  # Create a socket object
               
s.connect((host, port))

while True: 
        #receive connection
        r =  s.recv(1048) # receive 1048 bytes
        print r
        if "+" in r: 
                        #fafdsfas What is (adfafasf) + (adfaf \)
                result = re.match( r'.*\s*What\sis\s(.*)\s\+\s(.*)', r, re.M|re.I)
                suma = int(result.group(1)) + int(result.group(2))
                msg = str(suma) + "\n"
                s.send(msg)
        elif r == "":
                break

while True:
        r =  s.recv(1048)
      
        print r
        if ":" in r:
                string = r.split(':')[1].replace('\n', '').strip()
                print string
                hash = hashlib.sha512()
                hash.update(string)
                result = hash.hexdigest() + "\n"
                print result
                s.send(result)
        elif r == "":
                break

# s.close()