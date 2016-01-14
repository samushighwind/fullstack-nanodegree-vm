INSTRUCTIONS FOR RUNNING SERVER
===============================
0) Install dependencies, probably using `pip`. (You may need administrative privileges.)
```
pip install Flask
pip install SQLAlchemy
pip install Flask-SQLAlchemy
pip install WTForms
pip install Flask-WTF
```

1) To create and prepopulate the database, navigate to project root and run:
```
python database_setup.py
```
The database, `puppies.db`, is initialized in the `puppyapp` package directory.

2) To run the server, run:
```
python puppyserver.py
```

3) To reset the database, stop the server with Ctrl+C and repeat steps 1 and 2.
