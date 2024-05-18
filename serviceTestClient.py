# Test client for convertorMicroservice.py

import zmq

def main():
    context = zmq.Context()
    print("Connecting to the conversion microservice...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    while True:
        user_input = input("Enter value & unit(ex. '3.52 teaspoons'): ").strip().lower()
        if user_input == 'exit':
            stop_command = {"command": "stop"}
            print(f"Sending stop command: {stop_command}")
            socket.send_json(stop_command)
            break
        try:
            value, unit = user_input.split()
            value = float(value)
            data = {"value": value, "unit": unit}
            print(f"Sending request: {data}")
            socket.send_json(data)
            message = socket.recv_json()
            print(f"Received reply: {message}")
        except ValueError:
            print("Invalid input. Please enter the value and unit separated by a space, or 'exit' to stop.")
        except KeyError:
            print("Unexpected response from the server.")

if __name__ == "__main__":
    main()
