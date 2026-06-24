from  RunTimeAnalysis import *
import time

def display(event):
    print(event + '\n')

opcode = -1
rta = RunTimeAnalysis(20, 5, 25)
start = time.time()

while opcode != 0:
    print(f'current time {int(time.time() - start)}')
    opcodestr = input("opcode [0- exit, 1- mouse1 moved, 2- Mouse2 moved, 3- New Trial, 4- Analyze]: ")
    opcode = int(opcodestr)

    if opcode == 0:
        print("Program terminated")

    elif opcode == 1:
        rta.new_mouse_position(1)

    elif opcode == 2:
        rta.new_mouse_position(2)

    elif opcode == 3:
        rta.new_trial()

    elif opcode == 4:
        rta.event_analysis(display)

    else:
        print ("illegal opcode")