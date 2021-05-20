#!/usr/bin/env python3

# Import the required modules
import argparse
from nimbleclient import NimOSClient

# The NimbleInventory class
class NimbleInventory:
    def __init__(self, username, password, arrays):
        self.inventory = {}
        self.username = username
        self.password = password
        self.arrays = arrays
        self.fetch()

    # Loop over requested arrays and gather the data
    def fetch(self):
        for array in self.arrays:
            try:
                api = NimOSClient(array, self.username, self.password)
                entry = api.arrays.get()
                self.inventory[entry.attrs.get('name')] = [entry.attrs.get('version'),
                                           entry.attrs.get('extended_model'),
                                           entry.attrs.get('serial')]
            except:
                self.inventory[array] = ['n/a', 'n/a', 'n/a']

    # Print the list of arrays in a spreadsheet friendly manner
    def report(self):
        for xlsout in self.inventory:
            print ("{name}\t{version}\t{model}\t{serial}".format(name=xlsout,
                                                         version=self.inventory[xlsout][0],
                                                         model=self.inventory[xlsout][1],
                                                         serial=self.inventory[xlsout][2]))

# If called directly
if __name__ == '__main__':
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Nimble array inspector')
    parser.add_argument('--username', required=True,
                    type=str, help='Nimble OS username')
    parser.add_argument('--password', required=True,
                    type=str, help='Nimble OS password')
    parser.add_argument('--array', required=True, type=str,
                    help='Nimble array hostname or IP address', nargs='+')
    args = parser.parse_args()

    # New inventory
    data = NimbleInventory(args.username, args.password, args.array)

    # Report
    data.report()
