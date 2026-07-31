"""
Python script to act as the launch point to our Flask web application
Author: Karanja
Date: June - July 2026
"""


# -----------------------------------------------------------------------------------------------------------------
# Import the required modules
# -----------------------------------------------------------------------------------------------------------------
import secrets, string
from flask import Flask, request, render_template, make_response, url_for, redirect, jsonify, session, flash
from datetime import datetime, timezone
from flask_login import current_user, LoginManager
from flask_login import login_user, logout_user, login_required #For application authentication & authorisation
from typing import Optional

# Import modules for localisation
from flask_babel import Babel, format_datetime

# -----------------------------------------------------------------------------------------------------------------
# Import our custom modules
# -----------------------------------------------------------------------------------------------------------------
from sign_up import RegistrationForm
from login import LoginForm
from user_form import UserForm
from product_form import ProductForm

# -----------------------------------------------------------------------------------------------------------------
# Import our database modules
# -----------------------------------------------------------------------------------------------------------------
from models import Product, User, db, init_db, UserRole, Role
from seed_products_user_roles import seed_all
from wtforms.validators import Optional

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

# Configuration 3. Specify the path to our database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ds2509.db'
# improve app's performance by not tracking all db modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialise the database
init_db(app)
seed_all(app)

# Instantiate a Babel object and pass our app
babel = Babel(app)

# Set the FLask_login for the applications login functionality
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create a guest user to access our site's unrptected areas anonymously
class GuestUser:
    """
    Represents an anonymous (unauthenticated) user.

    This class provides the minimal interface expected by authentication
    systems such as Flask-Login for users who have not signed in.
    """
    def __init__(self):
        """Initialize a guest user"""
        self.full_name = 'Guest'
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True

    def is_admin_or_manager(self) -> bool:
        """
        Return whether the guest has administrative privileges.

        Returns:
            False, since guest users cannot have elevated permissions.
        """
        return False
    def get_id(self):
        """
        Return the unique identifier for the user.

        Returns:
            None, since guest users do not have a persistent identifier.
        """
        return None

# Function to get the user object for the current user, if the current user is authenticated,
# else it returns a Guest object
@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        return {'current_user': current_user}
    else:
        return {'current_user': GuestUser()}

# Function to generate the prefix for the product ids when adding new products in the products table
def generate_product_id():
    prefix = "01H73QEWM"
    alphabet = string.ascii_uppercase + string.digits
    while True:
        suffix = ''.join(secrets.choice(alphabet) for i in range(8))
        candidate = prefix + suffix
        if Product.query.get(candidate) is None: # When product id doesn't exist in the product table
            return candidate

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

