import pygame, Config, Utility
from pygame import *

class LoadSidescreenPlayerUtilityBar:

	def __init__(self, DISPLAY_LOC, SIZE, INTERFACE_IMAGE_DICT):
	
		self.id = "Player Utility Bar"
		self.objectType = "Sidescreen"
		
		# Rect & Surface #
		self.rect = pygame.Rect(DISPLAY_LOC + SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill([10, 10, 40])
		self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["Player Utility Bar"], [0, 0])
		
	def draw(self, WINDOW, MOUSE, INTERFACE_IMAGE_DICT):
	
		WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
		
		if MOUSE.hoverElement != None and type(MOUSE.hoverElement) == dict and MOUSE.hoverElement["Type"] == "Player Utility Bar Button":
			Utility.outline(WINDOW, [200, 200, 200], [self.rect.left + 3 + (26 * MOUSE.hoverElement["Button X Loc"]), self.rect.top + 3], [23, 23], 2)
		
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
		