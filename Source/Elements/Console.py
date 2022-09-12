import pygame, os, copy, Config, Utility, Caption
from pygame import *

class LoadConsole:

	def __init__(self, ID, LOCATION, CHAR_MAX, INTERFACE_IMAGE_DICT, FLAGS={}):
	
		self.objectType = "Console"
		self.collideShape = "Rectangle"
		self.id = ID
		self.flags = FLAGS
		
		self.font = Config.FONT_ROMAN_18
		self.charSize = self.font.size(" ")
		self.displayPage = 0
		self.displayLineList = []
		
		# Size #
		if CHAR_MAX[0] == "Screen" : CHAR_MAX[0] = (Config.SCREEN_SIZE[0] / self.charSize[0]) - 1
		if CHAR_MAX[1] == "Screen" : CHAR_MAX[1] = (Config.SCREEN_SIZE[1] / self.charSize[1])
		self.charMax = CHAR_MAX
		
		consoleWidthBuffer = 0
		lineHeightBuffer = 0
		if "Console Width Buffer" in FLAGS : consoleWidthBuffer = FLAGS["Console Width Buffer"]
		if "Line Height Buffer" in FLAGS : lineHeightBuffer = FLAGS["Line Height Buffer"]
		SIZE = [(self.charSize[0] * self.charMax[0]) + (consoleWidthBuffer * 2), ((self.charSize[1] + (lineHeightBuffer * 2)) * self.charMax[1])]
		
		# Rect & Surfaces #
		self.bgColor = [30, 10, 10]
		self.rect = pygame.Rect(LOCATION, SIZE)
		self.rectDisplay = pygame.Rect([LOCATION[0]+4, LOCATION[1]+4, SIZE[0]-8, SIZE[1]-8])
		self.surfaceDefault = pygame.Surface(SIZE)
		self.surfaceDefault.fill(self.bgColor)
		self.surfaceDefault.blit(INTERFACE_IMAGE_DICT["Border Console"], [0, 0])
		self.surfaceHoverDict = {}
		for i in range(1, self.charMax[0]+1):
			self.surfaceHoverDict[i] = pygame.Surface([self.charSize[0] * i, self.charSize[1] + (lineHeightBuffer * 2)])
			self.surfaceHoverDict[i].fill([100, 100, 100])
		
	def update(self):
	
		pass
		
	def addDisplayLine(self, LABEL, COLOR_CODE=None, CAPTION_LIST=[], TRIM_CHECK=True):
			
		if self.displayPage != 0 : self.displayPage = 0
			
		# Trim Label #
		if TRIM_CHECK:
			LABEL = LABEL.strip()
			while '  ' in LABEL : LABEL = LABEL.replace('  ', ' ')
		if COLOR_CODE == None:
			COLOR_CODE = str(len(LABEL)) + "w"
	
		if len(LABEL) <= self.charMax[0]:
			for caption in CAPTION_LIST:
				caption.strLabel = ' '.join(LABEL.split()[caption.wordIndex:caption.wordIndex+caption.wordCount])
				xBufferMod = len(' '.join(LABEL.split()[0:caption.wordIndex]))
				if caption.wordIndex > 0 and len(LABEL.split()) > 1 : xBufferMod += 1
				consoleWidthBuffer = 0
				if "Console Width Buffer" in self.flags : consoleWidthBuffer = self.flags["Console Width Buffer"]
				caption.x = self.rect.left + consoleWidthBuffer + (xBufferMod * self.charSize[0])
			self.displayLineList.append(DisplayLine(LABEL, COLOR_CODE, CAPTION_LIST))
			
		else:
			nextLineCaption = None
			while(len(LABEL) > 0):
				if len(LABEL) <= self.charMax[0] : splitIndex = len(LABEL)
				elif ' ' not in LABEL[0:self.charMax[0]] : splitIndex = self.charMax[0]
				else : splitIndex = LABEL[0:self.charMax[0]].rfind(' ')
				
				# Split Line #
				line = LABEL[0:splitIndex]
				LABEL = LABEL[splitIndex::]
				spaceCheck = False
				if len(LABEL) > 0 and LABEL[0] == ' ':
					LABEL = LABEL[1::]
					spaceCheck = True
					
				# Split Caption List #
				captionList = []
				delList = []
				if nextLineCaption != None:
					CAPTION_LIST.insert(0, nextLineCaption)
					nextLineCaption = None
				for i, caption in enumerate(CAPTION_LIST):
					if caption.wordIndex in range(0, len(line.split())):
						
						# Split Next Line Caption #
						if (caption.wordIndex + caption.wordCount) > len(line.split()) and len(LABEL) > 0:
							nextWordCount = (caption.wordIndex + caption.wordCount) - len(line.split())
							nextLineCaption = Caption.LoadCaption(0, nextWordCount)
							nextLineCaption.splitCaption = Caption.LoadCaption(caption.wordIndex, len(line.split()) - caption.wordIndex)
							nextLineCaption.splitCaptionType = "Next Line"
							nextLineCaption.splitCaption.strLabel = ' '.join(line.split()[caption.wordIndex:len(line.split())])
							caption.splitCaption = Caption.LoadCaption(0, nextLineCaption.wordCount)
							caption.splitCaptionType = "Previous Line"
							caption.splitCaption.strLabel = ' '.join(LABEL.split()[0:caption.splitCaption.wordCount])
							if len(LABEL) > len(line):
								caption.splitCaption.charSize = ' '.join(LABEL.split()[0:nextLineCaption.wordCount])
								
						xBufferMod = len(' '.join(line.split()[0:caption.wordIndex]))
						if caption.wordIndex > 0 and caption.splitCaptionType != "Next Line" and len(line.split()) > 1 : xBufferMod += 1
						consoleWidthBuffer = 0
						if "Console Width Buffer" in self.flags : consoleWidthBuffer = self.flags["Console Width Buffer"]
						caption.x = self.rect.left + consoleWidthBuffer + (xBufferMod * self.charSize[0])
						caption.strLabel = ' '.join(line.split()[caption.wordIndex:caption.wordIndex+caption.wordCount])
						if caption.splitCaption != None:
							caption.splitCaption.x = self.rect.left + consoleWidthBuffer
							if caption.splitCaptionType == "Next Line":
								if len(self.displayLineList) > 0:
									strPreviousLine = self.displayLineList[-1].label
									previousLineSectionSize = len(' '.join(strPreviousLine.split()[0:caption.splitCaption.wordIndex]))
									if caption.splitCaption.wordIndex > 0 and len(strPreviousLine.split()) > 1 : previousLineSectionSize += 1
									caption.splitCaption.x += previousLineSectionSize * self.charSize[0]
								
						captionList.append(caption)
						delList.append(i)
					
					else:
						caption.wordIndex -= len(line.split())
						
				delList.reverse()
				for i in delList : del CAPTION_LIST[i]
				
				# Split Color Code #
				colorCount = 0
				totalColorCount = 0
				targetColor = ""
				lineColorCode = ""
				breakCheck = False
				
				for i, letter in enumerate(COLOR_CODE):
					if Utility.stringIsNumber(letter):
						if colorCount != 0 : colorCount *= 10
						colorCount += int(letter)
					else:
						targetColor = targetColor + letter
						
						# If last letter of COLOR_CODE or the next character is a Number #
						if i+1 == len(COLOR_CODE) or (len(COLOR_CODE) > i+1 and Utility.stringIsNumber(COLOR_CODE[i+1])):
							
							totalColorCount += colorCount
							if i+1 == len(COLOR_CODE) or totalColorCount >= self.charMax[0]:
								
								COLOR_CODE = COLOR_CODE[(i+1)::]
								breakCheck = True
								
								# Split Color Code #
								if totalColorCount > self.charMax[0]:
									colorCount -= (totalColorCount - len(line))
									COLOR_CODE = str(totalColorCount - len(line)) + targetColor + COLOR_CODE
									
								if spaceCheck:
									lastIndex = -1
									for ii, letter2 in enumerate(COLOR_CODE):
										if ii > 0 and not Utility.stringIsNumber(letter2):
											lastIndex = ii
											break
									if lastIndex != -1 and Utility.stringIsNumber(COLOR_CODE[0:lastIndex]):
										newNum = int(COLOR_CODE[0:lastIndex]) - 1
										COLOR_CODE = str(newNum) + COLOR_CODE[(lastIndex)::]
									
							lineColorCode = lineColorCode + str(colorCount) + targetColor
							colorCount = 0
							targetColor = ""
							if breakCheck : break
						
				self.displayLineList.append(DisplayLine(line, lineColorCode, captionList))
				
	def draw(self, WINDOW, MOUSE, DRAW_TYPE):
	
		lineHeightBuffer = 0
		if "Line Height Buffer" in self.flags:
			lineHeightBuffer = self.flags["Line Height Buffer"]
			
		WINDOW.blit(self.surfaceDefault, [self.rect.left, self.rect.top])
		
		if len(self.displayLineList) > 0:
			if MOUSE.hoverElement != None and type(MOUSE.hoverElement) not in [dict] and MOUSE.hoverElement.objectType == "Caption" and len(MOUSE.hoverElement.strLabel) in self.surfaceHoverDict:
				WINDOW.blit(self.surfaceHoverDict[len(MOUSE.hoverElement.strLabel)], [MOUSE.hoverElement.x, MOUSE.hoverElement.y])
				if MOUSE.hoverElement.splitCaption != None and len(MOUSE.hoverElement.splitCaption.strLabel) in self.surfaceHoverDict:
					WINDOW.blit(self.surfaceHoverDict[len(MOUSE.hoverElement.splitCaption.strLabel)], [MOUSE.hoverElement.splitCaption.x, MOUSE.hoverElement.splitCaption.y])
			startIndex = len(self.displayLineList) - self.charMax[1] - self.displayPage
			if startIndex < 0 : startIndex = 0
			targetDisplayList = self.displayLineList[startIndex:startIndex+self.charMax[1]]
			targetDisplayList.reverse()
				
			consoleWidthBuffer = 0
			if "Console Width Buffer" in self.flags : consoleWidthBuffer = self.flags["Console Width Buffer"]
			xDrawLoc = self.rect.left + consoleWidthBuffer
			yDrawLoc = self.rect.bottom - self.charSize[1] - lineHeightBuffer
			for displayLine in targetDisplayList:
				Utility.writeColor(displayLine.label, displayLine.colorCode, Config.COLOR_DICT, [xDrawLoc, yDrawLoc], self.font, WINDOW)
				yDrawLoc -= self.charSize[1] + (lineHeightBuffer * 2)
				
			#if MOUSE.hoverElement != None and type(MOUSE.hoverElement) not in [dict] and MOUSE.hoverElement.objectType == "Caption":
			#	MOUSE.hoverElement.draw(WINDOW, MOUSE)
				
		if DRAW_TYPE == "All":
			if self.rect not in Config.DISPLAY_RECT_LIST:
				Config.DISPLAY_RECT_LIST.append(self.rect)
		else:
			if self.rectDisplay not in Config.DISPLAY_RECT_LIST:
				Config.DISPLAY_RECT_LIST.append(self.rectDisplay)
			
	def moveMouseWheel(self, DIR):
		
		moveCheck = False
		
		if DIR == 4 and (self.displayPage + self.charMax[1]) < len(self.displayLineList):
			self.displayPage += 1
			moveCheck = True
			
		elif DIR == 5 and self.displayPage > 0:
			self.displayPage -= 1
			moveCheck = True
			
		if moveCheck:
			Config.DRAW_SCREEN_DICT["cnslMain"] = True
					
