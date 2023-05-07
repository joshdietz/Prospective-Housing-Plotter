# Prospective Housing Plotter with Google Maps Integration

This Flask-based web app allows users to enter an address and view prospective housing options in relation to up to the work addresses of all the roommates. The app utilizes the Google Maps API to retrieve location data and plot the property on a map.

## Installation

To install and run the app, follow these steps:

1. Clone this repository onto your local machine.
2. Navigate to the root directory of the repository in your terminal.
3. Create a Python virtual environment by running the following command: `python -m venv env`.
4. Activate the virtual environment by running the following command:
   - For Mac/Linux users: `source env/bin/activate`
   - For Windows users: `.\env\Scripts\activate`
5. Install the necessary packages by running the following command: `pip install -r requirements.txt`.
6. Register for a Google Maps API key by following the instructions on the [Google Maps Platform documentation](https://developers.google.com/maps/gmp-get-started#create-project). Once you have your API key, create a `.env` file in the root directory of the repository and add the following line, replacing `YOUR_API_KEY` with your actual API key: `API_KEY=YOUR_API_KEY`.
7. Create a `persons.json` file in the root directory of the app. This file should be an array of JSON objects, where each object represents a "person" and contains the following keys:
   - `name`: the name of the roommate (string)
   - `work_address`: the address of the roommate's workplace (string)

## Usage

To run the app, activate the virtual environment (if it isn't already activated) and run the following command: `python3 app.py`. This will start the Flask development server and the app will be accessible at `http://localhost:5000` in your web browser.

Enter an address in the input fields, and click the "Submit" button to view the property details and plot on the map.
