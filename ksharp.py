import compiler
from sys import argv
import re
from json import load, dump
from os import system, path, listdir, mkdir, name

def transpile(fname):
    with open(fname)as f:
        with open(path.join(conf['outDir'], fname).removesuffix('ks')+'py', 'w')as fy:
            if conf['compact']:
                fy.write(re.sub(r'\n\s*\n', '\n', compiler.transpile_code(f.read())))
            else:
                fy.write(compiler.transpile_code(f.read()))

def listDir(c):
    for i in listdir(c):
        x = path.join(c, i)
        if x.endswith('.ks'):
            transpile(x)
        elif x in conf['includes']:
            listdir(x)

if __name__ == "__main__":
    if path.exists('ksconfig.json'):
        with open('ksconfig.json')as f:
            conf = load(f)
    else:
        conf = {'outDir': 'out', 'compact': True, 'includes': '', 'modules': []}
    if len(argv) == 1:
        print('ksharp <type>\ntypes:', 'build: builds', 'install: installs modules in the modules directory', 'init: create ksconfig file', sep='\n  ')
        quit()
    if argv[1] == 'build':
        if not path.exists(conf['outDir']):
            mkdir(conf['outDir'])
        listDir('.')
        if name == 'nt':...
        else:
            system(f'.venv/bin/python -m mypy {conf['outDir']}')
    elif argv[1] == 'run':
        if not path.exists(conf['outDir']):
            mkdir(conf['outDir'])
        listDir('.')
        if name == 'nt':...
        else:
            system(f'.venv/bin/python -m mypy {conf['outDir']}')
        if name == 'nt':...
        else:
            system(f'.venv/bin/python {path.join(conf['outDir'], 'main.py')}')
    elif argv[1] == 'install':
        if not path.exists('.venv'):
            system('python3 -m venv .venv')
        p = '.venv/lib/'+listdir('.venv/lib')[0]+'/site-packages/stdio'
        if not path.exists(p):
            mkdir(p)
            with open(path.join(p, '__init__.py'), 'w')as f:f.write('')
            with open(path.join(p, 'h.py'), 'w')as f:f.write("""from builtins import open as fopen
from typing import Generic, TypeVar, List, Any as any
T = TypeVar("T")

class Ptr(Generic[T]):
    def __init__(self, value: T):self.value = value
    
def printf(STRING: str, *values, end="\\n", flush=False):
  print(STRING.format(*values), end=end, flush=flush)
def scanf(toOut: Ptr):
  toOut.value = input()""")
        if name == 'nt':...
        else:
            system(f'.venv/bin/pip install mypy')
            for m in conf['modules']:
                system(f'.venv/bin/pip install {m}')
    elif argv[1] == 'init':
        with open('ksconfig.json', 'w')as f:
            dump({'outDir': 'out', 'compact': True, 'includes': '', 'modules': [], 'comments': False}, f, indent=2)
    else:
        print('ksharp <type>\ntypes:', 'build: builds', 'install: installs modules in the modules directory', 'init: create ksconfig file', sep='\n  ')