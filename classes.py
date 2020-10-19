#!/usr/bin/env python2

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from datetime import date
import sys
import json

today = date.today().strftime('%m') + "/" + date.today().strftime('%d')
todayfinal = datetime.datetime.strptime(today, "%m/%d")

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly']
DOCUMENT_ID = '1d_L2Rb9F21jgobyEOk3L8W99pQK05SzN7fbEshurKfE'

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/pi/classroom/creds/token.pickle'):
        with open('/home/pi/classroom/creds/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/pi/classroom/creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/pi/classroom/creds/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)
    service2 = build('docs', 'v1', credentials=creds)

    # Call the Classroom API
    resultsEng = service.courses().courseWork().list(courseId=123423892759, orderBy='dueDate asc').execute().get('courseWork')
    resultsGovern = service.courses().courseWork().list(courseId=126844223250, orderBy='dueDate asc').execute().get('courseWork')
    resultsACT = service.courses().courseWork().list(courseId=123201900052, orderBy='dueDate asc').execute().get('courseWork')

    docwords = 'College English:' + '\n'
    for items in resultsEng:
        title = items.get("title")
        monthdue = items.get("dueDate").get("month")
        daydue = items.get("dueDate").get("day")
        totaldue = str(monthdue) + "/" + str(daydue)
        finaldue = datetime.datetime.strptime(totaldue, "%m/%d")
        if todayfinal > finaldue:
            continue
        else:
            docwords = docwords + '     ' + str(title) + ' ' + str(totaldue) + '\n'

    docwords = docwords + "College Government:" + '\n'
    for items in resultsGovern:
        title = items.get("title")
        monthdue = items.get("dueDate").get("month")
        daydue = items.get("dueDate").get("day")
        totaldue = str(monthdue) + "/" + str(daydue)
        finaldue = datetime.datetime.strptime(totaldue, "%m/%d")
        if todayfinal > finaldue:
            continue
	else:
            docwords = docwords + '   ' + str(title) + ' ' + str(totaldue) + '\n'


    docwords = docwords + "ACT Prep:" + '\n'
    for items in resultsACT:
        title = items.get("title")
        monthdue = items.get("dueDate").get("month")
        daydue = items.get("dueDate").get("day")
        totaldue = str(monthdue) + "/" + str(daydue)
        finaldue = datetime.datetime.strptime(totaldue, "%m/%d")
        if todayfinal > finaldue:
            continue
        else:
            docwords = docwords + ' ' + str(title) + ' ' + str(totaldue) + '\n'


    requestpart = service2.documents().get(documentId=DOCUMENT_ID).execute().get('body').get('content')
    for item in requestpart:
        requestfinalIndex = item.get('endIndex')
    requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': requestfinalIndex - 1,
                }

            }

        },
    ]
   
    result = service2.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': requests}).execute()
    
    requests = [
         {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': docwords
            }
        },
    ]

    result = service2.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': requests}).execute()

if __name__ == '__main__':
    main()
