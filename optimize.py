'''
This is a test class currently implementing the optimization policy.
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

#Read the background and a hidden object image
img = cv2.imread('C:/Users/boswo/Desktop/Hidden Object Game/back.png')
img2 = cv2.imread('C:/Users/boswo/Desktop/Hidden Object Game/croc.png')
#Convert the images into an openCV compatable image
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert it to RGB channel
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) #convert it to RGB channel
#Load the shape of the images to be used later in cropping
h, w, c = img2.shape
h2, w2, c2, = img.shape

#Initialize a third image which is a cropped version of the first image, mainly initing another picture
img3 = img[:h, :w]

#Store the difference between the sliced image and the hideden object in a variable
minDiff = sum(abs(np.average(img3, axis = (0,1)) - np.average(img2, axis = (0,1))))

#Store variables to be used later in the loop
x = 0
y = 0
i = 0
j = 0

#Lopp through every slice of the image
while i < (w2 - w):
    j = 0
    while j < (h2 - h):
        #Take a slice of the image corresponding the height and width of the hidden object
        img3 = img[j:j+h, i:i+w]
        #plt.imshow(img3)
        #plt.show()
        #Determine if the new slice has a smaller difference in pixel average with the hidden object
        if (sum(abs(np.average(img3, axis = (0,1)) - np.average(img2, axis = (0,1)))) < minDiff):
            #Store the new minimum difference value
            minDiff = sum(abs(np.average(img3, axis = (0,1)) - np.average(img2, axis = (0,1))))
            #Used for debugging
            print("True")
            #Store the new ideal location of the hidden x and y coordinates
            x = i
            y = j
        #Increment the height being read
        j += h
    #Increment the width being read
    i += w
    #Used for debugging
    print(i)


#Pring the resulting image
print(x)
print(y)
print(minDiff)
#Display the selected slice of the background
img3 = img[y:y+h, x:x+w]
plt.imshow(img)
plt.show()
