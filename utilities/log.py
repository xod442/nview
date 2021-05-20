#!/usr/bin/env python3

# Import the required modules
from .make_client import client



def log(hostip,username,password):
    # Connect to the system
    api = client(hostip,username,password)
    # Setup some variables
    log_data = []
    # Get the arrays
    logs = api.audit_log.list()

    for l in logs:

        entry = api.audit_log.get(l.attrs['id']).attrs

        logz = [
                entry['type'],
                entry['object_name'],
                entry['time'],
                entry['status'],
                entry['user_name'],
                entry['error_code'],
                entry['source_ip']
               ]

        log_data.append(logz)


    return log_data
