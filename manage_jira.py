#!/usr/bin/python

import requests, sys, json

'''This line should probably be removed, it supresses warnings about non trusted certs'''
requests.packages.urllib3.disable_warnings()

def jira_get_ticket(server, cert, ticket_no):
    full_api_url = "https://" + server + "/rest/api/2/issue/" + ticket_no
    #print "Full Ticket URL : "+ " https://" + server + "/browse/" + ticket_no 
    #print "Full Ticket API URL : " + full_api_url
    r = requests.get(full_api_url, cert=cert, verify=False)
    return json.loads(r.content)


def jira_get_field(ticket, field_name):
    if ticket['fields'].has_key(field_name):
        return ticket['fields'][field_name]
    else:
        return "field not found"

def jira_pretty_print_all_fields(ticket):
    print json.dumps(ticket['fields'], sort_keys=True, indent=4)

def jira_update_field(server, cert, ticket_no, field_name, new_field_value):
    apiurl = "https://" + server + "/rest/api/2/issue/" + str(sys.argv[3])
    apiurl2 = "https://" + server + "/rest/api/2/issue/" + str(sys.argv[3]) 
    #print apiurl2
    #r = requests.get(apiurl, cert=cert_file_path, verify=False)
    #issue = json.loads(r.content)
    #fields = issue['fields']
    #print fields
    #print fields.keys()
    #print "Created: " + issue['fields']['created']
    #print "VM Launched: " + issue['fields']['customfield_12024']
    #print "VM Termination Date: " + issue['fields']['customfield_12025']
    #print issue['fields']['customfield_12025']
    #issue['fields']['customfield_12025']="2016-08-15"

    new_json_values = '{ "fields": { "%s": "%s" } }' % (field_name, new_field_value) 

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    #print json.dumps(fields, indent=4)
    r = requests.put(apiurl2, cert=cert, data=new_json_values, headers=headers, verify=False)
    print r.status_code
    #print r.reason
    #print r


def jira_add_comment(server, cert, ticket_no, comment):
   url = "https://" + server + "/rest/api/2/issue/" + ticket_no + "/comment"
   body = '{"body":"' + comment + '"}'
   r = requests.post(url, data=body, cert=cert, headers=({'Content-Type':'application/json'})) 
