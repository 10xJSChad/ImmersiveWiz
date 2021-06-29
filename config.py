broadcastSpace = "192.168.1.255" #Your lights' broadcast space

window = "" #The window to sync the lights to.
#Leave blank if you want the lights to always sync to whatever's on the screen

lightsOffThreshold = 30 #The total light value at which the lights turn off
#Set to 0 to never turn lights off

updateTime = 1 #How often to get the average screen color and update the lights (seconds)

colorMultiplier = 1 #How much to multiply the color values by

bulbBrightness = 255 #The brightness setting of the bulbs

colorToUse = "average" #Whether to use the "average" or "dominant" color of your screen
#I recommend keeping this on average as using the dominant color is very slow at the moment
