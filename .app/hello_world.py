# create our first "hello world" web page using python, flask and Pycharm

# Import required modules



from flask import Flask, request, render_template, make_response, url_for, redirect

# Declare and instantiate a flask object
app = Flask(__name__)

# Set the route to the index/home page
# route using decorators
@app.route('/')
@app.route('/index')
def hello_world():
    return (f'<h1>Hello, World from Karanja using Flask!</h1>'
            f"<p>Your browser is <b>{request.headers.get('User-Agent')}</b></p>"
            )

# set the route to the user page
@app.route("/user/<name>")
def user(name):
    return (f"<h1>Hello, {name} from Flask routes!</h1>")

# Set the route to the response page
@app.route("/response")
def response():
    #variable to hold a response
    response = make_response(f"<h1>This document carries a cookie.</h1>")
    response.set_cookie('answer','42')
    return response

# Page/route to display the cookie's value
@app.route('/show_cookie')
def show_cookie():
    answer = request.cookies.get('answer')
    return f"<h1>Cookie value is: {answer}</h1>"

# Page/route to redirec to the EICN website
@app.route('/redirect-edulink')
def redirect_edulink():
    return redirect("https://edulink.ac.ke")


# set the entry point to our Python web app
if __name__ == '__main__':
    app.run(debug=True)
