Using Twilio and GooglePlaces reads a text in the following format:

"current location;type of place to find"

Takes in your current location and a type of place you want to find (e.g. restaurants, gas station, etc.)

Responds with the nearest location and the directions.

Useful for people without smart phones and when without a data connections, uses normal SMS.

Uses virtualenv and Flask to push to heroku.

Dependencies (check requirements.txt):

pip install Flask gunicorn

pip install googlemaps

pip install requests

pip install twilio

Made in collaboration with Chris Bernt
