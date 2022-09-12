import pygame, random, Config
from pygame import *

def loadColorDict():

	codeDict = {"lr":[255, 80,  80],  "r":[255, 0,   0],   "dr":[145, 0,   0],   "ddr":[80,  0,   0],
				"lo":[255, 150, 75],  "o":[255, 100, 0],   "do":[170, 95,  0],   "ddo":[80,  40,  0],
				"ly":[255, 255, 80],  "y":[255, 255, 0],   "dy":[145, 145, 0],   "ddy":[80,  80,  0],
				"lg":[80,  255, 80],  "g":[0,   255, 0],   "dg":[0,   145, 0],   "ddg":[0,   80,  0],
				"lc":[80,  255, 255], "c":[0,   255, 255], "dc":[0,   145, 145], "ddc":[0,   80,  80],
				"lb":[80,  80,  255], "b":[0,   0,   255], "db":[0,   0,   145], "ddb":[0,   0,   80],
				"lv":[255, 80,  255], "v":[255, 0,   255], "dv":[145, 0,   145], "ddv":[80,  0,   80],
				"lm":[175, 80,  255], "m":[175, 0,   255], "dm":[95,  0,   145], "ddm":[75,  0,   80],
				"lw":[255, 255, 255], "w":[255, 255, 255], "dw":[220, 220, 220], "ddw":[150, 150, 150],
				"la":[150, 150, 150], "a":[150, 150, 150], "da":[120, 120, 120], "dda":[70,  70,  70],
				"x":[0, 0, 0]}
				
	return codeDict

def writeFast(LABEL, LOCATION, COLOR, FONT, SCREEN):

	# Location Mods #
	labelSize = FONT.size(LABEL)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = SCREEN.get_width() - labelSize[0]
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = SCREEN.get_height() - labelSize[1]
	
	labelRender = FONT.render(LABEL, True, COLOR)
	SCREEN.blit(labelRender, LOCATION)
	
def writeColor(LABEL, COLOR_CODE, COLOR_DICT, LOCATION, FONT, SCREEN):

	# Location Mods #
	labelSize = FONT.size(LABEL)
	if isinstance(LOCATION[0], str) and LOCATION[0].lower() == "left" : LOCATION[0] = 0
	elif isinstance(LOCATION[0], str) and LOCATION[0].lower() == "right" : LOCATION[0] = SCREEN.get_width() - labelSize[0]
	if isinstance(LOCATION[1], str) and LOCATION[1].lower() == "top" : LOCATION[1] = 0
	elif isinstance(LOCATION[1], str) and LOCATION[1].lower() == "bottom" : LOCATION[1] = SCREEN.get_height() - labelSize[1]
	
	# Regular Variables #
	targetColor = ""
	colorCount = 0
	printIndex = 0
	displayX = LOCATION[0]
	writeCheck = False
	
	for i, letter in enumerate(COLOR_CODE):
	
		# Sort #
		if stringIsNumber(letter):
			if colorCount != 0 : colorCount *= 10
			colorCount += int(letter)
		else:
			targetColor = targetColor + letter
			if len(COLOR_CODE) > i+1 and stringIsNumber(COLOR_CODE[i+1]):
				writeCheck = True
			
		# Write Check #
		if i+1 == len(COLOR_CODE):
			writeCheck = True
			
		# Write #
		if writeCheck == True:
			writeColor = [255, 255, 255]
			if targetColor in COLOR_DICT : writeColor = COLOR_DICT[targetColor]
			
			textString = LABEL[printIndex:printIndex+colorCount]
			textRender = FONT.render(textString, True, writeColor)	
			SCREEN.blit(textRender, [displayX, LOCATION[1]])
			
			printIndex += colorCount
			if printIndex == len(LABEL) : return
			displayX += FONT.size(textString)[0]
			colorCount = 0
			targetColor = ""
			writeCheck = False
		
