#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
import pytz
from typing import Union, Dict
from flask_babel import Babel, format_datetime
from flask import Flask, render_template, request, g


class Config:
    """Configuration settings for Flask Babel.
    """
    LANGUAGES = ["en", "fr"]  # Supported languages for the app
    BABEL_DEFAULT_LOCALE = "en"  # Default locale (language)
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
    If no user is found, returns None.
    """
    login_id = request.args.get('login_as', '')  # Get the user ID from query parameters
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Executes before each request to set up the user context.
    Stores the user information globally (in `g.user`).
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Determines the locale (language) for the current request.
    Checks the following sources in order: query string, user settings, headers.
    """
    queries = request.query_string.decode('utf-8').split('&')  # Parse the query string
    query_table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))  # Convert query string into a dictionary
    locale = query_table.get('locale', '')  # Get 'locale' query parameter
    if locale in app.config["LANGUAGES"]:
        return locale  # If locale is valid, use it
    
    # Check the user's preferred locale if available
    user_details = getattr(g, 'user', None)
    if user_details and user_details['locale'] in app.config["LANGUAGES"]:
        return user_details['locale']
    
    # Check the 'locale' header for the language preference
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale

    # Fallback to the default locale if no match is found
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone() -> str:
    """Determines the timezone for the current request.
    Checks the following sources in order: query string, user settings.
    """
    timezone = request.args.get('timezone', '').strip()  # Get the 'timezone' from query parameters
    if not timezone and g.user:
        timezone = g.user['timezone']  # Use the user's timezone if no query parameter is found
    try:
        return pytz.timezone(timezone).zone  # Try to return a valid timezone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']  # Fallback to default timezone if invalid timezone


@app.route('/')
def get_index() -> str:
    """Renders the home page with current time in the selected timezone.
    """
    g.time = format_datetime()  # Format current time based on the selected timezone
    return render_template('index.html')  # Render the homepage template


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on all available IPs at port 5000
