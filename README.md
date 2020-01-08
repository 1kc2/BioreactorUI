# Bioreactor Control System UI
Project files for the bioreactor control system and user interface.


## Overview
This is the user interface displayed on a computer, connected via USB to the MSP432 microcontroller. The entire system is comprised of stirring speed, heating and pH management and control systems. The UI also displays real-time values from each subsystem ( _via serial communication_ ) and plots these data on three graphs - the user can display any one of these graphs. Users with elevated access privileges can also manually adjust these values to suit their needs.


## Dependencies
* For serial communication between the MSP432 board and the UI, the external module [Pyserial](https://pypi.org/project/pyserial/) must also be installed.

* There are no other dependencies required to use the control system except for the _Energia_, _Code Composer Studio (CCS)_ and a version of _Python_ **3.6.9** or newer.

_Please do note that there are problems with Energia and CCS on newer versions of MacOS so the UI will only safely run on Windows and Linux._



## Running the UI
The UI is run by running the `controller.py` file but keep in mind that an Energia sketch needs to be currently running on the MSP board for any of its output to be displayed on the UI. No other files need to be accessed.

_As a side note: the system can detect the serial port being used by the MSP432 board at runtime depending on the operating system of the PC._
* _Windows: **COM34**_
* _Linux/Mac: **/dev/ttyACM0**_



## Using the UI
### The UI allows the user to:
* Observe real-time data from each subsystem in a simple graph plot
* Manager the operation of the control system (with the correct privileges)
* Shutdown the entire bioreactor if needed in emergency situations

The control system has to access levels: **GUEST** and **ADMIN**.
* The **GUEST** is able to view graphs representing the current state of the bioreactor and is able to shutdown operation altogether in emergency situations.

* The **ADMIN** can perform all actions a **GUEST** can but has an additional privilege: they have the option to alter the operation of the bioreactor in a separate menu, allowing them to adjust the pH, stirring speed and temperature of the bioreactor.


