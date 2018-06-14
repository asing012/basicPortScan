#!/usr/bin/env python
#Akshay Singh
# TCP port scanning tool

import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)
def bannerText(bannerSock): # to get the details of the open TCP ports
    try:
        bufferText = bannerSock.recv(1024)
        return bufferText
    except:
        s = "Time Out"
        return s

def connScan(tgtHost, tgtPort): # to start a connection with the TCP port 
    try:
        connSock = socket(AF_INET, SOCK_STREAM)
        connSock.connect((tgtHost, tgtPort))
        connSock.send("Hello World!")
        text = bannerText(connSock)
        screenLock.acquire()
        print("[+] TCP Port Open: %d"% tgtPort)
        print("[-] " + text)
    except:
        screenLock.acquire()
        print("[+] TCP Port Close: %d"% tgtPort)
    finally:
        screenLock.release()
        connSock.close()

def portScan(tgtHost, tgtPorts): # to start the port scan
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print(6)
        print("[+] Cannot resolve the host: " +tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("\n[+] Scan results for: " + tgtName[0])
    except:
        print("\n[+] Scan results for: " + tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        #print("Scanning ports " + tgtPort)
        t = Thread(target = connScan, args = (tgtHost, int(tgtPort)))
        t.start()

def main(): #setup parser and call portScan function
    parser = optparse.OptionParser('usage -H' + ' <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if(tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)

    portScan(tgtHost, tgtPorts)

if __name__=="__main__":
    main()
