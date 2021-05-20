#!/usr/bin/env python3

# Import the required modules
from .make_client import client
from datetime import datetime
from database.events import Events



def events(hostip,username,password):

    # Clear the events database.
    Events.objects().delete()

    # Connect to the system
    api = client(hostip,username,password)
    # Setup some variables
    event_data = []
    # Get the arrays
    event = api.events.list()

    for e in event:

        entry = api.events.get(e.attrs['id']).attrs

        time = datetime.fromtimestamp(entry['timestamp']).strftime('%d-%m-%y, %H:%M:%S')

        eventz = [
                entry['category'],
                time,
                entry['severity'],
                entry['summary']
                ]

        
        # Build database entry to save event
        record = Events(category=entry['category'],
                        time=time,
                        severity=entry['severity'],
                        summary=entry['summary'])

        # Save the record
        try:
            record.save()
        except:
            error="sub-ERR00x - Failed to initialize the events database"
            return render_template('error/gen_error.html', error=error)


        event_data.append(eventz)


    return event_data
