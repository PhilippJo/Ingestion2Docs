"""
Created on 11.04.2022 

@author: P Jordt

Before usage the follwing packages must be installed:
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
or run
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

import socketserver
import json
import time
from googleAPI import googleAPI

class MyTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, docid, bind_and_activate=True):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        self.docid = docid

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self.docid, self)
    
    
class MyTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, docid, server):
        self.docid = docid
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
          
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        data_json = self.request.recv(1024).decode('ascii')
        data = json.loads(data_json)
        answer = 'Data Received'
        answer_json = json.dumps(answer)
        self.request.sendall(answer_json.encode('ascii'))
        print('#SOCKETSERVER#')
        print("{} wrote at {}:".format(self.client_address[0], time.asctime()))
        print(data)
        print('#GOOGLE-API#')
        gapi = googleAPI(self.docid)
        commentstr = '' if data['comment'] == '' else '\n' + data['comment']
        scanstr = '' if data['scanid'] == '' and data['command'] == '' else '\n' + data['command'] if data['scanid'] == '' else '\n' + data['scanid'] if data['command'] == '' else '\n' + data['scanid'] + ' | ' + data['command']
        data_str = str(data['timestamp']) + ' (Automated Input)' + str(commentstr) + str(scanstr)
        gapi.write(data_str)
        print('#END#')

def start(HOST = "127.0.0.1", PORT = 65432, DOCUMENT_ID = ''):
        # Create the server, binding to localhost on port 65432
    with MyTCPServer((HOST, PORT), MyTCPHandler, docid=DOCUMENT_ID) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

if __name__ == "__main__":
    start(HOST = "127.0.0.1", PORT = 65432, DOCUMENT_ID = 'jfbijdhdnoz47trz9cmzr98czn94ztcn984ztcn984z')

