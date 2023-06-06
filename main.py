#! /usr/bin/python3.8

import sys
import time
import server
import socket
import file_info
from threading import Thread
from multiprocessing import Process

proc = None

def log(content,verbose=True):
    if verbose:
        print(content)
    with open(file_info.BASE_PATH+'/log.txt','a') as f:
        f.write(content+'\n')

# Set the file to be served
def set_file(file_path):
    file_info.set(file_path)

# Start the server
def start_server():
    global proc
    proc = Process(target=server.serve_file)
    proc.start()
    hostname=socket.gethostname()   
    ip=socket.gethostbyname(hostname)
    return f"{ip}:8080"

# Stop the server
def stop_server():
    if proc.is_alive():
        proc.terminate()
    log('Server stopped')

## DEBUGGING ##
def delay_stop():
    time.sleep(5)
    set_file(sys.argv[0])

if __name__=='__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        set_file(file)
        Thread(target=delay_stop).start()
        start_server()
    else :
        log('No file given\n\tSyntax: command file_path')
    
        