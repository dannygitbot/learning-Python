import socket
import time
import threading
import Queue
import sys
import os

socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

try:
    target = raw_input("[*] Type the target IP address: ")
    response = os.system("ping -c 1 -w 1 " + target + " > /dev/null 2>&1")
    if response == 0:
        print "[*] target IP is available!"
    else:
        print "[!] target IP is not available!"
        print "[!] Scanner is now exiting..."
        sys.exit(1)
    minPort = raw_input("[*] Type the minimum port number: ")
    maxPort = raw_input("[*] Type the maximum port number: ")

    try:
        if int(minPort) >= 0 and int(maxPort) >= 0 and int(maxPort) >= int(minPort):
            print("Starting Scan...")
        else:
            print "Invalid range of ports"
            print "[!] Scanner is now exiting..."
            sys.exit(1)
    except Exception:
        print "Invalid range of ports"
        print "[!] Scanner is now exiting..."
        sys.exit(1)
except KeyboardInterrupt:
    print "[!] User used Ctrl + C..."
    print "[!] Scanner is now exiting..."
    sys.exit(1)



def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print("[*] Port %s is open!") % port
        con.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        portscan(worker)
        q.task_done()

q = Queue.Queue()
startTime = time.time()

for x in range(40):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()


for worker in range(int(minPort), int(maxPort)):
    q.put(worker)

q.join()

totalTime = time.time() - startTime
print("[~] Scan finished in %s seconds!") % totalTime