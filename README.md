# Notes Web App
#### Video Demo:  <https://youtu.be/DrGtt3T42YE>
#### Description:
    
Notes is a flask based web application that allows users to make notes. Users need to register to have an account. Upon creating an account and logging in, each user can securly create, edit and store their own notes. All so created notes are private to just the user.

Additionally users can also search for notes (which is very helpful when one has a large number of notes), view history of their previous changes to various notes and change password.

Technologies used: HTML5, CSS, Boostrap, Python3, Flask, SQLite3


### Instaling and Running:
    
This project requires dependencies mentioned in requirements.txt file.
Ensure your system has flask, flask-session, cs50 python library, sqlite3 database and requests python module installed.
Upon installing all the dependencies. Using command `flask run` in VSCode will auto-forward a port and provide a link through which one can access the application.

### Directory Structure

    flask_session/
    app.py
    helpers.py
    notes.db
    requirements.txt
    static/
    templates/

- flask_session/ - This directory stores all session information locally

- app.py - Flask based python backend for the web app. It provides and handles all the backend function of the web application. From registering, authenticating user, to accessing the notes database, creating, reading, updating and modifying entires as necessary.

- helpers.py - Python file containing additional functions that are imported and used in the main file.

- notes.db - SQLite3 based database used to store all the data

- requirements.txt - Text file that lists all the prerequistes for running the web app

- static/ - Contains static component for the web app (i.e.. css/js files)

- templates/ - Contains all html file for the web applications
   - all.html : shows list of all the notes stored in the database
   - apology.html : returns an error message to user
   - change_password.html : landing page for user for changing password
   - edit.html : html page that allows user to modify existing notes
   - history.html : history of all changes made to notes
   - layout.html : basic html file that is used to render all other html files
   - login.html : login page
   - new.html : landing page for the user when creating a new note
   - register.html : registration page
   - search.html : landing page for the user to search through all the notes
   - search_result.html : renders results of the users search through all the notes
