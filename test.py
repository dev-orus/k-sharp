from compiler.syntax import *
from compiler import transpile

codeIn = """int* main(int x){
    x = [1, 2, 3, 4, 5];
}"""

out = transpile(codeIn)

print(out)