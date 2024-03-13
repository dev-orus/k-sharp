import compiler
from sys import argv
import re
from ksconfig import compact

if __name__ == "__main__":
    with open(argv[1])as f:
        with open(argv[1].removesuffix('ks')+'py', 'w')as fy:
            if compact:
                fy.write(re.sub(r'\n\s*\n', '\n', compiler.transpile_code(f.read())))
            else:
                fy.write(compiler.transpile_code(f.read()))
