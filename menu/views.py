

'''
2021 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "1.0.0"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Prototype"

Flask script that interacts with HPE Nimble
'''
from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import uuid
import os
import pygal
import json
from utilities.inventory import inventory
from utilities.log import log
from utilities.volumes import volumes
from utilities.events import events
from utilities.event_count import counter
from database.system import System
from database.events import Events
from database.volumes import Volumes
from utilities.get_creds import get
from utilities.save_creds import save
from database.creds import Creds
from utilities.make_client import client
from utilities.workflow import make_vol, smash_vol

menu_app = Blueprint('menu_app', __name__)

@menu_app.route('/menu_logs', methods=('GET', 'POST'))
def menu_logs():

    # Get logs from Nimble
    creds = get()
    hostip = str(creds[2], 'utf-8')
    username = str(creds[0], 'utf-8')
    password = str(creds[1],'utf-8')

    try:

        logz = log(hostip,username,password)
    except:
        error="ERR006 - Error getting system logs"
        return render_template('error/gen_error.html', error=error)

    return render_template('menu/logs.html', logz=logz)


@menu_app.route('/menu_events', methods=('GET', 'POST'))
def menu_events():

    # Get events from database
    events = Events.objects()
    eventz = []
    # rick.append('fail')
    for e in events:
        category = e.category
        time = e.time
        severity = e.severity
        summary = e.summary

        out = [category,time,severity,summary]

        eventz.append(out)

        dude = "dude"

    try:
        counts = counter()
    except:
        error="ERR005 - Error getting system event counts"
        return render_template('error/gen_error.html', error=error)



    chartData = [{
    "country": "Warning",
    "visits": counts[0]
    }, {
    "country": "Info",
    "visits": counts[1]
    }, {
    "country": "Critical",
    "visits": counts[2]
    }, {
    "country": "Notice",
    "visits": counts[3]
    }]


    return render_template('menu/events.html', eventz=eventz, dude=dude, chartData=chartData)
#--------------------------------Volume Section --------------------------------
@menu_app.route('/get_vol', methods=('GET', 'POST'))
def get_vol():
    '''
    Present Volume create form
    '''
    return render_template('menu/create_vol.html')


@menu_app.route('/create_vol', methods=('GET', 'POST'))
def create_vol():

    # Get creds from database
    creds = get()
    hostip = str(creds[2], 'utf-8')
    username = str(creds[0], 'utf-8')
    password = str(creds[1],'utf-8')

    #Get volume data from form
    name = request.form['name']
    size = request.form['size']
    limit_iops = request.form['limit_iops']

    # result = create_vol()
    result = make_vol(username,password,hostip,name,size,limit_iops)

    if result.attrs['id']:
        try:
            volz = volumes(hostip,username,password)
        except:
            error="ERR003 - Error getting system volumes after volume creation"
            return render_template('error/gen_error.html', error=error)

        msg = 'Volume created!'
        return render_template('success/success.html', msg=msg)
    else:
        error = 'Failed to create the volume ....call the wookiee'
        return render_template('error/gen_error.html', error=error)


@menu_app.route('/get_vol_delete', methods=('GET', 'POST'))
def get_vol_delete():
    '''
    Present Volume create form
    '''
    volz = []
    vols = Volumes.objects()
    for v in vols:
        name = v.name
        volz.append(name)

    return render_template('menu/delete_vol.html', volz=volz)


@menu_app.route('/delete_vol', methods=('GET', 'POST'))
def delete_vol():

    # Get creds from database
    creds = get()
    hostip = str(creds[2], 'utf-8')
    username = str(creds[0], 'utf-8')
    password = str(creds[1],'utf-8')

    #Get volume data from form
    name = request.form['name']

    result = smash_vol(username,password,hostip,name)

    if result.attrs['id']:
        try:
            volz = volumes(hostip,username,password)
        except:
            error="ERR003 - Error deleting system volumes"
            return render_template('error/gen_error.html', error=error)

        msg = 'Volume deleted!'
        return render_template('success/success.html', msg=msg)
    else:
        error = 'Failed to delete the volume ....call the wookiee'
        return render_template('error/gen_error.html', error=error)

#--------------------------------Snaps Section --------------------------------
@menu_app.route('/list_snaps', methods=('GET', 'POST'))
def list_snaps():

    # Get creds from database
    creds = get()
    hostip = str(creds[2], 'utf-8')
    username = str(creds[0], 'utf-8')
    password = str(creds[1],'utf-8')

    # Connect to the system
    api = client(hostip,username,password)

    volz = []
    vols = api.volumes.list()

    for vol in vols:
        current_vol = []
        name = vol.attrs['name']
        current_vol.append(name)
        snap_list = api.snapshots.list(vol_name=vol.attrs['name'])
        for snap in snap_list:
            current_vol.append(snap.attrs['name'])
        volz.append(current_vol)

    #rick.append('fail')
    return render_template('menu/list_snaps.html', volz=volz)


@menu_app.route('/get_snaps', methods=('GET', 'POST'))
def get_snaps():
    '''
    Under Development
    '''

    msg = "Functionaility under development, ask the wookie"
    return render_template('menu/future.html')

@menu_app.route('/create_snap', methods=('GET', 'POST'))
def create_snap():
    '''
    Under Development
    '''

    msg = "Functionaility under development, ask the wookie"
    return render_template('menu/future.html')

@menu_app.route('/get_snap_delete', methods=('GET', 'POST'))
def get_snap_delete():
    '''
    Under Development
    '''

    msg = "Functionaility under development, ask the wookie"
    return render_template('menu/future.html')

@menu_app.route('/delete_snap', methods=('GET', 'POST'))
def delete_snap():
    '''
    Under Development
    '''

    msg = "Functionaility under development, ask the wookie"
    return render_template('menu/future.html')

#--------------------------------Clone Section --------------------------------

@menu_app.route('/get_clone', methods=('GET', 'POST'))
def get_clone():
        '''
        Present Volume list to clone
        '''
        volz = []
        vols = Volumes.objects()
        for v in vols:
            name = v.name
            volz.append(name)

        return render_template('menu/create_clone.html', volz=volz)

@menu_app.route('/create_clone', methods=('GET', 'POST'))
def create_clone():
    '''
    Under Development
    '''

    msg = "Functionaility under development, ask the wookie"
    return render_template('menu/future.html')
