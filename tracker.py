#!/usr/bin/env python

import re
from bs4 import BeautifulSoup
from mechanize import Browser
br = Browser()

# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', 'Firefox')]

# Retrieve USCIS website
br.open( "http://egov.uscis.gov/casestatus/landing.do" )

# Select the form
br.select_form( 'caseStatusForm' )
# print br.form
br.form["appReceiptNum"] = 'LIN1690654088'

# Get the response
br.submit()

html = br.response().read()
soup = BeautifulSoup(html, 'html.parser')
#print soup.prettify()

for div in soup.findAll('div', {'class': 'current-status-sec'}):
  print div.text

