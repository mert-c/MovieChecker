import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from random import randrange

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    
    imgurl = indexmovie()[randrange(0,10)]    
    if not imgurl:
        imgurl = "/static/resized.png"
    return render_template("apology.html", top=code, bottom=escape(message), imgurl=imgurl), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(name):
    """Look up quote for symbol."""
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={name}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = quote['results']
        return quote
    except (KeyError, TypeError, ValueError):
        return None


def indexmovie():
    random = randrange(500,100000)
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/popular/?api_key={api_key}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = quote['results']
        return quote
    except (KeyError, TypeError, ValueError):
        return None

def poster(id):
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        quote = quote['poster_path']
        return "https://image.tmdb.org/t/p/w200" + quote
    except (KeyError, TypeError, ValueError):
        return None


def getdetails(id):
    """Look up quote for symbol."""
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        query = response.json()
        return query
    except (KeyError, TypeError, ValueError):
        return None