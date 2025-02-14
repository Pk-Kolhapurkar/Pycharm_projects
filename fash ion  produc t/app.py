import streamlit as st
import mysql.connector

# Establishing connection to MySQL database
db = mysql.connector.connect(
    host="sql6.freemysqlhosting.net",
    user="sql6695317",
    password="xWY2aLxsMw",
    database="sql6695317",
    port=3306
)
cursor = db.cursor()

# Streamlit page configuration
st.title("User Registration and Login")

# Function to check password criteria
def check_password(password):
    # Define criteria here (e.g., minimum length, uppercase, lowercase, etc.)
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    elif not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    elif not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    elif not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    else:
        return True, ""

# Registration and Login page
st.subheader("Registration and Login")

# Registration section
with st.form("registration_form"):
    st.write("## Register")
    new_username = st.text_input("New Username", key="new_username")
    new_email = st.text_input("Email Address", key="new_email")
    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    registration_button = st.form_submit_button("Register")
    if registration_button:
        if new_password == confirm_password:
            is_valid, message = check_password(new_password)
            if is_valid:
                try:
                    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (new_username, new_email, new_password))
                    db.commit()
                    st.success("Registration successful!")
                except mysql.connector.IntegrityError:
                    st.error("Username already exists. Please choose another.")
            else:
                st.error(message)
        else:
            st.error("Passwords do not match.")

# Login section
with st.form("login_form"):
    st.write("## Login")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    login_button = st.form_submit_button("Login")
    if login_button:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")
