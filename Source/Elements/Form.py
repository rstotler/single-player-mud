import pygame, os, Config, Utility, random
from pygame import *

class LoadForm:

	def __init__(self, ID, LOCATION, INTERFACE_IMAGE_DICT, FLAGS={}):
		
		self.id = ID
		self.objectType = "Form"
		self.collideShape = "Rectangle"
		self.flags = FLAGS
		
		# Form Variables #
		self.tick = -1
		self.charMax = 10 # Default Size
		self.userInput = ""
		self.userInputTemp = ""
		self.userInputList = []
		self.userInputListIndex = -1
		
		# Font #
		self.font = Config.FONT_ROMAN_16
		self.oneCharSize = self.font.size(" ")
		
		# Size #
		if "Max Width" in FLAGS and isinstance(FLAGS["Max Width"], int) : self.charMax = FLAGS["Max Width"]
		elif "Max Width" in FLAGS and FLAGS["Max Width"] == "Screen" : self.charMax = (Config.SCREEN_SIZE[0] / self.oneCharSize[0]) - 1
		widthBuffer = 0
		heightBuffer = 0
		if "Width Buffer" in FLAGS : widthBuffer = FLAGS["Width Buffer"]
		if "Height Buffer" in FLAGS : heightBuffer = FLAGS["Height Buffer"]
		SIZE = [(self.oneCharSize[0] * (self.charMax + 1)) + widthBuffer, self.oneCharSize[1] + (heightBuffer * 2)]
		
		# Location Mods #
		if LOCATION[0] == "Right" : LOCATION[0] = Config.SCREEN_SIZE[0] - SIZE[0]
		if LOCATION[1] == "Bottom" : LOCATION[1] = Config.SCREEN_SIZE[1] - SIZE[1]
		
		# Rect & Surface #
		self.bgColor = [10, 10, 40]
		self.rect = pygame.Rect(LOCATION, SIZE)
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill(self.bgColor)
		self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["Border Form"], [0, 0])
		
	def update(self, KEYBOARD):
	
		# Get Data #
		self.tick += 1
		underscoreCheck = False
		backspaceCheck = False
		
		# Update Data #
		if self.tick >= 120:
			self.tick = 0
			
		if self.tick in [0, 60]:
			underscoreCheck = True
			
		if len(self.userInput) > 0 and KEYBOARD.backspace and KEYBOARD.backspaceTick == 0:
			backspaceCheck = self.userInput[-1]
			self.userInput = self.userInput[0:-1]
			
		# Draw Dirty Rect #
		if underscoreCheck or backspaceCheck:
			Config.DRAW_SCREEN_DICT["frmMain"] = True
			
	def getInput(self, KEYBOARD, KEY):
	
		inputKey = KEYBOARD.isValidInputKey(KEY)
		if inputKey != -1:
			self.userInput = self.userInput + inputKey
			Config.DRAW_SCREEN_DICT["frmMain"] = True
			
	def processInput(self):
	
		if len(self.userInput) > 1:
			self.userInputList.append(self.userInput)
		self.userInput = ""
		self.userInputTemp = ""
		self.userInputListIndex = -1
		
		Config.DRAW_SCREEN_DICT["frmMain"] = True
		
	def scrollUserInputList(self, DIR):
	
		dirCheck = False
		if DIR == "up" and self.userInputListIndex < len(self.userInputList)-1:
			self.userInputListIndex += 1
			dirCheck = True
		elif DIR == "down" and self.userInputListIndex > -1:
			self.userInputListIndex -= 1
			dirCheck = True
			
		if dirCheck:
			if self.userInputListIndex != -1:
				if DIR == "up" and self.userInputListIndex == 0:
					self.userInputTemp = self.userInput
				self.userInput = self.userInputList[len(self.userInputList)-self.userInputListIndex-1]
			elif self.userInputListIndex == -1:
				self.userInput = self.userInputTemp
				self.userInputTemp = ""
				
		Config.DRAW_SCREEN_DICT["frmMain"] = True
			
	def draw(self, WINDOW, MOUSE):
	
		# Background #
		WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
			
		# User Input String #
		strUserInput = self.userInput
		if len(strUserInput) > self.charMax : strUserInput = self.userInput[-self.charMax:]
		if self.tick < 60 : strUserInput = strUserInput + "_"
		if strUserInput != "":
			widthBuffer = 0
			heightBuffer = 0
			if "Width Buffer" in self.flags : widthBuffer = self.flags["Width Buffer"]
			if "Height Buffer" in self.flags : heightBuffer = self.flags["Height Buffer"]
			xLoc = self.rect.left + (widthBuffer / 2)
			Utility.writeFast(strUserInput, [xLoc, self.rect.top + heightBuffer], [100, 100, 200], self.font, WINDOW)
			
		if self.rect not in Config.DISPLAY_RECT_LIST:
			Config.DISPLAY_RECT_LIST.append(self.rect)
			