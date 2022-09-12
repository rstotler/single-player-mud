import pygame, Config, Utility
from pygame import *

class LoadMouse:

	def __init__(self):
	
		self.x = 0
		self.y = 0
		self.oldX = 0
		self.oldY = 0
		
		self.clickLeft = False
		self.clickMiddle = False
		self.clickRight = False
		
		self.hoverScreen = None
		self.leftClickScreen = None
		
		self.hoverElement = None
		self.leftClickElement = None
		self.rightClickElement = None
		
	def update(self, WINDOW, DATA_PLAYER, ELEMENT_LIST=[], CLEAR_HOVER_TARGETS=True):
		
		# Update Position & Get Data #
		if True:
		
			# Update Position #
			self.oldX = self.x
			self.oldY = self.y
			self.x, self.y = pygame.mouse.get_pos()
			#self.x /= (WINDOW.get_width() + 0.0)
			#self.x = int(self.x * SCREEN.get_width())
			#self.y /= (WINDOW.get_height() + 0.0)
			#self.y = int(self.y * SCREEN.get_height())
			
			# Update Old Hover Object #
			oldHoverScreen = self.hoverScreen
			oldHoverElement = self.hoverElement
			
			if CLEAR_HOVER_TARGETS == True:
				self.hoverScreen = None
				self.hoverElement = None
			
			breakCheck = False
			drawScreenDict = {}
			
		# Get Hover Object Data #
		for element in ELEMENT_LIST:
		
			if element.objectType == "Sidescreen":
				if Utility.rectRectCollide([self.x, self.y], [element.rect.left, element.rect.top], [element.rect.width, element.rect.height]):
					self.hoverScreen = element
					
					# Room Screen #
					if element.id == "Room" and element.displayRoom != None:
						
						# Hover Mob Check #
						for roomMob in element.displayRoom.mobList + [DATA_PLAYER]:
							if Utility.rectRectCollide([self.x, self.y], [roomMob.rectArea.left, roomMob.rectArea.top], [roomMob.rectArea.width, roomMob.rectArea.height]):
								self.hoverElement = roomMob
								break
								
						# Hover Item Check #
						if self.hoverElement == None:
							for roomItem in element.displayRoom.itemList:
								if Utility.rectRectCollide([self.x, self.y], [roomItem.rectArea.left, roomItem.rectArea.top], [roomItem.rectArea.width, roomItem.rectArea.height]):
									self.hoverElement = roomItem
									break
									
					# Player Utility Screen #
					elif element.id == "Player Utility":
						if self.x >= (element.rect.left + 26) and self.x <= (element.rect.right - 50) \
						and self.y >= (element.rect.top + 26) and self.y <= (element.rect.bottom - 26):
							xLoc = (self.x - element.rect.left - 26)
							yLoc = (self.y - element.rect.top - 26)
							if (xLoc % 38) >= 0 and (xLoc % 38) <= 28:
								if (yLoc % 41) >= 0 and (yLoc % 41) <= 28:
									hoverIndex = ((yLoc / 41) * 6) + (xLoc / 38) + (element.scrollPage * 6)
									if element.displayItemList != None and (hoverIndex + 1) <= len(element.displayItemList):
										targetItem = element.displayItemList[hoverIndex]
									else : targetItem = None
									self.hoverElement = {"Type":"Inventory Button", "Button X Loc":xLoc / 38, "Button Y Loc":yLoc / 41, "Hover Item Data":targetItem}
									break
									
					# Player Utility Bar Screen #
					elif element.id == "Player Utility Bar":
						if self.x >= (element.rect.left + 3) and self.x <= (element.rect.left + (26 * 3)) \
						and self.y >= (element.rect.top + 3) and self.y <= (element.rect.bottom - 3):
							xLoc = (self.x - element.rect.left - 3)
							if (xLoc % 26) >= 0 and (xLoc % 26) <= 23:
								self.hoverElement = {"Type":"Player Utility Bar Button", "Button X Loc":xLoc / 26}
								break
								
			elif element.objectType == "Console":
				if Utility.rectRectCollide([self.x, self.y], [element.rect.left, element.rect.top], [element.rect.width, element.rect.height]):
					self.hoverScreen = element
					
					consoleWidthBuffer = 0
					if "Console Width Buffer" in element.flags : consoleWidthBuffer = element.flags["Console Width Buffer"]
					lineHeightBuffer = 0
					if "Line Height Buffer" in element.flags : lineHeightBuffer = element.flags["Line Height Buffer"]
					cellLoc = [self.x - element.rect.left - consoleWidthBuffer, self.y - element.rect.top]
					cellLoc[0] /= element.charSize[0]
					cellLoc[1] /= element.charSize[1] + (lineHeightBuffer * 2)
					hoverLineIndex = element.charMax[1] - cellLoc[1] - 1
					
					startIndex = len(element.displayLineList) - element.charMax[1] - element.displayPage
					if startIndex < 0 : startIndex = 0
					targetDisplayList = element.displayLineList[startIndex:startIndex+element.charMax[1]]
					targetDisplayList.reverse()
					
					if hoverLineIndex < len(targetDisplayList):
						strLabel = targetDisplayList[hoverLineIndex].label
						priorWordList = strLabel[0:cellLoc[0]+1].split()
						hoverWordIndex = len(priorWordList) - 1
						if cellLoc[0] < len(strLabel):
							for caption in targetDisplayList[hoverLineIndex].captionList:
								strTargetWordLabel = ' '.join(strLabel.split()[0:(caption.wordIndex+caption.wordCount)])
								if hoverWordIndex in range(caption.wordIndex, caption.wordIndex + caption.wordCount) and \
								cellLoc[0] < (len(strTargetWordLabel)):
									caption.y = element.rect.top + (cellLoc[1] * (element.charSize[1] + (lineHeightBuffer * 2)))
									if caption.splitCaption != None:
										if caption.splitCaptionType == "Next Line":
											caption.splitCaption.y = element.rect.top + (cellLoc[1] - 1) * (element.charSize[1] + (lineHeightBuffer * 2))
										elif caption.splitCaptionType == "Previous Line":
											caption.splitCaption.y = element.rect.top + (cellLoc[1] + 1) * (element.charSize[1] + (lineHeightBuffer * 2))
										
									self.hoverElement = caption
									breakCheck = True
									break
				
			elif element.collideShape == "Rectangle":
				if Utility.rectRectCollide([self.x, self.y], [element.rect.left, element.rect.top], [element.rect.width, element.rect.height]):
					self.hoverElement = element
					break
					
			elif element.collideShape == "Circle":
				if Utility.circleCircleCollide([element.rect.left+(element.rect.width/2), element.rect.top+(element.rect.width/2)], element.rect.width/2, [self.x, self.y], 0):
					self.hoverElement = element
					break
					
			if breakCheck : break
			
		# Update Hover Display Variables #
		if self.hoverElement != oldHoverElement and (self.hoverElement != None or oldHoverElement != None):
			
			# Get Data #
			targetEntity = None
			if self.hoverElement != None : targetEntity = self.hoverElement
			elif oldHoverElement != None : targetEntity = oldHoverElement
			
			# Update Screen Data #
			if targetEntity != None:
			
				if isinstance(targetEntity, dict):
					if targetEntity["Type"] == "Inventory Button":
						Config.DRAW_SCREEN_DICT["Player Utility"] = True
						Config.DRAW_SCREEN_DICT["Target Stats"] = True
					
					elif targetEntity["Type"] == "Player Utility Bar Button":
						Config.DRAW_SCREEN_DICT["Player Utility Bar"] = True
					
				elif getattr(targetEntity, 'objectType'):
					if targetEntity.objectType == "Item":
						Config.DRAW_SCREEN_DICT["Target Stats"] = True
						if targetEntity.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
						elif targetEntity.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
						
					elif targetEntity.objectType == "Player" or targetEntity in DATA_PLAYER.groupList:
						Config.DRAW_SCREEN_DICT["Target Stats"] = True
						Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
						
					elif targetEntity.objectType == "Mob":
						Config.DRAW_SCREEN_DICT["Target Stats"] = True
						Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
						
		return drawScreenDict
				