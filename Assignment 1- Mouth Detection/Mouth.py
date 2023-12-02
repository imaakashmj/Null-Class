import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk


def MouthDetection(file_path):
    global label1

    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    try:
        if len(faces) == 0:
            label1.configure(foreground="#011638", text="No face detected")
        else:
            # Iterate over the detected faces
            for (x, y, w, h) in faces:
                # Exclude the eye and nose regions from the face ROI
                roi_y = int(y + h/3)
                roi_h = int(h/1.5)
                roi_x = int(x + w/8)
                roi_w = int(w - w/4)
                face_roi = gray_image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

                # Detect mouths within the face ROI
                mouths = mouth_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(mouths) == 0:
                    label1.configure(foreground="#011638", text="Mouth Closed")
                else:
                    label1.configure(foreground="#011638", text="Mouth Opened")

    except:
        label1.configure(foreground="#011638", text="Unable to detect")


def show_Detect_button(file_path):
    detect_b = Button(top, text="Detect Mouth", command=lambda: MouthDetection(file_path), padx=10, pady=5)
    detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    detect_b.place(relx=0.79, rely=0.46)


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        show_Detect_button(file_path)
    except:
        pass


top = tk.Tk()
top.geometry('800x600')
top.title('Mouth Detector')
top.configure(background='#CDCDCD')

label1 = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mouth.xml')

upload = Button(top, text="Upload Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 20, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand='True')
label1.pack(side='bottom', expand='True')
heading = Label(top, text='Mouth Detector', pady=20, font=('arial', 25, 'bold'))
heading.configure(background='#CDCDCD', foreground="#364156")
heading.pack()

top.mainloop()
