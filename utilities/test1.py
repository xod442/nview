#!/usr/bin/env python3


from utilities.make_client import client

hostip = '10.132.0.19'
username = 'admin'
password = 'admin'

api = client(hostip,username,password)
inventory = {}
entry = api.arrays.get()

print(entry)
print(entry.attrs.get('id'))

x = api.arrays.get(entry.attrs.get('id')).attrs

print(x)

inventory[entry.attrs.get('name')] = [entry.attrs.get('version'),
                                       entry.attrs.get('extended_model'),
                                       entry.attrs.get('serial'),
                                       entry.attrs.get('role'),
                                       entry.attrs.get('gig_nic_port_count')]

print(inventory)
print('-------------------------------next section------------------------------')
