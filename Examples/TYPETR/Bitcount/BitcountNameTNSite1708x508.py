# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     LayerCatalogAnimation.py
#
#     The script assumes one or multiple Bitcount fonts to be installed in the system.
#     Otherwise the script will stop, opening the browser on the TypeNetwork store.
#     Purchase Bitcount fonts at https://store.typenetwork.com/foundry/typetr/fonts/bitcount
#     A single user license of Bitcount is $10.10 per font or $101 for the complete package of 300 styles).
#
#     TODO: Add Variable selection (color selector, checkbox, color wheel)
#
import os
from random import choice

import pagebot
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot import newFS, textBoxBaseLines

typetrStoreUrl = 'https://store.typenetwork.com/foundry/typetr'
EXPORT_PATH = '_export/BitcountLayerCatalogAnimation1708x508.gif'

USE_BITPATH = False

# Initial sample text. Can be altered in the text box of the popup window.
W = 1708 # Width of the sample image. TypeNetwork preference 2040 x 1020
H = 508 # Height of the sample image
padding = 16 # Padding between text and image side.
#t = u'π-day' #Typetr' # Initial sample string
t = 'Bitcount' # Initial sample string
monoSpaced = False
backgroundColor = (0, 0, 0)#(1, 1, 1) #0.1, 0.2, 0.5
italics = False
color = True
frames = 48
fd = 0.4 # Frame duration

# Bitcount is made from 3 spacing sets: 
#    - Monospaced (Grid, Mono)
#    - Proportional (Prop)
# Define the family name of fonts that we want to use, 
# including the type of spacing.
if monoSpaced:
    familyName = 'BitcountMono'
else:
    familyName = 'BitcountProp'
# Just get paths of the fonts, not the Font objects. 
# We want quick interactive response.
# Call imported method, to find all installed Bitcount fonts.
fontNamePaths = getFamilyFontPaths(familyName) 
if not italics:
    for fontName in fontNamePaths.keys():
        if 'Italic' in fontName or 'Double' in fontName:
            del fontNamePaths[fontName]

if USE_BITPATH:
    # Add Bitpath to selection pool of fonts
    if monoSpaced:
        familyName = 'BitpathMono'
    else:
        familyName = 'BitpathProp'

    bitpathPaths = getFamilyFontPaths(familyName)
    for fontName, fontPath in bitpathPaths.items(): # Merge the dictionaries
        if not italics and 'Italic' in fontName:
            continue
        fontNamePaths[fontName] = fontPath

# Define method to show a random sample
def drawSample(name):
    fss = []
    for frame in range(frames-1):
        if frame < frames/2:
            opacity = 1#0.2*random() # Not totally opaque.
            if color:
                c = choice((
                    (0, 0, 0, 0),
                    (1, 1, 1, 1),
                    (1, 1, 1, 1),
                    (0.8, 0.8, 0.8, 1),
                    (0.2, 0.3, 0.4, 0.7),
                    (0.1, 0.2, 0.3, 0.4),
                    (1, 0.4*0.1*random(), 1, opacity),
                    (0.2*random(), 0.5, 0.9, opacity),
                    (0.2*random(), 0.5, 1, opacity),
                    (1, 0.5*random(), 0.5*random(), opacity),
                    (0, 0.5*random(), random(), opacity),
                    (1, 0, random(), opacity),
                    (1, 0, random(), opacity),
                    (1, 0, random(), opacity),
                    (1, 0, random(), opacity),
                    (0.3, 0.2, 0.5*random(), opacity),
                    (random(), 0.5, 0, opacity),
                    (0.5, 0.3*random(), 1, opacity)
                ))
            else:
                r = g = b = random()*0.8
                c = r, g, b, opacity
        
        
            fontNameSingle = choice(fontNamePaths.keys())
            fontNameDouble = fontNameSingle.replace('Single', 'Double')
            # First half of frames, add
            fss.append((getFittingString(name, fontNameSingle, c), getFittingString(name, fontNameDouble, c)))
        else:
            # Remove last
            fss = fss[:-1]
        drawLayers(fss, frame) # Draw layers on several identical frames, using SIngle or Double.

         
def getFittingString(t, fontName, c):
    # Make formatted string of large type. 
    # Then see if it fits and calculate the fitting size.
    # First guess, to see if constructed formatted string fits.
    
    # Calculate the size for the given string for the selected font/spacing.
    # Then use the resulting with as source to calculate the fitting fontSize.
    initialFontSize = 500 
    fs = newFS(t, None, dict(font=fontName, 
        fontSize=initialFontSize))
    fsWidth, fsHeight = fs.size()
    fontSize =  initialFontSize * (W-3*padding) / fsWidth
    # Make new formatted string in fitting fontSize
    fs = newFS(t, None, dict(font=fontName, 
        fontSize=fontSize, textFill=c))
    return fs
        
def drawLayers(fss, frame):
    # Draw this layer in a couple of frame
    newPage(W, H)
    frameDuration(fd)
    #fill(backgroundColor[0],backgroundColor[1],backgroundColor[2])
    #rect(0, 0, W, H)
    y = 3*padding
    for fsSingle, fsDouble in fss:
        if frame < frames/2:
            fs = fsSingle
        else:
            fs = fsDouble
        text(fs, (2*padding, y+100))

if __name__ == '__main__':
         
    # If no Bitcount fonts could be found, open the browser on the TypeNetwork shop page and stop this script.
    if not fontNamePaths:
        os.system('open %s/fonts/%s' % (typetrStoreUrl, 'productus')) #familyName.lower())
    else:
        drawSample(t)
        saveImage(EXPORT_PATH) # Save the sample as file or animated gif.
        
        