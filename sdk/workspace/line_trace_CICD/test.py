import mmap
import contextlib
import time
import struct
print("start")


parameter1 = [-100.0, -1.0, -0.25, 0, 0.25, 1.0, 100.0]

base_offset = 540 + 32


def Parameter(offset):
    return base_offset + offset * 4


def Reset():
    with open("athrill_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            m[544] = 1
            time.sleep(1)
            m[544] = 0


def Setpara(para1):
    with open("unity_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            print("set", para1)
            m[Parameter(0):Parameter(0) + 4] = struct.pack('<f', para1)


# while True:
for i in parameter1:
    Setpara(i)
    while True:
        with open("unity_mmap.bin", mode="r+b") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                event = m[560]
                # GOAL
                if (event == 1):
                    print("GOAL")
                    goaltime_byte = m[564:572]
                    goaltime_int = int.from_bytes(goaltime_byte, 'little')
                    goaltime = goaltime_int/1000000
                    print("Goal time:", goaltime)
                    break
                # TIME_OVER
                elif (event == 2):
                    print("Time is over")
                    break
                # HIT_WALL
                elif (event == 3):
                    print("HIT WALL")
                    break
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
                time.sleep(1)
    print("Do reset")
    Reset()
