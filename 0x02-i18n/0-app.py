#!/usr/bin/env python3
"""
A basic Flask web application that serves an index page.
This app uses Flask to render an HTML template for the home page.
"""


from flask import Flask, render_template # type: ignore


app = Flask(__name__)

app.url_map.strict_slashes = False


@app.route('/')
def get_index() -> str:
    """
    Handles the request to the home page.

    This route renders the '0-index.html' template which contains the
    HTML structure for the home page, including a title and header.

    Returns:
        str: The rendered HTML page from the template.
    """
    

    return render_template('0-index.html')



if __name__ == '__main__':
    """
    The app runs on host '0.0.0.0' to make it accessible from any network interface.
    It listens on port 5000 by default.
    """
    app.run(host='0.0.0.0', port=5000)