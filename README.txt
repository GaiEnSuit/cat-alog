SETUP
1. Install Python3
2. Install Flask via "pip3 install Flask"
3. Install SQLalchemy via "pip install SQLAlchemy"
4. Install google-auth library via "pip3 install --upgrade google-auth"
5. Open port 80 on your server
6. Create an Oauth2.0 in your google cloud platform
7. Add "http://localhost:5000" to the Authorized JavaScript Origins list
8. In the file "app.py" under the "log in route" section set CLIENT_ID to your client id from your google console

Example:
@app.route('/login', methods=['POST'])
def logIn():
    if request.method == 'POST':
        # Please Set Your Client ID here
        CLIENT_ID = CLIENT_ID = "###########################"

APP USAGE

1. Change directory into the app folder
2. Run database_setup.py to create and configure database
3. Run populate.py to populate initial data to database
4. Run pip3 app.py
5. Open web browser and navigate to localhost:80

API

1. URL "localhost:5000/id/JSON" returns single cat with corresponding id
2. URL "localhost:5000/JSON" return all cats
