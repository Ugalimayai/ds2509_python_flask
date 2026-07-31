# Python script to create or seed products, users and their roles in the system
# NB: Ensure the python timezone model is installed (pip)

#import the required modules

import bcrypt
import pytz #(Python TimeZone)
from datetime import datetime
from models import db, User, UserRole, Product, Role


#Function to create/seed the application's initial roles in the database
def seed_initial_roles(now = None) -> None:

    roles = [
        {"name": "Admin", "description": "System administrator with full access.", "is_system_admin": True},
        {"name": "Manager", "description": "Store or branch manager with elevated access.", "is_system_admin": False},
        {"name": "staff", "description": "Regular staff member", "is_system_admin": False},
        {"name": "Customer", "description": "Regular customer", "is_system_admin": False}
    ]

    for role_data in roles:
        role = Role.query.filter_by(name=role_data["name"]).first()
        if role:
            continue
        role = Role(
            name = role_data["name"],
            description = role_data["description"],
            is_system_admin = role_data["is_system_admin"]
        )

        if now is None:
            role.created_at = now
            role.updated_at = now

        db.session.add(role)

    db.session.commit()

# Function to create/set the products in the database
# the -> syntax explains the return type
def seed_products() -> None: #function does not return anything

    if Product.query.count() != 0:
        return
    # Variable to hold the records to be inserted to the product table
        # Variable to hold the records to be inserted/added to the product table
        sample_records = [
            ('01H73QEWMF1KG6QADD', 'Ground beef parties - 25% Fat', 980.0),
            ('01H73QEWMFMWNQPSM', 'Coffee - Hazelnut Cream', 815.0),
            ('01H73QEWMGFSMTWR3X', 'Coffee - Flavoured', 905.0),
            ('01H73QEWMGHCW3PXFR', 'Tequila Rose Cream Liquor', 675.0),
            ('01H73QEWMG9MD4CTB9', 'Split Peas - Yellow, Dry', 820.0),
            ('01H73QEWMGTRXVQYY', 'Wine - Vineland Estate Semi - Dry', 855.0),
            ('01H73QEWMH3GCAA4P', 'Mushroom - Chanterelle, Dry', 585.0),
            ('01H73QEWMHM6WXBGM', 'Butter - KCC Salted', 760.0),
            ('01H73QEWMHPX9KZ2YV', 'Olives - Black, Pitted', 450.0),
            ('01H73QEWMHQ7T5R6WX', 'Pasta - Fettuccine, Egg', 320.0),
            ('01H73QEWMHR4F8S9D2', 'Cheese - Cheddar, Medium', 690.0),
            ('01H73QEWMHS1G3H5J7', 'Chicken - Whole Roasting', 1250.0),
            ('01H73QEWMHT9K8L2P4', 'Tomatoes - Cherry, Yellow', 380.0),
            ('01H73QEWMHV7M6N1Q3', 'Bread - Italian Roll With Herbs', 420.0),
            ('01H73QEWMHW5T9R7Y2', 'Salmon - Fillets', 1980.0),
            ('01H73QEWMHX3V8B6N5', 'Chocolate - Dark, 70% Cocoa', 550.0)
        ]

        # Insert above records in the products table using a for loop
        for record in sample_records:
            product = Product(id=record[0], name=record[1], price=record[2])
            db.session.add(product)

            # Commit the changes to the database after inserting the sample data
            db.session.commit()


