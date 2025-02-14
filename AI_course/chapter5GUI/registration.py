import streamlit as st
import re  # Add this line to import the 're' module
from database import connect_to_database

def register():
    st.title("Registration")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Password criteria regex pattern
    password_criteria = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

    if st.button("Register"):
        # Validate input
        if not username.strip() or not email.strip() or not password.strip():
            st.error("Please enter username, email, and password.")
        elif not password_criteria.match(password):
            st.error("Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long.")
        else:
            # Connect to database
            db = connect_to_database()
            cursor = db.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if result:
                st.error("Username already exists. Please choose a different one.")
            else:
                # Insert new user into database
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                db.commit()
                st.success("Registration successful. You can now log in.")

def main():
    register()

if __name__ == "__main__":
    main()
