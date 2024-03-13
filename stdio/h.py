from builtins import open as fopen
from typing import Generic, TypeVar, List, Any as any
T = TypeVar("T")

class Ptr(Generic[T]):
    def __init__(self, value: T):self.value = value
    
def printf(STRING: str, *values, end="\n", flush=False):
  print(STRING.format(*values), end=end, flush=flush)
def scanf(toOut: Ptr):
  toOut.value = input() 