#!/usr/bin/python

import requests, sys, json
from xml.dom.minidom import parse, parseString


if len(sys.argv) == 1:
    print "You need to include your cert eg. ./get_jira.py /path/to/cert.pem"
    sys.exit()

cert_file_path = str(sys.argv[1])
url = "https://jira-stage.dev.bbc.co.uk/si/jira.issueviews:issue-xml/" + str(sys.argv[2]) + "/" + str(sys.argv[2]) + ".xml"
print url
r = requests.get(url, cert=cert_file_path, verify=False)
#print r
#print r.content

#doc = parse('ticket_output.xml')
doc = parseString(r.content)
key = doc.getElementsByTagName('key')
issue_type = doc.getElementsByTagName('type')
assignee = doc.getElementsByTagName('assignee')
due = doc.getElementsByTagName('created')
customfield_names = doc.getElementsByTagName('customfieldname')
customfield_values = doc.getElementsByTagName('customfieldvalue')
vm_life = doc.getElementsByTagName('timeestimate')



print key[0].firstChild.nodeValue
print "Issue Type: " + issue_type[0].firstChild.nodeValue
print "Assignee: " + assignee[0].firstChild.nodeValue
print "Due Date: " + due[0].firstChild.nodeValue
#print "Termination Date: " + vm_life[0].firstChild.nodeValue
i = 0
for item in customfield_names:
   #print customfield_names[i].firstChild.nodeValue
   if customfield_names[i].firstChild.nodeValue == 'Current environment':
       print 'Current environment: ' + customfield_values[i].firstChild.nodeValue
   if customfield_names[i].firstChild.nodeValue == 'Backlog Priority':
       print 'Priority: ' + customfield_values[i].firstChild.nodeValue
   i = i + 1 
if key[0].attributes.has_key('id'):
   print key[0].attributes['id'].value


#Testing to post comment
url = "https://jira-stage.dev.bbc.co.uk/rest/api/2/issue/" + str(sys.argv[2]) + "/comment"
body = '{"body":"DEPLOYED SUCCESSFULLY"}' 
r = requests.post(url, data=body, cert=cert_file_path, headers=({'Content-Type':'application/json'}))
