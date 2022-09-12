import pygame, os, random, Config, Utility, SidescreenRoom, SidescreenPlayerStats, SidescreenMap, SidescreenTargetStats, SidescreenPlayerUtility, SidescreenPlayerUtilityBar, SidescreenBottomBar, SidescreenDebug
from pygame import *
from Data import DataWorld
from Elements import Console, Form

class LoadScreenGame:

	def __init__(self, WINDOW):
	
		self.level = "Game"
		self.displayTVBorder = False
		self.displayDebug = False
		self.displayFPS = True
	
		# Interactive Elements #
		self.cnslMain = None
		self.frmMain = None
		
		# Sidescreens #
		self.sidescreenBottomBar = None
		self.sidescreenRoom = None
		self.sidescreenTargetStats = None
		self.sidescreenMap = None
		self.sidescreenPlayerStats = None
		self.sidescreenPlayerUtility = None
		self.sidescreenPlayerUtilityBar = None
		self.sidescreenDebug = None
		
		# Surfaces #
		self.surfaceDebug = pygame.Surface([540, 280], pygame.SRCALPHA, 32)
		
		# Images #
		self.imageDict = self.loadImageDict(WINDOW)
		self.loadElements()
		
	def loadElements(self):
	
		LEFT_X_MARGIN = int(Config.SCREEN_SIZE[0] * .23)
				
		# Main Console #
		self.cnslMain = Console.LoadConsole("cnslMain", [LEFT_X_MARGIN, 377], [68, 15], self.imageDict["Interface"], {"Console Width Buffer":6,
																													  "Line Height Buffer":0})
		loadConsoleIntroMessage(self.cnslMain)
		
		# Main Form #
		self.frmMain = Form.LoadForm("frmMain", [self.cnslMain.rect.left, self.cnslMain.rect.bottom], self.imageDict["Interface"], {"Max Width":75,
																																    "Width Buffer":8,
																																    "Height Buffer":6})
																							 
		# Side Screens #
		if True:
			
			# Center #
			self.sidescreenBottomBar = SidescreenBottomBar.LoadSidescreenBottomBar([Config.SCREEN_SIZE[0], 29])
			
			# Left Side #
			self.sidescreenRoom = SidescreenRoom.LoadSidescreenRoom([Config.SCREEN_SIZE[0] - LEFT_X_MARGIN, 377])
			self.sidescreenTargetStats = SidescreenTargetStats.LoadSidescreenTargetStats(self.sidescreenRoom.rect.height, [LEFT_X_MARGIN, 104], self.imageDict["Interface"])
			
			# Right Side #
			self.sidescreenMap = SidescreenMap.LoadSidescreenMap([LEFT_X_MARGIN, 273])
			self.sidescreenPlayerStats = SidescreenPlayerStats.LoadSidescreenPlayerStats([self.sidescreenMap.displayLoc[0], self.sidescreenMap.rect.height], [self.sidescreenMap.rect.width, 104], self.imageDict["Interface"])
			self.sidescreenPlayerUtility = SidescreenPlayerUtility.LoadSidescreenPlayerUtility([self.sidescreenMap.displayLoc[0], self.sidescreenPlayerStats.rect.top + self.sidescreenPlayerStats.rect.height], [Config.SCREEN_SIZE[0] - self.sidescreenMap.displayLoc[0], 285])
			self.sidescreenPlayerUtilityBar = SidescreenPlayerUtilityBar.LoadSidescreenPlayerUtilityBar([self.sidescreenPlayerUtility.rect.left, self.sidescreenPlayerUtility.rect.bottom], [self.sidescreenPlayerUtility.rect.width, 29], self.imageDict["Interface"])
			
			self.sidescreenDebug = SidescreenDebug.LoadSidescreenDebug()
			
	def loadImageDict(self, WINDOW):
	
		imageDict = {}
		
		# Backgrounds #
		if True:
			imageDict["Background"] = {}
			for fileDir in os.listdir("../Image/Background/"):
				if fileDir[-4::] == ".png":
					pathID = fileDir[0:-4]
					itemID = fileDir[0:-4].replace("_", " ")
					
					# Create Day/Dawn/Night Images #
					if itemID.split()[0] in ["Sky", "Ground", "Mountains", "Trees"]:
						imageDict["Background"][itemID + " Day"] = pygame.image.load("../Image/Background/" + pathID + ".png").convert_alpha()
						
						imageDict["Background"][itemID + " Dawn"] = pygame.image.load("../Image/Background/" + pathID + ".png").convert_alpha()
						imageDict["Background"][itemID + " Dawn"].fill([100, 110, 50], None, pygame.BLEND_RGB_SUB)
						
						imageDict["Background"][itemID + " Night"] = pygame.image.load("../Image/Background/" + pathID + ".png").convert_alpha()
						imageDict["Background"][itemID + " Night"].fill([220, 220, 150], None, pygame.BLEND_RGB_SUB)
					
					else:
						imageDict["Background"][itemID] = pygame.image.load("../Image/Background/" + pathID + ".png").convert_alpha()
					
		# Interface #
		if True:
			imageDict["Interface"] = {}
			for fileDir in os.listdir("../Image/Interface/"):
				if fileDir[-4::] == ".png":
					pathID = fileDir[0:-4]
					itemID = fileDir[0:-4].replace("_", " ")
					imageDict["Interface"][itemID] = pygame.image.load("../Image/Interface/" + pathID + ".png").convert_alpha()
					
					# Hover Arrow #
					if itemID in ["Arrow Left", "Arrow Right"]:
						imageDict["Interface"][itemID + " Hover"] = pygame.image.load("../Image/Interface/" + pathID + ".png").convert_alpha()
						imageDict["Interface"][itemID + " Hover"].fill([0, 75, 0], None, pygame.BLEND_RGB_SUB)
			
			# Action Message Box #
			imageDict["Interface"]["Action Box"] = pygame.Surface([75, 20], pygame.SRCALPHA, 32)
			pygame.draw.rect(imageDict["Interface"]["Action Box"], [20, 20, 120], [2, 2, 71, 16])
			Utility.outline(imageDict["Interface"]["Action Box"], [100, 100, 100], [1, 1], [73, 18], 3)
			Utility.outline(imageDict["Interface"]["Action Box"], [200, 200, 200], [1, 1], [73, 18])
			
			# Item Box #
			imageDict["Interface"]["Item Box"] = pygame.Surface([125, 16], pygame.SRCALPHA, 32)
			pygame.draw.rect(imageDict["Interface"]["Item Box"], [20, 20, 120], [2, 2, 121, 12])
			Utility.outline(imageDict["Interface"]["Item Box"], [100, 100, 100], [1, 1], [123, 14], 3)
			Utility.outline(imageDict["Interface"]["Item Box"], [200, 200, 200], [1, 1], [123, 14])
			
			# Numbers #
			imageDict["Interface"]["Numbers Outline"] = []
			for i in range(10):
				surfaceNumber = Utility.renderOutlineText(str(i), Config.FONT_ROMAN_20)
				imageDict["Interface"]["Numbers Outline"].append(surfaceNumber)
			
		# Entities #
		imageDict["Entity"] = {}
		for fileDir in os.listdir("../Image/Entity/"):
			if fileDir[-4::] == ".png":
				pathID = fileDir[0:-4]
				entityID = fileDir[0:-4].replace("_", " ")
				
				imageDict["Entity"][entityID] = pygame.image.load("../Image/Entity/" + pathID + ".png").convert_alpha()
				
				imageDict["Entity"][entityID + " Red"] = pygame.image.load("../Image/Entity/" + pathID + ".png").convert_alpha()
				imageDict["Entity"][entityID + " Red"].fill([200, 0, 0], None, pygame.BLEND_RGB_ADD)
				imageDict["Entity"][entityID + " Red"].fill([0, 200, 200], None, pygame.BLEND_RGB_SUB)
			
				imageDict["Entity"][entityID + " White"] = pygame.image.load("../Image/Entity/" + pathID + ".png").convert_alpha()
				imageDict["Entity"][entityID + " White"].fill([200, 200, 200], None, pygame.BLEND_RGB_ADD)
				
				imageDict["Entity"][entityID + " Dire"] = pygame.image.load("../Image/Entity/" + pathID + ".png").convert_alpha()
				imageDict["Entity"][entityID + " Dire"].fill([30, 55, 30], None, pygame.BLEND_RGB_SUB)
				
		# Items #
		imageDict["Item"] = {}
		for fileDir in os.listdir("../Image/Item/"):
			if fileDir[-4::] == ".png":
				pathID = fileDir[0:-4]
				itemID = fileDir[0:-4].replace("_", " ")
				imageDict["Item"][itemID] = pygame.image.load("../Image/Item/" + pathID + ".png").convert_alpha()
		
		return imageDict
		
	def updateScreenAnimations(self, TICK_MILLISECOND, PLAYER_SOLAR_SYSTEM, DATA_PLAYER):
	
		# Get Data #
		if True:
			drawRoomList = []
			delDictList = []
			delAnimationList = []
			drawPlayerStats = False
	
		# Update Animation Timers #
		if self.sidescreenRoom.displayRoom != None:
			for roomMob in self.sidescreenRoom.displayRoom.mobList + [DATA_PLAYER]:
				deleteAnimationDict = {"Target Mob":roomMob, "Delete List":[]}
				deleteAnimationInListDict = {"Target Mob":roomMob, "Delete Dict":{}}
				
				for animationDictID in roomMob.animationDict:
				
					# Animation List #
					if type(roomMob.animationDict[animationDictID]) == list:
						for aNum, animationListDict in enumerate(roomMob.animationDict[animationDictID]):
							animationListDict["Timer"] -= 1
							
							# Damage Numbers #
							if animationDictID == "Damage Number List":
								animationListDict["Bounce Velocity"] -= animationListDict["Velocity Decrease"]
								animationListDict["Draw Y Loc"] -= animationListDict["Bounce Velocity"]
								
								if animationListDict["Bounce Count"] >= 3:
									animationListDict["Draw Y Loc"] = 0
								
								elif animationListDict["Draw Y Loc"] > 0:
									animationListDict["Bounce Velocity"] = 5.0
									animationListDict["Velocity Decrease"] *= 1.7
									animationListDict["Bounce Count"] += 1
									animationListDict["Draw Y Loc"] = 0
									if "Background Bottom" not in drawRoomList : drawRoomList.append("Background Bottom")
								
								if TICK_MILLISECOND % 5 == 0:
									if "Background Bottom" not in drawRoomList : drawRoomList.append("Background Bottom")
							
							# Timer == 0 #
							if animationListDict["Timer"] <= 0:
								if "Current Step" in animationListDict:
									pass
								else:
									if animationDictID in deleteAnimationInListDict["Delete Dict"]:
										deleteAnimationInListDict["Delete Dict"][animationDictID].append(aNum)
									else : deleteAnimationInListDict["Delete Dict"][animationDictID] = [aNum]
										
					# Single Animation #
					else:
						roomMob.animationDict[animationDictID]["Timer"] -= 1
						if roomMob.animationDict[animationDictID]["Timer"] <= 0:
							
							# Step Animation & Add Finished Animations To Delete List #
							if "Current Step" in roomMob.animationDict[animationDictID]:
								roomMob.animationDict[animationDictID]["Timer"] = roomMob.animationDict[animationDictID]["Timer Start"]
								roomMob.animationDict[animationDictID]["Current Step"] += 1
								if roomMob.animationDict[animationDictID]["Current Step"] > roomMob.animationDict[animationDictID]["Max Step"]:
									deleteAnimationDict["Delete List"].append(animationDictID)
							else : deleteAnimationDict["Delete List"].append(animationDictID)
							
							# Update Draw Data #
							if roomMob.objectType == "Player" or roomMob in DATA_PLAYER.groupList:
								Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
							else : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
							
				if len(deleteAnimationDict["Delete List"]) > 0:
					delDictList.append(deleteAnimationDict)
					
					# Update Draw Data #
					if roomMob.objectType == "Player" or roomMob in DATA_PLAYER.groupList:
						Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
					else : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
					
				if len(deleteAnimationInListDict["Delete Dict"]) > 0:
					for animationDictID in deleteAnimationInListDict["Delete Dict"]:
						delList = deleteAnimationInListDict["Delete Dict"][animationDictID]
						delList.reverse()
						delAnimationList.append({"Target Mob":roomMob, "Animation ID":animationDictID, "Delete List":delList})
						
					# Update Draw Data #
					if roomMob.objectType == "Player" or roomMob in DATA_PLAYER.groupList:
						Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
					else : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
					
				# Update Action Bar Timer (Current Action Message Box) #
				if roomMob.currentAction != None and roomMob.currentAction["Type"] == "Attacking" and "Action Bar Timer" in roomMob.currentAction:
					roomMob.currentAction["Action Bar Timer"] += .019
					if roomMob.currentAction["Action Bar Timer"] > roomMob.currentAction["Attack Data"].attackTimer:
						roomMob.currentAction["Action Bar Timer"] = roomMob.currentAction["Attack Data"].attackTimer
					
					if TICK_MILLISECOND % 5 == 0:
						if "Background Bottom" not in drawRoomList : drawRoomList.append("Background Bottom")
						if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Attacking":
							Config.DRAW_SCREEN_DICT["Player Stats"] = True
					
		# Delete Animations #
		if True:
						
			# Delete Finished Animations #
			for delDict in delDictList:
				for animationDictID in delDict["Delete List"]:
					del delDict["Target Mob"].animationDict[animationDictID]
			
			# Delete Finished Animation Lists #
			for delDict in delAnimationList:
				for aNum in delDict["Delete List"]:
					del delDict["Target Mob"].animationDict[delDict["Animation ID"]][aNum]
			
		# Draw Room #
		if len(drawRoomList) > 0:
			for drawAreaID in drawRoomList:
				if "Room" in Config.DRAW_SCREEN_DICT and drawAreaID not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append(drawAreaID)
				elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = [drawAreaID]
					
	def draw(self, FPS, WINDOW, MOUSE, DATA_GAME):
		
		# Get Data #
		playerArea = DataWorld.getParentArea(DATA_GAME.solarSystemDict[DATA_GAME.dataPlayer.currentSolarSystem], DATA_GAME.dataPlayer)
		playerRoom = playerArea.roomDict[DATA_GAME.dataPlayer.currentRoom]
		
		# Draw Screens #
		if len(Config.DRAW_SCREEN_DICT) > 0:
				
			# Update Room Surfaces #
			if True:
				updateRoomSurfaceCheck = False
				if "Update Room Entity Surface" in Config.DRAW_SCREEN_DICT:
					self.sidescreenRoom.updateEntitySurface(DATA_GAME.dataPlayer, self.imageDict["Entity"], self.imageDict["Item"])
					updateRoomSurfaceCheck = True
				if "Update Room Group Entity Surface" in Config.DRAW_SCREEN_DICT:
					self.sidescreenRoom.updateGroupEntitySurface(DATA_GAME.dataPlayer, self.imageDict["Entity"], self.imageDict["Item"])
					updateRoomSurfaceCheck = True
				if updateRoomSurfaceCheck == True:
					if "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = ["Background Bottom"]
					elif "All" not in Config.DRAW_SCREEN_DICT["Room"] and "Background Bottom" not in Config.DRAW_SCREEN_DICT["Room"]:
						Config.DRAW_SCREEN_DICT["Room"].append("Background Bottom")
					
			# Center #
			if "cnslMain" in Config.DRAW_SCREEN_DICT:
				cnslDrawArea = "All"
				if Config.DRAW_SCREEN_DICT["cnslMain"] == "No Border" : cnslDrawArea = "No Border"
				self.cnslMain.draw(WINDOW, MOUSE, cnslDrawArea)
			if "frmMain" in Config.DRAW_SCREEN_DICT:
				self.frmMain.draw(WINDOW, MOUSE)
			if "Bottom Bar" in Config.DRAW_SCREEN_DICT:
				self.sidescreenBottomBar.draw(WINDOW, MOUSE)
				
			# Left Side #
			if "Room" in Config.DRAW_SCREEN_DICT:
				drawDataDict = {}
				if "Don't Clear Mouse Hover Targets" in Config.DRAW_SCREEN_DICT["Room"]:
					drawDataDict["Don't Clear Mouse Hover Targets"] = True
					delIndex = Config.DRAW_SCREEN_DICT["Room"].index("Don't Clear Mouse Hover Targets")
					del Config.DRAW_SCREEN_DICT["Room"][delIndex]
				drawDataDict["Draw List"] = Config.DRAW_SCREEN_DICT["Room"]
				
				playerPlanetDict = {}
				if DATA_GAME.dataPlayer.currentPlanet != None:
					playerPlanet = DATA_GAME.solarSystemDict[DATA_GAME.dataPlayer.currentSolarSystem].planetDict[DATA_GAME.dataPlayer.currentPlanet]
					playerPlanetDict = {"Minutes In Day":playerPlanet.currentMinutesInDay, "Dawn Minutes":playerPlanet.dawnMinutes, "Sunrise Minutes":playerPlanet.sunriseMinutes, "Dusk Minutes":playerPlanet.duskMinutes, "Sunset Minutes":playerPlanet.sunsetMinutes}
				
				self.sidescreenRoom.draw(drawDataDict, WINDOW, MOUSE, DATA_GAME.dataPlayer, playerPlanetDict, playerRoom, DATA_GAME.dataPlayer.mobTargetList, self.displayTVBorder, self.imageDict["Background"], self.imageDict["Interface"], self.imageDict["Entity"], self.imageDict["Item"])
				
			if "Target Stats" in Config.DRAW_SCREEN_DICT:
				targetEntity = None
				if MOUSE.hoverElement != None and hasattr(MOUSE.hoverElement, 'objectType') : targetEntity = MOUSE.hoverElement
				elif isinstance(MOUSE.hoverElement, dict) and "Hover Item Data" in MOUSE.hoverElement : targetEntity = MOUSE.hoverElement["Hover Item Data"]
				self.sidescreenTargetStats.draw(WINDOW, MOUSE, DATA_GAME.dataPlayer, targetEntity, self.imageDict["Interface"], self.imageDict["Entity"], self.imageDict["Item"])
				
			# Right Side #
			if "Map" in Config.DRAW_SCREEN_DICT:
				self.sidescreenMap.draw(WINDOW, DATA_GAME.dataPlayer, playerArea, self.imageDict["Interface"], self.displayTVBorder)
			if "Player Stats" in Config.DRAW_SCREEN_DICT:
				self.sidescreenPlayerStats.draw(WINDOW, DATA_GAME.dataPlayer)
			if "Player Utility" in Config.DRAW_SCREEN_DICT:
				self.sidescreenPlayerUtility.draw(WINDOW, MOUSE, DATA_GAME.dataPlayer, self.imageDict["Interface"])
			if "Player Utility Bar" in Config.DRAW_SCREEN_DICT:
				self.sidescreenPlayerUtilityBar.draw(WINDOW, MOUSE, self.imageDict["Interface"])
				
		# Debug Screen/FPS (Only Screens Constantly Updated) #
		if True:
			if self.displayDebug:
				self.sidescreenDebug.draw(DATA_GAME.tickSynch, WINDOW, DATA_GAME.solarSystemDict, DATA_GAME.dataPlayer)
				
			if self.displayFPS:
				pygame.draw.rect(WINDOW, [0, 0, 0], [self.sidescreenMap.rect.right-46, 0, 46, 13])
				Utility.writeFast(FPS, ["Right", 0], [200, 200, 200], Config.FONT_ROMAN_16, WINDOW)
				Config.DISPLAY_RECT_LIST.append(pygame.Rect([self.sidescreenMap.rect.right-46, 0, 46, 13]))
		
		# Display Screen #
		#pygame.transform.scale(SCREEN, Config.RESOLUTION_LIST[Config.RESOLUTION_INDEX], WINDOW)
		pygame.display.update(Config.DISPLAY_RECT_LIST)
		Config.DISPLAY_RECT_LIST = []
		Config.DRAW_SCREEN_DICT = {}
	
	def toggleScreen(self, ID_TARGET_SCREEN):
	
		if ID_TARGET_SCREEN == "Debug":
			if self.displayDebug == True : self.displayDebug = False
			elif self.displayDebug == False : self.displayDebug = True
			
			# Update Display Variables #
			if "Room" in Config.DRAW_SCREEN_DICT and "All" not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append("All")
			elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = ["All"]
					
		elif ID_TARGET_SCREEN == "FPS":
			if self.displayFPS == True : self.displayFPS = False
			elif self.displayFPS == False : self.displayFPS = True
			
			# Update Display Variables #
			Config.DRAW_SCREEN_DICT["Map"] = True
			
		elif ID_TARGET_SCREEN == "Border":
			if self.displayTVBorder == True : self.displayTVBorder = False
			elif self.displayTVBorder == False : self.displayTVBorder = True
	
	def getElementList(self):
	
		elementList = []
		
		elementList.append(self.cnslMain)
		elementList.append(self.sidescreenRoom)
		elementList.append(self.sidescreenMap)
		elementList.append(self.sidescreenPlayerUtility)
		elementList.append(self.sidescreenPlayerUtilityBar)
		
		return elementList
		
