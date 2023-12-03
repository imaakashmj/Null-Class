import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np


def detect_wrinkles(file_path):
    try:
        image = cv2.imread(file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=10)

        for x, y, w, h in faces:
            cropped_img = gray_image[y:y+h, x:x+w]
            edges = cv2.Canny(cropped_img, 30, 150)  # Adjust the threshold values here
            number_of_edges = np.count_nonzero(edges)

        if number_of_edges > 4500:
            print("Wrinkles Found")
            label1.configure(foreground="#011638", text="Wrinkles Detected")
        else:
            print("No Wrinkles Found")
            label1.configure(foreground="#011638", text="No Wrinkles Detected")

        # Display the processed image
        processed_image = Image.fromarray(edges)
        processed_image.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(processed_image)
        sign_image.configure(image=im)
        sign_image.image = im

    except Exception as e:
        print("Error:", str(e))
        label1.configure(foreground="#011638", text="Error: Unable to process image")


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        show_detect_button(file_path)
    except Exception as e:
        print("Error:", str(e))


def show_detect_button(file_path):
    detect_b = Button(top, text="Detect Wrinkles", command=lambda: detect_wrinkles(file_path), padx=10, pady=5)
    detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    detect_b.place(relx=0.79, rely=0.46)


top = tk.Tk()
top.geometry('800x600')
top.title('Wrinkle Detector')
top.configure(background='#CDCDCD')

label1 = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

upload = Button(top, text="Upload Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 20, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand='True')
label1.pack(side='bottom', expand='True')
heading = Label(top, text='Wrinkle Detector', pady=20, font=('arial', 25, 'bold'))
heading.configure(background='#CDCDCD', foreground="#364156")
heading.pack()

# Load the face cascade classifier
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

top.mainloop()
