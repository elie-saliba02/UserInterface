# User Interface
User Interface for SsMachMo 

Current State of the project :
Gateway can scan for only one server device and connect to it, and toggle its LED.
Currently the application has one process and two threads. Main thread for the user interface and a worker thread for the bluetooth connection. The threads are communicating via a queue. Queues are FIFO type of communication, convenient because they are thread safe and therefore no need to worry about race conditions. 

Future Development: 
Want the Gateway to collect a stream of data from the microphone and the accelerometer. This is done by indication or notification. 
Need to build a GATT profile on the peripheral device and make it compatible with the gateway. Note: add a time charactersitic within this profile to determine for how long we want to collect this data. 
Send data to the openPHM project. Chapter 9 from the book.
Scan for multiple devices with a specific UUID. Allow the gateway to connect to multiple devices at the same time. This can be done by giving each connection its own process to run in. The User Interface can run in the main process, that creates a sub-process for each connection. Subprocess creates a thread for the BLE conncetion, and another one for the cloud data upload. That requires us to find a way to communicate between processes.

Demo:
Flash Blinky Example on peripheral device. Compile the python project, scan, connect, and toggle LED button to watch the LED0 on board turn ON and OFF.
Optional : Connect an LED to Pins 8 and Gnd. 

Libraries : Bleak, Asyncio, PyQt5

GUI:

<img width="251" alt="Screen Shot 2023-05-04 at 3 19 43 PM" src="https://user-images.githubusercontent.com/113550223/236309644-2f8f871a-882f-4cd0-aac1-fdf41da5979c.png">

Board:

<img width="685" alt="Screen Shot 2023-05-04 at 3 27 29 PM" src="https://user-images.githubusercontent.com/113550223/236309691-10fecdff-3719-425f-97d9-e5ee8a9c0b8b.png">



Recommended IDE : PyCharm

Reference book : Python concurrency with asyncio by Matthew Fowler
