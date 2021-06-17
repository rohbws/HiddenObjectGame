from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from random import *
from time import time

'''
Class that controls the entire game
'''
class App(object):


    #Function to run when start game button is pressed
    def endWait(self):
        #For testing
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
        self.croc = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/croc.png")
        #Make the crocodile smaller
        self.croc = self.croc.subsample(6)
        #Make the background smaller
        self.backgnd = self.backgnd.subsample(3)
        #Calculate some basic information on the background image
        self.backgnd_width = (self.backgnd.width()/2)
        self.backgnd_height = (self.backgnd.height()/2)
        #Add the background to the canvas
        self.canvas.create_image(self.backgnd_width,self.backgnd_height,image=self.backgnd)
        #Initialize a bamboo structure to surround the timer
        self.bamboo = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/bamboo.png")
        self.bamboo = self.bamboo.subsample(3)
        self.canvas.create_image(1400, 80, image=self.bamboo)
        #Initialze the desired time to play the game
        self.time = 30
        #Initialze multiple crocodiles
        crocPos = [[798, 433], [1004, 89], [457, 334], [693, 192], [356, 757], [34, 717]]
        #Initialize a variable to store the current number of crocs
        self.numCrocs = 0
        #Iterate through the crocPos array
        for idx in range(len(crocPos)):
            #Add crocodiles to the canvas
            self.images.append(self.canvas.create_image(crocPos[idx][0],crocPos[idx][1], image=self.croc))
            self.posList.append([crocPos[idx][0],crocPos[idx][1]])
            self.textList.append("Crocidile")
            #Increment the number of crocs
            self.numCrocs += 1
        
        #Initialize a text description of the crocs
        self.crocs = self.canvas.create_text(1400,210,fill="black",font="Docktrin 20 bold", text=(str(self.numCrocs)+" Crocodiles"))

        # Perform the same actions on the cobra
        self.cobra = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/cobra.png")
        self.cobra = self.cobra.subsample(10)
        snakePos = [[345, 273], [944, 344], [196, 579]]
        #snakePos = [[345, 273]]
        self.numCobras = 0

        #Iterate through every snake position
        for idx in range(len(snakePos)):
            self.images.append(self.canvas.create_image(snakePos[idx][0],snakePos[idx][1], image=self.cobra))
            self.posList.append([snakePos[idx][0],snakePos[idx][1]])
            self.textList.append("Cobra")
            #Increment the number of snakes
            self.numCobras += 1

        #Initialize a text listing the description of the cobras
        self.cobras = self.canvas.create_text(1400,180,fill="black",font="Docktrin 20 bold", text=(str(self.numCobras)+" Cobras"))

        #Load the spider image
        self.spider = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/spider.png")
        self.spider = self.spider.subsample(5)

        #Initialize preset spider images
        self.spiderPos= [[877, 369], [1084, 412], [1220, 353], [908, 705], [728, 770], [69, 240], [458, 91], [153, 46]]
        #self.spiderPos= [[877, 369]]
        self.numSpids = 0

        #Iterate through every preset spider
        for idx in range(len(self.spiderPos)):
            self.images.append(self.canvas.create_image(self.spiderPos[idx][0], self.spiderPos[idx][1], image = self.spider))
            self.posList.append(self.spiderPos[idx])
            self.textList.append("Spider")
            #Increment the number of spiders
            self.numSpids += 1

        #Initialize the number of spiders
        self.spids = self.canvas.create_text(1400,240,fill="black",font="Docktrin 20 bold", text=(str(self.numSpids)+" Spiders"))

        #Load the scorpion image
        self.scorpion = PhotoImage( file = "C:/Users/boswo/Desktop/Hidden Object Game/scorp.png")
        self.scorpion = self.scorpion.subsample(5)

        #Load preset scorpion positions
        self.scorpPos= [[50, 50], [178, 767], [636, 622], [475, 475], [1128, 589], [915, 798], [543, 268], [858, 138], [1194, 66]]
        #self.scorpPos= [[50, 50]]
        self.numScorps = 0

        #Iterate through every scorp pos preset
        for idx in range(len(self.scorpPos)):
            self.images.append(self.canvas.create_image(self.scorpPos[idx][0], self.scorpPos[idx][1], image = self.scorpion))
            self.posList.append(self.scorpPos[idx])
            self.textList.append("Scorp")
            #Increment the number of scorpions
            self.numScorps += 1

        #Add a text description of the scorpions
        self.scorps = self.canvas.create_text(1400,270,fill="black",font="Docktrin 20 bold", text=(str(self.numScorps)+" Scorpions"))

        #Run the game
        self.runGame()

    '''
    Function to remove an image if the registered click is near to a hidden object
    Created on 6/12/21
    '''
    def rem(self, x, y):
        #Ensure the game is not over
        if not self.gameOver:
            #Variable to increment through the list
            i = 0
            #Iterate through the array containing the images loaded on the canvas
            for img in self.images:
                #Determine if the registered click is near to the indexed hidden object
                if (abs(x - self.posList[i][0]) < 30 and abs(y - self.posList[i][1]) < 30):
                    #Remove that image from the canvas
                    self.canvas.delete(self.images[i])
                    self.images.pop(i)

                    #Determine which class of object was clicked
                    if self.textList[i] == "Cobra":
                        #Decrement the number of cobras
                        self.numCobras -= 1
                        #Repaint the cobra listing
                        self.canvas.delete(self.cobras)
                        self.cobras = self.canvas.create_text(1400,180,fill="black",font="Docktrin 20 bold", text=(str(self.numCobras)+" Cobras"))
                    elif self.textList[i] == "Crocidile":
                        #Decrement the number of crocodiles
                        self.numCrocs -= 1
                        #Repaint the crocodile listing
                        self.canvas.delete(self.crocs)
                        self.crocs = self.canvas.create_text(1400,210,fill="black",font="Docktrin 20 bold", text=(str(self.numCrocs)+" Crocodiles"))
                    elif self.textList[i] == "Spider":
                        #Decrement the number of spiders
                        self.numSpids -= 1
                        #Repaint the spider listing
                        self.canvas.delete(self.spids)
                        self.spids = self.canvas.create_text(1400,240,fill="black",font="Docktrin 20 bold", text=(str(self.numSpids)+" Spiders"))
                    elif self.textList[i] == "Scorp":
                        #Decrement the number of scorpions
                        self.numScorps -= 1
                        #Repaint the scorpion listing
                        self.canvas.delete(self.scorps)
                        self.scorps = self.canvas.create_text(1400,270,fill="black",font="Docktrin 20 bold", text=(str(self.numScorps)+" Scorpions"))

                    #Remove the current listing that was clicked from the lists used throughout the program
                    self.posList.pop(i)
                    self.textList.pop(i)
                    #Decrement i as an object has been removed from an array
                    i -= 1
                #Increment i as we iterate through the array
                i += 1
            #Reset i
            i = 0
        #Can be used for debugging to print the current image list
        for img in self.images:
            #print(self.posList[i]) 
            i += 1

    '''
    Function to run the game with a count up timer
    Created on 6/12/21
    '''
    def runGame(self):
        #Initialize a time variable with a float containing the current time
        tim = time()
        #Set that the player has not won the game
        self.win = False
        #Store the current number of minutes
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