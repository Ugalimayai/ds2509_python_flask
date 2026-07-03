"""
Python script to act as the launch point to our Flask web application
Author: Karanja
Date: June - July 2026
"""


# -----------------------------------------------------------------------------------------------------------------
# Import the required modules
# -----------------------------------------------------------------------------------------------------------------
import secrets, string
from flask import Flask, request, render_template, make_response, url_for, redirect, jsonify, session
from datetime import datetime

# Import modules for localisation
from flask_babel import Babel, format_datetime

# -----------------------------------------------------------------------------------------------------------------
# Declare and create/instantiate the Flask object
# -----------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

# Set our application configurations
# Configuration 1. Add the configurations for supported languages
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es', 'fr', 'de', 'sw']

# Configuration 2. Create the application's secret key to protect our site from CSRF attacks
app.config['SECRET_KEY'] = secrets.token_urlsafe(32) # you can also use app_key=secrets.token_hex(18)
# Instantiate a Babel object and pass our app
babel = Babel(app)

# Set the route to the index/home page

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    # get the user's browser and store it in the var
    browser = request.headers.get('User-Agent')

    # Determine the browser based on the browser string
    if 'Firefox' in browser:
        user_agent = 'Firefox'
    elif 'Chrome' in browser:
        user_agent = "Chrome"
    elif 'Opera' in browser:
        user_agent = 'Opera'
    elif 'Safari' in browser:
        user_agent = 'Safari'
    elif 'Edge' in browser:
        user_agent = 'Edge'
    elif 'IE' in browser:
        user_agent = 'Internet Explorer'
    else:
        user_agent = 'Unknown'

    
    # Display the home page and pass the user-agent var to it
    return render_template('index.html', user_agent=user_agent)

# Detect the best matching language from the user's request
def get_locale():
    return request.args.get('lang', 'en') # default to English when no language is selected

babel.init_app(app, locale_selector=get_locale)

#Route to the time page
@app.route('/time')
def show_time():
    current_time = datetime.now()
    formatted_time = format_datetime(current_time, format='full') #format the time to a human readable style
    return render_template('localised-time.html', current_time=formatted_time)


# Route to the modified user page

@app.route('/user')
@app.route('/user/<username>')
def mod_user(username:str=None):
    return render_template('mod_user.html', username=username)


# #Code to simulate an internal server error by raising an exception
# @app.route('/trigger-500')
# def trigger_500():
#    # Deliberately raise an error in our server
#    raise Exception("Deliberate internal exception")



# Pages to handle site errors
# 1. Handle when authentication is required and has not been provided or failed(401 error)
@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

# 2. Handle when user is authenticated but does not have permission to access a resource (403 error)
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

# 3. Handle when page is not found(404 error)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 4. Handle internal server error(500 error)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 5. Handle when the website is overloaded or temporarily down for upgrades/maintenance(503 error)
@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html'), 503


# set entry point
if __name__ == '__main__':
    app.run(debug=True)