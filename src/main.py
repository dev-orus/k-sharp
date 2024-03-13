from dataclasses import dataclass
from stdio.h import *
@dataclass
class Point:
  x: int
def main() -> int:
  mytest: Ptr[Point] = Ptr(Point(10))
  mytest.value.x
  {'x': mytest.value.x}
  printf("{0}", mytest.value.x)
  return 0
if __name__ == "__main__":main()