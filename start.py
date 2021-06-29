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

async def changeAll(color): #Self explanatory
    global bulbs
    for bulb in bulbs:
        await bulb.turn_on(PilotBuilder(rgb = (color)))
        
async def allOff(): #Self explanatory
    global bulbs
    for bulb in bulbs:
        await bulb.turn_off()
  
def intensifyColor(color, multiplier):
    newColors = []
    for x in color:
        x *= multiplier
        if x > 255: x = 255
        newColors.append(x)
    color = (newColors[0], newColors[1], newColors[2])
    return color

async def main():  
    while True:
        if (GetWindowText(GetForegroundWindow()) == config.window or config.window == ""): #Self explanatory
            #Takes a screenshot of your main screen
            screenshot = pyautogui.screenshot()
            screenshot.save(r'screenshot.png') #Saves it to the working folder
            
            #Gets the average color
            screenshot = cv2.imread('screenshot.png')
            avg_color_per_row = numpy.average(screenshot, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)
            avg_color_fixed = (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
            
            #IMPORTANT
            #avg_color[0] is blue
            #avg_color[1] is green
            #avg_color[2] is red
            
            #Gets the total value of the red, green & blue values of the average color
            totalValue = int(avg_color[2]) + int(avg_color[1]) + int(avg_color[0])
            if totalValue > config.lightsOffThreshold: #lightsOffThreshold is the value at which the lights turn off
                await changeAll(intensifyColor(avg_color_fixed, config.colorMultiplier))    
            else: await allOff() #Turns the lights off if the total value is less than lightsOffThreshold
            
            #print(str(avg_color) + " | " + str(totalValue))
            
        else: 1+1
        
        time.sleep(config.updateTime)
        
loop = asyncio.get_event_loop()
loop.run_until_complete(initialize())
    
th = threading.Thread(target=asyncio.run(main()))
th.start()