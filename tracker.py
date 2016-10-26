#!/usr/bin/env python

import re
import json
from pprint import pprint
from bs4 import BeautifulSoup
from mechanize import Browser
br = Browser()


myCaseNum = 1690654088
date = 'May 12'
formType = 'Form I-485'
numRange = 400
dataBase = {}

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]

with open('data.txt') as infile:
  dataBase = json.load(infile)

# query USCIS check my case webpage
for n in range (0-numRange, numRange):
  caseNum = str(myCaseNum + n)
  if caseNum not in dataBase:
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
      if all (keyWord in status.text for keyWord in [formType, date]):
        print(status.text)
        receiptNum = re.search('LIN(\d+)', status.text).group(1)
        if 'Fingerprint Fee Was Received' in status.text:
          dataBase[receiptNum] = 'Fingerprint Fee Was Received'
        elif 'Case Was Approved' in status.text:
          dataBase[receiptNum] = 'Case Was Approved'
        elif 'Case Rejected' in status.text:
          dataBase[receiptNum] = 'Case Rejected'


numTotalCase = 0
numApproved = 0
numRejected = 0
numFPReceived = 0

for case in dataBase:
  numTotalCase += 1
  if dataBase[case]=='Fingerprint Fee Was Received':
    numFPReceived += 1
  elif dataBase[case]=='Case Was Approved':
    numApproved += 1
  elif dataBase[case]=='Case Rejected':
    numRejected += 1

# store data
with open('data.txt', 'w') as outfile:
  json.dump(dataBase, outfile)


# Print final statistics
print '*********************************'
print 'For ' + formType + ' received by USCIS on ' + date + ', we found the following statistics: '
print 'total number of I-485 application received: ' + str(numTotalCase)
print 'Case Was Approved: ' + str(numApproved)
print 'Fingerprint Fee Was Received ' + str(numFPReceived)
print 'Case Was Rejected ' + str(numRejected)