def loadConsoleIntroMessage(CONSOLE):

	titleList = ["",
				 "   vvv#### ##   v#######  #####  ####  #  ## #####  #### vvv####",
				 "   #  ## #  ##  ## ##  ## #   ^ ##  ## ## ## #   ^ ##  # #  ## #",
				 "      ##     ## ## ## ##^ ###   ##  ## ## ## ###    #v      ##",
				 "      ##      ###^ ##v^   ##  v ## #^  ## ## ##  v    ##    ##",
				 "      #^      ##   ##     ^####  ####v ^###  ^#### ####     #^",
				 "             ##    ##",
				 "           v##     #                                     "+Config.VERSION,
				 ""]

	cWhole = u"\u2588"
	cTop = u"\u2580"
	cBottom = u"\u2584"
	randomColor = random.choice(['r','o','y','g','c','b','v','m','w','a'])
	for lNum, line in enumerate(titleList):
		cString = ""
		for c in line:
			if c == '#' : cString = cString + cWhole
			elif c == '^' : cString = cString + cTop
			elif c == 'v' : cString = cString + cBottom
			elif c == ' ' : cString = cString + ' '
			else : cString = cString + c
		if lNum > 4 : targetColor = "dd" + randomColor
		elif lNum > 3 : targetColor = "d" + randomColor
		elif lNum > 1 : targetColor = randomColor
		else : targetColor = "l" + randomColor
		colorCode = str(len(cString)) + targetColor
		if lNum == len(titleList) - 2:
			colorCode = str(len(cString) - len(Config.VERSION)) + "dd" + randomColor + "2w1y" + str(len(Config.VERSION)) + "w"
		CONSOLE.addDisplayLine(cString, colorCode, [], False)
		
	for iNum in range(5):
		CONSOLE.addDisplayLine("")

