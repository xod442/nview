#!/usr/bin/env python3

# Import the required modules
from .make_client import client
from database.system import System
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
from mongoengine import Q
import requests

requests.packages.urllib3.disable_warnings()

def inventory(hostip,username,password):

    # Clear the volumes database.
    System.objects().delete()

    # Connect to the system
    api = client(hostip,username,password)
    # Setup some variables
    inventory = {}
    # Get the arrays
    array = api.arrays.get()

    entry = api.arrays.get(array.attrs.get('id')).attrs

    inventory = [entry['version'],
                 entry['extended_model'],
                 entry['serial'],
                 entry['role'],
                 entry['gig_nic_port_count'],
                 entry['full_name'],
                 entry['usable_capacity_bytes'],
                 entry['usage']]

    version = inventory[0]
    model = inventory[1]
    serial = inventory[2]
    role = inventory[3]
    nics = str(inventory[4])
    name = inventory[5]
    usable = str(inventory[6])
    used = str(inventory[7])


    # Build database entry to save event

    record = System(version=version,
                    model=model,
                    serial=serial,
                    role=role,
                    name=name,
                    used=used,
                    usable=usable,
                    nics=nics)

    # Save the record
    try:
        record.save()
    except:
        error="sub-ERR00x - Failed to initialize the system database"
        return render_template('error/gen_error.html', error=error)

    return inventory