# Function to create/seed the app's initial user's in the database
def seed_initial_users(now=None) -> None:

    # EAT = pytz.timezone("Africa/Nairobi")
    # now - datetime.now(EAT)

    DEFAULT_PASSWORD = 'ChangeM3@123'

    # -------------------------------------------------------------------------
    # Seed data grouped by user's role in the app.
    # -------------------------------------------------------------------------

    seed_data = {
        "Admin":[
            {"email": "admin1@ds2509.ac.ke",
             "full_name": "Abigail Maina",
             "birth_date": datetime(1985, 3, 25).date(),
             "gender": "female",
             "phone": "0712345678"},
            {"email": "admin2@ds2509.ac.ke",
             "full_name": "James Kimani",
             "birth_date": datetime(1990, 11, 22).date(),
             "gender": "male",
             "phone": "0723345678"},
        ],
        "Manager": [
            {"email": "manager.msa@ds2509.ac.ke",
             "full_name": "Felicia Mwendwa",
             "birth_date": datetime(1988, 7, 10).date(),
             "gender": "female",
             "phone": "0734577901"},
            {"email": "manager.nbo@ds2509.ac.ke",
             "full_name": "Flora Mutahi",
             "birth_date": datetime(1990, 11, 22).date(),
             "gender": "female",
             "phone": "0745788911"}
        ],
        "Staff": [
            {"email": "staff1@ds2509.ac.ke",
             "full_name": "Mary Wanjiku",
             "birth_date": datetime(1995, 9, 18).date(),
             "gender": "female",
             "phone": "0756789210"},
            {"email": "staff2@ds2509.ac.ke",
             "full_name": "John Kiprono",
             "birth_date": datetime(1997, 1, 30).date(),
             "gender": "male",
             "phone": "0778910243"},
            {"email": "staff3@ds2509.ac.ke",
             "full_name": "Zainab Hassan",
             "birth_date": datetime(1996, 6, 12).date(),
             "gender": "female",
             "phone": "0778342901"},
            {"email": "staff4@ds2509.ac.ke",
             "full_name": "David Omondi",
             "birth_date": datetime(1994, 12, 3).date(),
             "gender": "male",
             "phone": "0789102455"},
        ],
        "Customer": [
            {"email": "customer.emily@ymail.com",
             "full_name": "Emily Ndinda",
             "birth_date": datetime(2000, 8, 25).date(),
             "gender": "female",
             "phone": "0790233455"},
            {"email": "customer.rahim@gmail.com",
             "full_name": "Rahim Juma",
             "birth_date": datetime(1998, 2, 14).date(),
             "gender": "male",
             "phone": "0711244577"},
            {"email": "customer.karanja@gmail.com",
             "full_name": "Karanja Nyadhi",
             "birth_date": datetime(2002, 8, 31).date(),
             "gender": "male",
             "phone": "011253988"},
            {"email": "n.arthur@edulink.ac.ke",
             "full_name": "Arthur Nyanjui",
             "birth_date": datetime(2007, 5, 8).date(),
             "gender": "male",
             "phone": "012567980"},
        ],
    }

    print("Seeding data...Please wait...")
    for role_name, users in seed_data.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print(f"⚠️ Role {role_name} does not exist.")
            continue

        for data in users:
            user = User.query.filter_by(email=data['email']).first()

            # -------------------------------------------------------------------------
            # Create the user if the user does not exist
            # -------------------------------------------------------------------------
            if not user:
                user = User(
                    email = data["email"],
                    full_name = data["full_name"],
                    birth_date = data["birth_date"],
                    gender = data["gender"],
                    phone = data["phone"],
                    is_active = True,
                    created_at = now,
                    updated_at =now,
                    last_login = now,
                    multi_factor_enabled = False
                )
                user.password_hash = bcrypt.hashpw(
                    DEFAULT_PASSWORD.encode('utf-8'),
                    bcrypt.gensalt()
                ).decode('utf-8')
                user.password_updated_at = now

                # Add to the database (user table) and commit
                db.session.add(user)
                db.session.flush() # Get the user's id
                print(f"☑️ Created user: {user.full_name}")

            else: #user creation fails
                print(f"🔁 User: {user.full_name} already exists.")
                #pass #to reduce no. of logs when a user already exists

            # -------------------------------------------------------------------------
            # Assign the user a role if missing
            # -------------------------------------------------------------------------
            role_exists = UserRole.query.filter_by(
                user_id = user.id,
                role_id = role.id,
                is_active = True
            ).first()

            if not role_exists:
                db.session.add(
                    UserRole(
                        user_id = user.id,
                        role_id = role.id,
                        assigned_at = now,
                        assigned_by = None,
                        is_active = True,
                    )
                )
                print(f"➕ Assigned role: {role_name}")
            else: #Role already assigned
                #print(f"🔁 Role already assigned: {role_name}")
                pass
        db.session.commit()
        print("🐝 User seeding complete!!!")

# Function to add data to all the tables
def seed_all(app):
    with app.app_context():
        EAT = pytz.timezone('Africa/Nairobi')
        now = datetime.now(EAT)

        # Call the above funcs
        seed_initial_roles(now=now)
        seed_products()
        seed_initial_users(now=now)
