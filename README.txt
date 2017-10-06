REQUIREMENTS
1. Python3
2. SQlalchemy
3. Sqlite
4. Requires google authentication library for python http://google-auth.readthedocs.io/en/latest/index.html#google-auth
5. Open port 5000
6. In the Log In Route replace placeholder with your google Client Id

Example:
# Login In Route
@app.route('/login', methods=['POST'])
def logIn():
# Client ID
CLIENT_ID = "CLIENT ID HERE"

USAGE

1. Change directory into the app folder
2. Run database_setup.py to create and configure database
3. Run populate.py to populate initial data to databse
4. Run app.py
5. Open web browser and navigate to localhost:5000

API

1. URL "localhost:5000/id/JSON" returns single cat with corresponding id
2. URL "localhost:5000/JSON" return all cats