class DisplayLine:

	def __init__(self, LABEL, COLOR_CODE=None, CAPTION_LIST=[]):
	
		self.label = LABEL
		self.colorCode = COLOR_CODE
		self.captionList = CAPTION_LIST
		
		if self.colorCode == None:
			self.colorCode = str(len(self.label)) + "w"
	
def addDisplayLineToDictList(DISPLAY_LINE, COLOR_CODE=None, FLAGS={}):

	# Stack Line Check - Check If Display Line In Display List #
	inDisplayListIndex = -1
	if "Stack Line" in FLAGS and FLAGS["Stack Line"] == True:
		for lineNum, tempDisplayLineDict in enumerate(Config.DISPLAY_LINE_DICT_LIST):
			if DISPLAY_LINE == tempDisplayLineDict["Display Line"]:
				inDisplayListIndex = lineNum
				break
	
	# Add Display Line To Display List #
	addCount = 1
	if "Count Mod" in FLAGS : addCount = FLAGS["Count Mod"]
	
	if inDisplayListIndex != -1:
		Config.DISPLAY_LINE_DICT_LIST[inDisplayListIndex]["Line Count"] += addCount
	else:
		displayLineDict = {"Display Line":DISPLAY_LINE, "Line Count":addCount}
		if COLOR_CODE == None : displayLineDict["Color Code"] = str(len(DISPLAY_LINE)) + "w"
		else : displayLineDict["Color Code"] = COLOR_CODE
		if "No Trim Check" in FLAGS : displayLineDict["No Trim Check"] = True
		
		Config.DISPLAY_LINE_DICT_LIST.append(displayLineDict)
	
def writeDisplayLinesToConsole(CONSOLE):

	if len(Config.DISPLAY_LINE_DICT_LIST) > 0:
		CONSOLE.addDisplayLine("")
		for displayLineDict in Config.DISPLAY_LINE_DICT_LIST:
			displayLine = displayLineDict["Display Line"]
			colorCode = str(len(displayLine)) + "w"
			if "Color Code" in displayLineDict : colorCode = displayLineDict["Color Code"]
			if displayLineDict["Line Count"] > 1:
				displayLine = displayLine + " (" + str(displayLineDict["Line Count"]) + ")"
				colorCode = colorCode + "2r" + str(len(str(displayLineDict["Line Count"]))) + "w1r"
			trimCheck = True
			if "No Trim Check" in displayLineDict : trimCheck = False
			CONSOLE.addDisplayLine(displayLine, colorCode, [], trimCheck)
			
		Config.DISPLAY_LINE_DICT_LIST = []
	
	Config.DRAW_SCREEN_DICT["cnslMain"] = "No Border"
	