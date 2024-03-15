import os
from json import dumps, loads
from completion import getCompletion

while True:
    # Get the data using stdio
    data = loads(input())
    if data['type'] == 'completion':
        print(getCompletion(data['source'], data['line'], data['col']))
    elif data['type'] == 'check':
        ...
