import pygame, os, Config, Utility
from Data import DataPlayer
from pygame import *

class LoadSidescreenTargetStats:

	def __init__(self, Y_LOC, SIZE, INTERFACE_IMAGE_DICT):
	
		self.id = "Target Stats"
		self.objectType = "Sidescreen"
	
		# Rect & Surface #
		self.rect = pygame.Rect([0, Y_LOC] + SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill([10, 10, 40])
		self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["Border Target Stats"], [0, 0])
		
	def moveMouse(self, MOUSE):
	
		pass
		
	def draw(self, WINDOW, MOUSE, DATA_PLAYER, TARGET_ENTITY, INTERFACE_IMAGE_DICT, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT):

		WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
		
		# Get Data #
		if True:
			targetEntityImage = None
			stringDisplayTitle = None
			stringTargetWeight = None
			
			if TARGET_ENTITY != None:
				if TARGET_ENTITY.objectType == "Player":
					stringDisplayTitle = "Player"
					if ENTITY_IMAGE_DICT != None and "Player" in ENTITY_IMAGE_DICT : targetEntityImage = ENTITY_IMAGE_DICT["Player"]
				
				elif TARGET_ENTITY.objectType == "Mob":
					stringDisplayTitle = TARGET_ENTITY.defaultTitle
					if ENTITY_IMAGE_DICT != None and TARGET_ENTITY.idImage in ENTITY_IMAGE_DICT : targetEntityImage = ENTITY_IMAGE_DICT[TARGET_ENTITY.idImage]
				
				elif TARGET_ENTITY.objectType == "Item":
					stringDisplayTitle = TARGET_ENTITY.defaultTitle
					stringTargetWeight = str(TARGET_ENTITY.getWeight())
					
					# Image Data #
					if stringDisplayTitle != None and ITEM_IMAGE_DICT != None:
						itemImageID = TARGET_ENTITY.idImage
						if TARGET_ENTITY.type == "Container" and TARGET_ENTITY.idImage == "Chest":
							if "Container Status" not in TARGET_ENTITY.flags : itemImageID = itemImageID + " Open"
							elif TARGET_ENTITY.flags["Container Status"] in ["Closed", "Locked"] : itemImageID = itemImageID + " Closed"
							else : itemImageID = itemImageID + " Open"
						if itemImageID in ITEM_IMAGE_DICT : targetEntityImage = ITEM_IMAGE_DICT[itemImageID]
					
		# Draw Image #
		if True:
			if TARGET_ENTITY != None and INTERFACE_IMAGE_DICT != None:
				WINDOW.blit(INTERFACE_IMAGE_DICT["Target Stats Entity Box"], [self.rect.left + 20, self.rect.top + 24])
			
			if targetEntityImage != None:
				imageXLoc = self.rect.left + 48 - (targetEntityImage.get_width() / 2)
				imageYLoc = self.rect.top + 52 - (targetEntityImage.get_height() / 2)
				entityImageSize = targetEntityImage.get_size()
				targetSizeIndex = -1
				
				# Reduce Size Of Large Images #
				if entityImageSize[0] > 46 : targetSizeIndex = 0
				if entityImageSize[1] > 46 and entityImageSize[1] > entityImageSize[0] : targetSizeIndex = 1
				if targetSizeIndex != -1:
					imageSizeMod = 1 - ((entityImageSize[targetSizeIndex] - 46) / (entityImageSize[targetSizeIndex] + 0.0))
					targetEntityImage = pygame.transform.scale(targetEntityImage, [int(entityImageSize[0] * imageSizeMod), int(entityImageSize[1] * imageSizeMod)])
					imageXLocMod = ((self.rect.left + 20 + 56) - (self.rect.left + 20 + int(entityImageSize[0] * imageSizeMod))) / 2
					imageYLocMod = ((self.rect.top + 24 + 56) - (self.rect.top + 24 + int(entityImageSize[1] * imageSizeMod))) / 2
					imageXLoc = self.rect.left + 20 + imageXLocMod
					imageYLoc = self.rect.top + 24 + imageYLocMod
				
				WINDOW.blit(targetEntityImage, [imageXLoc, imageYLoc])
			
		# Write Data #
		if True:
			if TARGET_ENTITY != None:
				stringTitle = TARGET_ENTITY.objectType.upper() + " STATS"
				stringTitleWidth = Config.FONT_ROMAN_11.size(stringTitle)[0]
				Utility.writeFast(stringTitle, [self.rect.right - 12 - stringTitleWidth, self.rect.top + 12], [28, 28, 84], Config.FONT_ROMAN_11, WINDOW)
			
			writeYLoc = self.rect.top + 25
			if stringDisplayTitle != None:
				Utility.writeFast(stringDisplayTitle, [self.rect.left + 89, writeYLoc], [200, 200, 200], Config.FONT_ROMAN_12, WINDOW)
				writeYLoc += 12
			if TARGET_ENTITY != None and "Quantity" in TARGET_ENTITY.flags:
				Utility.writeFast("Quantity: " + str(TARGET_ENTITY.flags["Quantity"]), [self.rect.left + 89, writeYLoc], [200, 200, 200], Config.FONT_ROMAN_12, WINDOW)
				writeYLoc += 12
			if stringTargetWeight != None:
				Utility.writeFast("Weight: " + stringTargetWeight + " kg", [self.rect.left + 89, writeYLoc], [200, 200, 200], Config.FONT_ROMAN_12, WINDOW)
				writeYLoc += 12
				
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
		