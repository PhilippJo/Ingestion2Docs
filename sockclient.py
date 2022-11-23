"""
Created on 11.04.2022 

@author: P Jordt
"""

import socket
import json
import time

class sockclient(object):

    def __init__(self, HOST = 'localhost', PORT = 9999):
        self.HOST = HOST
        self.PORT = PORT

    def write(self, scanid='', command= '', comment= ''):
        # Create a socket (SOCK_STREAM means a TCP socket)
        data = {'timestamp': time.asctime(), 'command': command, 'scanid': scanid, 'comment': comment}
        data_json = json.dumps(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect to server and send data
                sock.connect((self.HOST, self.PORT))
                sock.sendall(data_json.encode('ascii'))

                # Receive data from the server and shut down
                received_json = sock.recv(1024).decode('ascii')
                received = json.loads(received_json)
            except ConnectionRefusedError:
                received = 'ConnectionRefusedError: [WinError 10061] Es konnte keine Verbindung hergestellt werden, da der Zielcomputer die Verbindung verweigerte'
            except:
                received = 'Unknown Error occured!'
        print("Sent:     {}".format(data_json))
        print("Received: {}".format(received))

def write(scanid= 'idX', command= 'scan test abc', comment= 'test comment', *, HOST = '127.0.0.1', PORT = 65432):
    s = sockclient(HOST, PORT)
    s.write(scanid, command, comment)

if __name__ == "__main__":
    #Example how to forward the port with ssh
    #ssh -L 65432:127.0.0.1:65432 user@ipadress of socketserver

    #Test ingestion into doogle Docs file
    write(scanid= 'x', command= 'scan test 1 2 3 4', comment= 'test comment', HOST = '127.0.0.1', PORT = 65432)

    
    
