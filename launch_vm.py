#!/usr/bin/python

import requests, sys, json, datetime, calendar
from manage_jira import *
from clone_vm import *

'''Boolean values used to control the scripts operation'''
flag_update_ticket = True
flag_print_raw_ticket_summary = True 
flag_dump_all_fields = False 
flag_arg_validation = True 
flag_deploy_vm = True 
flag_add_comment_to_jira = True 



'''This initial update should be rewritten.  We should make use of the getaddr() functions and check against networks defined
   in settings.py to make sure that the ip addresses supplied are valid'''
def update_ticket():
   if flag_update_ticket:
      print " "
      print "Updating ticket with the following fields:" 
      print "   - Private IP Address : " + str(vm_private_ip)
      print "   - Public IP Address  : " + "212.58.243." + str(str(vm_private_ip).split('.')[3]) 
      print "   - VM Server Name     : " + "vm-" + str(vm_private_ip).replace(".", "-", 4) 
      jira_update_field(server, cert_file_path, ticket_no, "customfield_12022", str(vm_private_ip))
      jira_update_field(server, cert_file_path, ticket_no, "customfield_12023", "212.58.243." + str(str(vm_private_ip).split('.')[3]))
      jira_update_field(server, cert_file_path, ticket_no, "customfield_12021", "vm-" + str(vm_private_ip).replace(".", "-", 4)) 
      print " "

def print_raw_ticket_summary(ticket):
    if flag_print_raw_ticket_summary:
        print " "
        print "Full ticket summary (fields from Jira)"
        print "Ticket :              %s " % ticket_no
        print "Pipeline :            %s " % jira_get_field(ticket, "customfield_12009")
        print "Reporter :            %s " % jira_get_field(ticket, "reporter")['displayName']
        print "VM attributes requested"
        print "VM Server Name :      %s " % jira_get_field(ticket, "customfield_12021")
        print "OS :                  %s " % jira_get_field(ticket, "customfield_12001")['value']
        print "CPU Count :           %s " % jira_get_field(ticket, "customfield_12002")['value']
        print "Memory :              %s " % jira_get_field(ticket, "customfield_12003")['value']
        print "Disk size - OS :      %s " % jira_get_field(ticket, "customfield_12004")['value']
        print "Disk size - Data :    %s " % jira_get_field(ticket, "customfield_12005")['value']
        print "Private IP Address :  %s " % jira_get_field(ticket, "customfield_12022")
        print "Public IP Address :   %s " % jira_get_field(ticket, "customfield_12023")
        print "Network Bandwidth :   %s " % jira_get_field(ticket, "customfield_12006")['value']
        print "Site :                %s " % jira_get_field(ticket, "customfield_12007")['value']
        print "Tenancy Length :      %s " % jira_get_field(ticket, "customfield_12008")['value']
        print " "
    
def dump_all_fields(ticket):
    if flag_dump_all_fields:
        jira_pretty_print_all_fields(ticket)



'''Function used to validate all args gathered from the ticket prior to passing them to vsphere
   before deploying the vm we should seek approval from the user
   This function should take the passed ticket (jira fields format) and return fields in sanitized format'''
