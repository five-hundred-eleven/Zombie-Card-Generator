#!/usr/bin/env python

import sys, os
from os import path

import PIL, aggdraw, csv
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from math import sin, cos, radians

# Set directory paths.
cwd = path.abspath('')
sourceDirectory = path.abspath( "sourcefiles/" ) + '/'
imageDirectory = path.abspath( "sourcepics/" ) + '/'
exportDirectory = path.abspath( "generated/" ) + '/'

# Open the font of choice. 
font = path.abspath( sourceDirectory + "arial.ttf" )
# Open the template. Take care not to overwrite this; Note that this is stored as a string in opposed to a file.
templateFile = sourceDirectory + "zombiecard.png"
# Open the csv data sheet. This should not be changed in this script.
data = csv.reader( open( sourceDirectory + "players.csv", "rb" ), delimiter = ',',quotechar = '"' )
data.next() # skip header line

# Create variables for fonts and colors. Change these if you wish to adjust the color scheme.
nameFont = ImageFont.truetype(font, 28)
nameFontColor = (0, 0, 0)

headerFont = ImageFont.truetype(font, 20)
headerFontColor = (0, 0, 0)
  
infoFont = ImageFont.truetype(font, 20)
infoFontColor = (0, 50, 0) # dark green

statsFont = ImageFont.truetype(font, 22)
statsFontColor = (0, 0, 0)

pentagonColor = (255, 0, 0) # red

# The position of various elements. Measured in pixels from the top left of the image to the top left of the element.
namePosition = (104, 16)
agePosition = (106, 70)
sexPosition = (181, 70) # lol
majorPosition = (265, 70)

# Stats position. This is set up in a grid.
statsCollumnPos = [640, 770, 900]
statsRowPos = [571, 606, 640]

def statsPosition(x,y):
  return ( statsCollumnPos[x], statsRowPos[y] )

# info position.
infoPosition = (75, 540)

# Measurements for the center and radius of the pentagon.
pentagonPos = (762,340)
pentagonRadius = 190

# side is the target corner of the pentagon, counted clockwise from the top. Distance is the distance from the center.
def getPentagonCoords(corner, distance):
  angle = radians(corner*72 - 90)
  xCoord = distance * cos( angle )
  yCoord = distance * sin( angle )
  return [pentagonPos[0] + xCoord, pentagonPos[1] + yCoord]

def pentCoordSeq( distance ):
  coordlst = []
  for i in range(0, 5):
    coordlst.extend( getPentagonCoords(i, distance) )
  return coordlst

def pentStatSeq( statslst ):
  coordlst, i = [], 0
  for item in statslst:
    coordlst.extend( getPentagonCoords(i, int(item)*1.52 + 38) )
    i = i + 1
  return coordlst

# This function will split a string into a list of strings approximately charsPerLine in length (cutting them off inteligently).
def splitIntoLines(raw, charsPerLine):
  newlines = []
  nextNewline = charsPerLine
  i = 0

  for char in raw:
    if char == '\n':
      nextNewline = nextNewline + charsPerLine
    elif i == nextNewline and char == ' ':
      newlines.append( i )    
      nextNewline = nextNewline + charsPerLine
    elif i == nextNewline and char != ' ':
      nextNewline = nextNewline + 1
    i = i + 1

  for newline in newlines:
    raw = raw[:newline+0] + '\n' + raw[newline+1:]

  return raw.splitlines()

 
          
for line in data:
  
  name, age, sex, major, info = line[0], line[1], line[2], line[3], line[4]  
  print "Generating image for " + name + "..."

  # splitIntoLines splits info into a list of strings approx. 40 chars long. (Approx. because splits do not occur in words). 
  info = splitIntoLines(info, 35)

  img = Image.open( templateFile )
  draw = ImageDraw.Draw(img)

  draw.text(namePosition, name, nameFontColor, nameFont)
  draw.text(agePosition, age, headerFontColor, headerFont)
  draw.text(sexPosition, sex, headerFontColor, headerFont)
  draw.text(majorPosition, major, headerFontColor, headerFont)

  # Draw Additional Info, line by line.
  localInfoPos = infoPosition
  for infoLine in info:
    draw.text(localInfoPos, infoLine, infoFontColor, infoFont)
    localInfoPos = (70, localInfoPos[1] + 30)

  # Draw the stats. 
  # The first argument is a bit of a hackish way of getting the position of the element from a number 10-19.
  for c in range(10, 19):
    draw.text(statsPosition((c-10) % 3, (c-1)/3 - 3), line[c], statsFontColor, statsFont )

  adraw = aggdraw.Draw(img)

  medBlackPen = aggdraw.Pen( "black", 1 )
  heavyBlackPen = aggdraw.Pen( "black", 3 )
  backgroundBrush = aggdraw.Brush( "white" ) 
  statsBrush = aggdraw.Brush( "red" )

  outline = pentCoordSeq( 190 )
  adraw.polygon(outline, backgroundBrush)

  statsOutline = pentStatSeq( line[5:10] )
  adraw.polygon(statsOutline, statsBrush)
  
  adraw.polygon(outline, heavyBlackPen)

  for p in range(1,5):
    outline = pentCoordSeq( 190 - p*38 )
    adraw.polygon(outline, medBlackPen)
  
  adraw.flush()
  
  if line[19]:
    profilepic = path.abspath( imageDirectory + line[19] )
  else:
    profilepic = path.abspath( imageDirectory + name + ".jpg" )

  if path.exists( profilepic ):
    profilepic = Image.open( profilepic )
  else:
    print "Error: Profile picture not found for " + name
    profilepic = False 

  if profilepic:
    profileLocation = (75, 145, 472, 475)
    frameXSz = profileLocation[2] - profileLocation[0]
    frameYSz = profileLocation[3] - profileLocation[1]
    profilepic = profilepic.resize((frameXSz, frameYSz))
    img.paste(profilepic, profileLocation)

  img.save( exportDirectory + name + ".png" )
