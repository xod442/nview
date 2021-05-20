#!/usr/bin/env python3


from utilities.make_client import client

hostip = '10.132.0.19'
username = 'admin'
password = 'admin'

api = client(hostip,username,password)
print('-------------------------------volumes section------------------------------')
x = api.volumes.list()
print(x)
for vol in x:
    print(vol.attrs['id'])
    print(vol.attrs['name'])
    print(vol)
    #print(vars(vol.attrs))

    snap_list = api.snapshots.list(vol_name=vol.attrs['name'])
    for snap in snap_list:
        print(snap.attrs['name'])
'''
print('------------------------------pools section------------------------------')

y = api.pools.list()
for pool in y:
    print(pool.attrs['name'])
    print(pool.attrs['id'])

    list = api.pools.list(name=pool.attrs['name'])
    for l in list:
        print(l.attrs['name'])
        print(l.attrs['id'])
        print('-----------------------------array------------------------------')

    array = api.arrays.list()
    for l in array:
        print(l)
print('-------------------------------shelves section------------------------------')

shelf = api.shelves.list()
for l in shelf:
    print(l)
print('-------------------------------network section------------------------------')
# <NetworkInterface(id=1c319f63b3abcd36ba000000010000000001010000, name=eth1)>
net = api.network_interfaces.list()
for l in net:
    print(l)
print('-------------------------------events section------------------------------')
event = api.events.list(detail=True)
for e in event:
    #  e = api.events.list(id=l.attrs['id'])
    print(e)
print('-------------------------------users section------------------------------')
users = api.users.list(detail=True)
print(users)
print('-------------------------------arrays section------------------------------')
entry = api.arrays.get()
inventory = {}
for e in entry:
     print(e.attrs.get('version'))
     print(e.attrs.get('extended_model'))
     print (e.attrs.get('serial'))



# api.volumes.get('0649686580b78e0b16000000000000000000000005').attrs.
'''
