
'''

Elcano Carla Simulator Capstone
UW Bothell, 2020

Advisor : Tyler Folsom

Team 2019 : Zach Gale, Jonah Lim, Matthew Moscola, Francisco Navarro-Diaz
Team 2020 : Colton Sellers, Brandon Thompson

simulator.py

Version: 1.0

The main purposes of this program are:
    - Control creation of actors within Carla.
    - Retrieve simulated sensor data from actors and send to router board.
    - Interpret actuation data from router board and send actuation commands to Carla.

Much of the code that prepares the simulation (spawning actors and sensors) can be found in the examples
that come with the CARLA simulator download.

CARLA open-source simulator can be found here: http://Carla.org/

'''

#External imports
import sys

#import Carla and and Sensors
import Carla
import Elcano

def main(COMPort = 'COM10', IP = 'localhost', Port = 2000):

    #Create the simulated vehicle and connect to server
    trike = Elcano.SimulatedVehicle()
    trike.connectToSim(IP, Port)

    #Create the interface obj and connect to router
    Interface = Elcano.RouterboardInterface()
    Interface.connectToBoard(COMPort, baudrate = 115200, timeout=5)


    #Create command map for incoming commands from routerboard
    commandMap = {
        0: Interface.actuateThrottle,
        1: Interface.actuateSteering,
        2: Interface.actuateBraking,
        3: Interface.getAccelerometer,
    }

    #After initial setup this is the loop that processes commands from routerboard
    try:
        while True:

                #Commands in buffer
                if Interface.serial.in_waiting:

                    #Get the command function, if it doesn't exist, return failure.
                    command = commandMap.get(list(Interface.serial.read())[0], "Failure")

                    #If its a failure, continue go back to while loop.
                    #Will add some logging later to catch these errors in communication.
                    if command == "Failure":
                        continue
                    
                    #Execute the command
                    command(trike)
                    

    except KeyboardInterrupt:
        trike.destroy()
        sys.exit()


