# this code profiler keeps track of frame rate and calculates the CPU usage of the 5 most
# time-consuming functions. It does not handle nested functions. Time spent in nested function
# will be accrued both to the calling and nested function.

import time
from Experiment_Launcher_code.ModuleConfiguration import __FRAME_RATE_ONLY


FunctionEntries = {}
AveragePeriodStart = 0
FrameCounter = 0
IdleLoopsCounter = 0
FunctionStartTime = {}
FunctionName = []
FunctionTime = []
MainLoopHandlingTime = []
MainLoopStartTime = 0

def IdleLoop():
    global IdleLoopsCounter
    IdleLoopsCounter += 1

def NewFrame():
    global FrameCounter
    FrameCounter += 1

def EnterMainLoop():
    global FrameCounter, AveragePeriodStart
    global FunctionName, FunctionTime, IdleLoopsCounter
    global MainLoopStartTime, MainLoopHandlingTime

    if AveragePeriodStart == 0:   # first period starts
        AveragePeriodStart = time.time()

    if MainLoopStartTime == 0:
        MainLoopStartTime = time.time()
    else:
        print(f'Code Profiler Error. Main loop handling routine missing exit point')

    period = time.time() - AveragePeriodStart
    if period > 20:
        framerate = FrameCounter/period
        idleloops = IdleLoopsCounter/period
        print(f'Frame Rate= : {framerate:.2f}')
        print(f'Idle Loops= : {idleloops:.2f}')
        MainLoopCPUUsage = sum(MainLoopHandlingTime) / period * 100
        print(f'CPU usage= : {MainLoopCPUUsage:.2f}')
        MainLoopHandlingTime = []
        AveragePeriodStart = time.time()
        FrameCounter = 0
        IdleLoopsCounter = 0
        CalculateFunctionAverages(period)
        for index in range(len(FunctionTime)):
            if FunctionTime[index] > 0:
                print(f'CPU usage: {FunctionName[index]}, {FunctionTime[index]:.2e}%')

def ExitMainLoop():
    global MainLoopStartTime, MainLoopHandlingTime

    if MainLoopStartTime == 0:
        print(f'Code Profiler Error. Main loop handling routine missing entry point')
    else:
        MainLoopHandlingTime.append(time.time() - MainLoopStartTime)
        MainLoopStartTime = 0

def EnterFunction(name):
    global FunctionStartTime

    if name in FunctionStartTime and FunctionStartTime[name] != 0:
        print(f'Code Profiler Error. Function {name} missing an exit point')
    else:
        FunctionStartTime[name] = time.time()

def ExitFunction(name):
    global FunctionStartTime, FunctionEntries

    if name in FunctionStartTime:
        functiontime = time.time() - FunctionStartTime[name]
        FunctionStartTime[name] = 0

        if name not in FunctionEntries:
            # FunctionEntries[name] = [functiontime]
            FunctionEntries[name] = []
        FunctionEntries[name].append(functiontime)
    else:
        print(f'Code Profiler Error. Function {name} missing an entry point')


def CalculateFunctionAverages(period):
    global FunctionEntries, FunctionName, FunctionTime

    if __FRAME_RATE_ONLY:
        FunctionEntries = {}
    else:
        topcount = 5
        FunctionName = [''] * topcount
        FunctionTime = [0] * topcount

        for function in FunctionEntries:
            functionCPUUsage = sum(FunctionEntries[function]) / period * 100
            for index in range(topcount):
                if functionCPUUsage > FunctionTime[index]:
                    for pushindex in range(topcount - 1, index, -1):
                        FunctionName[pushindex] = FunctionName[pushindex - 1]
                        FunctionTime[pushindex] = FunctionTime[pushindex - 1]
                    FunctionName[index] = function
                    FunctionTime[index] = functionCPUUsage
                    break

        FunctionEntries = {}

