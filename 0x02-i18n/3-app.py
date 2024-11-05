#!/usr/bin/env python3
"""
A basic Flask web application that supports internationalization (i18n) and localization (l10n) using Flask-Babel.

This app serves a home page that can be rendered in multiple languages (English and French) based on the user's browser preferences.
Flask-Babel is used to handle the localization of content such as titles and headers for each supported language.
"""
from flask_babel import Babel
from flask import Flask, render_template, request

# Configuration class for setting up Flask-Babel with supported languages and timezone.
class Config:
    """
    Configuration for Flask-Babel, which is used to provide internationalization (i18n) and localization (l10n) support in this Flask app.

    This configuration defines:
    - A list of supported languages (`LANGUAGES`).
    - The default language (`BABEL_DEFAULT_LOCALE`), which is English in this case.
    - The default timezone (`BABEL_DEFAULT_TIMEZONE`), set to UTC.
    """
    LANGUAGES = ["en", "fr"]  # Supported languages: English ('en') and French ('fr')
    BABEL_DEFAULT_LOCALE = "en"  # Default locale (language) is English
    BABEL_DEFAULT_TIMEZONE = "UTC"  # Default timezone is UTC

# Initialize the Flask application object.
app = Flask(__name__)

# Load the configuration settings from the Config class into the app.
app.config.from_object(Config)

# Disable strict slashes so that URLs with or without trailing slashes are treated equally.
app.url_map.strict_slashes = False

# Initialize the Babel extension for localization support in the app.
babel = Babel(app)

# Define a function to select the user's preferred language based on their 'Accept-Language' header.
@babel.localeselector
def get_locale() -> str:
    """
    Selects the best matching language for the user based on the 'Accept-Language' HTTP header.

    This function is called by Flask-Babel to determine which language to render the page in.
    It checks the user's browser preferences and selects the best match from the available supported languages.
    
    Returns:
        str: The best matching language code (either 'en' for English or 'fr' for French).
    """
    # Flask-Babel uses this method to automatically select the best language match
    return request.accept_languages.best_match(app.config["LANGUAGES"])

# Define the home route for the index page.
@app.route('/')
def get_index() -> str:
    """
    The home page route, which renders the '3-index.html' template.

    This function handles the request to the home page and renders a template that will display content
    in the user's preferred language (either English or French).

    Returns:
        str: The rendered HTML template ('3-index.html'), which is localized based on the user's language.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    """
    Runs the Flask web application on all network interfaces (0.0.0.0) and listens on port 5000.
    
    This allows the application to be accessible on any device within the network. The app will
    serve the web pages and automatically render the content in the preferred language of the user.
    """
    app.run(host='0.0.0.0', port=5000)
