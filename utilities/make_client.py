from nimbleclient import NimOSClient

def client(hostip,username,password):

    # URL to create an organization.
    api = NimOSClient(hostip,username,password)

    return api