def arg_validation(ticket):
    sanitized_values_ready_for_deploy = {} 
    if flag_arg_validation:
        #print "validate args here"
        '''sanitize hostname'''
        sanitized_values_ready_for_deploy['arg_hostname'] = jira_get_field(ticket, "customfield_12021")
        '''sanitize OS'''
        if jira_get_field(ticket, "customfield_12001")['value'] == "RHEL 6.x":
            sanitized_values_ready_for_deploy['arg_OS'] = "centos65"
        elif ira_get_field(ticket, "customfield_12001")['value'] == "Win Server 2012":
            sanitized_values_ready_for_deploy['arg_OS'] = "winserver2012" 
        '''sanitize tenancy'''
        if jira_get_field(ticket, "customfield_12008")['value'] == "1 month":
            sanitized_values_ready_for_deploy['arg_tenancy'] =1
        elif jira_get_field(ticket, "customfield_12008")['value'] == "3 months":
            sanitized_values_ready_for_deploy['arg_tenancy'] =3
        elif jira_get_field(ticket, "customfield_12008")['value'] == "6 months":
            sanitized_values_ready_for_deploy['arg_tenancy'] =6
        elif jira_get_field(ticket, "customfield_12008")['value'] == "1 year":
            sanitized_values_ready_for_deploy['arg_tenancy'] =12
        '''sanitize cpu count'''
        if jira_get_field(ticket, "customfield_12002")['value'] == "1vCPU - Small":
            sanitized_values_ready_for_deploy['arg_cpu'] =1
        elif jira_get_field(ticket, "customfield_12002")['value'] == "2vCPU - Medium":
            sanitized_values_ready_for_deploy['arg_cpu'] =2
        elif jira_get_field(ticket, "customfield_12002")['value'] == "4vCPU - Large":
            sanitized_values_ready_for_deploy['arg_cpu'] =4
        '''sanitize memory'''
        if jira_get_field(ticket, "customfield_12003")['value'] == "1GB - Small":
            sanitized_values_ready_for_deploy['arg_mem'] =1
        elif jira_get_field(ticket, "customfield_12003")['value'] == "2GB - Medium":
            sanitized_values_ready_for_deploy['arg_mem'] =2
        elif jira_get_field(ticket, "customfield_12003")['value'] == "4GB - Large":
            sanitized_values_ready_for_deploy['arg_mem'] =4
        elif jira_get_field(ticket, "customfield_12003")['value'] == "8GB - XL":
            sanitized_values_ready_for_deploy['arg_mem'] =8
        ''' MORE COPYING BETWEEN ticket and sanitized_values_ready_for_deploy HERE'''
        #vm_server_name = "vm-" + str.replace(".", "-", 4) jira_get_field(ticket, "customfield_12021") 
        return sanitized_values_ready_for_deploy

def add_comment(server, cert_file_path, ticket_no, comment):
   if flag_add_comment_to_jira:
       jira_add_comment(server, cert_file_path, ticket_no, comment)
 
       
def add_months(sourcedate,months):
   month = sourcedate.month - 1 + months
   year = int(sourcedate.year + month / 12 )
   month = month % 12 + 1
   day = min(sourcedate.day,calendar.monthrange(year,month)[1])
   return datetime.date(year,month,day)
 

def deploy_vm(ticket):
    if flag_deploy_vm:
        sanitized = arg_validation(ticket) 
        deploy_vm_hostname = sanitized['arg_hostname']
        deploy_vm_template = sanitized['arg_OS'] #arg_template
        deploy_vm_cpus = sanitized['arg_cpu']
        deploy_vm_mem = sanitized['arg_mem']
        deploy_vm_ip = jira_get_field(ticket, "customfield_12022") 
        #deploy_vm_cpus = 2 
        #deploy_vm_mem  = 4 
        #print "Starting Deploy...."
        deployresult = deploy(deploy_vm_hostname, deploy_vm_template, deploy_vm_ip, deploy_vm_cpus, deploy_vm_mem)   
        #deployresult = "success"
        print deployresult
        if deployresult == "success":
            print "VM Deployed" 
            add_comment(server, cert_file_path, ticket_no, "VM Deployed")
            today = datetime.date.today()
            if flag_update_ticket:
                jira_update_field(server, cert_file_path, ticket_no, "customfield_12024", str(today))
                vm_term_date = add_months(today,sanitized['arg_tenancy'])
                jira_update_field(server, cert_file_path, ticket_no, "customfield_12025", str(vm_term_date))


if __name__ == "__main__":
    if getpass.getuser() != 'root':
        sys.exit("You must be root to run this.  Quitting.")

    '''We should be using argparse here to parse parameters and do some validation'''
    if len(sys.argv) == 1:
        print "Example : ./launch_vm.py jira-stage.blah.co.uk /path/to/key.pem ticket_number vm_private_ip"
        sys.exit()

    server = str(sys.argv[1])
    cert_file_path = str(sys.argv[2])
    ticket_no = str(sys.argv[3])
    vm_private_ip = str(sys.argv[4])


    '''dict to store all raw fields parsed from ticket, these fields are then passed to each jira operation'''
    ticket = []

    '''This command initialises the ticket dict, it should be re-run if we think the ticket has been updated
    whilst working on it'''
    ticket = jira_get_ticket(server, cert_file_path, ticket_no)      

    update_ticket()
    
    '''Ticket re-assigned as we have just run some updates'''
    ticket = jira_get_ticket(server, cert_file_path, ticket_no)

    print_raw_ticket_summary(ticket)

    '''Not really needed but useful for debugging'''
    dump_all_fields(ticket)

    '''arg_validation should really be called from within deploy_vm'''
    arg_validation(ticket)

    deploy_vm(ticket)        
 
