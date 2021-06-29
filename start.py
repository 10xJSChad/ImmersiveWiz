import pyautogui
import cv2
import numpy
import asyncio
import time
import threading
import config
import os

from win32gui import GetWindowText, GetForegroundWindow
from pywizlight import wizlight, PilotBuilder, discovery

bulbs = []

async def initialize(): 
    global bulbs
    bulbs = await discovery.discover_lights(broadcast_space=config.broadcastSpace)

async def changeAll(color):
    global bulbs
    for bulb in bulbs:
        await bulb.turn_on(PilotBuilder(rgb = (color)))
        
async def allOff():
    global bulbs
    for bulb in bulbs:
        await bulb.turn_off()
        
async def setBrightness(newBrightness): 
    global bulbs
    for bulb in bulbs:
        await bulb.turn_on(PilotBuilder(brightness = newBrightness))
  
def intensifyColor(color, multiplier):
    newColors = []
    for x in color:
        x *= multiplier
        if x > 255: x = 255
        newColors.append(x)
    color = (newColors[0], newColors[1], newColors[2])
    return color

def getAverageColor(screenshot):
        avg_color_per_row = numpy.average(screenshot, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
        return avg_color

def getDominantColor(screenshot):
    colors, count = numpy.unique(screenshot.reshape(-1,screenshot.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]
            
async def main():  
    while True:
        if (GetWindowText(GetForegroundWindow()) == config.window or config.window == ""):
            
            #Takes a screenshot of your main screen
            screenshot = pyautogui.screenshot()
            screenshot.save(r'screenshot.png') #Saves it to the working folder
            
            screenshot = cv2.imread('screenshot.png')
            
            #Gets the average or dominant color
            if config.colorToUse == "dominant": 
                screenColor = getDominantColor(screenshot)
            else: screenColor = getAverageColor(screenshot)
            
            #Formats it for the bulbs 
            screenColorFixed = (int(screenColor[2]), int(screenColor[1]), int(screenColor[0]))
            
            #IMPORTANT
            #screenColor[0] is blue
            #screenColor[1] is green
            #screenColor[2] is red
            
            #screenColorFixed[0] is red
            #screenColorFixed[1] is green
            #screenColorFixed[2] is blue
            
            #Gets the total value of the red, green & blue values of the average color
            totalValue = screenColorFixed[0] + screenColorFixed[1] + screenColorFixed[2]
            if totalValue > config.lightsOffThreshold: #lightsOffThreshold is the value at which the lights turn off
                await changeAll(intensifyColor(screenColorFixed, config.colorMultiplier))  
                await setBrightness(config.bulbBrightness)
            else: await allOff() #Turns the lights off if the total value is less than lightsOffThreshold
            
            #print(str(screenColorFixed) + " | " + str(totalValue))
            
        else: 1+1
        
        time.sleep(config.updateTime)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(initialize())
    
th = threading.Thread(target=asyncio.run(main()))
th.start()