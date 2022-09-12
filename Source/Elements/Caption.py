import pygame, Utility
from pygame import *

class LoadCaption:

	def __init__(self, WORD_INDEX, WORD_COUNT, CAPTION_TYPE="", FLAGS={}):
	
		self.objectType = "Caption"
		self.captionType = CAPTION_TYPE
		self.wordIndex = WORD_INDEX
		self.wordCount = WORD_COUNT
		self.strLabel = ""
		self.x = 0
		self.y = 0
		self.splitCaption = None
		self.splitCaptionType = None
		self.flags = FLAGS
	
		# Surfaces #
		SIZE = [300, 150]
		self.rect = pygame.rect.Rect([100, 100], SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill([20, 20, 100])
		
	def draw(self, SCREEN, MOUSE):
	
		if self.captionType == "Get Item":
			pass
			#SCREEN.blit(self.surfaceDefault, [displayX, displayY])
			