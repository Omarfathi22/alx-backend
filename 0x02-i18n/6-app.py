#!/usr/bin/env python3
"""A simple Flask app with internationalization support.
"""
from flask_babel import Babel
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Configuration for Flask Babel.
    """
    LANGUAGES = ["en", "fr"]  # Supported languages
    BABEL_DEFAULT_LOCALE = "en"  # Default language
    BABEL_DEFAULT_TIMEZONE = "UTC"  # Default timezone


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Example users with different locales and timezones
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Fetches a user based on the 'login_as' query parameter.
    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Sets up the user context before each request.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Determines the locale for the current request.
    """
    locale = request.args.get('locale', '')  # Check for 'locale' in query string
    if locale in app.config["LANGUAGES"]:
        return locale
    
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:  # Check user-specific locale
        return g.user['locale']
    
    header_locale = request.headers.get('locale', '')  # Check for 'locale' in headers
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    
    return request.accept_languages.best_match(app.config["LANGUAGES"])  # Fallback to best match


@app.route('/')
def get_index() -> str:
    """Render the homepage.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