def renderOutlineText(TEXT, FONT, PX_OUTLINE=2, COLOR_TEXT=[230, 230, 230], COLOR_OUTLINE=[10, 10, 10]):

	surfaceText = FONT.render(TEXT, True, COLOR_TEXT).convert_alpha()
	textWidth = surfaceText.get_width() + 2 * PX_OUTLINE
	textHeight = FONT.get_height()

	surfaceOutline = pygame.Surface([textWidth, textHeight + 2 * PX_OUTLINE]).convert_alpha()
	surfaceOutline.fill([0, 0, 0, 0])
	surfaceMain = surfaceOutline.copy()
	surfaceOutline.blit(FONT.render(str(TEXT), True, COLOR_OUTLINE).convert_alpha(), [0, 0])
	
	circleCache = {}
	for dx, dy in circlePoints(circleCache, PX_OUTLINE):
		surfaceMain.blit(surfaceOutline, [dx + PX_OUTLINE, dy + PX_OUTLINE])
		
	surfaceMain.blit(surfaceText, [PX_OUTLINE, PX_OUTLINE])
	
	return surfaceMain
	
def circlePoints(CIRCLE_CACHE, R):

	R = int(round(R))
	if R in CIRCLE_CACHE:
		return CIRCLE_CACHE[R]
	
	x, y, e = R, 0 , 1 - R
	CIRCLE_CACHE[R] = points = []
	
	while x >= y:
		points.append([x, y])
		y += 1
		if e < 0:
			e += 2 * y - 1
		else:
			x -= 1
			e += 2 * (y - x) - 1
	
	points += [[y, x] for x, y in points if x > y]
	points += [[-x, y] for x, y in points if x]
	points += [[x, -y] for x, y in points if y]
	points.sort()
	
	return points
	
def outline(SCREEN, COLOR, LOCATION, SIZE, LINE_WIDTH=1):
	
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0] + SIZE[0] - 1, LOCATION[1]], LINE_WIDTH)                             # Top Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1]], [LOCATION[0], LOCATION[1] + SIZE[1] - 1], LINE_WIDTH)                             # Left Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0] + SIZE[0] - 1, LOCATION[1]], [LOCATION[0] + SIZE[0] - 1, LOCATION[1] + SIZE[1] - 1], LINE_WIDTH) # Right Line
	pygame.draw.line(SCREEN, COLOR, [LOCATION[0], LOCATION[1] + SIZE[1] - 1], [LOCATION[0] + SIZE[0] - 1, LOCATION[1] + SIZE[1] - 1], LINE_WIDTH) # Bottom Line
	
def stringIsNumber(STRING):

	try:
		int(STRING)
		return True
	except ValueError:
		return False

def generateRandomId():
	
	randomId = str(random.randrange(1000000, 9999999))
	randomIndex = random.randrange(len(randomId))
	randomAlpha1 = random.choice(Config.ALPHABET_STRING)
	randomAlpha2 = random.choice(Config.ALPHABET_STRING)
	randomId = randomId[0:randomIndex] + randomAlpha1 + randomId[randomIndex::] + randomAlpha2
	
	return randomId
	
def createKeyList(TARGET_STRING):

	TARGET_STRING = TARGET_STRING.lower()
	keyList = [TARGET_STRING]

	if len(TARGET_STRING.split()) > 2:
		for iNum in range(len(TARGET_STRING.split())-2):
			if ' '.join(TARGET_STRING.split()[0:iNum+2]) not in keyList:
				keyList.append(' '.join(TARGET_STRING.split()[0:iNum+2]))
		
	if len(TARGET_STRING.split()) > 1:
		for skillKeyword in TARGET_STRING.split():
			if skillKeyword not in keyList:
				keyList.append(skillKeyword)
				
	return keyList
	
def rectRectCollide(RECT1_LOC, RECT2_LOC, SIZE):

	if RECT1_LOC[0] in range(RECT2_LOC[0], RECT2_LOC[0] + SIZE[0]):
		if RECT1_LOC[1] in range(RECT2_LOC[1], RECT2_LOC[1] + SIZE[1]):
			return True

	return False

def circleCircleCollide(CIRCLE1_LOC, CIRCLE1_RADIUS, CIRCLE2_LOC, CIRCLE2_RADIUS):

	import math
	dx = CIRCLE1_LOC[0] - CIRCLE2_LOC[0]
	dy = CIRCLE1_LOC[1] - CIRCLE2_LOC[1]
	dr = math.sqrt((dx ** 2) + (dy ** 2))
	
	if dr <= CIRCLE1_RADIUS + CIRCLE2_RADIUS:
		return True
	
	return False
	