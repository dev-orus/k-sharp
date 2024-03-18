import os
from json import dumps

# Windows not supported (yet)
if os.name == 'nt':...
else:
    d = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(d, 'env')):
        os.system(f'python3 -m venv {os.path.join(d, 'env')}')
        os.system(f'{os.path.join(d, 'env', 'bin', 'pip')} install regex jedi')
    if not os.path.exists(os.path.join(d, 'bin')):
        os.mkdir(os.path.join(d, 'bin'))
    with open(os.path.join(d, 'bin', 'ksharp'), 'w')as f:
        f.write(f"""#!sh
{os.path.join(d, 'env', 'bin', 'python3')} {os.path.join(d, 'ksharp.py')} $1""")
    with open(os.path.join(d, 'bin', 'ksharp-lsp'), 'w')as f:
        f.write(f"#!/bin/bash\necho '{dumps({'env': os.path.join(d, 'env', 'bin', 'python3'), 'file': os.path.join(d, 'lsp.py')})}'")
    os.system('chmod +x '+os.path.join(d, 'bin', 'ksharp'))
    os.system('chmod +x '+os.path.join(d, 'bin', 'ksharp-lsp'))
    print(f'now on your bashrc, zshrc, etc: add this:\nexport PATH="{os.path.join(d, 'bin')}:$PATH"')
