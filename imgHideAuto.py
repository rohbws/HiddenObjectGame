'''
IN DEVELOPMENT
This class uses optimization to hide the hidden objects, the game generates itself
'''
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from random import *
from time import time
import numpy as np
import cv2

#Class that runs the entire game
class App(object):
    '''
    This function finds the ideal location to place the hidden object
    Developed on 6/15/21
    '''
    def optimize(self):
        #Read the backgrounf image and a spider hidden object with opencv
        img = cv2.imread('C:/Users/boswo/Desktop/Hidden Object Game/back.png')
        img2 = cv2.imread('C:/Users/boswo/Desktop/Hidden Object Game/spider.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert it to RGB channel
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB) #convert it to RGB channel
        #Store the shape of the images, height and width
        h, w, c = img2.shape
        h2, w2, c2, = img.shape

        #Initialize a new slice of the background image
        img3 = img[:h, :w]

        #Store the difference in pixel average between the hidden object and the upper-left slice
        minDiff = sum(abs(np.average(img3, axis = (0,1)) - np.average(img2, axis = (0,1))))

        #Variables to be used in the loop while iterating
        x = 0
        y = 0
        i = 0
        j = 0

        #Loop through the width of the image
        while i < (w2 - w):
            j = 0
            #Iterate through the height of the image
            while j < (h2 - h):
                #Take a slice of the background image, identical in shape to the hidden object
                img3 = img[j:j+h, i:i+w]
                #plt.imshow(img3)
                #plt.show()
                #Compare the current difference between the current piece and hidden object with the previos minimum value
                if (sum(abs(np.average(img3, axis = (0,1)) - np.average(img2, axis = (0,1)))) < minDiff):
                    #Set the new minimum difference
                    minDiff = sum(abs(np.average(img3, axis = (0,1)) - np.average(img2, axis = (0,1))))
                    #Store the current x and y location
                    x = i
                    y = j
                #Increment the width
                j += h
            #Used for debugging
            print(i)
            #Increment the width
            i += w
        #Return the optimized x and y positions
        return x, y

    #Function to run when start game button is pressed
    def endWait(self):
        #For tesing
        print(str(self.startGame))
        #Trigger the start of the game
        self.startGame = False

    '''
    Constructor for the App class
    Initializes needed variables, a frame, and a start button
    '''
    def __init__(self):
        #Initialize a canvas
        self.root =  Tk()
        self.canvas = Canvas(self.root, height=1000, width=1870, bg='green')
        self.canvas.grid()
        #To be used later to store the objects placed on the canvas
        self.images=[]
        self.posList=[]
        self.textList=[]
        #Booleans to be used later to process which stage of the game is active
        self.win = False
        self.gameOver = False
        self.startGame = True
        #Initialize a button to trigger start of game
        self.canvas.bind("<Button 1>",self.printcoords)
        self.startB = Button(self.canvas, text ="Start Game")
        self.startB['command'] = self.endWait

        #Place the button on the Canvas
        self.startB.place(x=935, y=500)

        #Move to next phase of the game
        self.addPics()

    #function to be called when mouse is clicked
    def printcoords(self, event):
        print(str(event.x) + " " + str(event.y))
        #Pass info about mouse click to the remove function
        self.rem(event.x, event.y)

    '''
    Initializes the game when the start button is pressed
    Created on 6/11/21
    '''
    def addPics(self):
        #Pause until game starts
        while (self.startGame == True):
            self.root.update_idletasks()
            self.root.update()
        #Remove the start button
        self.startB.destroy()
        #Initialize images to be used later
        self.backgnd = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/back.png" )
        self.croc = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/spider.png")
        #Make the crocodile smaller
        self.backgnd = self.backgnd.subsample(3)
        #Store some info on the background image
        self.backgnd_width = (self.backgnd.width()/2)
        self.backgnd_height = (self.backgnd.height()/2)
        #Initialize the background image
        self.canvas.create_image(self.backgnd_width,self.backgnd_height,image=self.backgnd)
        self.bamboo = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/bamboo.png")
        #Reduce the size of the bamboo image
        self.bamboo = self.bamboo.subsample(3)
        #Add the bamboo image to the canvas
        self.canvas.create_image(1400, 80, image=self.bamboo)
        #Initialize a time variable to use later
        self.time = 30
        #Determine the optimal location to hide the image
        x, y = self.optimize()
        #Given that the background image is scaled down by a factor of 3, we must scale the results of the optimization as well
        x = int(x/3)
        y = int(y/3)

        #A random factor to increase the size of the hidden object, making the game easier
        factor = 4
        factor = int(15 / factor)

        #Reduce the size of the hidden object, but increase it by the random factor
        self.croc = self.croc.subsample(factor)

        #Used for debugging
        print(x)
        print(y)
        #Taken from imgHide.py, store the location to hide the object in a 2D array
        allPos = [[x, y]]
        self.numCrocs = 0
        #Iterate through the allPos array
        for idx in range(len(allPos)):
            #Add hidden objects at the calculated locations
            self.images.append(self.canvas.create_image(allPos[idx][0],allPos[idx][1], image=self.croc))
            self.posList.append([allPos[idx][0],allPos[idx][1]])
            #State that a hidden object has been added 
            self.textList.append("Crocidile")
            self.numCrocs += 1
        
        #List that there is one spider to be found on the canvas
        self.crocs = self.canvas.create_text(1400,210,fill="black",font="Docktrin 20 bold", text=(str(self.numCrocs)+" Spiders"))

        #Start the hidden object game
        self.runGame()
    '''
    Function to remove an image if the registered click is near to a hidden object
    Created on 6/12/21
    '''
    def rem(self, x, y):
        #Check that the game has not ended
        if not self.gameOver:
            #To be used later
            i = 0
            #Iterate through the images list
            for img in self.images:
                #Determine if a hidden object has been clicked
                if (abs(x - self.posList[i][0]) < 30 and abs(y - self.posList[i][1]) < 30):
                    #Remove the clicked hidden object
                    self.canvas.delete(self.images[i])
                    self.images.pop(i)
                    #Determine which hidden object has been clicked
                    if self.textList[i] == "Cobra":
                        #Decrement the number of crobras to be clicked
                        self.numCobras -= 1
                        #Reset the cobra listing
                        self.canvas.delete(self.cobras)
                        self.cobras = self.canvas.create_text(1400,180,fill="black",font="Docktrin 20 bold", text=(str(self.numCobras)+" Cobras"))
                    elif self.textList[i] == "Crocidile":
                        self.numCrocs -= 1
                        self.canvas.delete(self.crocs)
                        self.crocs = self.canvas.create_text(1400,210,fill="black",font="Docktrin 20 bold", text=(str(self.numCrocs)+" Crocodiles"))
                    elif self.textList[i] == "Spider":
                        self.numSpids -= 1
                        self.canvas.delete(self.spids)
                        self.spids = self.canvas.create_text(1400,240,fill="black",font="Docktrin 20 bold", text=(str(self.numSpids)+" Spiders"))
                    elif self.textList[i] == "Scorp":
                        self.numScorps -= 1
                        self.canvas.delete(self.scorps)
                        self.scorps = self.canvas.create_text(1400,270,fill="black",font="Docktrin 20 bold", text=(str(self.numScorps)+" Scorpions"))

                    #Remove the hidden object from the remaining lists
                    self.posList.pop(i)
                    self.textList.pop(i)
                    #Decrement i as an object has been found
                    i -= 1
                    #Increment i to iterate through the list
                i += 1
            #Reset i
            i = 0
        #Can be used for debugging
        for img in self.images:
            #print(self.posList[i]) 
            i += 1

    '''
    Function to run the game with a count up timer
    Created on 6/12/21
    '''
    def runGame(self):
        #Store the current time for use later
        tim = time()
        #Set that the game has not been solved
        self.win = False
        #The current number of minutes
        mins = 0
        #Iterate while there are images stored in the list
        while (len(self.images) > 0):
            #If the number of minutes is greater than 0, write the title in a separate fashion
            if mins > 0:
                #Determine if the number of seconds stored is less than 10
                if (int(time() - tim) < 10):
                    #Print out the time with minutes : 0 seconds
                    self.counter = self.canvas.create_text(1400,80,fill="black",font=("Old English Text MT", 40, "bold"), text=str(mins) + ":0" + str(int(time()-tim)))
                else:
                    #Print out the time with minutes : seconds
                    self.counter = self.canvas.create_text(1400,80,fill="black",font=("Old English Text MT", 40, "bold"), text=str(mins) + ":" + str(int(time()-tim)))
            else:
                #Print out the current seconds time
                self.counter = self.canvas.create_text(1400,80,fill="black",font=("Old English Text MT", 40, "bold"), text=str(int(time()-tim)))
            #Refresh the TKinter Frame
            self.root.update_idletasks()
            self.root.update()
            self.canvas.delete(self.counter)
            #Determine if secodns has incremented beyond 60 seconds
            if (int(time() - tim) > 59):
                #Increment the current time stored by 60 seconds
                tim += 60
                #Increment the stored minutes by one minute
                mins += 1
        #Additional refresh, same as above but repeated as the game is now over
        if mins > 0:
            if (int(time() - tim) < 10):
                self.counter = self.canvas.create_text(1400,80,fill="black",font=("Old English Text MT", 40, "bold"), text=str(mins) + ":0" + str(int(time()-tim)))
            else:
                self.counter = self.canvas.create_text(1400,80,fill="black",font=("Old English Text MT", 40, "bold"), text=str(mins) + ":" + str(int(time()-tim)))
        else:
            self.counter = self.canvas.create_text(1400,80,fill="black",font=("Old English Text MT", 40, "bold"), text=str(int(time()-tim)))

        #End the game
        self.endGame()
    
    '''
    Function to destroy uneeded frame items now that the game is complete
    Not very complicated given that one cannot loose the game
    Creted on 6/13/21
    '''
    def endGame(self):
        #Tell the player congratulations
        self.canvas.create_text(self.backgnd_width,2*self.backgnd_height+50,fill="black",font=("Times", 80, "bold"), text="Congratulations!")
        #Pause the frame
        self.gameOver = True
        self.canvas.mainloop()
#Actually run when program is run. This function initiates and runs the game
app = App()