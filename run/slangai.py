import os
import streamlit as st
from PIL import Image
from main import gesture_to_text

# Function to display the first photo of each letter
def display_photos(sentence):
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

    # Display images on the Streamlit UI
    for image_path in image_paths:
        image = Image.open(image_path)
        st.image(image, caption=f"Letter: {sentence[image_paths.index(image_path)]}", use_column_width=True)

# Streamlit app
st.title("S.lang AI Translator")

# User selection for translation mode
translation_mode = st.radio("Select Translation Mode:", ("Gesture to Text", "Text to Gesture"))
select_button = st.button("Select")  # Button to trigger the selected translation mode

if select_button:
    if translation_mode == "Gesture to Text":
        st.write("Use hand gestures to translate to text.")
        # Streamlit UI to capture hand gestures using OpenCV
        st.info("Make hand gestures in front of your webcam.")
        opencv_result = gesture_to_text()  # Use the OpenCV function

        # Display the sentence created by the user on the Streamlit UI
        st.write("Gesture Translation:", opencv_result)

    elif translation_mode == "Text to Gesture":
        st.write("Type your sentence to translate to gestures.")
        # Streamlit UI to get user input and display images using the image classification script
        sentence = st.text_input("Enter your sentence:")
        if st.button("Translate"):
            display_photos(sentence)
