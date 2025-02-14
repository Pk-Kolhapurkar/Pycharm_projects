import streamlit as st
import mysql.connector
import re
import os
from PIL import Image
import tensorflow
import numpy as np
import pickle

from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm



# Function to insert user into the MySQL database
def insert_user_into_mysql(username, email, password):
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

        # Query to insert user into the database
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        data = (username, email, password)
        cursor.execute(query, data)

        # Commit changes and close cursor
        connection.commit()
        cursor.close()

        return True

    except mysql.connector.Error as error:
        st.error(f"Error inserting user into MySQL database: {error}")
        return False

    finally:
        # Close the database connection
        if 'connection' in locals() and connection.is_connected():
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

# Function to check if a username already exists in the MySQL database
def username_exists_in_mysql(username):
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

# Define your registration function
def register():
    st.title("Registration Page")
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
            st.error("Password must be at least 8 characters long and contain at least one digit, one uppercase letter, and one lowercase letter.")
        # Check if the username already exists in MySQL database
        elif username_exists_in_mysql(new_username):
            st.error("Username already exists. Please choose a different username.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please enter matching passwords.")
        else:
            # Insert user into MySQL database with original password
            if insert_user_into_mysql(new_username, new_email, new_password):
                st.success("Registration successful!")
            else:
                st.error("Failed to register user. Please try again.")

# Define your login function
def login():
    st.title("Login Page")
    # Add your login code here
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Authenticate user with provided credentials
        if authenticate_user(username, password):
            st.success("Login successful!")
            # Direct user to the website page
            st.markdown("[Go to website page](https://www.example.com)")
        else:
            st.error("Invalid username or password")

# Main Streamlit app
def main():

    ##Give title to the app
    st.title("This is my app")

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Login", "Register"])

    # Show registration page if selected in the sidebar
    if page == "Register":
        register()

    # Show login page if selected in the sidebar
    elif page == "Login":
        login()

def website_page():
    st.title("Fashion Recommender System")
    st.markdown("Welcome to the Fashion Recommender System!")

    model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    model.trainable = False
    model = tf.keras.Sequential([
        model,
        GlobalMaxPooling2D()
    ])

    def feature_extraction(img_path, model):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        expanded_img_array = np.expand_dims(img_array, axis=0)
        preprocessed_img = preprocess_input(expanded_img_array)
        result = model.predict(preprocessed_img).flatten()
        normalized_result = result / norm(result)
        return normalized_result

    def recommend(features, feature_list):
        neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
        neighbors.fit(feature_list)
        distances, indices = neighbors.kneighbors([features])
        return indices

    uploaded_file = st.file_uploader("Choose an image")
    if uploaded_file is not None:
        img_path = "uploaded_image.jpg"
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        display_image = image.load_img(img_path, target_size=(300, 300))
        st.image(display_image, caption="Uploaded Image", use_column_width=True)

        features = feature_extraction(img_path, model)
        indices = recommend(features, feature_list)

        col1, col2, col3, col4, col5 = st.beta_columns(5)
        with col1:
            st.image(filenames[indices[0][0]])
        with col2:
            st.image(filenames[indices[0][1]])
        with col3:
            st.image(filenames[indices[0][2]])
        with col4:
            st.image(filenames[indices[0][3]])
        with col5:
            st.image(filenames[indices[0][4]])

# Load necessary data for fashion recommender system
feature_list = np.array(pickle.load(open('embeddings.pkl', 'rb')))
filenames = pickle.load(open('filenames.pkl', 'rb'))

# Routing
page = st.sidebar.radio("Navigation", ["Website Page", "Login", "Register"])
if page == "Website Page":
    website_page()
elif page == "Login":
    login()
elif page == "Register":
    register()

# Redirect to main application page if logged in
if st.session_state.get("logged_in"):
    website_page()

# Run the main app
if __name__ == "__main__":
    main()
