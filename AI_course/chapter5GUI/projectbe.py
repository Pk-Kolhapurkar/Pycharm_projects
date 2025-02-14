import streamlit as st
import mysql.connector
import re

# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="sql6.freemysqlhosting.net",
        user="sql6695317",
        password="xWY2aLxsMw",
        database="sql6695317",
        port="3306"
    )

# Registration Page
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

# Login Page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Connect to database
        db = connect_to_database()
        cursor = db.cursor()

        # Validate credentials
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            st.success("Login successful.")
        else:
            st.error("Invalid username or password.")

# Main function to run the app
def main():
    # import library
    import streamlit as st

    ##Give title to the app
    st.title("This is my app")

    # running the app by streamlit run main_app.py

    # Header
    st.header("This is header")
    st.subheader("Tis is a subheader")

    # plain text
    st.text("This is a text")

    # markdown
    st.markdown("this is some text")

    # button
    st.button("this is a button")

    # checkbox
    st.checkbox("this is a checkbox")

    # radio button
    st.radio('radio', ['Option1', 'option2', 'option3'])

    # selectbox
    st.selectbox('select', ['try1', 'try2', 'try3'])

    # multiselect
    st.multiselect('multiselect', ['try1', 'try2', 'try3'])

    # color picker
    st.color_picker("colr picker")

    # date input
    st.date_input("Data Input")

    # time input
    st.time_input("Time input")

    # text input
    st.text_input("Text input", placeholder="Enter your prompt")  # Corrected here

    # number input
    st.number_input('Number input', min_value=1, max_value=50)

    # text area
    st.text_area("text area", placeholder="Enter your text here")

    # sliders
    st.slider("text area", )

    '''
    #progress bar
    import time
    my_progressbar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_progressbar.progress(percent_complete+1)

    #spinner
    with st.spinner("Waiting..."):
        time.sleep(5)
    '''

    # coloumns
    col1, col2 = st.columns(2)
    with col1:
        st.header("This is coloumn 1")
        st.text("Write text here")

    with col2:
        st.header("This is coloumn 2")
        st.text("Write text here")

    # Add image from file uploader & display
    # we use PIL python imaging library
    image = st.file_uploader("upload the file", type=["png", "jpg"])
    if image:
        st.image(image, caption="upload image")

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Login", "Register"])
    if page == "Login":
        login()
    elif page == "Register":
        register()

if __name__ == "__main__":
    main()
