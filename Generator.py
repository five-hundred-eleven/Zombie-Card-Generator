#!/usr/bin/env python

import sys, os
from os import path

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Set directory paths.
cwd = path.abspath('')
sourceDirectory = path.abspath( "sourcefiles/" ) + '/'
imageDirectory = path.abspath( "sourcepics/" ) + '/'
exportDirectory = path.abspath( "generated/" ) + '/'

# Open the font freesans
freesans = path.abspath( sourceDirectory + "FreeSans.ttf" )
# Open the template. Take care not to overwrite this.
template = Image.open(sourceDirectory + "zombiecard.png")
# Open the csv data sheet. This should not be changed in this script.
data = csv.reader( open( sourceDirectory + "players.csv", "rb" ), delimiter = ',',quotechar = '"' )
data.next() # skip header line

# Create variables for fonts and colors. Change these if you wish to adjust the color scheme.
nameFont = ImageFont.truetype(freesans, 28)
nameFontColor = (0, 0, 0)

headerFont = ImageFont.truetype(freesans, 20)
headerFontColor = (0, 0, 0)
  
infoFont = ImageFont.truetype(freesans, 20)
infoFontColor = (0, 150, 0) # dark green

statsFont = ImageFont.truetype(freesans, 20)
statsFontColor = (0, 0, 0)

pentagonColor = (255, 0, 0) # red

# The position of various elements. Measured in pixels from the top left of the image to the top left of the element.
namePosition = (100, 18)
agePosition = (110, 65)
sexPosition = (185, 65) # lol
majorPosition = (265, 65)

# Stats position. This is set up in a grid.
statsRowPos = [630, 760, 890]
statsCollumnPos = [570, 610, 650]

def statsPosition(x,y):
  return ( statsRowPos[x], statsCollumnPos[y] )

# info position.
infoPosition = (70, 530)

for line in data:
  
  name, age, sex, major, info = line[0], line[1], line[2], line[3], line[4]
  
# Insert newlines into info as needed. Here, this is primitively set to every 60 chars.
  i, inc = 60, 60
  while i < info:
    info = info[:i] + '\n' + info[i:]
    i = i + inc 

  img = template
  draw = ImageDraw.Draw(img)

  draw.text(namePosition, name, nameFontColor, nameFont)
  draw.text(agePosition, age, headerFontColor, headerFont)
  draw.text(sexPosition, sex, headerColor, headerFont)
  draw.text(majorPosition, major, headerFontColor, headerFont)

draw = ImageDraw.Draw(img)
img.save( exportName )


