# create our first "hello world" web page using python, flask and Pycharm

# Import required modules


from flask import Flask, request, render_template

# Declare and instantiate a flask object
app = Flask(__name__)

# Set the route to the index/home page
@app.route('/')
@app.route('/index')

def hello_world():
    return (f'<h1>Hello, World from Flask!</h1>')

# set the entry point to our Python web app
if __name__ == '__main__':
    app.run(debug=True)
