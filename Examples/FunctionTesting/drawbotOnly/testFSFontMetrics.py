#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting usage of DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFSFontMetrics.py
#
import sys
from pagebot.contexts import defaultContext as context
if not context.isDrawBot:
    sys.exit('Example only runs on DrawBot.')

b = context.b # Builder is DrawBot

txt = "Hellog World"
x, y = 10, 100

# set a font
b.font("Verdana")
# set a font size
b.fontSize(300)
# draw the text
b.text(txt, (x, y))

# calculate the size of the text
textWidth, textHeight = b.textSize(txt)

# set a red stroke color
b.stroke(1, 0, 0)
# loop over all font metrics
for metric in (0, b.fontDescender(), b.fontAscender(), b.fontXHeight(), b.fontCapHeight()):
    # draw a red line with the size of the drawn text
    b.line((x, y+metric), (x+textWidth, y+metric))
