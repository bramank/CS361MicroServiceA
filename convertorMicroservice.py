import zmq

def convertor(value, unit):
    conversions = {
        'teaspoons': {'teaspoons': 1, 'tablespoons': 1/3, 'cups': 1/48},
        'tablespoons': {'teaspoons': 3, 'tablespoons': 1, 'cups': 1/16},
        'cups': {'teaspoons': 48, 'tablespoons': 16, 'cups': 1}
    }
    
    if unit not in conversions:
        raise ValueError(f"Unsupported unit: {unit}")
    
    result = {}
    for units, factor in conversions[unit].items():
        result[units] = round(value * factor, 2)
    
    return result

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("CONVERSION MICROSERVICE HAS STARTED...")
    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        if message.get('command') == 'stop':
            print("STOPPING CONVERSION SERVICE...")
            break
        try:
            value = message['value']
            unit = message['unit']
            result = convertor(value, unit)
            response = {"status": "success", "data": result}
        except Exception as e:
            response = {"status": "error", "message": str(e)}
        socket.send_json(response)

if __name__ == "__main__":
    main()
