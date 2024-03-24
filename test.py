from compiler.syntax import *
from compiler import transpile

codeIn = """if (x) {}
try {
    x()
}
except (a as e) {
 pass
}"""

out = transpile(codeIn)

print(out)