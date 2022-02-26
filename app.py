from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

#from tempfile import mkdtemp
from helpers import login_required, apology


app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///notes.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return apology("TODO")


@app.route("/login", methods=["GET","POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]["user_id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password != confirmation")

        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)
        r = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(r) == 0:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
        else:
            return apology("username already exists")
        flash("You were Registered !")
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/new", methods=["GET","POST"])
@login_required
def new():
    if request.method == "POST":
        if not request.form.get("label"):
            return apology("Field label can not be empty")

        if not request.form.get("title"):
            return apology("Note must have a title")

        if not request.form.get("description"):
            return apology("note must have a description")

        user_id = session["user_id"]
        title = request.form.get("title")
        description = request.form.get("description")
        label = request.form.get("label")
        db.execute("INSERT INTO notes(user_id, title, description, label) VALUES (?, ?, ?, ?)", user_id, title, description, label)
        row = db.execute("SELECT note_id FROM notes WHERE user_id = ? AND title = ? and label = ? AND description = ?", user_id, title, label, description)
        note_id = row[0]["note_id"]
        db.execute("INSERT INTO timeline(note_id, user_id) VALUES(?, ?)", note_id, user_id)
        return redirect("/")

    else:
        return render_template("new.html")

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    rows = db.execute("SELECT label, title, description, time FROM notes, TIMELINE WHERE notes.note_id = TIMELINE.note_id AND notes.user_id = ?",user_id)
    return render_template("history.html", rows=rows)
