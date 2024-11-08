#!/usr/bin/env python3
"""A simple Flask app with internationalization support.
"""
from flask_babel import Babel, _
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """Configuration for Flask Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Sample users with different locales and timezones
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Fetches a user based on the 'login_as' query parameter."""
    login_id = request.args.get('login_as')
    if login_id and login_id.isdigit():
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Runs before each request to set up the user context."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Determines the locale for the current request."""
    # Check if the locale is explicitly set in the request arguments
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    # Check if the logged-in user has a preferred locale
    if g.user and g.user.get("locale") in app.config["LANGUAGES"]:
        return g.user["locale"]
    # Fall back to the best match based on request headers
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """The homepage of the app."""
    return render_template('5-index.html', user=g.user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
