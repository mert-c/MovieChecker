import os
from urllib.parse import quote
import requests
import helpers as helpers

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask import flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, getdetails, indexmovie, login_required, lookup, indexmovie

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///moviecheck.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show random movies"""
    flash("Welcome! Take a look at the most popular movies today!")
    movies = indexmovie()
    return render_template("index.html", movies=movies)


@ app.route("/history")
@ login_required
def history():
    flash("You can view your history here.")
    """Show history of searches"""
    hist = db.execute(
        "SELECT * FROM actions WHERE user_id = ? ORDER BY history DESC;", session["user_id"])
    return render_template("history.html", hist=hist)


@ app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You Should Provide a Username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You Should Provide a Password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid Username and/or Password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        flash("Hi, please log in or register.")
        return render_template("login.html")


@ app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logged out! :(")
    return redirect("/")


@ app.route("/search", methods=["GET", "POST"])
@ login_required
def search():
    if request.method == "POST":
        query = request.form.get("mname")
        res = lookup(query)
        db.execute("INSERT INTO actions(user_id, action, query) VALUES(?, ?, ?);",
                   session["user_id"], "Search", query)
        if len(res) <= 0:
            flash("We couldn't find any movies with that name!")
            return render_template("search.html")
        flash("Here are the results:")
        return render_template("searched.html", res=res)
    else:
        flash("Go on, search a movie!")   
        return render_template("search.html")

@ app.route("/me", methods=["GET","POST"])
def me():  
    return render_template("me.html")

@ app.route("/fav", methods=["GET","POST"])
@ login_required
def fav():  
    if request.method == "POST":
        # add selected row movie to favorites
        movie_id = request.args.get('movie_id') 
        user_id = session["user_id"]
        query = getdetails(movie_id)
        print(query)
        print(query["original_title"])
        check = db.execute("SELECT movie_id FROM favorites WHERE user_id = ? AND movie_id = ?", user_id, movie_id)
        if check:
            return apology("You already favorited this movie!")
        else:
            db.execute("INSERT INTO favorites (user_id, movie_id, title, poster, rating) VALUES(?, ?, ?, ?, ?);", session["user_id"], query["id"], query["original_title"], query["poster_path"], query["vote_average"])
            db.execute("INSERT INTO actions(user_id, action, query) VALUES(?, ?, ?);", session["user_id"], "Favorite", query["original_title"])
            favs = db.execute("SELECT * FROM favorites WHERE user_id = ? ORDER BY rating DESC", session["user_id"]) 
            flash("Added to favorites!")
            return render_template("favorites.html", favs=favs)
    elif request.method == "GET":
        favs = db.execute("SELECT * FROM favorites WHERE user_id = ?", session["user_id"])
        flash("Here are your favorite movies!")
        return render_template("favorites.html", favs=favs)
    


@ app.route("/remove", methods=["GET","POST"])
@ login_required
def removefav():
    if request.method == "POST":
        # add selected row movie to favorites
        id = request.args.get("id")
        user_id = session["user_id"]
        query = getdetails(id)
        db.execute("DELETE FROM favorites WHERE user_id = ? AND movie_id = ?;", user_id, id)
        db.execute("INSERT INTO actions(user_id, action, query) VALUES(?, ?, ?);",
            session["user_id"], "Remove Favorite", query["original_title"])
        favs = db.execute("SELECT * FROM favorites WHERE user_id = ? ORDER BY rating DESC", session["user_id"])
        flash("Favorite removed :(")
        return render_template("favorites.html", favs=favs)


@ app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        user_id = request.form.get("username")
        upass = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted
        if not user_id:
            return apology("must provide username", 400)

        # Ensure username does not exist
        check = db.execute("SELECT * FROM users WHERE username = ?", user_id)
        if user_id and check:
            return apology("Username already taken, please choose a different username", 400)

        # Ensure password was submitted
        elif not upass or upass != confirmation:
            return apology("Passwords don't match!", 400)

        else:
            hasher = generate_password_hash(
                upass, method='pbkdf2:sha256', salt_length=8)
            db.execute(
                "INSERT INTO users (username, hash) VALUES(?,?)", user_id, hasher)
            flash("Registered!")
            return redirect("/login")
    else:
        flash("Please register to continue!")
        return render_template("register.html")


@ app.route("/reset", methods=["GET", "POST"])
@ login_required
def reset():
    if request.method == "POST":
        if not (password := request.form.get("password")):
            return apology("MISSING OLD PASSWORD")

        new_pass = request.form.get("new_password")
        new_pass = generate_password_hash(new_pass)
        rows = db.execute("SELECT * FROM users WHERE id = ?;",
                          session["user_id"])
        old_pass = rows[0]["hash"]

        if new_pass == old_pass:
            flash("Password reset failed!")
            return redirect("/reset")

        if not check_password_hash(old_pass, request.form.get("password")):
            return apology("INVALID PASSWORD")

        if not (new_password := request.form.get("new_password")):
            return apology("MISSING NEW PASSWORD")

        if not (confirmation := request.form.get("confirmation")):
            return apology("MISSING CONFIRMATION")

        if new_password != confirmation:
            return apology("PASSWORD NOT MATCH")

        db.execute("UPDATE users set hash = ? WHERE id = ?;",
                   new_pass, session["user_id"])
        flash("Password reset successful!")

        return redirect("/")
    else:
        flash("You can reset your password here")
        return render_template("passres.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
