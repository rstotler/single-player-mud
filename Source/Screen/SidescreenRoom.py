import pygame, random, Config, Utility, ScreenGame
from Data import DataWorld
from pygame import *

class LoadSidescreenRoom:

	def __init__(self, SIZE):
	
		self.id = "Room"
		self.objectType = "Sidescreen"
		self.displayLoc = [0, 0]
		self.displaySize = SIZE
		self.displayRoom = None
		self.displayRoomTimeOfDay = None
		self.bottomItemOverlapCheck = [False, False] # Mob Area (Left), Player Area (Right) #
	
		# Debug Area Data #
		self.displayDebugArea = False
		self.rectEnemyArea = pygame.Rect(0, 120, 650, 250)
		self.rectPlayerArea = pygame.Rect(660, 120, 326, 250)
		
		# Rects & Surfaces #
		self.rect = pygame.Rect(self.displayLoc + SIZE)
		self.rectTop = pygame.Rect([0, 0, SIZE[0], 115])
		self.rectBottom = pygame.Rect([0, self.rectTop.bottom, SIZE[0], SIZE[1] - self.rectTop.height])
		self.surfaceDefault = pygame.Surface(SIZE, pygame.SRCALPHA, 32)
		self.surfaceItems = None # temp
		self.surfaceEnemyEntities = pygame.Surface([650, self.rect.height], pygame.SRCALPHA, 32) # Enemy Area Width #
		self.surfaceGroupEntities = pygame.Surface([326, self.rect.height], pygame.SRCALPHA, 32) # Group Area Width #
		
	def moveMouseWheel(self, TARGET_BUTTON):
		
		pass
		
	def updateEntitySurface(self, DATA_PLAYER, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT):
		
		# Get Data #
		self.surfaceEnemyEntities.fill(0)
		entityDrawOrderDict = {}
		yLocList = []
		self.bottomItemOverlapCheck[0] = False
		
		# Get Draw Order #
		if self.displayRoom != None:
			for roomEntity in self.displayRoom.itemList + self.displayRoom.mobList:
				if (roomEntity.objectType == "Mob" and roomEntity not in DATA_PLAYER.groupList) \
				or (roomEntity.objectType == "Item" and roomEntity.dropSide == "Mob"):
					roomEntityYLoc = roomEntity.rectArea[1] + roomEntity.rectArea.height
					if roomEntityYLoc not in entityDrawOrderDict : entityDrawOrderDict[roomEntityYLoc] = [roomEntity]
					else : entityDrawOrderDict[roomEntityYLoc].append(roomEntity)
					if roomEntityYLoc not in yLocList : yLocList.append(roomEntityYLoc)
			yLocList.sort()
			
		# Draw Entities #
		for currentYLevel in yLocList:
			for roomEntity in entityDrawOrderDict[currentYLevel]:
			
				# Draw Entity Image #
				if True:
					idImage = "Default"
					entityImage = None
					
					# Get Image #
					if True:
						if roomEntity.objectType == "Item" and roomEntity.idImage == "Chest" and "Container Status" in roomEntity.flags:
							stringChestStatus = None
							if roomEntity.flags["Container Status"] == "Open" : stringChestStatus = "Open"
							elif roomEntity.flags["Container Status"] in ["Closed", "Locked"] : stringChestStatus = "Closed"
							if stringChestStatus != None and "Chest " + stringChestStatus in ITEM_IMAGE_DICT:
								idImage = "Chest " + stringChestStatus
						elif roomEntity.objectType == "Mob" and roomEntity.idImage in ENTITY_IMAGE_DICT : idImage = roomEntity.idImage
						elif roomEntity.objectType == "Item" and roomEntity.idImage in ITEM_IMAGE_DICT : idImage = roomEntity.idImage
						
						if roomEntity.objectType == "Item" : entityImage = ITEM_IMAGE_DICT[idImage]
						elif roomEntity.objectType == "Mob":
							entityImage = ENTITY_IMAGE_DICT[idImage]
							
							if "Attack" in roomEntity.animationDict:
								if roomEntity.animationDict["Attack"]["Current Step"] in [0, 2]:
									entityImage = ENTITY_IMAGE_DICT[roomEntity.idImage + " White"]
							
							elif "Get Hit" in roomEntity.animationDict:
								entityImage = ENTITY_IMAGE_DICT[roomEntity.idImage + " Red"]
							
							if entityImage == None:
								if "Dire Mob" in roomEntity.flags : entityImage = ENTITY_IMAGE_DICT[roomEntity.idImage + " Dire"]
								else : entityImage = ENTITY_IMAGE_DICT[roomEntity.idImage]
						
					# Draw Entity #
					if entityImage != None:
						entityXLoc = roomEntity.rectArea[0] - ((roomEntity.imageSize[0] - roomEntity.rectArea.width) / 2)
						entityYLoc = roomEntity.rectArea.bottom - roomEntity.imageSize[1]
						self.surfaceEnemyEntities.blit(entityImage, [entityXLoc, entityYLoc])
						#pygame.draw.rect(self.surfaceEnemyEntities, [20, 20, 70], [roomEntity.rectArea[0], roomEntity.rectArea[1], roomEntity.rectArea.width, roomEntity.rectArea.height])
						
						# Overlap Check #
						if roomEntity.rectArea.bottom - roomEntity.imageSize[1] < self.rectBottom.top:
							self.bottomItemOverlapCheck[0] = True
					
	def updateGroupEntitySurface(self, DATA_PLAYER, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT):
	
		# Get Data #
		self.surfaceGroupEntities.fill(0)
		entityDrawOrderDict = {}
		yLocList = []
		self.bottomItemOverlapCheck[1] = False
	
		# Get Draw Order #
		if self.displayRoom != None:
			for roomEntity in self.displayRoom.itemList + [DATA_PLAYER] + DATA_PLAYER.groupList:
				if roomEntity.objectType in ["Player", "Mob"] or (roomEntity.objectType == "Item" and roomEntity.dropSide == "Player"):
					roomEntityYLoc = roomEntity.rectArea[1] + roomEntity.rectArea.height
					if roomEntityYLoc not in entityDrawOrderDict : entityDrawOrderDict[roomEntityYLoc] = [roomEntity]
					else : entityDrawOrderDict[roomEntityYLoc].append(roomEntity)
					if roomEntityYLoc not in yLocList : yLocList.append(roomEntityYLoc)
			yLocList.sort()
			
		# Draw Entities #
		for currentYLevel in yLocList:
			for roomEntity in entityDrawOrderDict[currentYLevel]:
				
				# Draw Entity Image #
				if True:
					idImage = "Default"
					entityImage = None
					
					# Get Image ID #
					if True:
						if roomEntity.objectType == "Item" and roomEntity.idImage == "Chest" and "Container Status" in roomEntity.flags:
							stringChestStatus = None
							if roomEntity.flags["Container Status"] == "Open" : stringChestStatus = "Open"
							elif roomEntity.flags["Container Status"] in ["Closed", "Locked"] : stringChestStatus = "Closed"
							if stringChestStatus != None and "Chest " + stringChestStatus in ITEM_IMAGE_DICT:
								idImage = "Chest " + stringChestStatus
						elif roomEntity.objectType == "Player" : idImage = "Player"
						elif roomEntity.objectType == "Mob" and roomEntity.idImage in ENTITY_IMAGE_DICT : idImage = roomEntity.idImage
						elif roomEntity.objectType == "Item" and roomEntity.idImage in ITEM_IMAGE_DICT : idImage = roomEntity.idImage
						
						# Get Image #
						if idImage != None:
							if roomEntity.objectType == "Item" and idImage in ITEM_IMAGE_DICT : entityImage = ITEM_IMAGE_DICT[idImage]
							elif roomEntity.objectType in ["Player", "Mob"]:
								entityImage = ENTITY_IMAGE_DICT[idImage]
								
								if "Attack" in roomEntity.animationDict and (idImage + " White") in ENTITY_IMAGE_DICT:
									if roomEntity.animationDict["Attack"]["Current Step"] in [0, 2]:
										entityImage = ENTITY_IMAGE_DICT[idImage + " White"]
								
								elif "Get Hit" in roomEntity.animationDict and (idImage + " Red") in ENTITY_IMAGE_DICT:
									entityImage = ENTITY_IMAGE_DICT[idImage + " Red"]
								
								if roomEntity.objectType == "Mob" and entityImage == None:
									if "Dire Mob" in roomEntity.flags and (idImage + " Dire") in ENTITY_IMAGE_DICT : entityImage = ENTITY_IMAGE_DICT[idImage + " Dire"]
									else : entityImage = ENTITY_IMAGE_DICT[idImage]
							
					# Draw Entity #
					if entityImage != None:
						entityXLoc = roomEntity.rectArea[0] - ((roomEntity.imageSize[0] - roomEntity.rectArea.width) / 2) - self.rectPlayerArea.left
						entityYLoc = roomEntity.rectArea.bottom - roomEntity.imageSize[1]
						self.surfaceGroupEntities.blit(entityImage, [entityXLoc, entityYLoc])
						#pygame.draw.rect(self.surfaceGroupEntities, [20, 20, 70], [roomEntity.rectArea[0] - self.rectPlayerArea.left, roomEntity.rectArea[1], roomEntity.rectArea.width, roomEntity.rectArea.height])
						
						# Overlap Check #
						if roomEntity.rectArea.bottom - roomEntity.imageSize[1] < self.rectBottom.top:
							self.bottomItemOverlapCheck[1] = True
					
	def draw(self, DRAW_DATA_DICT, WINDOW, MOUSE, DATA_PLAYER, PLAYER_PLANET_DICT, PLAYER_ROOM, PLAYER_TARGET_LIST, DRAW_TV_BORDER, BACKGROUND_IMAGE_DICT, INTERFACE_IMAGE_DICT, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT):
		
		# Get Data #
		if True:
			oldRoom = self.displayRoom
			self.displayRoom = PLAYER_ROOM
			
			# Update Mouse (After Room) #
			clearMouseHoverTargets = True
			if "Don't Clear Mouse Hover Targets" in DRAW_DATA_DICT : clearMouseHoverTargets = False
			MOUSE.update(WINDOW, DATA_PLAYER, [self], clearMouseHoverTargets)
			
			if self.displayRoom != oldRoom:
				self.updateEntitySurface(DATA_PLAYER, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT)
				self.updateGroupEntitySurface(DATA_PLAYER, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT)
				
			# Get Time Data #
			dayRatio = None
			totalDaylightMinutes = None
			currentDaylightMinute = None
			if PLAYER_PLANET_DICT not in [{}, None]:
				if PLAYER_PLANET_DICT["Minutes In Day"] < PLAYER_PLANET_DICT["Dawn Minutes"] : self.displayRoomTimeOfDay = "Night"
				elif PLAYER_PLANET_DICT["Minutes In Day"] < PLAYER_PLANET_DICT["Sunrise Minutes"] : self.displayRoomTimeOfDay = "Dawn"
				elif PLAYER_PLANET_DICT["Minutes In Day"] < PLAYER_PLANET_DICT["Dusk Minutes"] : self.displayRoomTimeOfDay = "Day"
				elif PLAYER_PLANET_DICT["Minutes In Day"] < PLAYER_PLANET_DICT["Sunset Minutes"] : self.displayRoomTimeOfDay = "Dawn"
				else : self.displayRoomTimeOfDay = "Night"
				
				if self.displayRoomTimeOfDay != "Night":
					totalDaylightMinutes = PLAYER_PLANET_DICT["Sunset Minutes"] - PLAYER_PLANET_DICT["Dawn Minutes"]
					currentDaylightMinutes = PLAYER_PLANET_DICT["Minutes In Day"] - PLAYER_PLANET_DICT["Dawn Minutes"]
					dayRatio = currentDaylightMinutes / (totalDaylightMinutes + 0.0)
				
			drawTopImageCheck = False
			drawBottomImageCheck = False
			mobActionBoxList = []
			
			# Get Bottom Background Image #
			imageBackgroundBottom = None
			if self.displayRoom.inside == False and self.displayRoomTimeOfDay != None:
				backgroundImageID = "Ground " + self.displayRoom.floorType + " " + self.displayRoomTimeOfDay
				if backgroundImageID in BACKGROUND_IMAGE_DICT:
					imageBackgroundBottom = BACKGROUND_IMAGE_DICT[backgroundImageID]
			else:
				backgroundImageID = "Ground " + self.displayRoom.floorType + " Day"
				if backgroundImageID in BACKGROUND_IMAGE_DICT:
					imageBackgroundBottom = BACKGROUND_IMAGE_DICT[backgroundImageID]
		
			# Clear Previous Animations & Update Action Bars #
			if oldRoom != self.displayRoom:
				for tempMob in self.displayRoom.mobList:
					tempMob.animationDict = {}
					if tempMob.currentAction != None and tempMob.currentAction["Type"] == "Attacking":
						tempMob.currentAction["Action Bar Timer"] = tempMob.currentAction["Attack Data"].attackTimer - tempMob.currentAction["Timer"]
				
		# Draw Background Top/Bottom/Dirty Rects #
		if True:
			
			# Draw Background Top - Sky/Wall #
			if "All" in DRAW_DATA_DICT["Draw List"] or "Background Top" in DRAW_DATA_DICT["Draw List"] or oldRoom == None or oldRoom.inside != self.displayRoom.inside:
				
				# Outside - Sky #
				if self.displayRoom.inside == False and self.displayRoomTimeOfDay != None:
					
					# Draw To Screen #
					roomTopImage = BACKGROUND_IMAGE_DICT["Sky " + self.displayRoomTimeOfDay]
					WINDOW.blit(roomTopImage, [self.rectTop.left, self.rectTop.top])
					drawTopImageCheck = True
					
					# Draw Sun #
					if dayRatio != None:
						import math
						sunImage = BACKGROUND_IMAGE_DICT["Sun"]
						ratioX = ((currentDaylightMinutes + 0.0) / totalDaylightMinutes) * 180
						ratioY = ((currentDaylightMinutes + 0.0) / totalDaylightMinutes) * 360
						sunXLoc = int((self.rectTop.width / 2) - (sunImage.get_width() / 2) + (math.cos(math.radians(ratioX)) * 500))
						sunYLoc = int(sunImage.get_height() + ((math.cos(math.radians(ratioY)) * self.rectTop.bottom) / 1.7))
						WINDOW.blit(sunImage, [sunXLoc, sunYLoc], self.rectTop)
						
					# Draw Mountains #
					if True:
						mountainImage = BACKGROUND_IMAGE_DICT["Mountains " + self.displayRoomTimeOfDay]
						mountainYLoc = self.rectTop.bottom - mountainImage.get_height()
						WINDOW.blit(mountainImage, [self.rectTop.left, mountainYLoc])
					
					# Draw Forest #
					if True:
						treeImage = BACKGROUND_IMAGE_DICT["Trees " + self.displayRoomTimeOfDay]
						WINDOW.blit(treeImage, [self.rectTop.left, self.rectTop.bottom - treeImage.get_height()])
					
					# Draw Top Of Bottom Image #
					if imageBackgroundBottom != None and imageBackgroundBottom.get_height() > self.rectBottom.height:
						rectTopOfBottomImage = pygame.Rect([self.rectTop.left, self.rectTop.top, self.rect.width, (imageBackgroundBottom.get_height() - self.rectBottom.height)])
						WINDOW.blit(imageBackgroundBottom, [self.rectTop.left, self.rectTop.bottom - rectTopOfBottomImage.height], rectTopOfBottomImage)
						
				# Inside - Wall #
				elif self.displayRoom.inside == True:
					WINDOW.blit(BACKGROUND_IMAGE_DICT["Wall Metal"], [self.rectTop.left, self.rectTop.top])
					drawTopImageCheck = True
					
				# Top Of Entity Surface (Overlap) #
				if self.bottomItemOverlapCheck[0] == True:
					rectTopOfEntityImage = pygame.Rect([0, 0, self.rectEnemyArea.width, self.rectTop.height])
					WINDOW.blit(self.surfaceEnemyEntities, [self.rectEnemyArea.left, self.rectTop.top], rectTopOfEntityImage)
					
				if self.bottomItemOverlapCheck[1] == True:
					rectTopOfGroupEntityImage = pygame.Rect([0, 0, self.rectPlayerArea.width, self.rectTop.height])
					WINDOW.blit(self.surfaceGroupEntities, [self.rectPlayerArea.left, self.rectTop.top], rectTopOfGroupEntityImage)
					
			# Draw Background Bottom - Ground #
			if "All" in DRAW_DATA_DICT["Draw List"] or "Background Bottom" in DRAW_DATA_DICT["Draw List"] or oldRoom == None or oldRoom.floorType != self.displayRoom.floorType:
				
				# Draw Only Bottom If Inside And Bottom Image Has Top Parts #
				if self.displayRoom.inside == True and imageBackgroundBottom.get_height() > self.rectBottom.height:
					rectBottomOfBottomImage = pygame.Rect([self.rectBottom.left, (imageBackgroundBottom.get_height() - self.rectBottom.height), self.rect.width, self.rectBottom.height])
					WINDOW.blit(imageBackgroundBottom, [self.rectBottom.left, self.rectBottom.top], rectBottomOfBottomImage)
				
				# Draw Entire Bottom If Image Has No Top Parts #
				else : WINDOW.blit(imageBackgroundBottom, [self.rectBottom.left, self.rect.bottom - imageBackgroundBottom.get_height()])
				drawBottomImageCheck = True

			# Debug - Draw Area Polygons #
			if self.displayDebugArea != False:
				if self.displayDebugArea in ["Enemy", "All"] : pygame.draw.rect(WINDOW, [120, 0, 0], self.rectEnemyArea)
				if self.displayDebugArea in ["Player", "All"] : pygame.draw.rect(WINDOW, [0, 0, 120], self.rectPlayerArea)
				
		# Draw Enemy Entities & Items, Group Entities & Item Surfaces #
		if drawBottomImageCheck:
			WINDOW.blit(self.surfaceEnemyEntities, [self.rect.left, self.rect.top])
			WINDOW.blit(self.surfaceGroupEntities, [self.rectPlayerArea.left, self.rect.top])
			
		# Draw Entity Window Animations/Action Box Checks #
		for roomEntity in self.displayRoom.mobList + [DATA_PLAYER]:
			
			# Draw Damage Numbers #
			if "Damage Number List" in roomEntity.animationDict:
				numberXLoc = roomEntity.rectArea.left + (roomEntity.rectArea.width / 2)
				for damageNumberDict in roomEntity.animationDict["Damage Number List"]:
					numberYLoc = roomEntity.rectArea.bottom - INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_height() + damageNumberDict["Draw Y Loc"] + 4
					WINDOW.blit(damageNumberDict["Number Image"], [numberXLoc - (damageNumberDict["Number Image"].get_width() / 2), numberYLoc])
					
			# Mob Preparing Attack Check #
			if roomEntity.objectType == "Mob" and roomEntity.currentAction != None and roomEntity.currentAction["Type"] == "Attacking":
				mobActionBoxList.append(roomEntity)

			# Hover Check #
			if MOUSE.hoverElement == roomEntity and roomEntity.objectType == "Mob" and roomEntity not in mobActionBoxList:
				mobActionBoxList.append(roomEntity)
		
		# Draw Room Mob Action Message Boxes #
		if len(mobActionBoxList) > 0 and INTERFACE_IMAGE_DICT != None:
			for roomMob in mobActionBoxList:
				
				# Draw Action Message Box #
				boxWidth = INTERFACE_IMAGE_DICT["Action Box"].get_width()
				boxXLoc = roomMob.rectArea.left + (roomMob.rectArea.width / 2) - (boxWidth / 2)
				boxYLoc = roomMob.rectArea[1] - 25
				
				# Box Loc Checks #
				if True:
					if roomMob.objectType == "Player" or roomMob in DATA_PLAYER.groupList:
						if boxXLoc < self.rectPlayerArea.left : boxXLoc = self.rectPlayerArea.left
						elif boxXLoc + boxWidth > self.rectPlayerArea.right : boxXLoc = self.rectPlayerArea.right - boxWidth
					
					elif roomMob.objectType == "Mob":
						if boxXLoc < self.rectEnemyArea.left : boxXLoc = self.rectEnemyArea.left
						elif boxXLoc + boxWidth > self.rectEnemyArea.right : boxXLoc = self.rectEnemyArea.right - boxWidth
				
				WINDOW.blit(INTERFACE_IMAGE_DICT["Action Box"], [boxXLoc, boxYLoc])
				
				# HP / MP Bars #
				hpPercent = roomMob.currentHP / (roomMob.maxHP + 0.0)
				hpBarWidth = int((boxWidth - 5) * hpPercent)
				pygame.draw.line(WINDOW, [200, 50, 50], [boxXLoc + 4, boxYLoc + 5], [boxXLoc + hpBarWidth, boxYLoc + 5], 4)
				
				mpPercent = roomMob.currentMP / (roomMob.maxMP + 0.0)
				mpBarWidth = int((boxWidth - 5) * mpPercent)
				pygame.draw.line(WINDOW, [50, 50, 200], [boxXLoc + 4, boxYLoc + 10], [boxXLoc + mpBarWidth, boxYLoc + 10], 4)
				
				# Draw Action Bar #
				if roomMob.currentAction != None and roomMob.currentAction["Type"] == "Attacking":
					actionBarPercent = (roomMob.currentAction["Action Bar Timer"]) / (roomMob.currentAction["Attack Data"].attackTimer + 0.0)
					actionBarWidth = int((boxWidth - 5) * actionBarPercent)
					pygame.draw.line(WINDOW, [200, 200, 200], [boxXLoc + 4, boxYLoc + 14], [boxXLoc + actionBarWidth, boxYLoc + 14], 2)
		
		# Draw Item Message Box #
		if MOUSE.hoverElement != None and type(MOUSE.hoverElement) not in [dict] and MOUSE.hoverElement.objectType == "Item":
		
			# Draw Item Message Box #
			targetItem = MOUSE.hoverElement
			boxWidth = INTERFACE_IMAGE_DICT["Item Box"].get_width()
			boxXLoc = targetItem.rectArea.left + (targetItem.rectArea.width / 2) - (boxWidth / 2)
			boxYLoc = targetItem.rectArea[1] - 25
			
			# Box Loc Checks #
			if True:
				if targetItem.dropSide == "Player":
					if boxXLoc < self.rectPlayerArea.left : boxXLoc = self.rectPlayerArea.left
					elif boxXLoc + boxWidth > self.rectPlayerArea.right : boxXLoc = self.rectPlayerArea.right - boxWidth
				
				elif targetItem.dropSide == "Mob":
					if boxXLoc < self.rectEnemyArea.left : boxXLoc = self.rectEnemyArea.left
					elif boxXLoc + boxWidth > self.rectEnemyArea.right : boxXLoc = self.rectEnemyArea.right - boxWidth
			
			WINDOW.blit(INTERFACE_IMAGE_DICT["Item Box"], [boxXLoc, boxYLoc])
			
			# Title #
			itemNameString = targetItem.defaultTitle
			if len(itemNameString) > 14 : itemNameString = itemNameString[0:14] + ".."
			titleWidth = Config.FONT_ROMAN_12.size(itemNameString)[0]
			titleXOffset = (boxWidth - titleWidth) / 2
			Utility.writeFast(itemNameString, [boxXLoc + titleXOffset, boxYLoc + 3], [200, 200, 200], Config.FONT_ROMAN_12, WINDOW)
			
		# Display To Screen #
		if True:
			if "All" in DRAW_DATA_DICT["Draw List"] or (drawTopImageCheck == True and drawBottomImageCheck == True):
				if self.rect not in Config.DISPLAY_RECT_LIST:
					Config.DISPLAY_RECT_LIST.append(self.rect)
			elif drawTopImageCheck == True and drawBottomImageCheck == False:
				if self.rectTop not in Config.DISPLAY_RECT_LIST:
					Config.DISPLAY_RECT_LIST.append(self.rectTop)
			elif drawTopImageCheck == False and drawBottomImageCheck == True:
				if self.rectBottom not in Config.DISPLAY_RECT_LIST:
					Config.DISPLAY_RECT_LIST.append(self.rectBottom)
			