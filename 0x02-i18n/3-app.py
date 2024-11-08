#!/usr/bin/env python3
"""
A basic Flask web application that supports internationalization (i18n) and
localization (l10n) using Flask-Babel.

This app serves a home page that can be rendered in multiple languages (English
and French) based on the user's browser preferences. Flask-Babel handles
localization of content like titles and headers for each supported language.
"""

from flask_babel import Babel
from flask import Flask, render_template, request


# Configuration class for setting up Flask-Babel with supported languages.
class Config:
    """
    Configuration for Flask-Babel, used to provide internationalization (i18n)
    and localization (l10n) support in this Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Initialize the Flask application object.
app = Flask(__name__)

# Load configuration settings from Config class.
app.config.from_object(Config)

# Disable strict slashes for URL handling.
app.url_map.strict_slashes = False

# Initialize Babel extension for localization.
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Selects the best matching language for the user based on the
    'Accept-Language' HTTP header.

    Returns:
        str: The best matching language code (either 'en' or 'fr').
    """
    
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def get_index() -> str:
    """
    Home page route that renders the '3-index.html' template.

    Returns:
        str: The rendered HTML template, localized to the user's language.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    """
    Runs the Flask web application on all network interfaces (0.0.0.0) and
    listens on port 5000.
    """
    app.run(host='0.0.0.0', port=5000)
