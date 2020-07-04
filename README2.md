# Flask-JWT
Implementing JSON Web Tokens in Flask. JSON web tokens are a secure way to access resources.

The main file is run.py
use set/export to set FLASK_APP=run.py FLASK_DEBUG=1 flask run.
use of curl -d "username=<username>&password=<password>" -H 'Accept:application/json' <url here>
token will be received as response.
curl - "Authorization: token goes here " -H 'Accept:application/json' <url here to secured resource>
