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
def search():
    if request.method == "POST":
        user_id = session["user_id"]
        query = request.form.get("query")
        query = f"%{query}%"
        result = db.execute("SELECT label, title, description FROM notes WHERE user_id = ? AND description LIKE ?", user_id, query)
        return render_template("search_result.html", result=result)

    else:
        return render_template("search.html")


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
        db.execute("INSERT INTO timeline(note_id, user_id, modification) VALUES(?, ?, ?)", note_id, user_id, "added")
        return redirect("/")

    else:
        return render_template("new.html")

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    rows = db.execute("SELECT label, title, time, modification FROM notes, timeline WHERE notes.note_id = TIMELINE.note_id AND notes.user_id = ?",user_id)
    return render_template("history.html", rows=rows)

@app.route("/all")
@login_required
def index():
    user_id = session["user_id"]
    rows = db.execute("SELECT label, title, description FROM notes WHERE user_id = ?", user_id)
    return render_template("all.html", rows=rows)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    user_id = session["user_id"]
    title = request.form.get("title")
    db.execute("DELETE FROM notes WHERE user_id = ? AND title = ?", user_id, title)
    return redirect("/all")

@app.route("/edit", methods=["GET","POST"])
@login_required
def edit():
    user_id = session["user_id"]
    if request.method == "POST":
        if not request.form.get("old-title"):
            return apology("Can only edit a pre-exisiting note")

        if not request.form.get("new-label"):
            return apology("Field label can not be empty")

        if not request.form.get("new-title"):
            return apology("Note must have a title")

        if not request.form.get("new-description"):
            return apology("note must have a description")

        old_title = request.form.get("old-title")
        new_title = request.form.get("new-title")
        new_description = request.form.get("new-description")
        new_label = request.form.get("new-label")

        row = db.execute("SELECT note_id FROM notes WHERE user_id = ? AND title = ?", user_id, old_title)
        note_id = row[0]["note_id"]
        db.execute("UPDATE notes SET title = ?, label = ?, description = ? WHERE note_id = ? AND user_id = ?", new_title, new_label, new_description, note_id, user_id)
        db.execute("INSERT INTO timeline(note_id, user_id, modification) VALUES (?, ?, ?)", note_id, user_id, "edited")
        return redirect("/")

    else:
        titles = db.execute("SELECT title FROM notes WHERE user_id = ?", user_id)
        return render_template("edit.html", titles=titles)

@app.route("/password", methods=["GET","POST"])
@login_required
def change():
    if request.method == "POST":
        user_id = session["user_id"]
        if not request.form.get("old-password"):
            return apology("must provide existing password")

        old_password = request.form.get("old-password")
        row = db.execute("SELECT hash FROM users WHERE user_id = ?", user_id)
        hash = row[0]["hash"]

        if not check_password_hash(hash, old_password):
            return apology("wrong existing password")

        if not request.form.get("new-password"):
            return apology("must provide a new password")
        new_password = request.form.get("new-password")

        if not request.form.get("new-password-confirmation") or new_password != request.form.get("new-password-confirmation"):
            return apology("new password confirmation does not match new password")

        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE user_id = ?", new_hash, user_id)
        return redirect("/")

    else:
        return render_template("change_password.html")
