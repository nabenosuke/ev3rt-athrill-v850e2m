import mmap
import contextlib
import time
print("start")


def Reset():
    with open("athrill_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            m[544] = 1
            time.sleep(1)
            m[544] = 0


while True:
    while True:
        with open("unity_mmap.bin", mode="r+b") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                event = m[560]
                # GOAL
                if (event == 1):
                    print("GOAL")
                    time_byte = m[564:568]
                    time_int = int.from_bytes(time_byte, 'little')
                    time = time_int/1000000
                    print("Goal time:", time)
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
