#!/usr/bin/env python

import re
import json
from pprint import pprint
from bs4 import BeautifulSoup
from mechanize import Browser
import os.path
br = Browser()


myCaseNum = 1690654088
formType = 'Form I-485'
numRange = 400
dataBase = {}
visited = {}

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]

if os.path.isfile('data.txt'):
  with open('data.txt') as infile:
    dataBase = json.load(infile)
if os.path.isfile('visited.txt'):
  with open('visited.txt') as infile:
    visited = json.load(infile)

# query USCIS check my case webpage
for n in range (0-numRange, numRange):
  caseNum = str(myCaseNum + n)
  if caseNum not in visited:
    visited[caseNum] = 'visited'
    # Retrieve USCIS website
    br.open( "http://egov.uscis.gov/casestatus/landing.do" )
    # Select the form
    br.select_form( 'caseStatusForm' )
    # print br.form
    br.form["appReceiptNum"] = 'LIN' + caseNum

    # Get the response
    br.submit()
    html = br.response().read()
    soup = BeautifulSoup(html, 'html.parser')
    # print soup.prettify()

    # get current case status
    for status in soup.findAll('div', {'class': 'rows text-center'}):
      if all (keyWord in status.text for keyWord in [formType]):
        print(status.text)
        receiptNum = re.search('LIN(\d+)', status.text).group(1)
        if 'Fingerprint Fee Was Received' in status.text:
          dataBase[receiptNum] = 'Fingerprint Fee Was Received'
        elif 'Case Was Approved' in status.text:
          dataBase[receiptNum] = 'Case Was Approved'
        elif any (deny in status.text for deny in ['Case Was Rejected', 'Decision Notice Mailed']):
          dataBase[receiptNum] = 'Case Rejected'
        elif 'Case Was Received' in status.text:
          dataBase[receiptNum] = 'Case Received'
        elif 'Case Is Ready To Be Scheduled For An Interview' in status.text:
          dataBase[receiptNum] = 'Ready for Interview'
        elif any (RFE in status.text for RFE in ['Request for Additional Evidence Was Mailed', 'Request For Evidence Was Received']):
          dataBase[receiptNum] = 'RFE'
        elif 'Case Was Transferred' in status.text:
          dataBase[receiptNum] = 'Case Transferred'
        elif 'Name Was Updated' in status.text:
          dataBase[receiptNum] = 'Name Updated'

numTotalCase = 0
numApproved = 0
numRejected = 0
numFPReceived = 0
numReceived = 0
numInterview = 0
numRFE = 0
numTransfer = 0
numNameUpdated = 0

for case in dataBase:
  numTotalCase += 1
  if dataBase[case]=='Fingerprint Fee Was Received':
    numFPReceived += 1
  elif dataBase[case]=='Case Was Approved':
    numApproved += 1
  elif dataBase[case]=='Case Rejected':
    numRejected += 1
  elif dataBase[case]=='Case Received':
    numReceived += 1
  elif dataBase[case]=='Ready for Interview':
    numInterview += 1
  elif dataBase[case]=='RFE':
    numRFE += 1
  elif dataBase[case]=='Case Transferred':
    numTransfer += 1
  elif dataBase[case]=='Name Updated':
    numNameUpdated += 1

# store data
with open('data.txt', 'w') as outfile:
  json.dump(dataBase, outfile)
with open('visited.txt', 'w') as outfile:
  json.dump(visited, outfile)

template = '{0:45}{1:5}'
# Print final statistics
print '*********************************'
print 'For ' + str(2*numRange) + ' neighbors of LIN' + str(myCaseNum) +', we found the following statistics: '
print template.format('total number of I-485 application received: ', str(numTotalCase))
print template.format('Case Was Approved: ', str(numApproved))
print template.format('Fingerprint Fee Was Received: ', str(numFPReceived))
print template.format('Case Was Rejected: ', str(numRejected))
print template.format('Case Was Received: ', str(numReceived))
print template.format('Case Was Ready for Interview: ', str(numInterview))
print template.format('Case is RFE: ', str(numRFE))
print template.format('Case Was Transferred: ', str(numTransfer))
print template.format('Name Was Updated: ', str(numNameUpdated))
