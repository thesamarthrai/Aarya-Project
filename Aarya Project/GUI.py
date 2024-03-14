from tkinter import *
from PIL import Image,ImageTk,ImageSequence #pip install pillow
import time
import pygame  #pip install pygame
from pygame import mixer
mixer.init()


root = Tk()  #for screen size
root.geometry("1000x500")

def GUI():
    root.lift()  # so that when we open or run Jarvis it comes 1st on our screen
    root.attributes("-topmost",True)
    global img  # Image declaration
    img = Image.open("Jarvisgif2.gif")
    lbl = Label(root)
    lbl.place(x=0,y=0)
    i = 0
    mixer.music.load("Q.mp3")
    mixer.music.play()
    
    for img in ImageSequence.Iterator(img):
        img = img.resize((1000,500))  #So that it fills the screen
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(0.04)
    root.destroy()
    
GUI()
root.mainloop()    