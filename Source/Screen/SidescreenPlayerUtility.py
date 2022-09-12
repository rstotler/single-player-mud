import pygame, Config, Utility
from Data import DataWorld
from pygame import *

class LoadSidescreenPlayerUtility:

	def __init__(self, DISPLAY_LOC, SIZE):
	
		self.id = "Player Utility"
		self.objectType = "Sidescreen"
		self.displayItemList = None
		self.scrollPage = 0
		self.displayLevel = "Inventory"
	
		# Rect & Surface #
		self.rect = pygame.Rect(DISPLAY_LOC + SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill([20, 60, 10])
		
	def moveMouse(self, MOUSE):
	
		pass
		
	def moveMouseWheel(self, TARGET_BUTTON, WINDOW, MOUSE, DATA_PLAYER):
	
		scrollCheck = False
		if TARGET_BUTTON == 4 and self.scrollPage > 0:
			self.scrollPage -= 1
			scrollCheck = True
		elif TARGET_BUTTON == 5:
			self.scrollPage += 1
			scrollCheck = True
		
		if scrollCheck == True:
			MOUSE.update(WINDOW, DATA_PLAYER, [self])
			Config.DRAW_SCREEN_DICT["Target Stats"] = True
			Config.DRAW_SCREEN_DICT["Player Utility"] = True
			
	def updateScreen(self, TARGET_SCREEN_INDEX):
		
		if TARGET_SCREEN_INDEX == 0:
			self.displayLevel = "Inventory"
			
		elif TARGET_SCREEN_INDEX == 2:
			self.displayLevel = "Stats"
			
		Config.DRAW_SCREEN_DICT["Player Utility"] = True
			
	def updateDisplayItemList(self, TARGET_ITEM, UPDATE_TYPE):
	
		# Get Data #
		if True:
			if self.displayItemList == None : self.displayItemList = []
		
			itemInListIndex = False
			listQuantity = -1
			if len(self.displayItemList) > 0:
				for iNum, tempItem in enumerate(self.displayItemList):
					if TARGET_ITEM.idNum == tempItem.idNum:
						itemInListIndex = iNum
						if "Quantity" in tempItem.flags : listQuantity = tempItem.flags["Quantity"]
						break
	
		# Add Item #
		if UPDATE_TYPE == "Add":
			if "Quantity" not in TARGET_ITEM.flags or itemInListIndex == False:
				self.displayItemList.append(TARGET_ITEM)
				
		# Remove Item #
		elif UPDATE_TYPE == "Remove":
			if "Quantity" not in TARGET_ITEM.flags or (itemInListIndex != False and TARGET_ITEM.flags["Quantity"] == listQuantity):
				del self.displayItemList[itemInListIndex]
		
	def draw(self, WINDOW, MOUSE, DATA_PLAYER, INTERFACE_IMAGE_DICT):
	
		if self.displayLevel == "Inventory":
			self.drawInventory(WINDOW, MOUSE, DATA_PLAYER, INTERFACE_IMAGE_DICT)
			
		elif self.displayLevel == "Stats":
			self.drawStats(WINDOW, MOUSE, DATA_PLAYER, INTERFACE_IMAGE_DICT)
			
		# Update Screen Data #
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
	
	def drawInventory(self, WINDOW, MOUSE, DATA_PLAYER, INTERFACE_IMAGE_DICT):
	
		# Get Display Item List #
		if self.displayItemList == None:
			self.displayItemList = []
			for playerItem in DATA_PLAYER.inventoryList:
				self.displayItemList.append(playerItem)
		
		# Draw #
		if True:
			
			# Background & Hover Icon #
			WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
			WINDOW.blit(INTERFACE_IMAGE_DICT["Border Inventory"], [self.rect.left, self.rect.top])
			if type(MOUSE.hoverElement) == dict and MOUSE.hoverElement["Type"] == "Inventory Button":
				hoverSlotNum = (MOUSE.hoverElement["Button Y Loc"] * 6) + (MOUSE.hoverElement["Button X Loc"] + 1) + (6 * self.scrollPage)
				if self.displayItemList != None and hoverSlotNum <= len(self.displayItemList):
					buttonXLoc = self.rect.left + 26 + (MOUSE.hoverElement["Button X Loc"] * 38)
					buttonYLoc = self.rect.top + 26 + (MOUSE.hoverElement["Button Y Loc"] * 41)
					WINDOW.blit(INTERFACE_IMAGE_DICT["Inventory Icon Item Hover"], [buttonXLoc, buttonYLoc])
			
			# Inventory Item Icons #
			listStartIndex = (self.scrollPage * 6)
			if self.displayItemList != None and listStartIndex < len(self.displayItemList):
				currentXLoc = 26
				currentYLoc = 26
				
				for displayItem in self.displayItemList[listStartIndex:listStartIndex + 36]:
					if ("Inventory Icon " + str(displayItem.idIcon)) in INTERFACE_IMAGE_DICT : targetIconImage = INTERFACE_IMAGE_DICT["Inventory Icon " + displayItem.idIcon]
					else : targetIconImage = INTERFACE_IMAGE_DICT["Inventory Icon Default"]
					WINDOW.blit(targetIconImage, [self.rect.left + currentXLoc, self.rect.top + currentYLoc])
					
					currentXLoc += 38
					if currentXLoc > 216:
						currentXLoc = 26
						currentYLoc += 41
							
			# Write Weight Data #
			stringWeight = str(DATA_PLAYER.currentWeight) + "/" + str(DATA_PLAYER.maxWeight) + " kg"
			stringWeightWidth = Config.FONT_ROMAN_12.size(stringWeight)[0]
			Utility.writeFast(stringWeight, [self.rect.right - 50 - stringWeightWidth, self.rect.bottom - 21], [42, 113, 24], Config.FONT_ROMAN_12, WINDOW)
			
	def drawStats(self, WINDOW, MOUSE, DATA_PLAYER, INTERFACE_IMAGE_DICT):
		
		WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
		WINDOW.blit(INTERFACE_IMAGE_DICT["Border Player"], [self.rect.left, self.rect.top])
		