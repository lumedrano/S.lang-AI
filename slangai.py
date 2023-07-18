import streamlit as st
import os
from PIL import Image
from main import gesture_to_text

# Function to display the first photo of each letter
def display_photos(sentence):
    global photo_references, image_idx  # Use global variables for PhotoImage references and current image index
    image_idx = 0  # Initialize the current image index to 0

    def show_next_image():
        global image_idx
        if image_idx < len(photo_references):
            st.image(photo_references[image_idx], use_column_width=True)  # Show the current image
            image_idx += 1
            if image_idx < len(photo_references):
                st.write("Next image will appear in 0.5 seconds...")
                st.session_state.next_image_timer = st.session_state.next_image_timer - 1
                st.experimental_rerun()
            else:
                st.session_state.next_image_timer = 0

    # Create a list to store the image paths of each letter
    image_paths = []
    # Iterate through each letter in the sentence
    for letter in sentence:
        # Load the corresponding image from the folder A-Z
        folder_path = f"./data_mp/{letter.upper()}"  # Replace with your actual folder path
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):  # Replace ".jpg" with the appropriate image extension
                image_path = os.path.join(folder_path, filename)
                image_paths.append(image_path)
                break  # Stop after finding the first image

    # Load all images into Image references
    photo_references = []
    for image_path in image_paths:
        image = Image.open(image_path)
        photo_references.append(image)  # Store the reference

    # Start showing images
    if "next_image_timer" not in st.session_state:
        st.session_state.next_image_timer = 0
    if st.session_state.next_image_timer == 0:
        st.session_state.next_image_timer = len(photo_references)
        show_next_image()

# Streamlit app
st.title("S.lang AI Translator")

# User selection for translation mode

# User selection for translation mode
translation_mode = st.radio("Select Translation Mode:", ("Gesture to Text", "Text to Gesture"))
select_button = st.button("Select")  # Button to trigger the selected translation mode

if select_button:
    if translation_mode == "Gesture to Text":
        st.write("Use hand gestures to translate to text.")
        # Streamlit UI to capture hand gestures using OpenCV
        st.info("Make hand gestures in front of your webcam.")
        opencv_result = gesture_to_text()  # Use the OpenCV function
        st.write("Gesture Translation:", opencv_result)

    elif translation_mode == "Text to Gesture":
        st.write("Type your sentence to translate to gestures.")
        # Streamlit UI to get user input and display images using the image classification script
        sentence = st.text_input("Enter your sentence:")
        if st.button("Translate"):
            display_photos(sentence)
