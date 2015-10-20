"""
Network, VMware, and general settings for deploying a new Linux VM

Shamelessly stolen from https://gist.github.com/snobear/8788977

"""

from netaddr import IPNetwork, IPAddress

"""
General settings
"""
deploy_settings = dict()
deploy_settings["dns_servers"]      = ['10.1.0.17','8.8.4.4']
deploy_settings["vserver"]          = "10.3.0.89"
deploy_settings["port"]             = 443
deploy_settings["username"]         = "root"
deploy_settings["password"]         = "XXXXXX"
deploy_settings["mailfrom"]         = 'root@example.com'

"""
Networks
"""
# define settings for each of our networks
net = dict()

internal_lab = IPNetwork("10.3.0.0/24")
net[internal_lab] = dict()
net[internal_lab]["datacenter_name"] = 'infra.lab.local'
net[internal_lab]["cluster_name"]    = 'cluster1'
net[internal_lab]["datastore_name"]  = 'esx04-local'
net[internal_lab]["network_name"]    = 'bc-infra-lab-inet'
net[internal_lab]["gateway"]         = '10.3.0.1'
net[internal_lab]["subnet_mask"]     = str(internal_lab.netmask)

"""
routable_omaha = IPNetwork("123.456.78.90/25")
net[routable_omaha] = dict()
net[routable_omaha]["datacenter_name"] = 'Omaha'
net[routable_omaha]["cluster_name"]    = 'Omaha Server Cluster'
net[routable_omaha]["datastore_name"]  = 'Omaha datastore'
net[routable_omaha]["network_name"]    = 'Omaha Routable 1'
net[routable_omaha]["gateway"]         = '123.456.78.91'
net[routable_omaha]["subnet_mask"]     = str(routable_omaha.netmask)
"""


'''
Storage networks
'''
"""
internal_storage = IPNetwork("172.12.120.1/24")
net[internal_storage] = dict()
net[internal_storage]["network_name"] = '172.12.120.x storage net'
net[internal_storage]["subnet_mask"]  = str(internal_storage.netmask)
"""
