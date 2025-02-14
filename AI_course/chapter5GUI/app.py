import streamlit as st
import mysql.connector
import re
import random
import smtplib
from email.mime.text import MIMEText


# Function to authenticate user credentials from the database
def authenticate_user(username, password):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="sql6.freemysqlhosting.net",
            database="sql6695317",
            user="sql6695317",
            password="xWY2aLxsMw"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Query to check if the username and password match
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()  # Fetch the first row

        # If user exists, return True (authentication successful)
        if user:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")
        return False

    finally:
        # Close the cursor and database connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


# Function to send OTP to user's email
def send_otp(email, otp):
    try:
        # Your SMTP server details
        smtp_server = 'smtp.example.com'
        smtp_port = 587
        smtp_username = 'your_username'
        smtp_password = 'your_password'

        # Create a secure connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Construct the message
        msg = MIMEText(f'Your OTP is: {otp}')
        msg['Subject'] = 'Email Verification OTP'
        msg['From'] = smtp_username
        msg['To'] = email

        # Send the message
        server.sendmail(smtp_username, email, msg.as_string())
        server.quit()
        return True

    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False


# Function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))


# Define your login function
def login():
    st.header("Login Page")
    # Add your login code here
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Authenticate user with provided credentials
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.session_state.page = "Dashboard"  # Set the page to Dashboard
        else:
            st.error("Invalid username or password")


# Function to check if a username already exists in the database
def username_exists(username):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="sql6.freemysqlhosting.net",
            database="sql6695317",
            user="sql6695317",
            password="xWY2aLxsMw"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Query to check if the username exists
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()  # Fetch the first row

        # If user exists, return True
        if user:
            return True
        else:
            return False

    except mysql.connector.Error as error:
        st.error(f"Error: {error}")
        return False

    finally:
        # Close the cursor and database connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


# Function to validate email address format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


# Function to validate password strength
def validate_password(password):
    # Password must be at least 8 characters long
    if len(password) < 8:
        return False
    # Password must contain at least one digit
    if not any(char.isdigit() for char in password):
        return False
    # Password must contain at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    # Password must contain at least one lowercase letter
    if not any(char.islower() for char in password):
        return False
    return True


# Define your registration function
def register():
    st.header("Registration Page")
    # Add your registration code here
    new_username = st.text_input("New Username")
    new_email = st.text_input("Email Address")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        # Validate email format
        if not validate_email(new_email):
            st.error("Invalid email address format. Please enter a valid email address.")
        # Validate password strength
        elif not validate_password(new_password):
            st.error(
                "Password must be at least 8 characters long and contain at least one digit, one uppercase letter, and one lowercase letter.")
        # Check if the username already exists
        elif username_exists(new_username):
            st.error("Username already exists. Please choose a different username.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please enter matching passwords.")
        else:
            # Generate OTP
            otp = generate_otp()
            # Send OTP to user's email
            if send_otp(new_email, otp):
                st.success("OTP sent to your email. Please check your inbox.")
                # Proceed with further registration steps
                # (You may want to store the OTP in a database for verification)
            else:
                st.error("Failed to send OTP. Please try again.")


# Function to show dashboard content
def show_dashboard():
    st.header("Dashboard")
    # Add your content here
    st.write("Welcome to the dashboard!")
    # You can add more content or functionality here


# Main Streamlit app
def main():
    ##Give title to the app
    st.title("This is my app")

    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Login", "Register", "Dashboard"], index=0)

    # Show login page if selected in the sidebar or user manually navigates to Login page
    if page == "Login":
        login()
    # Show registration page if selected in the sidebar or user manually navigates to Register page
    elif page == "Register":
        register()
    # Show dashboard if selected in the sidebar and user is logged in or user is redirected after successful login
    elif page == "Dashboard" and (st.session_state.logged_in or st.session_state.page == "Dashboard"):
        show_dashboard()


# Run the main app
if __name__ == "__main__":
    main()
