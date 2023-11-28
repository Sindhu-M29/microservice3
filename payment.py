from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/getTotalAmount', methods=['GET'])
def get_total_amount():
    # Get the flight number and number of seats from query parameters
    flight_number = request.args.get('flight_number')
    num_seats = int(request.args.get('num_seats', 0))  # Default to 0 if not provided

    if not flight_number:
        return jsonify({'error': 'Flight number is required'}), 400




    Flight = f'http://172.17.0.3:5000/getAvailableFlights'

   
    api1_response = requests.get(Flight)

    if api1_response.status_code == 200:
        available_flights = api1_response.json()['flights']

        # Find the flight with the specified flight number
        selected_flight = next((flight for flight in available_flights if flight['flightNumber'] == flight_number), None)

        if selected_flight:
            # Calculate the total amount based on the specified number of seats
            total_amount = num_seats * selected_flight['fare']
            return jsonify({'flightNumber': flight_number, 'numSeats': num_seats, 'totalAmount': total_amount})
        else:
            return jsonify({'error': 'Flight not found'}), 404
    else:
        return jsonify({'error': 'Failed to retrieve data from API1'}), api1_response.status_code

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001)