def drawEntityStatBars(WINDOW, DATA_ENTITY, LOCATION, ACTION_BAR_WIDTH=141):

	# HP #
	hpString = str(DATA_ENTITY.currentHP)
	if DATA_ENTITY.maxHP != 0 : hpPercent = (DATA_ENTITY.currentHP + 0.0) / DATA_ENTITY.maxHP
	else : hpPercent = 0
	Utility.writeFast(hpString, [LOCATION[0], LOCATION[1]], [200, 200, 200], Config.FONT_ROMAN_12, WINDOW)
	pygame.draw.line(WINDOW, [170, 170, 170], [LOCATION[0] + 34, LOCATION[1] + 3], [LOCATION[0] + 34 + (ACTION_BAR_WIDTH * hpPercent), LOCATION[1] + 3], 5)
	
	# MP #
	mpString = str(DATA_ENTITY.currentMP)
	if DATA_ENTITY.maxMP != 0 : mpPercent = (DATA_ENTITY.currentMP + 0.0) / DATA_ENTITY.maxMP
	else : mpPercent = 0
	Utility.writeFast(mpString, [LOCATION[0], LOCATION[1] + 10], [200, 200, 200], Config.FONT_ROMAN_12, WINDOW)
	pygame.draw.line(WINDOW, [170, 170, 170], [LOCATION[0] + 34, LOCATION[1] + 11], [LOCATION[0] + 34 + (ACTION_BAR_WIDTH * mpPercent), LOCATION[1] + 11], 5)
	
	# Action Bar #
	if DATA_ENTITY.currentAction != None and DATA_ENTITY.currentAction["Type"] == "Attacking":
		if DATA_ENTITY.currentAction["Attack Data"].attackTimer != 0 : actionBarPercent = (DATA_ENTITY.currentAction["Action Bar Timer"]) / (DATA_ENTITY.currentAction["Attack Data"].attackTimer + 0.0)
		else : actionBarPercent = 0
		pygame.draw.line(WINDOW, [170, 170, 170], [LOCATION[0] + 34, LOCATION[1] + 17], [LOCATION[0] + 34 + (ACTION_BAR_WIDTH * actionBarPercent), LOCATION[1] + 17], 2)
