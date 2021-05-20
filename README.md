# nview-dev
gui for Nimble

# nview mongengine to work with StackStorm mongo DB !!!THIS APP IS INSTALLED ON A ST2 SERVER!!!

log in with admin first
-------------------------------------------------------------------------------------
mongo -u admin -p UkIbDILcNbMhkh3KtN6xfr9h admin  (passwd in /etc/st2/st2.config)

# Then create a new user
db.createUser({user: "appUser",pwd: "passwordForAppUser",roles: [ { role: "readWrite", db: "app_db" } ]})

# Add creds to the Flask application.py file
```
app.config['MONGODB_SETTINGS'] = {
        'db': 'app_db',
        'host': 'localhost',
        'port': 27017,
        'username': 'appUser',
        'password': 'passwordForAppUser',
        'authentication_source': 'admin'
        }
```

Now Flask app can access the st2 mongo database installation
