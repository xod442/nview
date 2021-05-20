# (c) Copyright 2020 Hewlett Packard Enterprise Development LP
# @author bsorge

'''
This was borrowed from the Nimble Python client. It was originally used to
print values to the screen.

I converted this into a flask utilitiy script.

R.Kauffman
'''

from .make_client import client
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import requests

requests.packages.urllib3.disable_warnings()


def make_vol(username,password,hostip,name,size,limit_iops):
    # Connect to the system
    api = client(hostip,username,password)
    # Create volume
    vol = api.volumes.get(name=name)
    if vol is None:
        try:
            vol = api.volumes.create(name=name, size=size, limit_iops=limit_iops)
            # msg="VOL-Success - Volume is now created!"
            # return render_template('success/success.html', msg=msg)
        except:
            vol="fail"
            # return render_template('error/gen_error.html', error=error)
    return vol

def smash_vol(username,password,hostip,name):
    # Connect to the system
    api = client(hostip,username,password)

    vol = api.volumes.get(name=name)
    if vol is not None:
        api.volumes.offline(id=vol.id)
        api.volumes.delete(id=vol.id)
    else:
        vol="fail"
    return vol
