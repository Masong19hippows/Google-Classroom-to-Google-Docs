#!/usr/bin/env python3

from Docs import update
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import sys
import pickle
import os
mydir = os.path.dirname(__file__)

today = datetime.date.today().strftime('%m') + "/" + datetime.date.today().strftime('%d')
todayfinal = datetime.datetime.strptime(today, "%m/%d")

SCOPES = ['https://www.googleapis.com/auth/classroom.student-submissions.me.readonly', 'https://www.googleapis.com/auth/documents']
DOCUMENT_ID = '1d_L2Rb9F21jgobyEOk3L8W99pQK05SzN7fbEshurKfE'

if os.path.exists(mydir + '/creds/token.pickle'):
    with open(mydir + '/creds/token.pickle', 'rb') as token:
        creds = pickle.load(token)
         
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(mydir + '/creds/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(mydir + '/creds/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
      
service = build('docs', 'v1', credentials=creds)



def main():

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    resultsEng = service.courses().courseWork().list(courseId=123423892759, orderBy='dueDate asc').execute().get('courseWork')
    resultsGovern = service.courses().courseWork().list(courseId=126844223250, orderBy='dueDate asc').execute().get('courseWork')
    resultsACT = service.courses().courseWork().list(courseId=123201900052, orderBy='dueDate asc').execute().get('courseWork')

    docwords = 'College English:' + '\n'
    for items in resultsEng:
        title = items.get("title")
        if items.get('dueDate') is None:
            continue
        monthdue = items.get("dueDate").get("month")
        daydue = items.get("dueDate").get('day')
        totaldue = str(monthdue) + "/" + str(daydue)
        finaldue = datetime.datetime.strptime(totaldue, "%m/%d")
        if todayfinal > finaldue:
            continue
        else:
            docwords = docwords + '     ' + str(title) + ' ' + str(totaldue) + '\n'

    docwords = docwords + "College Government:" + '\n'
    for items in resultsGovern:
        title = items.get("title")
        if items.get('dueDate') is None:
            continue
        monthdue = items.get("dueDate").get('month')
        daydue = items.get("dueDate").get('day')
        totaldue = str(monthdue) + "/" + str(daydue)
        finaldue = datetime.datetime.strptime(totaldue, "%m/%d")
        if todayfinal > finaldue:
            continue
        else:
            docwords = docwords + '   ' + str(title) + ' ' + str(totaldue) + '\n'


    docwords = docwords + "ACT Prep:" + '\n'
    for items in resultsACT:
        title = items.get("title")
        if items.get('dueDate') is None:
            continue
        monthdue = items.get("dueDate").get('month')
        daydue = items.get("dueDate").get('day')
        totaldue = str(monthdue) + "/" + str(daydue)
        finaldue = datetime.datetime.strptime(totaldue, "%m/%d")
        if todayfinal > finaldue:
            continue
        else:
            docwords = docwords + ' ' + str(title) + ' ' + str(totaldue) + '\n'
   
   
    update(DOCUMENT_ID).delEvry()
    update(DOCUMENT_ID).insertText(docwords, '1')



if __name__ == '__main__':
    main()
