import pygame, Config, Utility, ScreenGame
from Data import DataWorld
from pygame import *

class LoadSidescreenPlayerStats:

	def __init__(self, DISPLAY_LOC, SIZE, INTERFACE_IMAGE_DICT):
	
		self.id = "Player Stats"
		self.objectType = "Sidescreen"
	
		# Rect & Surface #
		self.rect = pygame.Rect(DISPLAY_LOC + SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill([70, 20, 70])
		self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["Border Player Stats"], [0, 0])
		
	def moveMouse(self, MOUSE):
	
		pass
		
	def draw(self, WINDOW, DATA_PLAYER):
		
		WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
		ScreenGame.drawEntityStatBars(WINDOW, DATA_PLAYER, [self.rect.left + 12, self.rect.top + 23])
		
		# Group Member Stats #
		if len(DATA_PLAYER.groupList) > 0:
			groupXLoc = 0
			for groupMob in DATA_PLAYER.groupList:
				ScreenGame.drawEntityStatBars(WINDOW, groupMob, [self.rect.left + 12 + groupXLoc, self.rect.top + 73], 47)
				groupXLoc += 94
		
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
		