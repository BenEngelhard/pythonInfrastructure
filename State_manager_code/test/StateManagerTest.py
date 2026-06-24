from State_manager_code.StateManager import StateManager
from State_manager_code.StateManager import States
from State_manager_code.StateManager import Events

##### main
events = 0
stateManager = StateManager()
stateManager.SetFixedTimeOut(10, 15)
stateManager.SetVariableTimeOut(5)

while events != -1:
    eventstr = input("enter event value: ")
    events = int(eventstr)

    if events == -1:
        print("Program terminated")
    else:
        currentState = stateManager.DetermineState(events)
        print(f'Current State: {currentState}')
        if currentState == States.End:
            print('Session Ended')
            events = -1


'''
        Mouse1InCenter = 1
        Mouse2InCenter = 2
        Mouse1Cooporated = 4
        Mouse2Cooporated = 8
        Mouse1Defected = 16
        Mouse2Defected = 32
        LastTrial = 64
        RewardDelivered = 128
        ExperimentStopped = 256

'''