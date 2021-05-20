

'''
2021 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0.

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
from utilities.log import log
from utilities.inventory import inventory
from utilities.volumes import volumes
from utilities.events import events
from utilities.event_count import counter
from database.system import System
from database.events import Events
from database.volumes import Volumes
from utilities.get_creds import get
from utilities.save_creds import save
from database.creds import Creds

main_app = Blueprint('main_app', __name__)

@main_app.route('/main', methods=('GET', 'POST'))
@main_app.route('/', methods=('GET', 'POST'))
@main_app.route('/index', methods=('GET', 'POST'))
def main():
    ''' This section for any database preprocesses and capture login creds
    '''
    # Do any preprocessing here

    # Clear credential database on new session.
    # Creds.objects().delete()

    return render_template('main/login3.html')

@main_app.route('/main_load', methods=('GET', 'POST'))
def main_load():


    # If this is a Post it is from the login screen capture creds and save
    if request.method == 'POST':

        #Get creds from login
        hostip = request.form['hostip']
        username = request.form['username']
        password = request.form['password']
        # Save the record

        try:
            savecreds=save(hostip,username,password)
        except:
            error="ERR001 - Failed to save login credentials"
            return render_template('error/error.html', error=error)

        try:
            inv = inventory(hostip,username,password)
        except:
            error="ERR002 - Invalid Credentials...better luck next time"
            return render_template('error/error.html', error=error)

        usable = int(inv[6])

        #In a production demo chaneg this to be used = inv[7]
        #used = inv[7]
        used = 14968658889

        try:
            volz = volumes(hostip,username,password)
        except:
            error="ERR003 - Error getting system volumes"
            return render_template('error/gen_error.html', error=error)

        try:
            eventz = events(hostip,username,password)
        except:
            error="ERR004 - Error getting system events"
            return render_template('error/gen_error.html', error=error)

        try:
            counts = counter()
        except:
            error="ERR004 - Error getting system event counts"
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


        # Pie chart
        chartData2 = [
        {
        "category": "Available Capacity Bytes",
        "column-1": usable
        },
        {
        "category": "Used Space",
        "column-1": used
        }
        ]

        return render_template('main/main_menu.html', chartData=chartData,
                                                      chartData2=chartData2,
                                                      inventory=inv,
                                                      volumes=volz,
                                                      events=eventz)
@main_app.route('/main_return', methods=('GET', 'POST'))
def main_return():

    inventory = System.objects()
    name = inventory[0].name
    version = inventory[0].version
    serial = inventory[0].serial
    role = inventory[0].role
    nics = inventory[0].nics
    model = inventory[0].model
    usable = inventory[0].usable
    used = inventory[0].used
    inv = [version,model,serial,role,nics,name]


    volumes = Volumes.objects()
    volz = []
    for v in volumes:
        name = v.name
        dedupe = v.dedupe
        block_size = v.block_size
        online = v.online
        thin = v.thin
        encrypt = v.encrypt

        out = [name,dedupe,block_size,online,thin,encrypt]
        volz.append(out)

    try:
        counts = counter()
    except:
        error="ERR004 - Error getting system event counts"
        return render_template('error/gen_error.html', error=error)

    #In a production demo delete this value
    used = 14968658889


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


    # Pie chart
    chartData2 = [
    {
    "category": "Available Capacity Bytes",
    "column-1": usable
    },
    {
    "category": "Used Space",
    "column-1": used
    }
    ]
    return render_template('main/main_menu.html', chartData=chartData,
                                                  chartData2=chartData2,
                                                  inventory=inv,
                                                  volumes=volz)

@main_app.route('/main_logout', methods=('GET', 'POST'))
def main_logout():

    # Dump the dbs
    System.objects().delete()
    Volumes.objects().delete()
    Events.objects().delete()

    return render_template('main/login3.html')

@main_app.route('/main_refresh', methods=('GET', 'POST'))
def main_refresh():


        creds = get()

        username = str(creds[0], 'utf-8')
        password = str(creds[1], 'utf-8')
        hostip = str(creds[2], 'utf-8')    

        try:
            inv = inventory(hostip,username,password)
        except:
            error="ERR002 - Invalid Credentials...better luck next time"
            return render_template('error/error.html', error=error)

        usable = int(inv[6])

        #In a production demo chaneg this to be used = inv[7]
        #used = inv[7]
        used = 14968658889

        try:
            volz = volumes(hostip,username,password)
        except:
            error="ERR003 - Error getting system volumes"
            return render_template('error/gen_error.html', error=error)

        try:
            eventz = events(hostip,username,password)
        except:
            error="ERR004 - Error getting system events"
            return render_template('error/gen_error.html', error=error)

        try:
            counts = counter()
        except:
            error="ERR004 - Error getting system event counts"
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


        # Pie chart
        chartData2 = [
        {
        "category": "Available Capacity Bytes",
        "column-1": usable
        },
        {
        "category": "Used Space",
        "column-1": used
        }
        ]

        return render_template('main/main_menu.html', chartData=chartData,
                                                      chartData2=chartData2,
                                                      inventory=inv,
                                                      volumes=volz,
                                                      events=eventz)
