import os

node = os.popen('/usr/bin/which node').read().strip()
print('using node: ', node)
os.system(f'sudo python3.12 pinstall.py {node}')