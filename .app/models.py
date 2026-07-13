# Python file to model the database tables


# Import the required modules
import bcrypt
from datetime import datetime, timezone
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Create a database object/instance
db = SQLAlchemy()

#Define the User Model/Class
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('male', 'female', name='gender_enum'), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc),
                           onupdate=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    multi_factor_enabled = db.Column(db.Boolean, default=True)
    password_updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Method to return a string representation of the object
    def __repr__(self):
        return f"Name: {self.full_name}, Email: {self.email}"

    # Method to hash and set the user's encrypted password
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.password_updated_at = datetime.now(timezone.utc)

    # Method to authenticate user
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    #Method to check whether the user's email already exists in the database
    @staticmethod
    def check_email_exists(email):
        return User.query.filter_by(email=email).first() is not None

    # Method to create the user's account in the database
    def create_user(self, email, full_name, birth_date, gender, password):
        if User.check_email_exists(email):
            raise ValueError('Email already registered')

        user = User(email = email, full_name = full_name, birth_date = birth_date, gender = gender, phone= phone)
        user.set_password(password)

        # Add the default user role of customer
        customer_role = Role.query.filter_by(name='Customer').first()
        if customer_role:
            user_role = UserRole(user = user, role = customer_role, assigned_by=None, is_active=True)
            db.session.add(user)
            db.session.commit()
            return user

        # Method to check where the user is an admin or manager
        def is_admin_or_manager(user):
            """Check if user is an administrator or manager"""
            if not self.is_authenticated:
                return False
            return any(ur.role.name == 'Admin' for ur in self.role if ur.is_active)

# Define the Role class/model
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_system_admin = db.Column(db.Boolean, default=False)

    # Method to return a string representation of the object
    def __repr__(self):
        return f"Role: {self.name}, Description: {self.description}"

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Link/Create relationships to the users and roles tables
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('user_role', lazy='true', cascade='all, delete-orphan'))
    role = db.relationship('Role', foreign_keys=[role_id], backref= db.backref('user_role', lazy='true', cascade='all, delete-orphan'))

    # Method to return a string rep of the user-role object
    def __repr__(self):
        return f"UserRole: {self.user.email}, Role: {self.role.name}"

# Define the product model
class Product(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    # need to keep tabs of inventory too

    #Method to return a string representation of the product
    def __repr__(self):
        return f"Product ID: {self.id}, Name: {self.name}, Price: {self.price}"

# TODO: Function to create the above tables in the db and populate with data
