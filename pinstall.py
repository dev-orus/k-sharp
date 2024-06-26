import os
from json import dumps
from sys import argv

# Windows not supported (yet)
if os.name == 'nt':...
else:
    input('WARNING: Please make sure you have the latest version of node and npm\nPress enter to continue')
    d = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(d, 'env')):
        os.system(f'python3.12 -m venv {os.path.join(d, 'env')}')
        os.system(f'{os.path.join(d, 'env', 'bin', 'pip')} install regex jedi')
    if not os.path.exists(os.path.join(d, 'bin')):
        os.mkdir(os.path.join(d, 'bin'))
    with open(os.path.join('/usr', 'bin', 'wisp'), 'w')as f:
        f.write(f"""#!/bin/bash
{os.path.join(d, 'env', 'bin', 'python3')} {os.path.join(d, 'wisp.py')} $1""")
    with open(os.path.join('/usr', 'bin', 'wisp-lsp'), 'w')as f:
        f.write(f'#!/bin/bash\n{argv[1]} {os.path.join(d, 'lsp', 'out', 'index.js')} "$@"')
    os.system('sudo chmod +x '+os.path.join('/usr', 'bin', 'wisp'))
    os.system('sudo chmod +x '+os.path.join('/usr', 'bin', 'wisp-lsp'))
    # os.system(f'echo \'export PATH="{os.path.join(d, 'bin')}:$PATH"\' >> ~/.bashrc')
    print('done')
    # print(f'Restart your terminal and try running wisp. if it doesnt work add this to your ~/.bashrc:\nexport PATH="{os.path.join(d, 'bin')}:$PATH"')

p = 'env/lib/'+os.listdir('env/lib')[0]+'/site-packages/stdio'
if not os.path.exists(p):
    os.mkdir(p)
    with open(os.path.join(p, '__init__.py'), 'w')as f:f.write("""import stdlib

def printf(STRING: str, *values, end="\\n", flush=False):
  print(STRING.format(*values), end=end, flush=flush)
def scanf(toOut: stdlib.Ptr):
  toOut.value = input()""")
p = 'env/lib/'+os.listdir('env/lib')[0]+'/site-packages/stdlib'
if not os.path.exists(p):
    os.mkdir(p)
with open(os.path.join(p, '__init__.py'), 'w')as f:f.write("""from typing import Generic, TypeVar, List, Any as any
T = TypeVar("T")
class Ptr(Generic[T]):
  def __init__(self, value: T):self.value = value""")