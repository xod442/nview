from utilities.inventory import inventory

hostip = '10.132.0.19'
username = 'admin'
password = 'admin'

ev = inventory(hostip,username,password)



for e in ev:
    print('--------------------new event-----------------------')
    print(e)
