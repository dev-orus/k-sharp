import os

if os.name == 'nt':...
else:
    d = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(d, '/bin/ksharp')):
        os.mkdir(os.path.join(d, '/bin/ksharp'))
    with open(os.path.join(d, '/bin/ksharp'), 'w')as f:
        f.write(f"""#!sh
python3 {os.path.join(d, 'ksharp.py')} $1""")
    os.system('chmod +x '+os.path.join(d, 'bin', 'ksharp'))
    print(f'now on your bashrc, zshrc, etc: add this: export PATH="{os.path.join(d, 'bin')}:$PATH"')