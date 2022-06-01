# BTAdmin
Administrative scripts and utilities for Senior Project at UOP.
BTAdmin performs decisionmaking based on processed data from the input modules (camera, radar, and GPS), and sends output to the hardware controllers (throttle, steering, brakes).
All input modules and the braking module were successfully implemented.
Communicates with each module via the `btcomms` script, which is a basic wrapper for UDS sockets.
Other files are for testing purposes.
