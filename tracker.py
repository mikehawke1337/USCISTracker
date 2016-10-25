#!/usr/bin/env python

import re
from bs4 import BeautifulSoup
from mechanize import Browser
br = Browser()


myCaseNum = 1690654088
date = 'May 12'
formType = 'Form I-485'
numRange = 1000
numTotalCase = 0
numApproved = 0
numRejected = 0
numFPReceived = 0

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]

# query USCIS check my case webpage
for n in range (0-numRange, numRange):
  # Retrieve USCIS website
  br.open( "http://egov.uscis.gov/casestatus/landing.do" )
  # Select the form
  br.select_form( 'caseStatusForm' )
  # print br.form
  caseNum = 'LIN' + str(myCaseNum + n)
  br.form["appReceiptNum"] = caseNum

  # Get the response
  br.submit()
  html = br.response().read()
  soup = BeautifulSoup(html, 'html.parser')
  # print soup.prettify()

  # get current case status
  for status in soup.findAll('div', {'class': 'rows text-center'}):
    if all (keyWord in status.text for keyWord in [formType, date]):
      print(status.text)
      numTotalCase += 1
      if 'Fingerprint Fee Was Received' in status.text:
        numFPReceived += 1
      elif 'Case Was Approved' in status.text:
        numApproved += 1
      elif 'Case Rejected' in status.text:
        numRejected += 1

# Print final statistics
print '*********************************'
print 'For ' + formType + ' received by USCIS on ' + date + ', we found the following statistics: '
print 'total number of I-485 application received: ' + str(numTotalCase)
print 'Case was approved: ' + str(numApproved)
print 'Fingerprint Fee Was Received ' + str(numFPReceived)
print 'Case Rejected ' + str(numRejected)

