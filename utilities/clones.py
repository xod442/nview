#!/usr/bin/env python3

# Import the required modules
from .make_client import client
from database.volumes import Volumes



def volumes(hostip,username,password):

    # Clear the volumes database.
    Volumes.objects().delete()

    # Connect to the system
    api = client(hostip,username,password)
    # Setup some variables
    volume = []
    # Get the arrays
    vols = api.volumes.list()

    for v in vols:

        entry = api.volumes.get(v.attrs['id']).attrs

        volz = [
                entry['name'],
                entry['dedupe_enabled'],
                entry['block_size'],
                entry['online'],
                entry['thinly_provisioned'],
                entry['encryption_cipher']
                ]

        # Stringify the vars
        name = entry['name']
        dedupe = str(entry['dedupe_enabled'])
        block_size = str(entry['block_size'])
        online = str(entry['online'])
        thin = str(entry['thinly_provisioned'])
        encrypt = entry['encryption_cipher']


        # Build database entry to save event
        record = Volumes(name=name,
                         dedupe=dedupe,
                         block_size=block_size,
                         online=online,
                         thin=thin,
                         encrypt=encrypt)

        # Save the record
        try:
            record.save()
        except:
            error="sub-ERR00x - Failed to initialize the volumes database"
            return render_template('error/gen_error.html', error=error)

        

        volume.append(volz)


    return volume
