import serial
import time

# Establish the connection on a specific port
ser = serial.Serial('COM11', 9600) # Replace 'COM3' with your Arduino's serial port
time.sleep(2) # Wait for the connection to be established

def send_command(command):
    ser.write(command.encode())

try:
    while True:
        cmd = input("Enter 'H' to turn on LED or 'L' to turn off LED: ")
        if cmd in ['H', 'L']:
            send_command(cmd)
        else:
            print("Invalid command")
except KeyboardInterrupt:
    ser.close()
