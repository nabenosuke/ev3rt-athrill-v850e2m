import mmap
import contextlib
import time
import struct
print("start")

parameter1 = [1, -0.5, -0.25, 0, 0.25]
parameter2 = [1, 0.005, 0.1, 0.5, 1]
parameter3 = [1, 2.5, 5, 7.5, 10]
parameter4 = [1, 0.5, 1, 1.15, 1.5]
parameter5 = [1, 0.02, 0.07, 0.09, 0.1]
parameter6 = [1, 0.05, 0.1, 0.2, 0.5]
parameter7 = [1, -0.01, -0.02, -0.1, -0.3]

base_offset = 540 + 32


def Parameter(offset):
    return base_offset + offset * 4


def Reset():
    with open("athrill_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            m[544] = 1
            time.sleep(1)
            m[544] = 0


def Setpara(para, j):
    with open("unity_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            print("set", para)
            m[Parameter(j):Parameter(j) + 4] = struct.pack('<f', para)


# リセットとパラメータ書き込みの順番
# while True:
for i in range(len(parameter1)):
    Setpara(parameter1[i], 1)
    Setpara(parameter2[i], 2)
    Setpara(parameter3[i], 3)
    Setpara(parameter4[i], 4)
    Setpara(parameter5[i], 5)
    Setpara(parameter6[i], 6)
    Setpara(parameter7[i], 7)
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
    print("Do reset")
    Reset()
