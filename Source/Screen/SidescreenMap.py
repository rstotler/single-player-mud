import pygame, Config, Utility
from Data import DataWorld
from pygame import *

class LoadSidescreenMap:

	def __init__(self, SIZE):
	
		# Screen Variables #
		self.id = "Map"
		self.objectType = "Sidescreen"
		self.displayLoc = [Config.SCREEN_SIZE[0]-SIZE[0], 0]
	
		# Map Varialbes #
		self.mapZoomLevel = 0
		self.mapCellSizeList = None
	
		# Rect & Surface #
		self.rect = pygame.Rect(self.displayLoc + SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceMapDict = None
		self.surfaceMapPlayerIconDict = None
		
	def initMap(self, TARGET_AREA):
	
		# Get Map ID #
		if "Spaceship Description" in TARGET_AREA.flags : newMapId = "Spaceship-" + "-" + TARGET_AREA.idArea + "-" + TARGET_AREA.idRandom
		else : newMapId = TARGET_AREA.idSolarSystem + "-" + TARGET_AREA.idPlanet + "-" + TARGET_AREA.idArea
		
		# Load Map Surfaces #
		if True:
			
			# Cell Terrain #
			if True:
				surfaceCellDict = {}
				surfaceCellDict["Default"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Default"].fill([140, 140, 140])
				surfaceCellDict["Water"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Water"].fill([20, 20, 90])
				surfaceCellDict["Beach"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Beach"].fill([90, 70, 50])
				surfaceCellDict["Grass"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Grass"].fill([20, 90, 20])
				surfaceCellDict["Forest"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Forest"].fill([15, 55, 15])
				surfaceCellDict["Mountain"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Mountain"].fill([45, 25, 10])
				surfaceCellDict["Desert"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE) ; surfaceCellDict["Desert"].fill([90, 70, 50])
			
			# World Map Alpha Cells #
			if True:
				surfaceCellDict["Alpha"] = []
				for i in range(20):
					newAlphaCell = pygame.Surface(Config.WORLD_MAP_CELL_SIZE, pygame.SRCALPHA, 32)
					alphaPercent = int((i * .05) * 190)
					newAlphaCell.fill([0, 0, 0, alphaPercent])
					surfaceCellDict["Alpha"].append(newAlphaCell)
					
			# Door Alpha Cells #
			if True:
				surfaceCellWallDict = {}
				surfaceCellWallDict["North"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE, pygame.SRCALPHA, 32)
				surfaceCellWallDict["East"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE, pygame.SRCALPHA, 32)
				surfaceCellWallDict["South"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE, pygame.SRCALPHA, 32)
				surfaceCellWallDict["West"] = pygame.Surface(Config.WORLD_MAP_CELL_SIZE, pygame.SRCALPHA, 32)
				pygame.draw.line(surfaceCellWallDict["North"], [0, 0, 0], [0, 0], [Config.WORLD_MAP_CELL_SIZE[0], 0])
				pygame.draw.line(surfaceCellWallDict["East"], [0, 0, 0], [Config.WORLD_MAP_CELL_SIZE[0], 0], Config.WORLD_MAP_CELL_SIZE)
				pygame.draw.line(surfaceCellWallDict["South"], [0, 0, 0], [0, Config.WORLD_MAP_CELL_SIZE[1]], Config.WORLD_MAP_CELL_SIZE)
				pygame.draw.line(surfaceCellWallDict["West"], [0, 0, 0], [0, 0], [0, Config.WORLD_MAP_CELL_SIZE[0]])
				
		# Draw Default Map #
		if True:
			surfaceMap = pygame.Surface([TARGET_AREA.mapTotalCellCount[0] * Config.WORLD_MAP_CELL_SIZE[0], TARGET_AREA.mapTotalCellCount[1] * Config.WORLD_MAP_CELL_SIZE[1]], pygame.SRCALPHA, 32)
			surfaceMap.convert_alpha()
			
			for currentRoomId in TARGET_AREA.roomDict:
				currentRoom = TARGET_AREA.roomDict[currentRoomId]
				if currentRoom.mapLoc != [None, None]:
					
					# Blit Base Map Cell #
					cellBlitLoc = [(currentRoom.mapLoc[0] * Config.WORLD_MAP_CELL_SIZE[0]), (currentRoom.mapLoc[1] * Config.WORLD_MAP_CELL_SIZE[1])]
					if currentRoom.mapTileType in surfaceCellDict : surfaceCell = surfaceCellDict[currentRoom.mapTileType]
					else : surfaceCell = surfaceCellDict["Default"]
					surfaceMap.blit(surfaceCell, cellBlitLoc)
					
					# Blit World Map Alpha Cell #
					if TARGET_AREA.idArea == "World Map":
						alphaCellIndex = int(20 * currentRoom.mapElevationValue)
						if alphaCellIndex < 0 : alphaCell = surfaceCellDict["Alpha"][0]
						elif alphaCellIndex > 19 : alphaCell = surfaceCellDict["Alpha"][19]
						elif alphaCellIndex in range(19) : alphaCell = surfaceCellDict["Alpha"][alphaCellIndex]
						surfaceMap.blit(alphaCell, cellBlitLoc)
						
					# Blit Inside Alpha Cell #
					elif currentRoom.inside:
						surfaceMap.blit(surfaceCellDict["Alpha"][8], cellBlitLoc)
					
					# Blit Door Line Cells #
					for exitDir in ["North", "East", "South", "West"]:
						if exitDir not in currentRoom.exitDict:
							surfaceMap.blit(surfaceCellWallDict[exitDir], cellBlitLoc)
					
					# Debug - Draw Room ID #
					if TARGET_AREA.idArea != "World Map":
						Utility.writeFast(str(currentRoom.idNum), [cellBlitLoc[0], cellBlitLoc[1]], [10, 10, 10], Config.FONT_ROMAN_12, surfaceMap)
					
		# Resize Default Map For Zoom #
		if True:
			DEFAULT_SIZE = [TARGET_AREA.mapTotalCellCount[0] * Config.WORLD_MAP_CELL_SIZE[0], TARGET_AREA.mapTotalCellCount[1] * Config.WORLD_MAP_CELL_SIZE[1]]
			self.surfaceMapDict = {}
			self.surfaceMapPlayerIconDict = {}
			self.mapCellSizeList = []
			for i, sizeRatio in enumerate(Config.MAP_RATIO_LIST):
				
				# Map Surface Transformation #
				self.surfaceMapDict[i] = pygame.transform.scale(surfaceMap, [int(round(DEFAULT_SIZE[0] * sizeRatio)), int(round(DEFAULT_SIZE[1] * sizeRatio))])
				
				# Cell Size List #
				surfaceRect = self.surfaceMapDict[i].get_rect()
				self.mapCellSizeList.append([ (surfaceRect.width / (TARGET_AREA.mapTotalCellCount[0]+0.0)),
											  (surfaceRect.height / (TARGET_AREA.mapTotalCellCount[1]+0.0)) ])
											  
				# Player Icon #
				defaultRect = self.surfaceDefault.get_rect()
				self.surfaceMapPlayerIconDict[i] = pygame.Surface([defaultRect.width, defaultRect.height], pygame.SRCALPHA, 32)
				playerIconLoc = [int(round(defaultRect.width / 2)), int(round(defaultRect.height / 2))]
				pygame.draw.circle(self.surfaceMapPlayerIconDict[i], [170, 10, 10], playerIconLoc, int(round(10 * sizeRatio)))
				
	def moveMouse(self, MOUSE):
	
		pass
		
	def moveMouseWheel(self, TARGET_BUTTON, DATA_PLAYER, PLAYER_SOLAR_SYSTEM):
		
		drawCheck = False
	
		if TARGET_BUTTON == 4 and self.mapZoomLevel > 0:
			self.mapZoomLevel -= 1
			drawCheck = True
		elif TARGET_BUTTON == 5 and self.mapZoomLevel + 1 in self.surfaceMapDict:
			self.mapZoomLevel += 1
			drawCheck = True
			
		if drawCheck:
			playerArea = DataWorld.getParentArea(PLAYER_SOLAR_SYSTEM, DATA_PLAYER)
			Config.DRAW_SCREEN_DICT["Map"] = True
		
	def draw(self, WINDOW, DATA_PLAYER, TARGET_AREA, INTERFACE_IMAGE_DICT, DRAW_TV_BORDER):

		# Get Data #
		defaultRect = self.surfaceDefault.get_rect()
		mapCellSize = self.mapCellSizeList[self.mapZoomLevel]
		currentRoom = TARGET_AREA.roomDict[DATA_PLAYER.currentRoom]
		startLoc = [(defaultRect.width / 2) - (mapCellSize[0] / 2), (defaultRect.height / 2) - (mapCellSize[1] / 2)]
		mapOffset = [-(int(round(currentRoom.mapLoc[0] * mapCellSize[0]))), -(int(round(currentRoom.mapLoc[1] * mapCellSize[1])))]
		mapDisplayLoc = [startLoc[0] + mapOffset[0], startLoc[1] + mapOffset[1]]
		
		# Draw Map To Default Surface #
		if self.surfaceMapDict != None:
			self.surfaceDefault.fill([10, 10, 30])
			if self.mapZoomLevel in self.surfaceMapDict:
				self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], mapDisplayLoc)
			
			# World Map Side Screen Copys (Seamless World) #
			if TARGET_AREA.idArea == "World Map":
				surfaceRect = self.surfaceMapDict[self.mapZoomLevel].get_rect()
				
				if mapDisplayLoc[0] > 0:
					self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0] - surfaceRect.width, mapDisplayLoc[1]])
					
					# Corners - Top Left, Bottom Left #
					if mapDisplayLoc[1] > 0:
						self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0] - surfaceRect.width, mapDisplayLoc[1] - surfaceRect.height])
					if mapDisplayLoc[1] < surfaceRect.height:
						self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0] - surfaceRect.width, mapDisplayLoc[1] + surfaceRect.height])
						
				if mapDisplayLoc[0] < surfaceRect.width:
					self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0] + surfaceRect.width, mapDisplayLoc[1]])
				
					# Corners - Top Right, Bottom Right #
					if mapDisplayLoc[1] > 0:
						self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0] + surfaceRect.width, mapDisplayLoc[1] - surfaceRect.height])
					if mapDisplayLoc[1] < surfaceRect.height:
						self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0] + surfaceRect.width, mapDisplayLoc[1] + surfaceRect.height])
						
				if mapDisplayLoc[1] > 0:
					self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0], mapDisplayLoc[1] - surfaceRect.height])
				if mapDisplayLoc[1] < surfaceRect.height:
					self.surfaceDefault.blit(self.surfaceMapDict[self.mapZoomLevel], [mapDisplayLoc[0], mapDisplayLoc[1] + surfaceRect.height])
				
			# Player Icon #
			self.surfaceDefault.blit(self.surfaceMapPlayerIconDict[self.mapZoomLevel], [0, 0])
				
		# Write Labels #
		Utility.writeFast("Planet: " + str(DATA_PLAYER.currentPlanet), [8, 30], [200, 200, 200], Config.FONT_ROMAN_12, self.surfaceDefault)
		Utility.writeFast("Area: " + str(TARGET_AREA.idArea), [8, 40], [200, 200, 200], Config.FONT_ROMAN_12, self.surfaceDefault)
				
		# Draw Map To Screen #
		self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["Border Map"], [0, 0])
		if DRAW_TV_BORDER : self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["TV Border Map"], [0, 0])
		WINDOW.blit(self.surfaceDefault, self.displayLoc)
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
		