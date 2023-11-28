from flask import Flask, jsonify, request
import requests
import os

# Use the environment variable for the URL
API_URL = os.environ.get('API_URL', 'http://127.0.0.1:5000')
URL = API_URL + "/getAvailableFlights"
# URL = "http://127.0.0.1:5000" + "/getAvailableFlights"

app = Flask(__name__)

@app.route('/getTotalAmount', methods=['GET'])
def get_total_amount():
    # Get the flight number and number of seats from query parameters
    flight_number = request.args.get('flight_number')
    num_seats = int(request.args.get('num_seats', 0))  # Default to 0 if not provided

    if not flight_number:
        return jsonify({'error': 'Flight number is required'}), 400

    if num_seats <= 0:
        return jsonify({'error': 'Number of seats must be greater than zero'}), 400

    try:
        # Use the URL variable instead of the string 'URL'
        api1_response = requests.get(URL)

        api1_response.raise_for_status()  # Raise an HTTPError for bad responses

        available_flights = api1_response.json()['flights']

        # Find the flight with the specified flight number
        selected_flight = next((flight for flight in available_flights if flight['flightNumber'] == flight_number), None)

        if selected_flight:
            # Calculate the total amount based on the specified number of seats
            total_amount = num_seats * selected_flight['fare']
            return jsonify({'flightNumber': flight_number, 'numSeats': num_seats, 'totalAmount': total_amount})
        else:
            return jsonify({'error': 'Flight not found'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to retrieve data from API1. {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
