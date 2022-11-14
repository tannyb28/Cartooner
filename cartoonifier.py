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
top.geometry('400x400')
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

  # images=[img, edges, new_img, final]

  # fig, axes = plt.subplots(2,2, figsize=(15,15), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
  # for i, ax in enumerate(axes.flat):
  #     ax.imshow(images[i], cmap='gray')

  final1 = Image.fromarray(final)
  final1.thumbnail((250,250))
  final1tk = ImageTk.PhotoImage(image=final1)
  imageLabel.configure(image=final1tk)
  imageLabel.image = final1tk
  # plt.show()

upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='black',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)
frame = tk.Frame(top)
frame.pack()
imageLabel = tk.Label(frame, background='white')
imageLabel.pack(side=TOP)

top.mainloop()



# edges = edge_mask(img, line_size, blur_value)



# def cartoonify(ImagePath):
#   # read image
#   originalImage = cv2.imread(ImagePath)
#   originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

#   # confirm image is chosen
#   if originalImage is None:
#     print("Can not find any image. Choose appropriate file")
#     sys.exit()
  
#   ReSized1 = cv2.resize(originalImage, (960, 540))

#   # convert image to grayscale
#   grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
#   ReSized2 = cv2.resize(grayScaleImage, (960, 540))

#   # smooth image with median blur
#   smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
#   ReSized3 = cv2.resize(smoothGrayScale, (960, 540))

#   # retrieve edges of image
#   getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
#     cv2.ADAPTIVE_THRESH_MEAN_C, 
#     cv2.THRESH_BINARY, 9, 9)
  
#   ReSized4 = cv2.resize(getEdge, (960, 540))

#   # bilateral filter to remove noise

  

