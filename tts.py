
# Import the required module for text 
# to speech conversion
from gtts import gTTS
import pygame

# This module is imported so that we can 
# play the converted audio
import os
  
# The text that you want to convert to audio
mytext = 'Welcome to geeksforgeeks!'
  
# Language in which you want to convert
language = 'da'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
# welcome 
myobj.save("output.mp3")
  

# Initialize pygame mixer module
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load('output.mp3')

# Start playing the MP3 file
pygame.mixer.music.play()

# Wait for the MP3 to finish playing
while pygame.mixer.music.get_busy():
    pass

# Cleanup the pygame mixer module
pygame.mixer.quit()