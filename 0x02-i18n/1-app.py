#!/usr/bin/env python3
"""
A basic Flask web application that supports internationalization (i18n)
using Flask-Babel. This app allows rendering of a home page with localization
support for multiple languages (English and French).
"""
from flask_babel import Babel
from flask import Flask, render_template

# Configuration class to set up Flask-Babel with the supported languages


class Config:
    """
    Configuration for Flask-Babel, which provides
    i18n and l10n support for Flask.
    This configuration defines the default locale
    and timezone for the app,
    and specifies the supported languages.
    """
    
    
    LANGUAGES = ["en", "fr"]  # List of supported languages (English and French)
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)

app.config.from_object(Config)


app.url_map.strict_slashes = False


babel = Babel(app)


@app.route('/')
def get_index() -> str:
    """
    The home page route, which renders the '1-index.html' template.

    This route serves the index page and uses Flask-Babel to handle language
    localization based on the user's preferred language (English or French).

    Returns:
        str: The rendered HTML page from the '1-index.html' template.
    """

    return render_template('1-index.html')


if __name__ == '__main__':
    """
    Starts the Flask app server. The application
    listens on all network interfaces
    (0.0.0.0) and uses port 5000 by default.
    """
    app.run(host='0.0.0.0', port=5000)
