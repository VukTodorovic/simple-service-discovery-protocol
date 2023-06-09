# simple-service-discovery-protocol
SSDP (Simple Service Discovery protocol) implemented in Python

## Description
- This project features an implementation of SSDP in Python programming language. It consists of 2 Python files, one representing the controller that broadcasts SSDP M-SEARCH message every 10 seconds to search for available devices on the network and other one that represents every smart device that sends SSDP NOTIFY-alive message to respond to M-SEARCH to notify the controller that it's alive and inform it about it's device specification.

## Controller
- Code for the controller is located at **controller.py** file.
- It is a simple networking program that creates 2 UDP sockets, one for sending the broadcast messages to search for available devices and other one to receive responses to. The receiving and the search socket are managed by different threads, search happens on the main thread of the program and receiving socket is managed by additional thread that is created. Search logic is simple, program sends M-SEARCH message over the socket encoded as UTF-8 and then sleeps for 10 seconds. The receiving logic is as follows: if the received message is of type "NOTIFY", extract the values from the message and print information about device that had sent it on the console.

## Smart device
- Code for the smart device is located at **smart_device.py** file.
- It is a mock program of the smart device that listens for the broadcasted datagrams and when receives one, it first checks that it is of type M-SEARCH and if it is, it first prints the data about the device that sent it, then it extracts the data from the message and fires up a function for handling the NOTIFY response using the thread pool with the arguments being ip address of the device that sent the M-SEARCH and MX being the maximum time that the device should wait before sending the NOTIFY message. Then in the NOTIFY handler function, first the thread sleeps between 0 and MX seconds and then sends a NOTIFY response encoded as UTF-8 string. It than prints to the console that the NOTIFY was sent with the information about the destination address and the delay that was waited before sending it. The tread pool approach is implemented because the smart device should not be blocked to listen for new M-SEARCH requests and responding to them while waiting to send the previous NOTIFY response.
