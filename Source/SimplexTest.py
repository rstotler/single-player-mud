import pygame, opensimplex, random
from pygame import *

def circleCircleCollide(CIRCLE1_LOC, CIRCLE1_RADIUS, CIRCLE2_LOC, CIRCLE2_RADIUS):
	
	import math
	dx = CIRCLE1_LOC[0] - CIRCLE2_LOC[0]
	dy = CIRCLE1_LOC[1] - CIRCLE2_LOC[1]
	dr = math.sqrt((dx ** 2) + (dy ** 2))
	
	if dr <= CIRCLE1_RADIUS + CIRCLE2_RADIUS:
		return True
	
	return False

def generateMap(SURFACE, CELL_SIZE, MAP_SIZE, CELL_DICT):

	mapData = []
	for renderLayer in range(4):

		simplexBase = opensimplex.OpenSimplex(random.randrange(2560))
		simplexDetail = opensimplex.OpenSimplex(random.randrange(2560))
		simplexFine = opensimplex.OpenSimplex(random.randrange(2560))

		for yNum in range(MAP_SIZE[1]):
			if renderLayer == 0 : mapData.append([])
			for xNum in range(MAP_SIZE[0]):
			
				if renderLayer == 0 : renderResolutionMod = 3.0
				elif renderLayer in [1, 2] : renderResolutionMod = 1.0
				elif renderLayer == 3 : renderResolutionMod = 1.4
				valueBase = simplexBase.noise2d(xNum / (48.0 * renderResolutionMod), yNum / (48.0 * renderResolutionMod))
				valueDetail = simplexDetail.noise2d(xNum / (18.0 * renderResolutionMod), yNum / (18.0 * renderResolutionMod))
				valueFine = simplexFine.noise2d(xNum / (8.0 * renderResolutionMod), yNum / (8.0 * renderResolutionMod))
				valueMap = valueBase + (valueDetail * .5) + (valueFine * .25)
				valueMap = (valueMap + 1.0) / 2.0
				if valueMap > 1.0 : valueMap = 1.0
				
				cellID = None
				if renderLayer == 0:
					if valueMap < .64 : cellID = "Grass"
					elif valueMap < .655 : cellID = "Beach"
					else : cellID = "Water"
				elif renderLayer == 1:
					if valueMap < .33 : cellID = "Water"
					elif valueMap < .37 : cellID = "Beach"
				elif renderLayer == 2:
					if valueMap < .21 : cellID = "Desert"
					elif valueMap > .65 : cellID = "Forest"
				elif renderLayer == 3:
					if valueMap > .73 : cellID = "Mountain"
					
				# Round Edges #
				if renderLayer == 3:
					if not circleCircleCollide([xNum, yNum], 1, [MAP_SIZE[0] / 2, MAP_SIZE[1] / 2], int(MAP_SIZE[0] * .485)):
						if cellID != "Mountain":
							cellID = "Beach"
					if not circleCircleCollide([xNum, yNum], 1, [MAP_SIZE[0] / 2, MAP_SIZE[1] / 2], int(MAP_SIZE[0] * .49)):
						cellID = "Water"
						
				# Assign Data #
				if renderLayer == 0:
					mapData[-1].append(cellID)
				elif cellID != None:
					if not (renderLayer == 1 and mapData[yNum][xNum] in ["Water"]) \
					and not (renderLayer == 2 and mapData[yNum][xNum] in ["Water"]) \
					and not (renderLayer == 3 and mapData[yNum][xNum] in ["Water"]):
						mapData[yNum][xNum] = cellID
		
	# Draw Map #
	for yNum, yList in enumerate(mapData):
		for xNum, cellData in enumerate(yList):
			if cellData != None:
				SURFACE.blit(CELL_DICT[cellData], [xNum * CELL_SIZE, yNum * CELL_SIZE])

CELL_SIZE = 3
MAP_SIZE = [256, 256]
surfaceMap = pygame.Surface([MAP_SIZE[0] * CELL_SIZE, MAP_SIZE[1] * CELL_SIZE])
window = pygame.display.set_mode([1500, 1000], False, 32)
clock = pygame.time.Clock()
displayLoc = [0, 0]
mouseLocOld = [0, 0]
mouseLoc = [0, 0]
mouseClick = False

cellDict = {}
cellColorDict = {"Water":[20, 20, 90], "Beach":[90, 70, 50], "Grass":[20, 90, 20], "Forest":[15, 55, 15], "Desert":[90, 70, 50], "Mountain":[45, 25, 10]}
for colorID in cellColorDict:
	surfaceCell = pygame.Surface([CELL_SIZE, CELL_SIZE])
	surfaceCell.fill(cellColorDict[colorID])
	cellDict[colorID] = surfaceCell

generateMap(surfaceMap, CELL_SIZE, MAP_SIZE, cellDict)

while True:
	clock.tick(60)	
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			raise SystemExit
		elif event.type == MOUSEMOTION:
			mouseLocOld[0] = mouseLoc[0]
			mouseLocOld[1] = mouseLoc[1]
			mouseLoc[0], mouseLoc[1] = pygame.mouse.get_pos()
			if mouseClick:
				displayLoc[0] += mouseLoc[0] - mouseLocOld[0]
				displayLoc[1] += mouseLoc[1] - mouseLocOld[1]
		elif event.type == MOUSEBUTTONDOWN and event.button == 1:
			mouseClick = True
		elif event.type == MOUSEBUTTONUP and event.button == 1:
			mouseClick = False
		elif event.type == KEYDOWN and event.key == K_SPACE:
			generateMap(surfaceMap, CELL_SIZE, MAP_SIZE, cellDict)
			
	window.fill([0, 0, 0])
	window.blit(surfaceMap, displayLoc)
	pygame.display.update()
	