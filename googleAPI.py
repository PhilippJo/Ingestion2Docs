"""
Created on 11.04.2022 

@author: P Jordt

Go to https://developers.google.com/docs/api/quickstart/python
code from quickstart guide was extended

Before usage the follwing packages must be installed:
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
or run
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

import os.path
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class googleAPI(object):
    def __init__(self, DOCUMENT_ID = '1KQEVZ4-V8LF5jIIUXRV9c6QFrIiKAeZrZyyp641ouqk'):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/documents']
        # The ID of a document.
        self.DOCUMENT_ID = DOCUMENT_ID
        self.matchstr = '{{input}}'


    def write(self, txtstr = 'appended test string'):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('docs', 'v1', credentials=creds)

            # Retrieve the documents contents from the Docs service.
            document = service.documents().get(documentId=self.DOCUMENT_ID).execute()

            timestr = time.strftime('%a %d.%m.%Y %H:%M')
            filestr = 'Document: {}'.format(document.get('title'))
            fullstr = '\n' + txtstr
            print(format(filestr  + fullstr))
            
            request_str = [{'replaceAllText': {'containsText': {'text': self.matchstr, 'matchCase':  'true'},'replaceText': txtstr}}]
            response = service.documents().batchUpdate(documentId=self.DOCUMENT_ID, body={'requests': request_str}).execute()
            if not response['replies'][0]['replaceAllText']:
                request_str = [{"insertText": {"text": fullstr,"endOfSegmentLocation": {"segmentId": ""}}}]
                service.documents().batchUpdate(documentId=self.DOCUMENT_ID, body={'requests': request_str}).execute()
        except HttpError as err:
            print(err)

def write2docs(text = 'test text!', DOCUMENT_ID = ''):
    gapi = googleAPI(DOCUMENT_ID)
    gapi.write(txtstr = text)

if __name__ == '__main__':

    write2docs(text  = 'test', DOCUMENT_ID = 'jfbijdhdnoz47trz9cmzr98czn94ztcn984ztcn984z')
