#!/usr/bin/env python3
"""
A basic Flask web application that supports internationalization (i18n)
using Flask-Babel. The app renders a home page and detects the preferred
language of the user (English or French) based on their `Accept-Language`
header.
"""
from flask_babel import Babel
from flask import Flask, render_template, request

# Configuration class to set up Flask-Babel with the supported languages
class Config:
    """
    Configuration for Flask-Babel, which provides i18n and l10n support for Flask.

    This configuration defines the default locale and timezone for the app,
    and specifies the supported languages.
    """
    LANGUAGES = ["en", "fr"]  # List of supported languages (English and French)
    BABEL_DEFAULT_LOCALE = "en"  # Default language is English
    BABEL_DEFAULT_TIMEZONE = "UTC"  # Default timezone is UTC

# Initialize the Flask application object.
app = Flask(__name__)

# Load the configuration from the Config class.
app.config.from_object(Config)

# Disable strict slashes to allow access to URLs with or without a trailing slash.
app.url_map.strict_slashes = False

# Initialize the Babel extension with the app to handle language localization.
babel = Babel(app)

# Define a function to retrieve the best match for the locale based on the user's request.
@babel.localeselector
def get_locale() -> str:
    """
    This function selects the appropriate locale for the user based on their
    `Accept-Language` header. The best matching language is returned.
    
    Flask-Babel uses this function to automatically set the locale for
    rendering the template in the correct language.

    Returns:
        str: The best matching language code from the user's `Accept-Language` header.
    """
    # Retrieve the best match for the language from the 'Accept-Language' header
    return request.accept_languages.best_match(app.config["LANGUAGES"])

# Define the route for the home/index page of the application.
@app.route('/')
def get_index() -> str:
    """
    The home page route, which renders the '2-index.html' template.

    This route serves the index page, which will be localized based on the
    user's preferred language (English or French).

    Returns:
        str: The rendered HTML page from the '2-index.html' template.
    """
    # Render and return the '2-index.html' template.
    return render_template('2-index.html')

# Start the Flask development server only if this script is executed directly.
if __name__ == '__main__':
    """
    Starts the Flask app server. The application listens on all network interfaces 
    (0.0.0.0) and uses port 5000 by default.
    """
    app.run(host='0.0.0.0', port=5000)
