import mmap
import contextlib
import time
print("start")

with open("unity_mmap.bin", mode="r+b") as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
        m[572] = 100
