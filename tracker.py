#!/usr/bin/env python

import re
import json
from pprint import pprint
from bs4 import BeautifulSoup
from mechanize import Browser
import os.path
br = Browser()

# Enter Service Center code below MSC = National Benefits Center
mySC = 'MSC'
# Enter Case Number without Service Center
myCaseNum = 1234567890

# Form Type to look for
formType = 'Form I-485'
# Range either direction of your Case Number
numRange = 10

# set to 1 if expanding numRange over multiple tries to avoid checking known cases again and again
# set to 0 if updating case status rather than expanding range
expandOnly = 1

visited = {}
dataBase = {}
wrongForm = {}
adjudicated = {}

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]


if os.path.isfile('visited.txt'):
  with open('visited.txt') as infile:
    visited = json.load(infile)
if os.path.isfile('data.txt'):
  with open('data.txt') as infile:
    dataBase = json.load(infile)
if os.path.isfile('wrongForm.txt'):
  with open('wrongForm.txt') as infile:
    wrongForm = json.load(infile)
if os.path.isfile('adjudicated.txt'):
  with open('adjudicated.txt') as infile:
    adjudicated = json.load(infile)

class Case:
  def check(self):
    # Retrieve USCIS website
    # URL seems to have changed
    br.open( "https://egov.uscis.gov/casestatus/mycasestatus.do" )
    # Select the form
    br.select_form( 'caseStatusForm' )
    # print br.form
    br.form["appReceiptNum"] = mySC + caseNum
  
    # Get the response
    br.submit()
    html = br.response().read()
    soup = BeautifulSoup(html, 'html.parser')
    # print soup.prettify()
 
    # get current case status
    for status in soup.findAll('div', {'class': 'rows text-center'}):
      if all (keyWord in status.text for keyWord in [formType]):
        print(status.text)
        receiptNum = re.search(mySC + '(\d+)', status.text).group(1)
        if 'Fingerprint Fee Was Received' in status.text:
          dataBase[receiptNum] = 'Fingerprint Fee Was Received'
        # Added fingerprints taken as separate line to show progress
        elif 'Case Was Updated To Show Fingerprints Were Taken' in status.text:
          dataBase[receiptNum] = 'Fingerprints Were Taken'
        elif 'Case Was Approved' in status.text:
          dataBase[receiptNum] = 'Case Was Approved'
          adjudicated[caseNum] = 'adjudicated'
	    # Capitalization of the word was has been changed apparently
        elif any (deny in status.text for deny in ['Case Was Rejected', 'Decision Notice Mailed', 'Case Rejected']):
          dataBase[receiptNum] = 'Case Rejected'
          adjudicated[caseNum] = 'adjudicated'
        elif 'Case Was Received' in status.text:
          dataBase[receiptNum] = 'Case Received'
        elif 'Case is Ready to Be Scheduled for An Interview' in status.text:
          dataBase[receiptNum] = 'Ready for Interview'
	    # Added RfIE
        elif any (RFE in status.text for RFE in ['Request for Additional Evidence Was Mailed', 'Request For Evidence Was Received', 'Request for Initial Evidence Was Sent']):
          dataBase[receiptNum] = 'RFE'
        elif 'Case Was Transferred' in status.text:
          dataBase[receiptNum] = 'Case Transferred'
        elif 'Name Was Updated' in status.text:
          dataBase[receiptNum] = 'Name Updated'
  	  # Added Card Mailed
        elif 'Card Was Mailed To Me' in status.text:
          dataBase[receiptNum] = 'Card Mailed'
          adjudicated[caseNum] = 'adjudicated'
      else:
        wrongForm[caseNum] = 'wrongForm'
case = Case()

# query USCIS check my case webpage
for n in range (0-numRange, numRange):
  caseNum = str(myCaseNum + n)
  if caseNum not in wrongForm:
    if caseNum not in adjudicated:
      if expandOnly == 1:
        if caseNum not in visited:
          case.check()
          visited[caseNum] = 'visited'
      else:
        case.check()
        visited[caseNum] = 'visited'

numTotalCase = 0
numApproved = 0
numRejected = 0
numFPReceived = 0
numCaseWithFP = 0
numReceived = 0
numInterview = 0
numRFE = 0
numTransfer = 0
numNameUpdated = 0
numCardMailed = 0

for case in dataBase:
  numTotalCase += 1
  if dataBase[case]=='Fingerprint Fee Was Received':
    numFPReceived += 1
  elif dataBase[case]=='Fingerprints Were Taken':
    numCaseWithFP += 1
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
  elif dataBase[case]=='Card Mailed':
    numCardMailed += 1

# store data
with open('visited.txt', 'w') as outfile:
  json.dump(visited, outfile)
with open('data.txt', 'w') as outfile:
  json.dump(dataBase, outfile)
with open('wrongForm.txt', 'w') as outfile:
  json.dump(wrongForm, outfile)
with open('adjudicated.txt', 'w') as outfile:
  json.dump(adjudicated, outfile)

template = '{0:45}{1:5}'
# Print final statistics
print ('*********************************')
print ('For ' + str(2*numRange) + ' neighbors of ' + mySC + str(myCaseNum) +', we found the following statistics: ')
print (template.format('total number of I-485 application received: ', str(numTotalCase)))

print ('\nPositives:')
print (template.format('Case Was Approved: ', str(numApproved)))
print (template.format('Card Was Mailed: ', str(numCardMailed)))
print (template.format('Case Is Ready for Interview: ', str(numInterview)))

print ('\nNegatives:')
print (template.format('Case is RFE: ', str(numRFE)))
print (template.format('Case Was Rejected: ', str(numRejected)))

print ('\nNeutral:')
print (template.format('Case Was Received: ', str(numReceived)))
print (template.format('Fingerprint Fee Was Received: ', str(numFPReceived)))
print (template.format('Fingerprints Were Taken: ', str(numCaseWithFP)))
print (template.format('Case Was Transferred: ', str(numTransfer)))
print (template.format('Name Was Updated: ', str(numNameUpdated)))

