import os
from json import dumps, loads
from completion import getCompletion, getDefinition
import sys
import traceback


parent = os.path.dirname(__file__)
buffer = ''

while True:
    # Get the data using stdio
    while True:
        buffer += sys.stdin.readline()
        try:
            loads(buffer)
            break
        except:...
    try:
        data = loads(buffer)
        buffer = ''
        if data['type'] == 'completion':
            out = dumps(getCompletion(str(data['source']), int(data['line']), int(data['col']), str(data['file'])))
            print(out, file=sys.stderr)
        elif data['type'] == 'check':
            ...
        elif data['type'] == 'definition':
            out = dumps(getDefinition(str(data['source']), int(data['line']), int(data['col']), str(data['file'])))
            print(out, file=sys.stderr)
    except Exception as e:
        with open(os.path.join(parent, 'err.log'), 'w') as f:
            f.write(str('\n'.join(traceback.format_exception(type(e), e, e.__traceback__))))

