from compiler.syntax import *
from compiler import transpile

codeIn = """use os::path::{dirname, exists};"""

out = transpile(codeIn)

print(out)