import pygame, Utility, Config
from pygame import *

class LoadButton:

	def __init__(self, ID, LOCATION, SIZE, FLAGS={}):
	
		self.objectType = "Button"
		self.collideShape = "Rectangle"
		self.id = ID
		self.flags = FLAGS
		
		# Location Offset #
		if LOCATION[0] == "Center":
			LOCATION[0] = (Config.SCREEN_SIZE[0] / 2) - (SIZE[0] / 2)
		if LOCATION[1] == "Center":
			LOCATION[1] = (Config.SCREEN_SIZE[1] / 2) - (SIZE[1] / 2)
		
		# Surfaces #
		self.rect = pygame.rect.Rect(LOCATION, SIZE)
		self.surfaceDefault = None
		if "Default Color" in FLAGS:
			self.surfaceDefault = pygame.Surface(SIZE)
			self.surfaceDefault.fill(FLAGS["Default Color"])
		self.surfaceHover = None
		if "Hover Color" in FLAGS:
			self.surfaceHover = pygame.Surface(SIZE)
			self.surfaceHover.fill(FLAGS["Hover Color"])
		self.surfaceClick = None
		if "Click Color" in FLAGS:
			self.surfaceClick = pygame.Surface(SIZE)
			self.surfaceClick.fill(FLAGS["Click Color"])
		
	def update(self):
	
		pass
		
	def draw(self, SCREEN, MOUSE):
	
		displaySurface = None
		if self.surfaceDefault != None : displaySurface = self.surfaceDefault
		if self.surfaceClick != None and self == MOUSE.hoverElement and MOUSE.clickLeft and self == MOUSE.leftClickElement : displaySurface = self.surfaceClick
		elif self.surfaceHover != None and self == MOUSE.hoverElement : displaySurface = self.surfaceHover
		if displaySurface != None:
			SCREEN.blit(displaySurface, [self.rect.left, self.rect.top])
			
		# Font Size #
		targetFont = Config.FONT_M
		if "Font" in self.flags : targetFont = self.flags["Font"]
			
		if "Label" in self.flags:
			fontColor = [100, 100, 200]
			if "Font Default Color" in self.flags : fontColor = self.flags["Font Default Color"]
			if "Font Click Color" in self.flags and self == MOUSE.hoverElement and MOUSE.clickLeft and self == MOUSE.leftClickElement : fontColor = self.flags["Font Click Color"]
			elif "Font Hover Color" in self.flags and self == MOUSE.hoverElement : fontColor = self.flags["Font Hover Color"]
			
			xOffset = self.rect.left
			yOffset = self.rect.top
			if "Label X Offset" in self.flags:
				if self.flags["Label X Offset"] == "Center" : xOffset += ((self.rect.width/2) - (targetFont.size(self.flags["Label"])[0]/2))
				else : xOffset += self.flags["Label X Offset"]
			if "Label Y Offset" in self.flags : yOffset += self.flags["Label Y Offset"]
			
			if isinstance(fontColor, str):
				Utility.writeColor(self.flags["Label"], fontColor, Config.COLOR_DICT, [xOffset, yOffset], targetFont, SCREEN)
			else:
				if isinstance(fontColor, str) : fontColor = [100, 100, 200]
				Utility.writeFast(self.flags["Label"], [xOffset, yOffset], fontColor, targetFont, SCREEN)
			