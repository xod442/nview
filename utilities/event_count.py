#!/usr/bin/env python3

# Import the required modules
from .make_client import client
from database.events import Events
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
from mongoengine import Q
import requests

requests.packages.urllib3.disable_warnings()

def counter():
    count = []
    warn = Events.objects(severity='warning')
    info = Events.objects(severity='info')
    crit = Events.objects(severity='critical')
    note = Events.objects(severity='notice')

    warn = len(warn)
    info = len(info)
    crit = len(crit)
    note = len(note)

    count = [warn,info,crit,note]

    # Connect to the system


    return count
