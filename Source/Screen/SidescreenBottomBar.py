import pygame, Config
from pygame import *

class LoadSidescreenBottomBar:

	def __init__(self, SIZE):
	
		self.id = "Bottom Bar"
		self.objectType = "Sidescreen"
	
		# Rect & Surface #
		self.displayLoc = [0, Config.SCREEN_SIZE[1] - SIZE[1]]
		self.rect = pygame.Rect(self.displayLoc + SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill([10, 30, 10])
		
	def moveMouse(self, MOUSE):
	
		pass
		
	def draw(self, SCREEN, MOUSE):
		
		SCREEN.blit(self.surfaceDefault, self.displayLoc)
		
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
		