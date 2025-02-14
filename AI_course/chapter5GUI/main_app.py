import streamlit as st

def main_app():
    st.title("Main Application")
    # Main application page code here
    # import library


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


def main():
    main_app()

if __name__ == "__main__":
    main()
