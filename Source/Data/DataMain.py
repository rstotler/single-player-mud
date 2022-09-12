import pygame, os, random, Config, Utility, GameProcess, DataGame, DataWorld, DataCombat, DataMob
from pygame import *
from Hardware import Mouse, Keyboard
from Screen import ScreenGame
from Elements import Console

class LoadDataMain:
	
	def __init__(self, WINDOW):
	
		self.mouse = Mouse.LoadMouse()
		self.keyboard = Keyboard.LoadKeyboard()
		self.dataScreen = ScreenGame.LoadScreenGame(WINDOW)
		self.dataGame = DataGame.LoadGame(self.dataScreen)
			
	def updateMain(self, FPS, WINDOW):
	
		# Process User Input & Update Game #
		screenElementList = self.processInput(WINDOW)
		self.dataGame.updateGame(WINDOW, self.mouse, self.dataScreen, "Default")
		self.dataScreen.frmMain.update(self.keyboard)
		
		# Update Main Console #
		if len(Config.DISPLAY_LINE_DICT_LIST) > 0:
			Console.writeDisplayLinesToConsole(self.dataScreen.cnslMain)
		
		# Draw Screen #
		self.dataScreen.updateScreenAnimations(self.dataGame.tickMillisecond, self.dataGame.solarSystemDict[self.dataGame.dataPlayer.currentSolarSystem], self.dataGame.dataPlayer)
		self.dataScreen.draw(FPS, WINDOW, self.mouse, self.dataGame)
		
	def processInput(self, WINDOW):
	
		self.keyboard.update()
	
		screenElementList = []
		for event in pygame.event.get():
		
			# Mouse Events #
			if event.type == MOUSEBUTTONDOWN:
				
				# Click Left/Middle/Right #
				if event.button == 1:
					self.mouse.clickLeft = True
					if self.mouse.hoverScreen != None:
						self.mouse.leftClickScreen = self.mouse.hoverScreen
					if self.mouse.hoverElement != None:
						self.mouse.leftClickElement = self.mouse.hoverElement
				elif event.button == 2:
					self.mouse.clickMiddle = True
				elif event.button == 3:
					self.mouse.clickRight = True
					if self.mouse.hoverElement != None:
						self.mouse.rightClickElement = self.mouse.hoverElement
				
				# Middle Mouse Wheel Up/Down #
				elif event.button in [4, 5]:
					if screenElementList == [] : screenElementList = self.dataScreen.getElementList()
					if self.mouse.hoverScreen != None:
						if self.mouse.hoverScreen.id == "cnslMain":
							self.mouse.hoverScreen.moveMouseWheel(event.button)
						elif self.mouse.hoverScreen.id == "Map":
							self.mouse.hoverScreen.moveMouseWheel(event.button, self.dataGame.dataPlayer, self.dataGame.solarSystemDict[self.dataGame.dataPlayer.currentSolarSystem])
						elif self.mouse.hoverScreen.id == "Player Utility":
							self.mouse.hoverScreen.moveMouseWheel(event.button, WINDOW, self.mouse, self.dataGame.dataPlayer)
							
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.mouse.clickLeft = False
					if self.mouse.leftClickElement != None:
						if self.mouse.hoverElement == self.mouse.leftClickElement:
							self.leftClickElement(WINDOW, self.mouse.leftClickElement)
						self.mouse.leftClickElement = None
					if self.mouse.leftClickScreen != None:
						self.mouse.leftClickScreen = None
				elif event.button == 2:
					self.mouse.clickMiddle = False
				elif event.button == 3:
					self.mouse.clickRight = False
					if self.mouse.rightClickElement != None:
						if self.mouse.hoverElement == self.mouse.rightClickElement:
							self.rightClickElement(self.mouse.rightClickElement)
						self.mouse.rightClickElement = None
		
			elif event.type == MOUSEMOTION:
				if screenElementList == [] : screenElementList = self.dataScreen.getElementList()
				self.mouse.update(WINDOW, self.dataGame.dataPlayer, screenElementList)
				
			# Keyboard Events #
			elif event.type == KEYDOWN:
				keyName = pygame.key.name(event.key)
				
				# Escape #
				if event.key == K_ESCAPE : raise SystemExit
				
				# Shift, Control, & Backspace #
				elif event.key in [K_LSHIFT, K_RSHIFT] and self.keyboard.shift == False : self.keyboard.shift = True
				elif event.key in [K_LCTRL, K_RCTRL] and self.keyboard.control == False : self.keyboard.control = True
				elif event.key == K_BACKSPACE and self.keyboard.backspace == False:
					self.keyboard.backspace = True
					self.keyboard.backspaceTick = -1
					
				# Enter - Process Form Input #
				elif keyName == "return":
					if len(self.dataScreen.frmMain.userInput) > 0:
						self.processInputBarInput(WINDOW)
						
				# Up/Down/Left/Right - Keyboard Movement #
				elif self.keyboard.control and keyName in ["up", "down", "left", "right"]:
					dirDict = {"up":"North", "down":"South", "left":"West", "right":"East"}
					targetDir = dirDict[keyName]
					GameProcess.userMove(self.dataGame.tickSynch, WINDOW, self.mouse, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, targetDir, self.dataScreen.sidescreenRoom, self.dataScreen.sidescreenMap, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Interface"], self.dataScreen.imageDict["Item"])
					
				# Scroll Main Form #
				elif keyName in ["up", "down"]:
					self.dataScreen.frmMain.scrollUserInputList(keyName)

				# Toggle Menus #
				elif self.keyboard.control == True and keyName == "f" : self.dataScreen.toggleScreen("FPS")
				elif self.keyboard.control == True and keyName == "d" : self.dataScreen.toggleScreen("Debug")
				elif self.keyboard.control == True and keyName == "b" : self.dataScreen.toggleScreen("Border")
				
				# Main Form Input #
				else : self.dataScreen.frmMain.getInput(self.keyboard, keyName)
				
			elif event.type == KEYUP:
				
				if event.key in [K_LSHIFT, K_RSHIFT] and self.keyboard.shift == True:
					self.keyboard.shift = False
				
				elif event.key in [K_LCTRL, K_RCTRL] and self.keyboard.control == True:
					self.keyboard.control = False
				
				elif event.key == K_BACKSPACE and self.keyboard.backspace == True:
					self.keyboard.backspace = False
					self.keyboard.backspaceTick = -1
				
			# Quit Event #
			elif event.type == QUIT:
				raise SystemExit
				
		return screenElementList
		
	def leftClickElement(self, WINDOW, TARGET_ELEMENT):
	
		# Get Data #
		playerRoom = DataWorld.getParentArea(self.dataGame.solarSystemDict[self.dataGame.dataPlayer.currentSolarSystem], self.dataGame.dataPlayer).roomDict[self.dataGame.dataPlayer.currentRoom]

		# Room Screen #
		if self.mouse.hoverScreen != None and self.mouse.hoverScreen.id == "Room":
			
			# Click On Item #
			if getattr(TARGET_ELEMENT, 'objectType') and TARGET_ELEMENT.objectType == "Item" and self.dataGame.dataPlayer.currentAction == None:
				
				# Pick Up Item #
				if "No Get" not in TARGET_ELEMENT.flags:
					GameProcess.addItemToEntityInventory(self.dataGame.dataPlayer, TARGET_ELEMENT, playerRoom, "All", self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"], {"Delete Check":True})
					Config.DRAW_SCREEN_DICT["Target Stats"] = True
					
				# Open/Empty No Get Chests #
				elif "No Get" in TARGET_ELEMENT.flags and TARGET_ELEMENT.flags["No Get"] == True and TARGET_ELEMENT.type == "Container":
					
					# Open Chest #
					if "Container Status" in TARGET_ELEMENT.flags and TARGET_ELEMENT.flags["Container Status"] == "Closed":
						TARGET_ELEMENT.flags["Container Status"] = "Open"
						
						# Update Screen Data #
						if TARGET_ELEMENT.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
						elif TARGET_ELEMENT.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
						Config.DRAW_SCREEN_DICT["Target Stats"] = True
						
					# Empty Chest #
					elif "Container Status" in TARGET_ELEMENT.flags and TARGET_ELEMENT.flags["Container Status"] == "Open":
						playerRoom.emptyContainer(TARGET_ELEMENT, self.dataGame.dataPlayer)
						
						# Update Screen Data #
						if TARGET_ELEMENT.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
						elif TARGET_ELEMENT.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
						Config.DRAW_SCREEN_DICT["Target Stats"] = True
			
		# Player Utility Screen (Inventory) #
		#if self.mouse.hoverScreen != None and self.mouse.hoverScreen.id == "Player Utility" and self.mouse.hoverScreen.displayLevel == "Inventory":
			
			
		# Player Utility Bar Screen #
		if self.mouse.hoverScreen != None and self.mouse.hoverScreen.id == "Player Utility Bar" and self.mouse.hoverElement != None:
			self.dataScreen.sidescreenPlayerUtility.updateScreen(self.mouse.hoverElement["Button X Loc"])				

		# ### Old Code (Captions) - Redo This ### #
		if False:	
			if self.mouse.leftClickElement != None:
				
				if self.mouse.leftClickElement.type == "Caption":
					
					if self.mouse.leftClickElement.captionType == "Room Exit":
						roomData = self.mouse.leftClickElement.flags["Room Data"]
						if self.dataGame.dataPlayer.currentSolarSystem == roomData.idSolarSystem and self.dataGame.dataPlayer.currentPlanet == roomData.idPlanet and self.dataGame.dataPlayer.currentArea == roomData.idArea and self.dataGame.dataPlayer.currentRoom == roomData.idNum:
							targetDir = self.mouse.leftClickElement.flags["Target Direction"]
							#GameProcess.userMove(self.dataGame.tickSynch, self.dataScreen.cnslMain, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, targetDir, 1, self.dataScreen.sidescreenMap)
		
					elif self.mouse.leftClickElement.captionType in ["Get Item", "Get # Item"]:
						pass
	
	def rightClickElement(self, TARGET_ELEMENT):
	
		pass

	def processInputBarInput(self, WINDOW):
	
		# Format User Input String #
		userInput = self.dataScreen.frmMain.userInput.lower().strip()
		while '  ' in userInput : userInput = userInput.replace('  ', ' ')
		userInputList = userInput.split()
		
		if len(userInputList) > 0:
			if self.dataGame.solarSystemDict != None and self.dataGame.dataPlayer != None:
				
				# Get Data #
				if True:
					currentSolarSystem = self.dataGame.solarSystemDict[self.dataGame.dataPlayer.currentSolarSystem]
					currentArea = DataWorld.getParentArea(currentSolarSystem, self.dataGame.dataPlayer)
					currentRoom = currentArea.roomDict[self.dataGame.dataPlayer.currentRoom]
					inputProcessed = False
				
				# User Input - Room Commands #
				if True:
					if not inputProcessed and userInputList[0] in ["look", "l"]:
						
						LOOK_DIR = None
						if len(userInputList) > 1 and userInputList[1] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
							if userInputList[1] in ["north", "n"] : LOOK_DIR = "North"
							elif userInputList[1] in ["east", "e"] : LOOK_DIR = "East"
							elif userInputList[1] in ["south", "s"] : LOOK_DIR = "South"
							elif userInputList[1] in ["west", "w"] : LOOK_DIR = "West"
					
						inIndex = -1
						if "in" in userInputList : inIndex = userInputList.index("in")
						
						# Look #
						if len(userInputList) == 1:
							getRoomFlags = {}
							if "In Spaceship" in self.dataGame.dataPlayer.flags:
								targetSpaceship = self.dataGame.solarSystemDict[self.dataGame.dataPlayer.currentSolarSystem].getTargetSpaceship(self.dataGame.dataPlayer.currentArea)
								currentRoom = targetSpaceship.roomDict[self.dataGame.dataPlayer.currentRoom]
							else : currentRoom = self.dataGame.solarSystemDict[self.dataGame.dataPlayer.currentSolarSystem].planetDict[self.dataGame.dataPlayer.currentPlanet].areaDict[self.dataGame.dataPlayer.currentArea].roomDict[self.dataGame.dataPlayer.currentRoom]
							currentRoom.displayRoom(currentArea, self.dataGame.solarSystemDict, self.dataGame.dataPlayer)

						# Look Dir #
						elif len(userInputList) == 2 and LOOK_DIR != None:
							LOOK_DIR_NUM = 1
							GameProcess.userLookDir(WINDOW, self.mouse, self.dataGame.tickSynch, currentArea, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, LOOK_DIR, LOOK_DIR_NUM, self.dataScreen.sidescreenRoom, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Interface"], self.dataScreen.imageDict["Item"])
							
						# Look Dir Num #
						elif len(userInputList) == 3 and LOOK_DIR != None and Utility.stringIsNumber(userInputList[2]) and int(userInputList[2]) > 0:
							LOOK_DIR_NUM = int(userInputList[2])
							GameProcess.userLookDir(WINDOW, self.mouse, self.dataGame.tickSynch, currentArea, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, LOOK_DIR, LOOK_DIR_NUM, self.dataScreen.sidescreenRoom, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Interface"], self.dataScreen.imageDict["Item"])
							
						# Look Item @Index In Container @Index #
						elif len(userInputList) > 5 and "in" in userInputList[3::] and len(userInputList[1:inIndex]) > 1 and Utility.stringIsNumber(userInputList[inIndex-1]) and int(userInputList[inIndex-1]) > 0 and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:inIndex-1])
							TARGET_INDEX = int(userInputList[inIndex-1]) - 1
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1:-1])
							IN_TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
						
						# Look Item @Index In Container #
						elif len(userInputList) > 4 and "in" in userInputList[3::] and len(userInputList[1:inIndex]) > 1 and Utility.stringIsNumber(userInputList[inIndex-1]) and int(userInputList[inIndex-1]) > 0 and userInputList[-1] != "in":
							STR_TARGET = ' '.join(userInputList[1:inIndex-1])
							TARGET_INDEX = int(userInputList[inIndex-1]) - 1
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1::])
							IN_TARGET_INDEX = -1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
						
						# Look Item In Container @Index #
						elif len(userInputList) > 4 and "in" in userInputList[2::] and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:inIndex])
							TARGET_INDEX = 0
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1:-1])
							IN_TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
						
						# Look Item In Container #
						elif len(userInputList) > 3 and "in" in userInputList[2::] and userInputList[-1] != "in":
							STR_TARGET = ' '.join(userInputList[1:inIndex])
							TARGET_INDEX = 0
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1::])
							IN_TARGET_INDEX = -1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
						
						# Look Item/Mob @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							STR_IN_TARGET = None
							IN_TARGET_INDEX = None
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
						
						# Look Item/Mob/Other #
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							STR_IN_TARGET = None
							IN_TARGET_INDEX = None
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["examine", "examin", "exami", "exam", "exa", "ex"]:
					
						inIndex = -1
						if "in" in userInputList : inIndex = userInputList.index("in")
						
						# Examine Item @Index In Container @Index #
						if len(userInputList) > 5 and "in" in userInputList[3::] and len(userInputList[1:inIndex]) > 1 and Utility.stringIsNumber(userInputList[inIndex-1]) and int(userInputList[inIndex-1]) > 0 and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:inIndex-1])
							TARGET_INDEX = int(userInputList[inIndex-1]) - 1
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1:-1])
							IN_TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
							
						# Examine Item @Index In Container #
						elif len(userInputList) > 4 and "in" in userInputList[3::] and len(userInputList[1:inIndex]) > 1 and Utility.stringIsNumber(userInputList[inIndex-1]) and int(userInputList[inIndex-1]) > 0 and userInputList[-1] != "in":
							STR_TARGET = ' '.join(userInputList[1:inIndex-1])
							TARGET_INDEX = int(userInputList[inIndex-1]) - 1
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1::])
							IN_TARGET_INDEX = -1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
							
						# Examine Item In Container @Index #
						elif len(userInputList) > 4 and "in" in userInputList[2::] and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:inIndex])
							TARGET_INDEX = 0
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1:-1])
							IN_TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
							
						# Examine Item In Container #
						elif len(userInputList) > 3 and "in" in userInputList[2::] and userInputList[-1] != "in":
							STR_TARGET = ' '.join(userInputList[1:inIndex])
							TARGET_INDEX = 0
							STR_IN_TARGET = ' '.join(userInputList[inIndex+1::])
							IN_TARGET_INDEX = -1
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
							
						# Examine Item/Mob @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							STR_IN_TARGET = None
							IN_TARGET_INDEX = None
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
							
						# Examine Item/Mob/Other #	
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							STR_IN_TARGET = None
							IN_TARGET_INDEX = None
							GameProcess.userExamine(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, STR_IN_TARGET, IN_TARGET_INDEX)
							
						else : Console.addDisplayLineToDictList("Examine what?", "12w1y")
					
						inputProcessed = True
						
					if not inputProcessed and userInputList[0] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
						
						TARGET_DIR = userInputList[0]
						if TARGET_DIR in ["north", "n"] : TARGET_DIR = "North"
						elif TARGET_DIR in ["east", "e"] : TARGET_DIR = "East"
						elif TARGET_DIR in ["south", "s"] : TARGET_DIR = "South"
						elif TARGET_DIR in ["west", "w"] : TARGET_DIR = "West"
					
						# @MoveDir #
						GameProcess.userMove(self.dataGame.tickSynch, WINDOW, self.mouse, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_DIR, self.dataScreen.sidescreenRoom, self.dataScreen.sidescreenMap, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Interface"], self.dataScreen.imageDict["Item"])
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["open", "ope", "op", "close", "clos", "clo", "cl", "lock", "loc", "lo", "unlock", "unloc"]:
						
						# Get Target Variables #
						TARGET_ACTION = userInputList[0]
						TARGET_DIR = None
						if TARGET_ACTION in ["open", "ope", "op"] : TARGET_ACTION = "Open"
						elif TARGET_ACTION in ["close", "clos", "clo", "cl"] : TARGET_ACTION = "Close"
						elif TARGET_ACTION in ["lock", "loc", "lo"] : TARGET_ACTION = "Lock"
						elif TARGET_ACTION in ["unlock", "unloc"] : TARGET_ACTION = "Unlock"
						if len(userInputList) == 2 and userInputList[1] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
							TARGET_DIR = userInputList[1]
							if TARGET_DIR in ["north", "n"] : TARGET_DIR = "North"
							elif TARGET_DIR in ["east", "e"] : TARGET_DIR = "East"
							elif TARGET_DIR in ["south", "s"] : TARGET_DIR = "South"
							elif TARGET_DIR in ["west", "w"] : TARGET_DIR = "West"
						
						# OCLU @Dir #
						if len(userInputList) == 2 and TARGET_DIR != None:
							TARGET_COUNT = 1
							GameProcess.userOCLUDoor(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_ACTION, TARGET_COUNT, TARGET_DIR)
						
						# OCLU All Door #
						elif len(userInputList) == 3 and userInputList[1] == "all" and userInputList[2] in ["door", "doors"]:
							TARGET_COUNT = "All"
							GameProcess.userOCLUDoor(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_ACTION, TARGET_COUNT, TARGET_DIR)
						
						# OCLU All #
						elif len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userOCLUItem(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_ACTION, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# OCLU All Item #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userOCLUItem(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_ACTION, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# OCLU Item @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]):
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userOCLUItem(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_ACTION, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# OCLU Item #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userOCLUItem(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_ACTION, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						else : Console.addDisplayLineToDictList(TARGET_ACTION+" what?", str(len(TARGET_ACTION))+"w5w1y")
					
						inputProcessed = True
						
					if not inputProcessed and userInputList[0] in ["enter", "ente", "ent", "en"]:
						
						# Enter TargetSpaceship #
						if len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							GameProcess.userEnterSpaceship(WINDOW, self.mouse, self.dataGame.tickSynch, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, STR_TARGET, self.dataScreen.sidescreenMap, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Interface"], self.dataScreen.imageDict["Item"])
						
						# Enter #
						else:
							STR_TARGET = None
							GameProcess.userEnterSpaceship(WINDOW, self.mouse, self.dataGame.tickSynch, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, STR_TARGET, self.dataScreen.sidescreenMap, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Interface"], self.dataScreen.imageDict["Item"])
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in Config.SPACESHIP_COMMANDS_KEYLIST:
						GameProcess.userControlSpaceship(currentArea, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, userInputList)
						inputProcessed = True
					
				# User Input - Item Commands #
				if True:
					if not inputProcessed and userInputList[0] in ["put", "pu"]:
						
						inIndex = -1
						if "in" in userInputList : inIndex = userInputList.index("in")
						
						# Put All In Container @Index #
						if len(userInputList) > 4 and userInputList[1] == "all" and userInputList[2] == "in" and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = "All"
							TARGET_ITEM_INDEX = -1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put All In Container #
						elif len(userInputList) > 3 and userInputList[1] == "all" and userInputList[2] == "in":
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = "All"
							TARGET_ITEM_INDEX = -1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1::])
							TARGET_CONTAINER_INDEX = 0
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put All Target In Container @Index #
						elif len(userInputList) > 5 and userInputList[1] == "all" and "in" in userInputList[3:-2] and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = ' '.join(userInputList[2:inIndex])
							TARGET_ITEM_INDEX = -1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put All Target In Container #
						elif len(userInputList) > 4 and userInputList[1] == "all" and "in" in userInputList[3:-1]:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = ' '.join(userInputList[2:inIndex])
							TARGET_ITEM_INDEX = -1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1::])
							TARGET_CONTAINER_INDEX = 0
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put Count# Target In Container @Index #
						elif len(userInputList) > 5 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0 and "in" in userInputList[3:-1] and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET_ITEM = ' '.join(userInputList[2:inIndex])
							TARGET_ITEM_INDEX = -1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put Count# Target In Container #
						elif len(userInputList) > 4 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0 and "in" in userInputList[3:-1]:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET_ITEM = ' '.join(userInputList[2:inIndex])
							TARGET_ITEM_INDEX = -1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1::])
							TARGET_CONTAINER_INDEX = 0
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put Target @Index In Container @Index #
						elif len(userInputList) > 5 and "in" in userInputList[3:-2] and Utility.stringIsNumber(userInputList[inIndex-1]) and int(userInputList[inIndex-1]) > 0 and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:inIndex-1])
							TARGET_ITEM_INDEX = int(userInputList[inIndex-1]) - 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put Target In Container @Index #
						elif len(userInputList) > 4 and "in" in userInputList[2:-2] and len(userInputList[inIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:inIndex])
							TARGET_ITEM_INDEX = 0
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put Target @Index In Container #
						elif len(userInputList) > 4 and "in" in userInputList[3:-1] and Utility.stringIsNumber(userInputList[inIndex-1]) and int(userInputList[inIndex-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:inIndex-1])
							TARGET_ITEM_INDEX = int(userInputList[inIndex-1]) - 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1::])
							TARGET_CONTAINER_INDEX = 0
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						# Put Target In Container #
						elif len(userInputList) > 3 and "in" in userInputList[2:-1]:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:inIndex])
							TARGET_ITEM_INDEX = 0
							STR_TARGET_CONTAINER = ' '.join(userInputList[inIndex+1::])
							TARGET_CONTAINER_INDEX = 0
							GameProcess.userPutIn(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
					
						else : Console.addDisplayLineToDictList("Put what in what?", "17w")
					
						inputProcessed = True
						
					if not inputProcessed and userInputList[0] in ["get", "ge", "g"] and ("from" in userInputList or "fro" in userInputList or "fr" in userInputList):
						
						if "from" in userInputList : fromIndex = userInputList.index("from")
						elif "fro" in userInputList : fromIndex = userInputList.index("fro")
						elif "fr" in userInputList : fromIndex = userInputList.index("fr")
						
						# Get All From All #
						if len(userInputList) == 4 and userInputList[1] == "all" and userInputList[2] in ["from", "fro", "fr"] and userInputList[3] == "all":
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = "All"
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = "All"
							STR_TARGET_CONTAINER = "All"
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All From All Container #
						elif len(userInputList) > 4 and userInputList[1] == "all" and userInputList[2] in ["from", "fro", "fr"] and userInputList[3] == "all":
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = "All"
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = "All"
							STR_TARGET_CONTAINER = ' '.join(userInputList[4::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All From Container @Index #
						elif len(userInputList) > 4 and userInputList[1] == "all" and userInputList[2] in ["from", "fro", "fr"] and len(userInputList[3::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = "All"
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All From Container #
						elif len(userInputList) > 3 and userInputList[1] == "all" and userInputList[2] in ["from", "fro", "fr"]:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = "All"
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[3::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All Target From All #
						elif len(userInputList) > 4 and userInputList[1] == "all" and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[-2] in ["from", "fro", "fr"] and userInputList[-1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = ' '.join(userInputList[2:-2])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = "All"
							STR_TARGET_CONTAINER = "All"
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All Target From All Container #
						elif len(userInputList) > 5 and userInputList[1] == "all" and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[fromIndex+1] == "all" and len(userInputList) > fromIndex+2:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = "All"
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+2::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All Target From Container @Index #
						elif len(userInputList) > 5 and userInputList[1] == "all" and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and len(userInputList[fromIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get All Target From Container #
						elif len(userInputList) > 4 and userInputList[1] == "all" and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[-1] not in ["from", "fro", "fr"]:
							TARGET_COUNT = "All"
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Count# Target From All #
						elif len(userInputList) > 4 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0 and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[-2] in ["from", "fro", "fr"] and userInputList[-1] == "all":
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = "All"
							STR_TARGET_CONTAINER = "All"
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Count# Target From All Container #
						elif len(userInputList) > 5 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0 and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[fromIndex+1] == "all" and len(userInputList) > fromIndex+2:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = "All"
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+2::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Count# Target From Container @Index #
						elif len(userInputList) > 5 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0 and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and len(userInputList[fromIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Count# Target From Container #
						elif len(userInputList) > 4 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0 and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[-1] not in ["from", "fro", "fr"]:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET_ITEM = ' '.join(userInputList[2:fromIndex])
							TARGET_ITEM_INDEX = -1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Target @Index From Container @Index #
						elif len(userInputList) > 5 and len(userInputList[1:fromIndex]) > 1 and Utility.stringIsNumber(userInputList[fromIndex-1]) and int(userInputList[fromIndex-1]) > 0 and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and len(userInputList[fromIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:fromIndex-1])
							TARGET_ITEM_INDEX = int(userInputList[fromIndex-1]) - 1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Target @Index From Container #
						elif len(userInputList) > 4 and len(userInputList[1:fromIndex]) > 1 and Utility.stringIsNumber(userInputList[fromIndex-1]) and int(userInputList[fromIndex-1]) > 0 and ("from" in userInputList[3::] or "fro" in userInputList[3::] or "fr" in userInputList[3::]) and userInputList[-1] not in ["from", "fro", "fr"] and not Utility.stringIsNumber(userInputList[-1]):
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:fromIndex-1])
							TARGET_ITEM_INDEX = int(userInputList[fromIndex-1]) - 1
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Target From Container @Index #
						elif len(userInputList) > 4 and ("from" in userInputList[2::] or "fro" in userInputList[2::] or "fr" in userInputList[2::]) and len(userInputList[fromIndex+1::]) > 1 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:fromIndex])
							TARGET_ITEM_INDEX = 0
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1:-1])
							TARGET_CONTAINER_INDEX = int(userInputList[-1]) - 1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						# Get Target From Container #
						elif len(userInputList) > 3 and ("from" in userInputList[2::] or "fro" in userInputList[2::] or "fr" in userInputList[2::]) and userInputList[-1] not in ["from", "fro", "fr"]:
							TARGET_COUNT = 1
							STR_TARGET_ITEM = ' '.join(userInputList[1:fromIndex])
							TARGET_ITEM_INDEX = 0
							CONTAINER_COUNT = 1
							STR_TARGET_CONTAINER = ' '.join(userInputList[fromIndex+1::])
							TARGET_CONTAINER_INDEX = -1
							GameProcess.userGetFrom(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_COUNT, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, self.dataScreen.imageDict["Item"])
							
						else : Console.addDisplayLineToDictList("Get what from what?", "19w")
					
						inputProcessed = True
						
					if not inputProcessed and userInputList[0] in ["get", "ge", "g"]:
						
						# Get All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userGet(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Get Count# Item #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userGet(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Get All Item #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userGet(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Get Item @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userGet(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Get Item #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userGet(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						else : Console.addDisplayLineToDictList("Get what?", "8w1y")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["drop", "dro", "dr"]:
						
						# Drop All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userDrop(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Drop Count# Item #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userDrop(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Drop All Item #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userDrop(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Drop Item @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userDrop(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						# Drop Item #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userDrop(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, self.dataScreen.sidescreenPlayerUtility, self.dataScreen.imageDict["Item"])
						
						else : Console.addDisplayLineToDictList("Drop what?", "9w1y")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["fill", "fil"]:
					
						# Fill All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userFillLiquidContainer(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Fill Count# TargetLiquidContainer #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userFillLiquidContainer(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Fill All TargetLiquidContainer #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userFillLiquidContainer(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Fill LiquidContainer @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userFillLiquidContainer(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Fill LiquidContainer #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userFillLiquidContainer(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						else : Console.addDisplayLineToDictList("Fill what?")
					
						inputProcessed = True
						
					if not inputProcessed and userInputList[0] in ["empty", "empt", "emp"]:
						
						# Empty Count# TargetContainer #
						if len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userEmpty(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Empty All TargetContainer #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userEmpty(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Empty Container @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userEmpty(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Empty All #
						elif len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userEmpty(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Empty Container #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userEmpty(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						else : Console.addDisplayLineToDictList("Empty what?")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["eat", "ea"]:
						
						# Eat All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userEat(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Eat Count# TargetFood #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userEat(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Eat All TargetFood #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userEat(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Eat Food @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userEat(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Eat Food #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userEat(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						else : Console.addDisplayLineToDictList("Eat what?", "8w1y")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["drink", "drin", "dri"]:
					
						# Drink All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userDrink(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Drink Count# TargetLiquidContainer #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userDrink(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Drink All TargetLiquidContainer #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userDrink(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Drink TargetLiquidContainer @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userDrink(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Drink TargetLiquid/TargetLiquidContainer #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userDrink(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						else : Console.addDisplayLineToDictList("Drink what?")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["wear", "wea", "we", "wield", "wiel", "wie", "wi"]:
						
						# Wear All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							STR_TARGET = "All"
							TARGET_INDEX = -1
							TARGET_HAND = None
							GameProcess.userWear(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, TARGET_HAND)
							
						# Wear Item @Index @TargetHand #
						elif len(userInputList) > 3 and userInputList[-1] in ["left", "right"] and Utility.stringIsNumber(userInputList[-2]) and int(userInputList[-2]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-2])
							TARGET_INDEX = int(userInputList[-2]) - 1
							TARGET_HAND = userInputList[-1][0].upper() + userInputList[-1][1::] + " Hand"
							GameProcess.userWear(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, TARGET_HAND)
							
						# Wear Item @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							TARGET_HAND = None
							GameProcess.userWear(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, TARGET_HAND)
							
						# Wear Item @TargetHand #
						elif len(userInputList) > 2 and userInputList[-1] in ["left", "right"]:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = 0
							TARGET_HAND = userInputList[-1][0].upper() + userInputList[-1][1::] + " Hand"
							GameProcess.userWear(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, TARGET_HAND)
							
						# Wear Item #
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							TARGET_HAND = None
							GameProcess.userWear(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, TARGET_HAND)
							
						else : Console.addDisplayLineToDictList("Wear what?", "9w1y")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["remove", "remov", "remo", "rem", "re"]:
					
						# Remove All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							STR_TARGET = "All"
							TARGET_HAND = None
							GameProcess.userRemove(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_HAND)
						
						# Remove Item @TargetHand #
						elif len(userInputList) > 2 and userInputList[-1] in ["left", "right"]:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_HAND = userInputList[-1][0].upper() + userInputList[-1][1::] + " Hand"
							GameProcess.userRemove(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_HAND)
						
						# Remove Item #
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_HAND = None
							GameProcess.userRemove(currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_HAND)
						
						else : Console.addDisplayLineToDictList("Remove what?", "11w1y")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["press", "pres", "pre", "pr", "push", "pus", "pu"]:
						
						if len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							GameProcess.userPressButton(currentArea, self.dataGame.dataPlayer, STR_TARGET, self.dataScreen.imageDict["Entity"], self.dataScreen.imageDict["Item"])
							
						else:
							GameProcess.userPressButton(currentArea, self.dataGame.dataPlayer, None, self.dataScreen.imageDict["Entity"], self.dataScreen.imageDict["Item"])
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["plant", "plan", "pla", "pl"]:
					
						# Plant All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userPlantSeed(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Plant Count# TargetSeed #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userPlantSeed(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Plant All TargetSeed #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userPlantSeed(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Plant Seed @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userPlantSeed(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Plant Seed #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userPlantSeed(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						else : Console.addDisplayLineToDictList("Plant what?", "11w")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["switch", "switc", "swit", "swi"]:
					
						# Switch Hands #
						if len(userInputList) == 2 and userInputList[1] in ["hands", "hand", "han", "ha", "h"]:
							GameProcess.switchHands(self.dataGame.dataPlayer)
							inputProcessed = True
						
						# Switch Weapons #
						elif len(userInputList) == 2 and userInputList[1] in ["weapons", "weapon", "weapo", "weap", "wea", "we", "w"]:
							GameProcess.switchWeapons(self.dataGame.dataPlayer)
							inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["reload", "reloa", "relo", "rel", "re", "r"]:
						
						# Reload Left AmmoType #
						if len(userInputList) > 2 and userInputList[1] in ["left", "lef", "le", "l"]:
							STR_TARGET_WEAPON = "Left"
							STR_TARGET_AMMO = ' '.join(userInputList[2::])
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
						
						# Reload Right AmmoType #
						elif len(userInputList) > 2 and userInputList[1] in ["right", "righ", "rig", "ri", "r"]:
							STR_TARGET_WEAPON = "Right"
							STR_TARGET_AMMO = ' '.join(userInputList[2::])
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
						
						# Reload TargetWeapon AmmoType #
						elif len(userInputList) > 2:
							STR_TARGET_WEAPON = userInputList[1]
							STR_TARGET_AMMO = ' '.join(userInputList[2::])
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
						
						# Reload Left #
						elif len(userInputList) == 2 and userInputList[1] in ["left", "lef", "le", "l"]:
							STR_TARGET_WEAPON = "Left"
							STR_TARGET_AMMO = None
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
						
						# Reload Right #
						elif len(userInputList) == 2 and userInputList[1] in ["right", "righ", "rig", "ri", "r"]:
							STR_TARGET_WEAPON = "Right"
							STR_TARGET_AMMO = None
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
						
						# Reload TargetWeapon #
						elif len(userInputList) > 1:
							STR_TARGET_WEAPON = ' '.join(userInputList[1::])
							STR_TARGET_AMMO = None
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
							
						# Reload #
						elif len(userInputList) == 1:
							STR_TARGET_WEAPON = None
							STR_TARGET_AMMO = None
							GameProcess.userReloadWeapon(self.dataGame.dataPlayer, STR_TARGET_WEAPON, STR_TARGET_AMMO)
							
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["unload", "unloa", "unlo", "unl", "un"]:
					
						# Unload Left #
						if len(userInputList) == 2 and userInputList[1] in ["left", "lef", "le", "l"]:
							STR_TARGET = "Left"
							GameProcess.userUnloadWeapon(self.dataGame.dataPlayer, STR_TARGET)
						
						# Unload Right #
						elif len(userInputList) == 2 and userInputList[1] in ["right", "righ", "rig", "ri", "r"]:
							STR_TARGET = "Right"
							GameProcess.userUnloadWeapon(self.dataGame.dataPlayer, STR_TARGET)
						
						# Unload All #
						elif len(userInputList) == 2 and userInputList[1] == "all":
							STR_TARGET = "All"
							GameProcess.userUnloadWeapon(self.dataGame.dataPlayer, STR_TARGET)
						
						# Unload TargetWeapon #
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							GameProcess.userUnloadWeapon(self.dataGame.dataPlayer, STR_TARGET)
						
						# Unload #
						elif len(userInputList) == 1:
							STR_TARGET = None
							GameProcess.userUnloadWeapon(self.dataGame.dataPlayer, STR_TARGET)
							
						inputProcessed = True
				
				# User Input - Player Commands #
				if True:
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["inventory", "inv", "in", "i"]:
						self.dataGame.dataPlayer.displayInventory()
						inputProcessed = True
					
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["gear", "gea", "equipment", "equipmen", "equipme", "equipm", "equip", "equi", "equ", "eq"]:
						self.dataGame.dataPlayer.displayGear()
						inputProcessed = True
					
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["skills", "skill", "skil", "ski", "sk"]:
						self.dataGame.dataPlayer.displaySkills()
						inputProcessed = True
					
				# User Input - Mob Commands #
				if True:
					if not inputProcessed and userInputList[0] in ["target", "targe", "targ", "tar", "ta"] and ((len(userInputList) > 2 and userInputList[-1] in ["north", "n", "east", "e", "south", "s", "west", "w"]) or (len(userInputList) > 3 and userInputList[-2] in ["north", "n", "east", "e", "south", "s", "west", "w"] and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0)):
						
						# Get Target Dir & End Index #
						if True:
							if userInputList[-1] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
								inputDir = userInputList[-1]
								endIndex = -1
							else:
								inputDir = userInputList[-2]
								endIndex = -2
							targetDir = None
							if inputDir in ["north", "n"] : targetDir = "North"
							elif inputDir in ["east", "e"] : targetDir = "East"
							elif inputDir in ["south", "s"] : targetDir = "South"
							elif inputDir in ["west", "w"] : targetDir = "West"
						
						# Target All @Dir / TargetRoomDistance #
						if userInputList[1] == "all" and userInputList[2] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							GameProcess.userTargetMobInRoom(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Target All Mob @Dir / TargetRoomDistance #
						elif userInputList[1] == "all" and userInputList[2] not in ["north", "n", "east", "e", "south", "s", "west", "w"] and not Utility.stringIsNumber(userInputList[2]):
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2:endIndex])
							TARGET_INDEX = -1
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							GameProcess.userTargetMobInRoom(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Target Count# Mob @Dir / TargetRoomDistance #
						elif len(userInputList) > 3 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2:endIndex])
							TARGET_INDEX = -1
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							GameProcess.userTargetMobInRoom(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Target Mob @Index @Dir / TargetRoomDistance #
						elif len(userInputList) > 3 and Utility.stringIsNumber(userInputList[endIndex-1]) and int(userInputList[endIndex-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:endIndex-1])
							TARGET_INDEX = int(userInputList[endIndex-1]) - 1
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							GameProcess.userTargetMobInRoom(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Target Mob @Dir / TargetRoomDistance #
						else:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:endIndex])
							TARGET_INDEX = 0
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							GameProcess.userTargetMobInRoom(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["target", "targe", "targ", "tar", "ta"]:
					
						# Target All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = "All"
							TARGET_INDEX = -1
							GameProcess.userTargetMob(currentRoom, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Target All Mob #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							TARGET_COUNT = "All"
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userTargetMob(currentRoom, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
					
						# Target Count# Mob #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							TARGET_INDEX = -1
							GameProcess.userTargetMob(currentRoom, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
					
						# Target Mob @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userTargetMob(currentRoom, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
						
						# Target Mob #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userTargetMob(currentRoom, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
							
						else:
							strInput = "Target"
							if userInputList[0] in ["focus", "focu", "foc"] : strInput = "Focus on"
							Console.addDisplayLineToDictList(strInput + " who?", str(len(strInput)) + "w4w1y")
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["untarget", "untarge", "untarg", "untar", "unta", "unt", "un"]:
						
						# Untarget All #
						if len(userInputList) == 2 and userInputList[1] == "all":
							GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, None, None, None, "Stop Targeting All")
							
						# Untarget All Mob #
						elif len(userInputList) > 2 and userInputList[1] == "all":
							STR_TARGET = ' '.join(userInputList[2::])
							GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, None, STR_TARGET, None, "Stop Targeting All Mob")
							
						# Untarget Count# #
						elif len(userInputList) == 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							TARGET_COUNT = int(userInputList[-1])
							GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, None, None, "Stop Targeting Count#")
							
						# Untarget Count# Mob #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[1]) and int(userInputList[1]) > 0:
							TARGET_COUNT = int(userInputList[1])
							STR_TARGET = ' '.join(userInputList[2::])
							GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, None, "Stop Targeting Count# Mob")
							
						# Untarget Mob @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, None, STR_TARGET, TARGET_INDEX, "Stop Targeting Mob @Index")
							
						# Untarget Mob #
						elif len(userInputList) > 1:
							TARGET_COUNT = 1
							STR_TARGET = ' '.join(userInputList[1::])
							GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, TARGET_COUNT, STR_TARGET, None, "Stop Targeting Mob")
							
						# Untarget #
						else : GameProcess.userStopTargeting(currentArea, self.dataGame.dataPlayer, None, None, None, "Stop Targeting")
							
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["tame", "tam"]:
					
						# Tame Mob @Index #
						if len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userTame(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX)
						
						# Tame Mob #
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userTame(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX)
						
						# Tame #
						else:
							GameProcess.userTame(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, None, None)
							
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["disband", "disban", "disba", "disb", "dis"]:
					
						# Disband Mob @Index #
						if len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							GameProcess.userDisband(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX)
						
						# Disband Mob #
						elif len(userInputList) > 1 and ' '.join(userInputList[1::]) not in ["all", "group"]:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							GameProcess.userDisband(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX)
						
						# Disband #
						else:
							GameProcess.userDisband(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, "All", None)
							
						inputProcessed = True
					
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["list", "lis", "li"]:
						DataMob.listWares(currentArea, self.dataGame.dataPlayer)
						inputProcessed = True
				
				# User Input - Combat Commands #
				if True:
					if not inputProcessed and userInputList[0] in ["attack", "attac", "atta", "att", "at", "a"]:
						
						# Get Input Dir & End Index #
						if True:
							inputDir = None
							endIndex = None
							if len(userInputList) > 2 and userInputList[-1] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
								inputDir = userInputList[-1]
								endIndex = -1
							elif len(userInputList) > 3 and userInputList[-2] in ["north", "n", "east", "e", "south", "s", "west", "w"] and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
								inputDir = userInputList[-2]
								endIndex = -2
							if inputDir != None:
								targetDir = None
								if inputDir in ["north", "n"] : targetDir = "North"
								elif inputDir in ["east", "e"] : targetDir = "East"
								elif inputDir in ["south", "s"] : targetDir = "South"
								elif inputDir in ["west", "w"] : targetDir = "West"
							
						# Attack Target @Index @Dir / @TargetRoomDistance #
						if endIndex != None and len(userInputList) > 3 and Utility.stringIsNumber(userInputList[endIndex-1]) and int(userInputList[endIndex-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:endIndex-1])
							TARGET_INDEX = int(userInputList[endIndex-1]) - 1
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							DataCombat.userAttack(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Attack Target @Dir / @TargetRoomDistance #
						elif endIndex != None and len(userInputList) > 2:
							STR_TARGET = ' '.join(userInputList[1:endIndex])
							TARGET_INDEX = 0
							TARGET_ROOM_DISTANCE = 1
							if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
							DataCombat.userAttack(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Attack Target @Index #
						elif len(userInputList) > 2 and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							STR_TARGET = ' '.join(userInputList[1:-1])
							TARGET_INDEX = int(userInputList[-1]) - 1
							TARGET_ROOM_DISTANCE = None
							targetDir = None
							DataCombat.userAttack(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
						
						# Attack Target #
						elif len(userInputList) > 1:
							STR_TARGET = ' '.join(userInputList[1::])
							TARGET_INDEX = 0
							TARGET_ROOM_DISTANCE = None
							targetDir = None
							DataCombat.userAttack(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
							
						# Attack #
						else:
							STR_TARGET = None
							TARGET_INDEX = None
							TARGET_ROOM_DISTANCE = None
							targetDir = None
							DataCombat.userAttack(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
					
						inputProcessed = True
					
					if not inputProcessed and userInputList[0] in ["cast", "cas", "ca", "c"]:
					
						# Get Input Dir & End Index #
						if True:
							inputDir = None
							targetDir = None
							endIndex = None
							targetMobStartIndex = None
							
							if len(userInputList) > 2 and userInputList[-1] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
								inputDir = userInputList[-1]
								endIndex = -1
							elif len(userInputList) > 3 and userInputList[-2] in ["north", "n", "east", "e", "south", "s", "west", "w"] and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
								inputDir = userInputList[-2]
								endIndex = -2
							if inputDir != None:
								if inputDir in ["north", "n"] : targetDir = "North"
								elif inputDir in ["east", "e"] : targetDir = "East"
								elif inputDir in ["south", "s"] : targetDir = "South"
								elif inputDir in ["west", "w"] : targetDir = "West"
					
						# Function: Get Spell & Target Mob Index #
						def getTargetMobIndex(TARGET_STRING):
							targetMobStartIndex = -1
							targetStringList = TARGET_STRING.split()
							sNumList = range(len(targetStringList))
							del sNumList[0]
							if len(sNumList) == 0 : sNumList = [1]
							else : sNumList.append(sNumList[-1]+1)
							sNumList.reverse()
						
							for sNum in sNumList:
								tempString = ' '.join(targetStringList[0:sNum])
								if tempString in Config.SPELL_MASTER_KEY_LIST:
									targetMobStartIndex = sNum + 1
									break
						
							return targetMobStartIndex
						
						# Cast Spell All/Self @Dir/@Num #
						if not inputProcessed and len(userInputList) > 3 and endIndex != None and userInputList[endIndex-1] in ["all", "self"]:
							STR_TARGET_SPELL = ' '.join(userInputList[1:endIndex-1])
							if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
								STR_TARGET_MOB = userInputList[endIndex-1][0].upper() + userInputList[endIndex-1][1::]
								TARGET_INDEX = -1
								TARGET_ROOM_DISTANCE = 1
								if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
								DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
								inputProcessed = True
						
						# Cast Spell @Target @Index @Dir/@Num #
						if not inputProcessed and endIndex != None and Utility.stringIsNumber(userInputList[endIndex-1]) and int(userInputList[endIndex-1]) > 0:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[1:endIndex]))
							if targetMobStartIndex != -1 and len(userInputList[targetMobStartIndex::]) > 2:
								STR_TARGET_SPELL = ' '.join(userInputList[1:targetMobStartIndex])
								if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex:endIndex-1])
									TARGET_INDEX = int(userInputList[endIndex-1]) - 1
									TARGET_ROOM_DISTANCE = 1
									if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
									DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
									inputProcessed = True
						
						# Cast Spell @Dir/@Num #
						if not inputProcessed and len(userInputList) > 2 and endIndex != None:
							STR_TARGET_SPELL = ' '.join(userInputList[1:endIndex])
							if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
								STR_TARGET_MOB = None
								TARGET_INDEX = -1
								TARGET_ROOM_DISTANCE = 1
								if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
								DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
								inputProcessed = True
						
						# Cast Spell @Target @Dir/@Num #
						if not inputProcessed and endIndex != None:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[1:endIndex]))
							if targetMobStartIndex != -1 and len(userInputList[targetMobStartIndex::]) > 1:
								STR_TARGET_SPELL = ' '.join(userInputList[1:targetMobStartIndex])
								if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex:endIndex])
									TARGET_INDEX = 0
									TARGET_ROOM_DISTANCE = 1
									if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
									DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
									inputProcessed = True
								
						# Cast Spell All/Self #
						if not inputProcessed and len(userInputList) > 2 and endIndex == None and userInputList[-1] in ["all", "self"]:
							STR_TARGET_SPELL = ' '.join(userInputList[1:-1])
							if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
								STR_TARGET_MOB = userInputList[-1][0].upper() + userInputList[-1][1::]
								TARGET_INDEX = -1
								TARGET_ROOM_DISTANCE = 0
								DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
								inputProcessed = True
						
						# Cast Spell #
						if not inputProcessed and len(userInputList) > 1 and ' '.join(userInputList[1::]) in Config.SPELL_MASTER_KEY_LIST:
							STR_TARGET_SPELL = ' '.join(userInputList[1::])
							STR_TARGET_MOB = None
							TARGET_INDEX = -1
							TARGET_ROOM_DISTANCE = None
							DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
							inputProcessed = True
						
						# Cast Spell @Target @Index #
						if not inputProcessed and len(userInputList) > 3 and endIndex == None and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[1:-1]))
							if targetMobStartIndex != -1 and len(userInputList[targetMobStartIndex::]) > 1:
								STR_TARGET_SPELL = ' '.join(userInputList[1:targetMobStartIndex])
								if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex:-1])
									TARGET_INDEX = int(userInputList[-1]) - 1
									TARGET_ROOM_DISTANCE = 0
									DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
									inputProcessed = True
								
						# Cast Spell @Target #
						if not inputProcessed and len(userInputList) > 2 and endIndex == None:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[1::]))
							if targetMobStartIndex != -1:
								STR_TARGET_SPELL = ' '.join(userInputList[1:targetMobStartIndex])
								if STR_TARGET_SPELL in Config.SPELL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex::])
									TARGET_INDEX = 0
									TARGET_ROOM_DISTANCE = 0
									DataCombat.userUseSkillEntity(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SPELL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE, "Cast Spell")
									inputProcessed = True
							
						# Cast #
						if not inputProcessed and len(userInputList) == 1:
							Console.addDisplayLineToDictList("Cast what?", "9w1y")
							inputProcessed = True
							
						if not inputProcessed:
							Console.addDisplayLineToDictList("That is not a known spell.", "25w1y")
							inputProcessed = True
						
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["stop", "sto", "st"]:
						DataCombat.targetStopAttack(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, self.dataGame.dataPlayer)
						inputProcessed = True
					
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["parry", "parr", "par", "pa", "p"]:
						DataCombat.targetParry(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, self.dataGame.dataPlayer)
						inputProcessed = True
					
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in ["dodge", "dodg", "dod", "do", "d"]:
						DataCombat.targetDodge(self.dataGame.solarSystemDict, self.dataGame.dataPlayer, self.dataGame.dataPlayer)
						inputProcessed = True
					
					if not inputProcessed: # Skill @Target @Index @Dir/@Num #
						
						# Get Input Dir & End Index #
						if True:
							inputDir = None
							targetDir = None
							endIndex = None
							targetMobStartIndex = None
							
							if len(userInputList) > 1 and userInputList[-1] in ["north", "n", "east", "e", "south", "s", "west", "w"]:
								inputDir = userInputList[-1]
								endIndex = -1
							elif len(userInputList) > 2 and userInputList[-2] in ["north", "n", "east", "e", "south", "s", "west", "w"] and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
								inputDir = userInputList[-2]
								endIndex = -2
							if inputDir != None:
								if inputDir in ["north", "n"] : targetDir = "North"
								elif inputDir in ["east", "e"] : targetDir = "East"
								elif inputDir in ["south", "s"] : targetDir = "South"
								elif inputDir in ["west", "w"] : targetDir = "West"
					
						# Function: Get Skill & Target Mob Index #
						def getTargetMobIndex(TARGET_STRING):
							targetMobStartIndex = -1
							targetStringList = TARGET_STRING.split()
							sNumList = range(len(targetStringList))
							del sNumList[0]
							if len(sNumList) == 0 : sNumList = [1]
							else : sNumList.append(sNumList[-1]+1)
							sNumList.reverse()
						
							for sNum in sNumList:
								tempString = ' '.join(targetStringList[0:sNum])
								if tempString in Config.SKILL_MASTER_KEY_LIST:
									targetMobStartIndex = sNum
									break
						
							return targetMobStartIndex
						
						# Skill All/Self @Dir/@Num #
						if not inputProcessed and len(userInputList) > 2 and endIndex != None and userInputList[endIndex-1] in ["all", "self"]:
							STR_TARGET_SKILL = ' '.join(userInputList[0:endIndex-1])
							if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
								STR_TARGET_MOB = userInputList[endIndex-1][0].upper() + userInputList[endIndex-1][1::]
								TARGET_INDEX = -1
								TARGET_ROOM_DISTANCE = 1
								if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
								GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
								inputProcessed = True
						
						# Skill @Target @Index @Dir/@Num #
						if not inputProcessed and endIndex != None and Utility.stringIsNumber(userInputList[endIndex-1]) and int(userInputList[endIndex-1]) > 0:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[0:endIndex]))
							if targetMobStartIndex != -1 and len(userInputList[targetMobStartIndex::]) > 2:
								STR_TARGET_SKILL = ' '.join(userInputList[0:targetMobStartIndex])
								if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex:endIndex-1])
									TARGET_INDEX = int(userInputList[endIndex-1]) - 1
									TARGET_ROOM_DISTANCE = 1
									if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
									GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
									inputProcessed = True
						
						# Skill @Dir/@Num #
						if not inputProcessed and len(userInputList) > 1 and endIndex != None:
							STR_TARGET_SKILL = ' '.join(userInputList[0:endIndex])
							if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
								STR_TARGET_MOB = None
								TARGET_INDEX = -1
								TARGET_ROOM_DISTANCE = 1
								if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
								GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
								inputProcessed = True
						
						# Skill @Target @Dir/@Num #
						if not inputProcessed and endIndex != None:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[0:endIndex]))
							if targetMobStartIndex != -1 and len(userInputList[targetMobStartIndex::]) > 1:
								STR_TARGET_SKILL = ' '.join(userInputList[0:targetMobStartIndex])
								if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex:endIndex])
									TARGET_INDEX = 0
									TARGET_ROOM_DISTANCE = 1
									if Utility.stringIsNumber(userInputList[-1]) : TARGET_ROOM_DISTANCE = int(userInputList[-1])
									GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
									inputProcessed = True
								
						# Skill All/Self #
						if not inputProcessed and len(userInputList) > 1 and endIndex == None and userInputList[-1] in ["all", "self"]:
							STR_TARGET_SKILL = ' '.join(userInputList[0:-1])
							if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
								STR_TARGET_MOB = userInputList[-1][0].upper() + userInputList[-1][1::]
								TARGET_INDEX = -1
								TARGET_ROOM_DISTANCE = 0
								GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
								inputProcessed = True
								
						# Skill #
						if not inputProcessed and ' '.join(userInputList) in Config.SKILL_MASTER_KEY_LIST:
							STR_TARGET_SKILL = ' '.join(userInputList)
							STR_TARGET_MOB = None
							TARGET_INDEX = -1
							TARGET_ROOM_DISTANCE = None
							GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
							inputProcessed = True
						
						# Skill @Target @Index #
						if not inputProcessed and len(userInputList) > 2 and endIndex == None and Utility.stringIsNumber(userInputList[-1]) and int(userInputList[-1]) > 0:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[0:-1]))
							if targetMobStartIndex != -1 and len(userInputList[targetMobStartIndex::]) > 1:
								STR_TARGET_SKILL = ' '.join(userInputList[0:targetMobStartIndex])
								if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex:-1])
									TARGET_INDEX = int(userInputList[-1]) - 1
									TARGET_ROOM_DISTANCE = 0
									GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
									inputProcessed = True
								
						# Skill @Target #
						if not inputProcessed and len(userInputList) > 1 and endIndex == None:
							targetMobStartIndex = getTargetMobIndex(' '.join(userInputList[0::]))
							if targetMobStartIndex != -1:
								STR_TARGET_SKILL = ' '.join(userInputList[0:targetMobStartIndex])
								if STR_TARGET_SKILL in Config.SKILL_MASTER_KEY_LIST:
									STR_TARGET_MOB = ' '.join(userInputList[targetMobStartIndex::])
									TARGET_INDEX = 0
									TARGET_ROOM_DISTANCE = 0
									GameProcess.userUseSkill(self.dataGame.solarSystemDict, currentArea, self.dataGame.dataPlayer, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, targetDir, TARGET_ROOM_DISTANCE)
									inputProcessed = True
									
				# Other Commands #
				if True:
					
					# Manifest - God Commands #
					if not inputProcessed and userInputList[0] in ["manifest", "manifes", "manife", "manif", "mani", "man"]:
						
						if len(userInputList) > 1:
							GameProcess.userGodCommand(currentArea, self.dataGame.solarSystemDict, self.dataGame.dataPlayer, userInputList[1::])
							
						else:
							Console.addDisplayLineToDictList("Manifest what?")
						
						inputProcessed = True
					
					# Emotes #
					if not inputProcessed and len(userInputList) == 1 and userInputList[0] in Config.EMOTE_DICT:
						Console.addDisplayLineToDictList(Config.EMOTE_DICT[userInputList[0]]["Display Line"], Config.EMOTE_DICT[userInputList[0]]["Color Code"])
						inputProcessed = True
					
				if not inputProcessed:
					Console.addDisplayLineToDictList("Huh?", "3w1y")
						
			self.dataScreen.frmMain.processInput()
			
