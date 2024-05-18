# CS361MicroServiceA

This microservice converts given values into teaspoons, tablespoons, and cups. It uses ZeroMQ for communication with a client. 'convertorMicroservice.py' is the main convertor program. 'serviceTestClient.py' is an example client that can be used to test the convertor.

## Starting The Convertor
The program can be launched form the terminal or by another process using Python's subprocess module. The example call below will launch the program as a subprocess and surpress the native status messages from the convertor.

_subprocess.Popen(['python', 'convertorMicroservice.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)_

## Requesting Data
Once 'convertorMicroservice.py' is running, it accepts JSON data in the form _data = {"value": value, "unit": unit}_, with value being any float & unit being 'teaspoons', 'tablespoons', & 'cups'. The program
will convert a given value & unit into all three units. For example, _{'value': 3.5, "unit": 'tablespoons'}_ is converted into _{'teaspoons': 10.5, 'tablespoons': 3.5, 'cups': 0.22}_. All conversions are rounded
to the second decimal place. 

The convertor program listens for data from the default socket of 5555:

 _context = zmq.Context()_
 
 _socket = context.socket(zmq.REP)_
 
 _socket.bind("tcp://*:5555")_
 
_message = socket.recv_json()_

Converts the data:

_value = message['value']_

_unit = message['unit']_

_result = convertor(value, unit)_

And sends the response:

_response = {"status": "success", "data": result}_

_socket.send_json(response)_

## Recieving Data
To receive data from 'convertorMicroservice.py', the receiving program should do the following:

Establish a ZeroMQ socket connection:

_context = zmq.Context()_

_socket = context.socket(zmq.REQ)_

_socket.connect("tcp://localhost:5555")_

Send data:

_data = {"value": value, "unit": unit}_

_socket.send_json(data)_

Listen for the response:

_message = socket.recv_json()_

_print(f"Received reply: {message}")_

## Stopping the Conversion Microservice
To stop 'convertorMicroservice.py', send a 'stop' command in the form of _{"command": "stop"}_ to shutdown the microservice from a client. 
