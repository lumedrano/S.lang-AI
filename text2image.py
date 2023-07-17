import os
from PIL import Image, ImageTk
import tkinter as tk


##TODO: get the images to show up consecutively with scroll bar and make the textbox stay if I want to edit and retranslate something else.

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

    # Display the photos in the GUI
    x = 0
    photo_references = []  # List to store PhotoImage references
    for image_path in image_paths:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        photo_references.append(photo)  # Store the reference
        label = tk.Label(root, image=photo)
        label.photo = photo  # Keep a reference to the PhotoImage to prevent garbage collection
        label.place(x=x, y=0)
        x += photo.width()

# Create GUI
root = tk.Tk()
root.title("Sign Language Translator")

# Input box
input_label = tk.Label(root, text="Enter your sentence:")
input_label.pack()
input_box = tk.Entry(root)
input_box.pack()

# Button to trigger translation
translate_button = tk.Button(root, text="Translate", command=lambda: display_photos(input_box.get()))
translate_button.pack()

# Canvas (Not used in this version, you can remove this line if desired)
canvas = tk.Canvas(root, width=800, height=300)
canvas.pack()

root.mainloop()
