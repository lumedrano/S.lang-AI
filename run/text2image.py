import os
from PIL import Image, ImageTk
import tkinter as tk


# Function to display the first photo of each letter
def display_photos(sentence):
    #remove spaces from user sentence input
    sentence = sentence.replace(" ", "")

    global photo_references, image_idx  # Use global variables for PhotoImage references and current image index
    image_idx = 0  # Initialize the current image index to 0

    def show_next_image():
        global image_idx
        if image_idx < len(photo_references):
            canvas.delete("all")  # Clear previous image
            canvas.create_image(0, 0, anchor=tk.NW, image=photo_references[image_idx])  # Show the current image
            image_idx += 1
            root.after(500, show_next_image)  # Schedule the next image transition after 500ms

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

    # Load all images into PhotoImage references
    photo_references = []
    for image_path in image_paths:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        photo_references.append(photo)  # Store the reference

    # Start showing images
    show_next_image()

# Create GUI
root = tk.Tk()
root.title("S.lang AI Translator")

# Input box
input_label = tk.Label(root, text="Enter your sentence:")
input_label.pack()
input_box = tk.Entry(root)
input_box.pack()

# Frame to hold canvas
frame = tk.Frame(root)
frame.pack()

# Canvas to display images
canvas = tk.Canvas(frame, width=800, height=600)
canvas.pack()

# Button to trigger translation
translate_button = tk.Button(root, text="Translate", command=lambda: display_photos(input_box.get()))
translate_button.pack()

# List to store PhotoImage references
photo_references = []
image_idx = 0  # Variable to keep track of the current image index

root.mainloop()
