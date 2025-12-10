import time
from enum import Enum

class States(Enum):
        Start = 1
        CenterReward = 2
        TrialStarted = 3
        M1CM2C = 4
        M1CM2D = 5
        M1DM2C = 6
        M1DM2D = 7
        TrialCompleted = 8
        ReturnTimeOut = 9
        DecisionTimeOut = 10
        M1FirstInCenter = 11
        M2SecondInCenter = 12
        M2FirstInCenter = 13
        M1SecondInCenter = 14
        Abort = 15
        End = 16

class Events(Enum):
        Mouse1InCenter = 1
        Mouse2InCenter = 2
        Mouse1Cooporated = 4
        Mouse2Cooporated = 8
        Mouse1Defected = 16
        Mouse2Defected = 32
        LastTrial = 64
        RewardDelivered = 128
        ExperimentStopped = 256

class StateManager:
        def __init__(self):

            self.NextState = {
                        States.Start: [States.CenterReward, States.End],
                        States.CenterReward: [States.TrialStarted],
                        States.TrialStarted: [States.M1CM2C, States.M1CM2D, States.M1DM2C, States.M1DM2D, States.End],
                        States.M1CM2C: [States.TrialCompleted, States.End],
                        States.M1CM2D: [States.TrialCompleted, States.End],
                        States.M1DM2C: [States.TrialCompleted, States.End],
                        States.M1DM2D: [States.TrialCompleted, States.End],
                        States.TrialCompleted: [States.End, States.M1FirstInCenter, States.M2FirstInCenter, States.End],
                        States.ReturnTimeOut: [States.End],
                        States.DecisionTimeOut: [States.End],
                        States.M1FirstInCenter: [States.M2SecondInCenter],
                        States.M2SecondInCenter: [States.TrialStarted, States.End],
                        States.M2FirstInCenter: [States.M1SecondInCenter],
                        States.M1SecondInCenter: [States.TrialStarted, States.End],
                        States.Abort: [States.TrialStarted, States.End],
                        States.End: [States.End]
                    }

            self.TransitionEvent = {
                        States.Start: [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value,
                                       Events.ExperimentStopped.value],
                        States.CenterReward: [],
                        States.TrialStarted: [Events.Mouse1Cooporated.value + Events.Mouse2Cooporated.value,
                                              Events.Mouse1Cooporated.value + Events.Mouse2Defected.value,
                                              Events.Mouse1Defected.value + Events.Mouse2Cooporated.value,
                                              Events.Mouse1Defected.value + Events.Mouse2Defected.value,
                                              Events.ExperimentStopped.value],
                        States.M1CM2C: [],
                        States.M1CM2D: [],
                        States.M1DM2C: [],
                        States.M1DM2D: [],
                        States.TrialCompleted: [Events.LastTrial.value,
                                                Events.Mouse1InCenter.value, Events.Mouse2InCenter.value,
                                                Events.ExperimentStopped.value],
                        States.ReturnTimeOut: [Events.ExperimentStopped.value],
                        States.DecisionTimeOut: [Events.ExperimentStopped.value],
                        States.M1FirstInCenter: [Events.Mouse2InCenter.value],
                        States.M2SecondInCenter: [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value,
                                                  Events.ExperimentStopped.value],
                        States.M2FirstInCenter: [Events.Mouse1InCenter.value],
                        States.M1SecondInCenter: [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value,
                                                  Events.ExperimentStopped.value],
                        States.Abort: [Events.Mouse1InCenter.value + Events.Mouse2InCenter.value,
                                      Events.ExperimentStopped.value],
                        States.End: []
                    }

            self.TimeOutState = {
                States.Start: None,
                States.CenterReward: States.TrialStarted,
                States.TrialStarted: States.DecisionTimeOut,
                States.M1CM2C: States.TrialCompleted,
                States.M1CM2D: States.TrialCompleted,
                States.M1DM2C: States.TrialCompleted,
                States.M1DM2D: States.TrialCompleted,
                States.TrialCompleted: States.ReturnTimeOut,
                States.ReturnTimeOut: States.Abort,
                States.DecisionTimeOut: States.Abort,
                States.M1FirstInCenter: States.ReturnTimeOut,
                States.M2SecondInCenter: None,
                States.M2FirstInCenter: States.ReturnTimeOut,
                States.M1SecondInCenter: None,
                States.Abort: None,
                States.End: None
            }

            self.TransitionTimeOut = {
                States.Start: None,
                States.CenterReward: 1,
                States.TrialStarted: 10,  # 10 seconds is a default value. It is replaced by the SetTimeOut functions.
                States.M1CM2C: 0,
                States.M1CM2D: 0,
                States.M1DM2C: 0,
                States.M1DM2D: 0,
                States.TrialCompleted: 10,  # 10 seconds is a default value. It is replaced by the SetTimeOut functions.
                States.ReturnTimeOut: 1,
                States.DecisionTimeOut: 1,
                States.M1FirstInCenter: 10, # 10 seconds is a default value. It is replaced by the SetTimeOut functions.
                States.M2SecondInCenter: None,
                States.M2FirstInCenter: 10, # 10 seconds is a default value. It is replaced by the SetTimeOut functions.
                States.M1SecondInCenter: None,
                States.Abort: None,
                States.End:None
            }

            self.current_state = States.Start
            self.StateStartTime = time.time()

        def SetFixedTimeOut(self, decision_time, return_time):
            self.TransitionTimeOut[States.TrialStarted] = decision_time
            self.TransitionTimeOut[States.TrialCompleted] = return_time

        def SetVariableTimeOut(self, return_time):
            self.TransitionTimeOut[States.M1FirstInCenter] = return_time
            self.TransitionTimeOut[States.M2FirstInCenter] = return_time

        def DetermineState(self, events):
            TransitionEvents = self.TransitionEvent[self.current_state]

            # Check and Perform Event base transition
            for i, event in enumerate(TransitionEvents):
                if event & events == event:

                    # Transition to the next state based on the event
                    self.current_state = self.NextState[self.current_state][i]
                    self.StateStartTime = time.time()
                    return self.current_state

            # Check and Perform timeout base transition
            if self.TimeOutState[self.current_state]:
                if time.time() - self.StateStartTime > self.TransitionTimeOut[self.current_state]:

                    self.current_state = self.TimeOutState[self.current_state]
                    #print("timeout state",self.current_state )
                    self.StateStartTime = time.time()

            return self.current_state