import cv2 #for image processing
import easygui
from matplotlib import image #to open the filebox
import numpy as np #to store image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image

top=tk.Tk()
top.geometry('600x600')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
  ImagePath=easygui.fileopenbox()
  cartoonify(ImagePath)

def color_quantize(img, k):
  # transform image
  data = np.float32(img).reshape((-1,3))

  # determine criteria
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

  # k-means clustering
  ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
  center = np.uint8(center)
  result = center[label.flatten()]
  result = result.reshape(img.shape)
  return result

def edge_mask(img, line_size, blur_value):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray_blur = cv2.medianBlur(gray, blur_value)
  edges = cv2.adaptiveThreshold(gray_blur, 235, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
  return edges

def cartoonify(ImagePath):
  img = cv2.imread(ImagePath)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

  if img is None:
    print("Can not find any image. Choose appropriate file")
    sys.exit()

  line_size = 9
  blur_value = 5
  edges = edge_mask(img, line_size, blur_value)

  total_color = 9
  new_img = color_quantize(img, total_color)

  blurred = cv2.bilateralFilter(new_img, d=7, sigmaColor=200, sigmaSpace=200)

  final = cv2.bitwise_and(blurred, blurred, mask=edges)

  final1 = Image.fromarray(final)
  final1.thumbnail((400,400))
  final1tk = ImageTk.PhotoImage(image=final1)
  imageLabel.configure(image=final1tk)
  imageLabel.image = final1tk

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='black',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)
frame = tk.Frame(top)
frame.pack()
imageLabel = tk.Label(frame, background='white')
imageLabel.pack(side=TOP)

top.mainloop()

