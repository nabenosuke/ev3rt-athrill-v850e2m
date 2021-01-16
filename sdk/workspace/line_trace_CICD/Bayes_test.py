import mmap
import contextlib
import time
import struct
import GPy
import GPyOpt
import numpy as np
print("start")

loop_num = 3
penalty_time = 60
moter_power = 15
search_num = 15
flag_maximize = True

"""
parameters = []
parameters.append([0.9, 0.9, 0.9, 0.9, 0.6, 0.6, 0.6, 0.6])
parameters.append([0.1, 0.1, 0.3, 0.3, 0.1, 0.1, 0.3, 0.3])
parameters.append([1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5])
parameters.append([15, 15, 15, 15, 15, 15, 15, 15])

parameters_num = len(parameters)
test_num = len(parameters[0])
"""


base_offset = 540 + 32

result_file = open("result.txt", mode="w")


def Parameter_address(offset):
    return base_offset + offset * 4


def Reset():
    with open("athrill_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            m[544] = 1
            Unity_stop()
            time.sleep(1)
            m[544] = 0


def Unity_start():
    with open("athrill_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            m[548] = 1
            #print("unity_start")


def Unity_stop():
    with open("athrill_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            m[548] = 0
            #print("unity_stop")


def Setpara(parameter):
    with open("unity_mmap.bin", mode="r+b") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)) as m:
            string = "Set "
            for i in range(len(parameter)):
                string += str(parameter[i]) + ", "
                para_addr = Parameter_address(i)
                m[para_addr:para_addr +
                    4] = struct.pack('<f', parameter[i])
            print(string)
            result_file.writelines([string, "\n"])


def Do_test(x):
    Setpara([x[:,0], x[:,1], x[:,2], moter_power])
    #Setpara([x[:,0], x[:,1], 1, moter_power])
    #Unity_start()
    goal_count = 0
    fail_count = 0
    goaltime_sum = 0
    while(goal_count < loop_num and fail_count < loop_num):
        Unity_start()
        time.sleep(1)
        while True:
            # wait event
            with open("unity_mmap.bin", mode="r+b") as f:
                with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                    event = m[560]
                    # GOAL
                    if (event == 1):
                        goal_count += 1
                        print("GOAL")
                        goaltime_byte = m[532:540]
                        goaltime_double = struct.unpack('<Q', goaltime_byte)
                        goaltime = (int(goaltime_double[0])) / 1000000
                        goaltime_sum += goaltime
                        #print("Goal time:", goaltime)
                        result_file.writelines([str(goaltime), "\n"])
                        break
                    # TIME_OVER
                    elif (event == 2):
                        fail_count += 1
                        print("Time is over")
                        break
                    # HIT_WALL
                    elif (event == 3):
                        fail_count += 1
                        print("HIT WALL")
                        break
        Reset()
    #Unity_stop()
    if (goal_count == loop_num):
        goaltime_ave = goaltime_sum / loop_num
        print("Goaltime average:", goaltime_ave, "\n")
        result = penalty_time - goaltime_ave
    else:
        print("FAILED \n")
        result = 0
    time.sleep(10)
    return result


Unity_stop()
bounds = [{'name': 'Kp', 'type': 'continuous', 'domain': (0,1)},{'name': 'Ki', 'type': 'continuous', 'domain': (0,1)}, {'name': 'Kd', 'type': 'continuous', 'domain': (0,1)}]
#bounds = [{'name': 'Kp', 'type': 'continuous', 'domain': (0,1)},{'name': 'Ki', 'type': 'continuous', 'domain': (0,1)}]

myBopt = GPyOpt.methods.BayesianOptimization(f=Do_test, domain=bounds, maximize = flag_maximize)
myBopt.run_optimization(max_iter=15)
myBopt.plot_acquisition()

opt_para=str(myBopt.x_opt)
print(opt_para)
opt_time=str(penalty_time - myBopt.fx_opt)
print(opt_time)
result_file.close()
print("end")
time.sleep(1000)