# Route to the register/sign-up page
@app.route('/sign-up', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data(e.g. save to our database)
        try:
            # Check whether the user's email already exists in the database
            if User.query.filter_by(email=form.email.data).first():
                flash(f'The email {form.email.data} is already registered.'
                      f'\nPlease choose a different email.', 'danger')
                return render_template('sign_up.html', form=form)
            if User.query.filter_by(phone=form.phone.data).first():
                flash(f'The phone number {form.phone.data} is already registered.'
                      f'\nPlease choose a different phone number.',"danger")
                return render_template('sign_up.html', form=form)

            # Create the new user in the database user table
            new_user = User(
                email = form.email.data,
                full_name = form.names.data,
                birth_date = form.birthdate.data,
                gender = form.gender.data.lower(),
                phone = form.phone.data,
                is_active = True
            )
            #Set the user's password
            new_user.set_password(form.password.data)

            # Add the new user's data to the database
            db.session.add(new_user)
            db.session.flush() # to get the user an ID

            # Assign the new user the defaut role of customer
            customer_role = Role.query.filter_by(name='Customer').first()
            if customer_role:
                user_role = UserRole(
                    user_id = new_user.id,
                    role_id = customer_role.id,
                    assigned_by = None,
                    is_active = True
                )
                db.session.add(user_role)
            db.session.commit()
            flash(f"Registration successful. You can now log in.")
        except Exception as e:
            db.session.rollback()
            flash(f"Sorry, there was an error during registration:\n{str(e)}", "danger")
            return render_template('sign_up.html', form=form)
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")
    return render_template('sign_up.html', form=form)

# Route to the login page
@app.route('/login', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
@app.route('/sign-in', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process the form data (e.g redirect to inbox, proceed to check out, view post/profile etc.)

        # Get the next page from the query parameter or session
        next_page = request.args.get('next') or session.pop('next', None)

        if form.validate_on_submit():
            # Find user by email address
            user = User.query.filter_by(email=form.email.data).first()

            if user and user.check_password(form.password.data):
                # Login the user
                login_user(user, remember=True)
                user.last_login = datetime.now()
                db.session.commit()

                flash(f"Welcome back, {user.full_name}!", "success")

                # Redirect user to the intended pafe/index
                if next_page and next_page != url_for('login'):
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))
            else:
                flash("Invalid username or password.", "danger")
        else:
            # Flash validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")

        # Store the next page in session for after successful login
        if request.args.get('next'):
            session['next'] = request.args.get('next')

    return render_template('login.html', form=form)

# Route to logout/sign out user
@app.route('/logout')
@app.route('/sign-out')
@login_required # requires the user to be logged in
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Route to add a new user(accessed by admins only)
@app.route('/add-user', methods=['GET', 'POST'])
@login_required # requires the user to be logged in
def add_user():
    #check if the current user is an admin
    if not current_user.is_admin_or_manager() or not any(ur.role.name=='Admin'
                                                         for ur in current_user.user_role if ur.is_active):
        flash(f"Access Denied, insufficient privileges.", 'danger')
        return redirect(url_for('index'))
    form = UserForm()
    if form.validate_on_submit():
        try:
            # Check whether the user's email already exists in the database
            if User.query.filter_by(email=form.email.data).first():
                flash(f'The email {form.email.data} is already registered.'
                      f'\nPlease choose a different email.', 'error')
                return render_template('signup.html', form=form)
            if User.query.filter_by(phone=form.phone.data).first():
                flash(f'The phone number {form.phone.data} is already registered.'
                      f'\nPlease choose a different phone number.',"error")
                return render_template('sign_up.html', form=form)

            # Create the new user in the database user table
            new_user = User(
                email = form.email.data,
                full_name = form.full_name.data,
                birth_data = form.birth_date.data,
                gender = form.gender.data.lower(),
                phone = form.phone.data,
                is_active = True
            )
            #Set the user's password
            new_user.set_password(form.password.data)

            # Add the new user's data to the database
            db.session.add(new_user)
            db.session.flush() # to get the user an ID

            # Assign the new user's role
            role = Role.query.filter_by(name=form.role.data).first()
            if role:
                user_role = UserRole(
                    user_id = new_user.id,
                    role_id = role.id,
                    assigned_by = current_user.id, # user id of currently logged in administrator
                    is_active = True
                )
                db.session.add(user_role)

            db.session.commit()
            flash(f"User {new_user.full_name} successfully created.", 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating user:\n{str(e)}", "danger")
            return render_template('add-user.html', form=form)

        return render_template('add-user.html', form=form)

#Route to the products page
@app.route('/products')
def products():
    # Get all the products from the product table in the ds2509 database
    products = Product.query.all()
    return render_template('products.html', products=products)

#Route to the add products page
@app.route('/add_products')
def add_products():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            id = form.name.data.replace(' ','').upper(),
            name = form.name.data,
            price = form.price.data,
        )
        # Add and persist the new product to the database
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('add-product.html', form=form)

#Route to the add products page
@app.route('/edit_product/<string:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if product is None:
        return redirect(url_for('products'))
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        # Persist the new product details to the database
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('edit_product.html', form=form)

#Route to the delete products page
@app.route('/delete_product/<string:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product is None:
        return redirect(url_for('products'))
    else:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('products'))

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