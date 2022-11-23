# googleDocsAPI

 Simple python scripts using socket connection and googles Docs API to ingest a data string into a google docs document. In the document the string is ether ingested at the end of the document or at a specific position inside the document, simply defined by including ``{{input}}`` at the desired document position.
 
## Description

### googleAPI.py:  
Python class to communicate with the googleDocsAPI and handle the authentification/authorization process. 

### sockserver.py:  
Simple python class to start a socket server and listen for input from a sockclient, further on, ingesting this input into a google docs file utilising the googleDocsAPI.

### sockclient.py:
Simple python class and function to gather a string and send it via socket connection to the sockserver.

## Usage

### googleAPI.py:  
No need to interact with this class, its used in the sockserver (see below). What is happing in there is that a instance of the googleAPI class is initilized and the write function of this class is used.  
````python
gapi = googleAPI(DOCUMENT_ID)
'gapi.write(txtstr = text)
````

To use the google API one needs to create credentials beforehand and copy them into the working directory of the sockserver.py.  
1. Go to ``console.cloud.google.com`` and create a project
2. Enable Google Docs API: ``Menu > APIs & Services > Enabled APIs  & services``, click on ``enable APIs and services``, search for ``docs`` and enable the API
3. Setup consent screen: ``Menu > APIs & Services > OAuth consent screen``, set a name of the app, set scope to ``https://www.googleapis.com/auth/documents`` and define (test) users by including their email adresses
4. Create Credential: ``Menu > APIs & Services > Credentials``, click  on ``Create Credentials`` and select ``Oauth Client ID``, Application type is ``Desktop App``
5. Download .json containg the credential and paste it into the working directory which includes googleAPI.py

(See google python quickstart for some further informations: https://developers.google.com/docs/api/quickstart/python)

### sockserver.py:  
Modify the HOST, PORT and DOCUMENT_ID in the last line of the script to your personal needs (the given parameter were useful for a setup using SSH port forwarding OR both, sockclient and sockserver, running on the same machine)

````python 
start(HOST = "127.0.0.1", PORT = 65432, DOCUMENT_ID = 'jfbijdhdnoz47trz9cmzr98czn94ztcn984ztcn984z') 
````

Then run the script  
To end the script press CTRL+C  
The Document ID can be found in the URL of the desired document. (e.g. .../*jfbijdhdnoz47trz9cmzr98czn94ztcn984ztcn984z*/edit)

### sockclient.py:
Import this python module into your script and use function ``sockclient.write``  

e.g.   
````python 
import sockclient
sockclient.write(scanid= 'x', command= 'scan test 1 2 3 4', comment= 'test comment', HOST = '127.0.0.1', PORT = 65432)
````

(It may be necessary to use port forwarding using SSH to transfer data from sockclient to sockserver)
