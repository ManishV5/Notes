# Notes Web App
#### Video Demo:  <URL HERE>
#### Description:
    Notes is a flask based web application that allows users to register to have an account. Upon creating an account and logging in, each user can securly create, edit and store their own notes. All so created notes are private to just the user.

    Additionally users can also search for notes (which is very helpful when a user has a large number of notes), view history of their previous modifications of notes and change password.

    Technologies used: HTML5, CSS, Boostrap, Python3, Flask, SQLite3


### Instaling and Running:
    This project requires dependencies mentioned in requirements.txt file.
    Ensure your system has flask, flask-session, cs50 python library, sqlite3 database and requests python module installed.
    Upon installing the all dependencies. Using command flask-run in VSCode will auto-forward a port and provide a link through which one can access the application.

### Directory Structure
    flask_session/
    app.py
    helpers.py
    notes.db
    requirements.db
    static/
    templates/

    flask_session