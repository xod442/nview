#!/usr/bin/env python3


from utilities.make_client import client

hostip = '10.132.0.19'
username = 'admin'
password = 'admin'
c = 1
api = client(hostip,username,password)
print('-------------------------------volumes section------------------------------')
x = api.volumes.list()
for vol in x:
    print('-------------------------------volumes info------------------------------')
    print(vol.attrs['id'])
    detail = api.volumes.get(vol.attrs['id']).attrs
    print(detail['block_size'])
    print(vol.attrs['name'])
    print(vol)

    #print(vars(vol.attrs))
