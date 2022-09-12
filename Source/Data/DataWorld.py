import pygame, os, math, copy, random, opensimplex, Config, Utility, DataItem, DataMob, DataCombat, DataSpaceshipModule
from Elements import Console, Caption
from pygame import *

class SolarSystem:

	def __init__(self, ID_SOLAR_SYSTEM):
	
		# ID Variables #
		self.idSolarSystem = ID_SOLAR_SYSTEM
		
		# Solar System Variables #
		self.spaceshipList = []
		self.planetDict = {}

	def getPlanetDataList(self):
	
		# Sort Planet List #
		planetDictList = []
		for planetName in self.planetDict:
			planet = self.planetDict[planetName]
			if planet.type == "Planet":
				planetDict = {"ID":planet.idPlanet, "Distance":planet.distanceFromCenter, "Key List":planet.keyList}
				insertCheck = False
				
				for pNum, tempPlanetDict in enumerate(planetDictList):
					if planetDict["Distance"] < tempPlanetDict["Distance"]:
						insertIndex = pNum
						insertCheck = True
						break
				if not insertCheck : planetDictList.append(planetDict)
				else : planetDictList.insert(insertIndex , planetDict)
	
		return planetDictList

	def getTargetSpaceship(self, TARGET_AREA_ID, TARGET_RANDOM_ID=None):
	
		targetSpaceship = None
		
		for spaceship in self.spaceshipList:
			if TARGET_AREA_ID == spaceship.idArea and (TARGET_RANDOM_ID == None or TARGET_RANDOM_ID == spaceship.idRandom):
				targetSpaceship = spaceship
				break
				
		return targetSpaceship
	
class Planet:

	def __init__(self, ID_SOLAR_SYSTEM, ID_PLANET, PLANET_TYPE="Star", TARGET_STAR=None, DISTANCE_FROM_CENTER=0, HOURS_IN_DAY=400, HOURS_IN_YEAR=1135296000, AXIAL_TILT=0, ATMOSPHERE_LEVEL=0, ATMOSPHERE_TYPE="Default"):
	
		# ID Variables #
		self.type = PLANET_TYPE
		self.idSolarSystem = ID_SOLAR_SYSTEM
		self.idPlanet = ID_PLANET
		self.tickSynch = 0
		self.keyList = []
		
		# Planet Variables #
		self.x = DISTANCE_FROM_CENTER
		self.y = 0
		
		self.targetStar = TARGET_STAR
		if PLANET_TYPE == "Star" : self.starBrightness = 1.0
		else : self.starBrightness = 0
		self.axialTilt = AXIAL_TILT
		self.distanceFromCenter = DISTANCE_FROM_CENTER
		self.atmosphereLevel = ATMOSPHERE_LEVEL
		self.atmosphereType = ATMOSPHERE_TYPE
		
		self.totalHoursInDay = HOURS_IN_DAY
		self.totalHoursInYear = HOURS_IN_YEAR
		
		self.currentMinutes = 0
		self.currentHours = 0
		self.currentDays = 0
		self.currentYears = 0
		self.currentMinutesInDay = 0
		self.currentHoursInYear = 0
		self.constantHoursInYear = 0
		
		self.nightMinutes = 0
		self.dawnMinutes = 0
		self.sunriseMinutes = 0
		self.duskMinutes = 0
		self.sunsetMinutes = 0
		self.nightCheck = True
		
		self.areaDict = {}
	
	# Update Functions #
	def update(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE):

		# Tick Timers #
		self.tickSynch += 1
		self.currentMinutes += 1
		self.currentMinutesInDay += 1
		targetDrawList = []
		
		# Night/Day Set/Message #
		if True:
			playerRoom = getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
			isPlayerPlanetCheck = (UPDATE_TYPE == "Default" and "In Spaceship" not in DATA_PLAYER.flags and \
								   DATA_PLAYER.currentSolarSystem == self.idSolarSystem and DATA_PLAYER.currentPlanet == self.idPlanet)
			
			if self.currentMinutesInDay == self.dawnMinutes:
				if isPlayerPlanetCheck and playerRoom.inside == False:
					Console.addDisplayLineToDictList("The sky begins to lighten.", "4w1dc2ddc11w1dw6ddw1y")
					if "All" not in targetDrawList : targetDrawList.append("All")
			elif self.currentMinutesInDay == self.sunriseMinutes:
				self.nightCheck = False
				if isPlayerPlanetCheck and playerRoom.inside == False:
					Console.addDisplayLineToDictList("The Sun rises over the horizon.", "4w1dy2ddy16w1dw6ddw1y")
					if "All" not in targetDrawList : targetDrawList.append("All")
			elif self.currentMinutesInDay == self.duskMinutes:
				if isPlayerPlanetCheck and playerRoom.inside == False:
					Console.addDisplayLineToDictList("The Sun begins to set.", "4w1dy2ddy11w1dw2ddw1y")	
					if "All" not in targetDrawList : targetDrawList.append("All")
			elif self.currentMinutesInDay == self.sunsetMinutes:
				self.nightCheck = True
				if isPlayerPlanetCheck and playerRoom.inside == False:
					Console.addDisplayLineToDictList("The Sun sinks beyond the horizon.", "4w1dy2ddy18w1dw6ddw1y")
					if "All" not in targetDrawList : targetDrawList.append("All")
	
		# Draw Background Top Check #
		if isPlayerPlanetCheck and "All" not in targetDrawList:
			targetDrawList.append("Background Top")
			
		# Update Timers #
		if self.currentMinutes >= 60:
			self.currentHours += 1
			self.currentHoursInYear += 1
			self.currentMinutes = 0
			
			if self.currentHours >= self.totalHoursInDay:
				self.currentDays += 1
				self.currentHours = 0
				self.currentMinutesInDay = 0
				self.updateNightDayMinutes()
				
				if self.currentHoursInYear >= self.totalHoursInYear:
					self.currentYears += 1
					self.currentDays = 0
					self.currentHoursInYear = 0
		
		# Draw Room #
		if len(targetDrawList) > 0:
			for drawAreaID in targetDrawList:
				if "Room" in Config.DRAW_SCREEN_DICT and drawAreaID not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append(drawAreaID)
				elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = [drawAreaID]
			Config.DRAW_SCREEN_DICT["Room"].append("Don't Clear Mouse Hover Targets")
					
	def updateNightDayMinutes(self):
	
		import math
		yearRatio = int(math.cos(math.radians(((self.currentHoursInYear + .0) / (self.totalHoursInYear)) * 360)) * 100) * -1
		equation = int(round(((((self.axialTilt + .0) / 100) * yearRatio) / 100) * (int(round((self.totalHoursInDay * 60) / 2)))))
		self.nightMinutes = (self.totalHoursInDay * 60) - (int(round(((self.totalHoursInDay * 60) / 2))) + equation)
		self.dawnMinutes = int(round(((self.nightMinutes + .0) / 3)))
		self.sunriseMinutes = int(round(((self.nightMinutes + .0) / 2)))
		self.duskMinutes = (int(round(((self.nightMinutes + .0) / 2))) + (((self.totalHoursInDay * 60) - self.nightMinutes)))
		self.sunsetMinutes = (int(round(((self.nightMinutes + .0) / 1.5))) + (((self.totalHoursInDay * 60) - self.nightMinutes)))
	
	def tickConstantTime(self):
	
		self.constantHoursInYear += 1
		if self.constantHoursInYear >= self.totalHoursInYear:
			self.constantHoursInYear = 0
			
		self.updateLocation()
	
	def setConstantTime(self):
	
		self.constantHoursInYear = self.currentHoursInYear
		self.updateLocation()
	
	def updateLocation(self):

		import math
		self.x = int(math.cos(math.radians(((self.constantHoursInYear+.0) / self.totalHoursInYear) * 360)) * self.distanceFromCenter)
		self.y = int(int(math.sin(math.radians(((self.constantHoursInYear+.0) / self.totalHoursInYear) * 360)) * self.distanceFromCenter) / 1.5)
	
	def setNightDay(self):
	
		self.nightCheck = True
		if self.currentMinutesInDay >= self.sunriseMinutes and self.currentMinutesInDay < self.sunsetMinutes:
			self.nightCheck = False
		
	def synchData(self, TICK_SYNCH):
	
		tickSeconds = TICK_SYNCH - self.tickSynch
		self.tickSynch = TICK_SYNCH
		
		# Minutes #
		self.currentMinutes += tickSeconds % 60
		if self.currentMinutes >= 60:
			self.currentHours += 1
			self.currentHoursInYear += 1
			self.currentMinutes -= 60
			
		# Hours, Days & Years #
		self.currentHours += tickSeconds / 60
		self.currentHoursInYear += tickSeconds / 60
		self.currentMinutesInDay += tickSeconds
		while self.currentHours >= self.totalHoursInDay:
			self.currentDays += 1
			self.currentHours -= self.totalHoursInDay
			
			if self.currentMinutesInDay >= self.totalHoursInDay * 60:
				self.currentMinutesInDay -= self.totalHoursInDay * 60
			
			if self.currentDays * self.totalHoursInDay >= self.totalHoursInYear:
				self.currentYears += 1
				self.currentDays -= self.totalHoursInYear / self.totalHoursInDay
				self.currentHoursInYear -= self.totalHoursInYear
			
		# Temp Hours #
		self.constantHoursInYear = self.currentHoursInYear
		self.updateLocation()
		
		self.updateNightDayMinutes()
		self.setNightDay()
		
	# Utility Functions #
	def getDateString(self):
	
		strDays = str(self.currentDays + 1)
		if len(strDays) == 1 : strDays = "0" + strDays
		strDate = strDays + "/" + str(self.totalHoursInYear / self.totalHoursInDay) + "/" + str(self.currentYears)
		
		return strDate
		
	def getTimeString(self):
	
		strHours = str(self.currentHours)
		if len(strHours) == 1 : strHours = "0" + strHours
		strMinutes = str(self.currentMinutes)
		if len(strMinutes) == 1 : strMinutes = "0" + strMinutes
		strTime = strHours + ":" + strMinutes
		
		return strTime
		
	def generateWorldMap(self, DATA_PLAYER, ID_SOLAR_SYSTEM, ITEM_IMAGE_DICT):
	
		# Get Data #
		if True:
			idArea = "World Map"
			areaWorldMap = Area(ID_SOLAR_SYSTEM, self.idPlanet, idArea)
			areaWorldMap.flags["Launch Pad Room List"] = [0]
		
		# Generate Map #
		for renderLayer in range(4):
			roomCount = 0
			simplexBase = opensimplex.OpenSimplex(random.randrange(2560))
			simplexDetail = opensimplex.OpenSimplex(random.randrange(2560))
			simplexFine = opensimplex.OpenSimplex(random.randrange(2560))
		
			for yNum in range(Config.WORLD_MAP_SIZE[1]):     # Height #
				for xNum in range(Config.WORLD_MAP_SIZE[0]): # Width #
				
					# Get Noise Data #
					if True:
						if renderLayer == 0 : renderResolutionMod = 3.0
						elif renderLayer in [1, 2] : renderResolutionMod = 1.0
						elif renderLayer == 3 : renderResolutionMod = 1.4
						valueBase = simplexBase.noise2d(xNum / (48.0 * renderResolutionMod), yNum / (48.0 * renderResolutionMod))
						valueDetail = simplexDetail.noise2d(xNum / (18.0 * renderResolutionMod), yNum / (18.0 * renderResolutionMod))
						valueFine = simplexFine.noise2d(xNum / (8.0 * renderResolutionMod), yNum / (8.0 * renderResolutionMod))
						valueMap = valueBase + (valueDetail * .5) + (valueFine * .25)
						valueMap = (valueMap + 1.0) / 2.0
						if valueMap > 1.0 : valueMap = 1.0
						
					# Get Cell Type #
					if True:
						cellID = None
						if renderLayer == 0:
							if valueMap < .64 : cellID = "Grass"
							elif valueMap < .655 : cellID = "Beach"
							else : cellID = "Water"
						elif renderLayer == 1:
							if valueMap < .33 : cellID = "Water"
							elif valueMap < .37 : cellID = "Beach"
						elif renderLayer == 2:
							if valueMap < .21 : cellID = "Desert"
							elif valueMap > .65:
								targetRoom = areaWorldMap.roomDict[roomCount]
								if targetRoom.mapTileType == "Grass":
									targetRoom.flags["Initialize Trees"] = True
						elif renderLayer == 3:
							if valueMap > .73 : cellID = "Mountain"
							
					# Round Edges #
					if renderLayer == 3:
						if not Utility.circleCircleCollide([xNum, yNum], 1, [Config.WORLD_MAP_SIZE[0] / 2, Config.WORLD_MAP_SIZE[1] / 2], int(Config.WORLD_MAP_SIZE[0] * .465)):
							targetCellID = areaWorldMap.roomDict[roomCount].mapTileType
							if targetCellID not in ["Water", "Mountain"]:
								cellID = "Beach"
						if not Utility.circleCircleCollide([xNum, yNum], 1, [Config.WORLD_MAP_SIZE[0] / 2, Config.WORLD_MAP_SIZE[1] / 2], int(Config.WORLD_MAP_SIZE[0] * .47)):
							cellID = "Water"
							
					# Assign Data #
					if renderLayer == 0:
						newRoom = Room(roomCount, ID_SOLAR_SYSTEM, self.idPlanet, idArea)
						newRoom.mapTileType = cellID
						areaWorldMap.roomDict[roomCount] = newRoom
					elif cellID != None:
						targetRoom = areaWorldMap.roomDict[roomCount]
						if not (renderLayer == 1 and targetRoom.mapTileType in ["Water"]) \
						and not (renderLayer == 2 and targetRoom.mapTileType in ["Water"]) \
						and not (renderLayer == 3 and targetRoom.mapTileType in ["Water"]):
							targetRoom.mapTileType = cellID
							
					# Initialize Trees #
					if renderLayer == 3 and "Initialize Trees" in targetRoom.flags:
						if targetRoom.mapTileType == "Grass":
							for treeNum in range(random.randrange(2, 5)):
								itemTree = DataItem.loadPrefab(13, ITEM_IMAGE_DICT)
								itemTree.setPlantStage(3, ITEM_IMAGE_DICT)
								targetRoom.addItem(itemTree, DATA_PLAYER)
						del targetRoom.flags["Initialize Trees"]
		
					# Generate Room Data #
					if renderLayer == 3:
						targetRoom = areaWorldMap.roomDict[roomCount]
						
						if targetRoom.mapTileType == "Water" : targetRoom.title = "In The Ocean"
						elif targetRoom.mapTileType == "Beach" : targetRoom.title = "On A Beach"
						elif targetRoom.mapTileType == "Grass" : targetRoom.title = "Grasslands"
						elif targetRoom.mapTileType == "Desert" : targetRoom.title = "In A Desert"
						elif targetRoom.mapTileType == "Mountain" : targetRoom.title = "Climbing A Mountain"
						
						targetRoom.titleColorCode = str(len(newRoom.title)) + "w"
						targetRoom.mapLoc = [xNum, yNum]
						targetRoom.mapElevationValue = 0.0
						#elevationValue = 1.0 - valueMap
						#newRoom.mapElevationValue = elevationValue # Shadow Effect On Map #
							
						# Set Floor Type (For Room Background Image) #
						targetRoom.floorType = "Dirt"
						if targetRoom.mapTileType in ["Beach", "Desert"] : targetRoom.floorType = "Sand"
						elif targetRoom.mapTileType == "Water" : targetRoom.floorType = "Water"
							
						# Exits #
						if yNum > 0 : targetRoom.exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":roomCount - Config.WORLD_MAP_SIZE[0]}
						if xNum != Config.WORLD_MAP_SIZE[0]-1 : targetRoom.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":roomCount + 1}
						if yNum != Config.WORLD_MAP_SIZE[1]-1 : targetRoom.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":roomCount + Config.WORLD_MAP_SIZE[0]}
						if xNum > 0 : targetRoom.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":roomCount - 1}
						
						# Seamless Exits On World Map #
						if idArea == "World Map":
							if yNum == 0 : targetRoom.exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":targetRoom.idNum + (Config.WORLD_MAP_SIZE[0] * (Config.WORLD_MAP_SIZE[1] - 1))}
							elif yNum == Config.WORLD_MAP_SIZE[1]-1 : targetRoom.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":targetRoom.idNum - (Config.WORLD_MAP_SIZE[0] * (Config.WORLD_MAP_SIZE[1] - 1))}
							if xNum == 0 : targetRoom.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":targetRoom.idNum + (Config.WORLD_MAP_SIZE[0] - 1)}
							elif xNum == Config.WORLD_MAP_SIZE[0]-1 : targetRoom.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM, "Planet":self.idPlanet, "Area":idArea, "Room":targetRoom.idNum - (Config.WORLD_MAP_SIZE[0] - 1)}
						
					roomCount += 1
			
		self.areaDict[idArea] = areaWorldMap
	
class Area:

	# Initialization Functions #
	def __init__(self, ID_SOLAR_SYSTEM, ID_PLANET, ID_AREA):
	
		# ID Variables #
		self.idSolarSystem = ID_SOLAR_SYSTEM
		self.idPlanet = ID_PLANET
		self.idArea = ID_AREA
		self.idRandom = None
		self.tickSynch = 0
		self.flags = {}
		self.flags["Launch Pad Room List"] = []
		
		# Area Update Dicts #
		self.weatherDict = {}
		self.wetTimerAreaDict = {}
		self.wetTimerRoomDict = {}
		
		# Area Variables #
		self.roomDict = {}
		self.latitude = 0
		self.currentTemperature = 0
		self.mapTotalCellCount = [0, 0]
		
		# Synch Dict Lists #
		self.synchWeatherDictList = []
	
	def generateSpaceship(self, DATA_PLAYER, SOLAR_SYSTEM_DICT, TARGET_SOLAR_SYSTEM_ID, ITEM_IMAGE_DICT):
	
		self.idRandom = Utility.generateRandomId()
		self.currentTemperature = 72
		self.flags["Spaceship Description"] = "You see nothing special."
		self.flags["Spaceship Key List"] = ["debug", "spaceship", "debug spaceship", "a debug spaceship"]
		self.flags["Spaceship Door Status"] = "Unlocked"
		self.flags["Spaceship Door Key Num"] = 12345
		self.flags["Spaceship Speed"] = 0
		
		self.flags["Spaceship Module List"] = []
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Launch Module"))
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Landing Module"))
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Scan Planet Module"))
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Radar Module"))
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Manual Control Module"))
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Autopilot Module"))
		self.flags["Spaceship Module List"].append(DataSpaceshipModule.loadModule("Throttle Module"))
		
		del self.flags["Launch Pad Room List"]
		
		# Room 0 - Hallway #
		if True:
			room0 = Room(0, None, None, self.idArea)
			room0.title = "A Spaceship Hallway"
			room0.titleColorCode = "19w"
			room0.exitDict["North"] = {"Room":1}
			room0.exitDict["East"] = {"Room":3}
			room0.exitDict["South"] = {"Room":2}
			room0.exitDict["West"] = "Spaceship Exit"
			room0.flags["Spaceship Main Door"] = True
			
			itemChest = DataItem.loadPrefab(10, ITEM_IMAGE_DICT)
			for i in range(10) : room0.addItemToContainer(itemChest, DataItem.loadPrefab(13, ITEM_IMAGE_DICT))
			for i in range(10) : room0.addItemToContainer(itemChest, DataItem.loadPrefab(14, ITEM_IMAGE_DICT))
			for i in range(10) : room0.addItemToContainer(itemChest, DataItem.loadPrefab(15, ITEM_IMAGE_DICT))
			for i in range(10) : room0.addItemToContainer(itemChest, DataItem.loadPrefab(16, ITEM_IMAGE_DICT))
			for i in range(10) : room0.addItemToContainer(itemChest, DataItem.loadPrefab(17, ITEM_IMAGE_DICT))
			for i in range(10) : room0.addItemToContainer(itemChest, DataItem.loadPrefab(18, ITEM_IMAGE_DICT))
			room0.addItem(itemChest, DATA_PLAYER)
			
			self.roomDict[0] = room0
			
		# Room 1 - Cockpit #
		if True:
			room1 = Room(1, None, None, self.idArea)
			room1.title = "A Cockpit"
			room1.titleColorCode = "10w"
			room1.exitDict["South"] = {"Room":0}
			
			spaceshipControlPanel = DataItem.loadPrefab(-3, ITEM_IMAGE_DICT, {"Spaceship Control Panel":True})
			room1.addItem(spaceshipControlPanel, DATA_PLAYER)
			
			self.roomDict[1] = room1
		
		# Cockpit Door #
		self.roomDict[0].createDoor(SOLAR_SYSTEM_DICT, TARGET_SOLAR_SYSTEM_ID, "North", {"Key Num":12345, "Automatic":True})

		# Room 2 - Spaceship Garden #
		if True:
			room2 = Room(2, None, None, self.idArea)
			room2.title = "A Spaceship Garden"
			room2.titleColorCode = "18w"
			room2.exitDict["North"] = {"Room":0}
			room2.floorType = "Grass"
			room2.loadItem(20, DATA_PLAYER, ITEM_IMAGE_DICT)
			self.roomDict[2] = room2
			
		# Room 3 - Spaceship Training Room #
		if True:
			room3 = Room(3, None, None, self.idArea)
			room3.title = "A Training Room"
			room3.titleColorCode = "15w"
			room3.exitDict["West"] = {"Room":0}
			
			trainingCenterControlPanel = DataItem.loadPrefab(-3, ITEM_IMAGE_DICT)
			trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 1", "Target ID":2, "Key List":Utility.createKeyList("button 1")})
			trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 2", "Target ID":3, "Key List":Utility.createKeyList("button 2")})
			trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 3", "Target ID":4, "Key List":Utility.createKeyList("button 3")})
			trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 4", "Target ID":5, "Key List":Utility.createKeyList("button 4")})
			room3.addItem(trainingCenterControlPanel, DATA_PLAYER)
			
			self.roomDict[3] = room3
			
		# Set Spaceship Flags #
		for roomId in self.roomDict:
			targetRoom = self.roomDict[roomId]
			targetRoom.idSolarSystem = self.idSolarSystem
			targetRoom.idAreaRandom = self.idRandom
			targetRoom.inside = True
			targetRoom.flags["Light"] = True
			targetRoom.flags["In Spaceship"] = True
	
	def zeroAreaCoordinates(self, SOLAR_SYSTEM_DICT):
	
		# Examine Room Function #
		def examineRoomData(CURRENT_LOC, TARGET_ROOM, EXAMINED_ROOM_LIST):
			
			self.roomDict[TARGET_ROOM.idNum].mapLoc = copy.deepcopy(CURRENT_LOC)
			EXAMINED_ROOM_LIST.append(TARGET_ROOM.idNum)
			#print(str(TARGET_ROOM.idNum) + "-" + str(self.roomDict[TARGET_ROOM.idNum].mapLoc))
			
			firstRoom = copy.deepcopy(TARGET_ROOM)
			for targetExitDir in ["North", "East", "South", "West"]:
	
				if targetExitDir != "North":
					CURRENT_LOC = firstRoom.mapLoc
					#print(str(firstRoom.idNum) + " " + str(CURRENT_LOC) + " " + str(self.roomDict[firstRoom.idNum].mapLoc) + " " + str(firstRoom.mapLoc) + " " + str(targetExitDir))
					
				if targetExitDir in TARGET_ROOM.exitDict:
					tempArea, tempRoom, tempMessage = getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, self, TARGET_ROOM, targetExitDir, 1, True)
					if tempArea == self and tempRoom.idNum not in EXAMINED_ROOM_LIST:
						
						if targetExitDir == "North" : CURRENT_LOC[1] -= 1
						elif targetExitDir == "East" : CURRENT_LOC[0] += 1
						elif targetExitDir == "South" : CURRENT_LOC[1] += 1
						elif targetExitDir == "West" : CURRENT_LOC[0] -= 1
						
						EXAMINED_ROOM_LIST = examineRoomData(CURRENT_LOC, tempRoom, EXAMINED_ROOM_LIST)
						CURRENT_LOC = copy.deepcopy(self.roomDict[firstRoom.idNum].mapLoc)
						firstRoom.mapLoc = copy.deepcopy(self.roomDict[firstRoom.idNum].mapLoc)
						
			return EXAMINED_ROOM_LIST
	
		# Get Map Dimensions #
		if self.idArea == "World Map":
			examinedRoomIdList = []
			for roomId in self.roomDict : examinedRoomIdList.append(roomId)
			mapTotalCellCount = Config.WORLD_MAP_SIZE
		else:
			examinedRoomIdList = []
			for currentRoomId in self.roomDict:
				if currentRoomId not in examinedRoomIdList:
					currentLoc = [0, 0]
					currentRoom = self.roomDict[currentRoomId]
					examinedRoomIdList = examineRoomData(currentLoc, currentRoom, examinedRoomIdList)
		
		# Zero Map Dimensions To Top-Left Corner #
		if len(examinedRoomIdList) > 0:
			
			yModList = []
			currentStartIndex = 0
			maxTopLeftPoint = [0, 0]
			maxBottomRightPoint = [0, 0]
			self.mapTotalCellCount = [0, 0]
			
			for tempIndex, currentRoomId in enumerate(examinedRoomIdList):
				currentRoom = self.roomDict[currentRoomId]
				
				if currentRoom.mapLoc[0] < maxTopLeftPoint[0] : maxTopLeftPoint[0] = currentRoom.mapLoc[0]
				elif currentRoom.mapLoc[0] > maxBottomRightPoint[0] : maxBottomRightPoint[0] = currentRoom.mapLoc[0]
				if currentRoom.mapLoc[1] < maxTopLeftPoint[1] : maxTopLeftPoint[1] = currentRoom.mapLoc[1]
				elif currentRoom.mapLoc[1] > maxBottomRightPoint[1] : maxBottomRightPoint[1] = currentRoom.mapLoc[1]
				
				if ((tempIndex+1) == len(examinedRoomIdList) or (self.roomDict[examinedRoomIdList[tempIndex+1]].mapLoc == [0, 0])):
					
					yMod = 0
					if len(yModList) > 0:
						for tempSize in yModList : yMod += (tempSize + 1)
					
					for tempRoomId in examinedRoomIdList[currentStartIndex:tempIndex+1]:
						tempRoom = self.roomDict[tempRoomId]
						tempRoom.mapLoc[0] += abs(maxTopLeftPoint[0])
						tempRoom.mapLoc[1] += abs(maxTopLeftPoint[1]) + yMod
						if tempRoom.mapLoc[0] > self.mapTotalCellCount[0] : self.mapTotalCellCount[0] = tempRoom.mapLoc[0]
						if tempRoom.mapLoc[1] > self.mapTotalCellCount[1] : self.mapTotalCellCount[1] = tempRoom.mapLoc[1]
					
					yModList.append(abs(maxTopLeftPoint[1]) + 1 + abs(maxBottomRightPoint[1]))
					currentStartIndex = tempIndex + 1
					maxTopLeftPoint = [0, 0]
					maxBottomRightPoint = [0, 0]
					
			self.mapTotalCellCount[0] += 1
			self.mapTotalCellCount[1] += 1
	
	# Update Functions #
	def update(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, UPDATE_TYPE, TICK_SPEED=1):
		
		self.tickSynch += TICK_SPEED
		
		# Update Temperature & Create Weather - Every 10 Seconds #
		if "Spaceship Description" not in self.flags:
			if (UPDATE_TYPE == "Default" and self.tickSynch % 10 == 0) or UPDATE_TYPE == "Synch":
				self.currentTemperature = self.getTemperature(SOLAR_SYSTEM_DICT)
				self.adjustWeather(SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE)
				self.createWeatherChance(SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, UPDATE_TYPE, TICK_SPEED)
				self.updateWeather(SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, UPDATE_TYPE, TICK_SPEED)
				self.tickAreaWetTimers(SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE, TICK_SPEED)
	
		# Update Spaceship (Area) - Every Second #
		else : self.updateSpaceship(SOLAR_SYSTEM_DICT, DATA_PLAYER, TICK_SPEED, UPDATE_TYPE)
		
	def updateSpaceship(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, TICK_SPEED, UPDATE_TYPE):
	
		# Launch Timer #
		if self.flags["Spaceship Status"] == "Launching" and "Spaceship Launch Timer" in self.flags:
			self.flags["Spaceship Launch Timer"] -= TICK_SPEED
			if self.flags["Spaceship Launch Timer"] <= 0:
				self.flags["Spaceship Launch Stage"] += 1
				
				if self.flags["Spaceship Launch Stage"] == 1:
					self.flags["Spaceship Launch Timer"] = 2
					if UPDATE_TYPE == "Default":
						Console.addDisplayLineToDictList("A computerized voice says, \"Commencing launch countdown.\"")
					
				elif self.flags["Spaceship Launch Stage"] == 2:
					self.flags["Spaceship Launch Timer"] = 4
					if UPDATE_TYPE == "Default":
						Console.addDisplayLineToDictList("The ship rumbles as the engines start up.")
					
				elif self.flags["Spaceship Launch Stage"] == 3:
					self.flags["Spaceship Launch Timer"] = 6
					if UPDATE_TYPE == "Default":
						Console.addDisplayLineToDictList("The engine roars as you blast off!")
					targetRoom = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[self.flags["Landed Data"]["Planet"]].areaDict[self.flags["Landed Data"]["Area"]].roomDict[self.flags["Landed Data"]["Room"]]
					targetRoom.removeSpaceshipFromRoom(self.idArea, self.idRandom)
					
				elif self.flags["Spaceship Launch Stage"] == 4:
					self.flags["Spaceship Launch Timer"] = 7
					if UPDATE_TYPE == "Default":
						Console.addDisplayLineToDictList("The ship rumbles as it makes its fiery ascent.")
					
				elif self.flags["Spaceship Launch Stage"] == 5:
					self.flags["Spaceship Status"] = "Orbit"
					self.flags["Spaceship Orbit Target"] = DATA_PLAYER.currentPlanet
					del self.flags["Spaceship Launch Timer"]
					del self.flags["Spaceship Launch Stage"]
					del self.flags["Landed Data"]
					DATA_PLAYER.currentPlanet = None
					
					# Update Mob Data #
					for tempRoomId in self.roomDict:
						tempRoom = self.roomDict[tempRoomId]
						for tempMob in tempRoom.mobList : tempMob.currentPlanet = None
						# Do I Need More Stuff In Here? (Items?)
					
					if UPDATE_TYPE == "Default":
						Console.addDisplayLineToDictList("You begin orbiting " + self.flags["Spaceship Orbit Target"] + ".")
					
		# Landing Timer #
		elif self.flags["Spaceship Status"] == "Landing" and "Spaceship Landing Timer" in self.flags:
			self.flags["Spaceship Landing Timer"] -= TICK_SPEED
			if self.flags["Spaceship Landing Timer"] <= 0:
				self.flags["Spaceship Landing Stage"] += 1
				
				if self.flags["Spaceship Landing Stage"] == 1:
					self.flags["Spaceship Landing Timer"] = 5
					Console.addDisplayLineToDictList("The vessel rumbles as it turns toward the planet.")
				
				elif self.flags["Spaceship Landing Stage"] == 2:
					self.flags["Spaceship Landing Timer"] = 5
					Console.addDisplayLineToDictList("You feel a sense of weightlessness as you begin your descent.")
					
				elif self.flags["Spaceship Landing Stage"] == 3:
					self.flags["Spaceship Landing Timer"] = 7
					Console.addDisplayLineToDictList("The ship rumbles as it descends toward the plant.")
			
				elif self.flags["Spaceship Landing Stage"] == 4:
					self.flags["Spaceship Landing Timer"] = 5
					Console.addDisplayLineToDictList("The ship begins to slow down as it approaches the landing pad.")
			
				elif self.flags["Spaceship Landing Stage"] == 5:
					targetPlanet = self.flags["Spaceship Landing Target Planet"]
					targetArea = self.flags["Spaceship Landing Target Area"]
					targetRoom = self.flags["Spaceship Landing Target Room"]
					targetRoom = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[targetPlanet].areaDict[targetArea].roomDict[targetRoom]
					targetRoom.addSpaceshipToRoom(self)
				
					if DATA_PLAYER.currentPlanet != self.flags["Landed Data"]["Planet"]:
						DATA_PLAYER.currentPlanet = self.flags["Landed Data"]["Planet"]
						
					# Update Mob Data #
					for tempRoomId in self.roomDict:
						tempRoom = self.roomDict[tempRoomId]
						for tempMob in tempRoom.mobList : tempMob.currentPlanet = self.flags["Landed Data"]["Planet"]
					
					del self.flags["Spaceship Landing Target Planet"]
					del self.flags["Spaceship Landing Target Area"]
					del self.flags["Spaceship Landing Target Room"]
					del self.flags["Spaceship Landing Timer"]
					del self.flags["Spaceship Landing Stage"]
					
					Console.addDisplayLineToDictList("You feel a slight thud as the ship lands.")
			
		# In Flight #
		elif self.flags["Spaceship Status"] == "Flight" and "Spaceship Flight Timer" in self.flags:
			self.flags["Spaceship Flight Timer"] -= TICK_SPEED
			if self.flags["Spaceship Flight Timer"] <= 0:
				self.flags["Spaceship Flight Timer"] = Config.SPACESHIP_TIMER["Update"]
				
				# Autopilot #
				if self.flags["Spaceship Flight Type"] == "Autopilot":
					targetPlanet = self.flags["Spaceship Flight Target"]
					xDiff = targetPlanet.x - self.flags["Spaceship X Loc"]
					yDiff = targetPlanet.y - self.flags["Spaceship Y Loc"]
					spaceshipSpeed = int(self.flags["Spaceship Speed"] * Config.SPACESHIP_TIMER["Speed"] * TICK_SPEED)
					moveSize = spaceshipSpeed
					xMaxMoveCheck = False
					xMoveSize = 0
					yMoveSize = 0
					
					if xDiff > (spaceshipSpeed / 2) : xMoveSize = (spaceshipSpeed / 2) ; moveSize = (spaceshipSpeed / 2)
					elif xDiff < -(spaceshipSpeed / 2) : xMoveSize = -(spaceshipSpeed / 2) ; moveSize = (spaceshipSpeed / 2)
					else : xMoveSize = xDiff ; moveSize -= abs(xDiff) ; xMaxMoveCheck = True
					if yDiff > moveSize : yMoveSize = moveSize ; moveSize = 0
					elif yDiff < -moveSize : yMoveSize = -moveSize ; moveSize = 0
					else : yMoveSize = yDiff ; moveSize -= yDiff
					if moveSize > 0 and not xMaxMoveCheck:
						if xDiff > 0 : xMoveSize += moveSize
						elif xDiff < 0 : xMoveSize += -moveSize
					
					# Move Ship #
					self.flags["Spaceship X Loc"] += xMoveSize
					self.flags["Spaceship Y Loc"] += yMoveSize
					
					# Orbit Check #
					if targetPlanet.x - self.flags["Spaceship X Loc"] in range(50):
						if targetPlanet.y - self.flags["Spaceship Y Loc"] in range(50):
							self.flags["Spaceship Status"] = "Orbit"
							self.flags["Spaceship Speed"] = 0
							self.flags["Spaceship Orbit Target"] = self.flags["Spaceship Flight Target"].idPlanet
							del self.flags["Spaceship Flight Timer"]
							del self.flags["Spaceship Flight Type"]
							del self.flags["Spaceship Flight Target"]
							del self.flags["Spaceship X Loc"]
							del self.flags["Spaceship Y Loc"]
							
							Console.addDisplayLineToDictList("You begin orbiting " + self.flags["Spaceship Orbit Target"] + ".")
					
				# Manual Control #
				elif self.flags["Spaceship Flight Type"] == "Manual Control":
					pass
	
	def getTemperature(self, SOLAR_SYSTEM_DICT):
	
		import math
		parentPlanet = SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[self.idPlanet]
		starBrightness = SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[parentPlanet.targetStar].starBrightness
		
		temperature = 278.3 * (math.pow(starBrightness, .25) / math.sqrt(parentPlanet.distanceFromCenter / 1000.0))
		temperature = int(round(((temperature - 273) * 1.8) + 32))
		temperaturePercent = int(round(((35.0 / 100) * temperature)))
		distancePercent = 100 - int(round((parentPlanet.distanceFromCenter + .0) / 500))
		if distancePercent > 100 : distancePercent = 100
		elif distancePercent < 0 : distancePercent = 0
		nightDayRatio = int(round(math.cos(math.radians(((parentPlanet.currentMinutesInDay + .0)/(parentPlanet.totalHoursInDay * 60)) * 360)) * 100)) * -1
		
		# Atmosphere #
		atmosphereMod = 0
		distanceTempA  = int(round(((distancePercent + .0) / 100) * temperature))
		if distanceTempA < 0 : distanceTempA = distanceTempA * -1
		atmosphereMod += int(round((parentPlanet.atmosphereLevel + .0) * distanceTempA)) * 2
		nightDayRatio += parentPlanet.atmosphereLevel * 2
		
		# Latitude #
		latMod = 0
		if temperature >= 0 : latMod += int(round(((self.latitude + .0) / 100) * ((((distancePercent + .0) / 100) * temperature))))
		elif temperature < 0 : latMod += int(round(((self.latitude + .0) / 100) * ((((distancePercent + .0) / 100) * (temperature * -1)))))
		
		# Day/Night ## Atmosphere - Applied To Night/Day Ratio #
		nightDayMod = 0
		if temperature >= 0 : nightDayMod += int(round(((nightDayRatio + .0) / 100) * (((distancePercent + .0) / 100) * temperaturePercent)))
		elif temperature < 0 : nightDayMod += int(round(((nightDayRatio + .0) / 100) * (((distancePercent + .0) / 100) * (temperaturePercent * -1))))
		
		# Season/Tilt #
		seasonMod = 0
		seasonPercent = int(math.cos(math.radians(((parentPlanet.currentHoursInYear + .0) / (parentPlanet.totalHoursInYear)) * 360)) * 100) * -1
		tiltPerc = int(round(((parentPlanet.axialTilt + .0) / 90) * 100))
		distanceTemp = int(round(((distancePercent + .0) / 100) * temperature))
		tempSeason = int(round(((tiltPerc + .0) / 100) * distanceTemp))
		if parentPlanet.axialTilt != 0:
			if seasonPercent != 0:
				if seasonPercent in range(1, 101) or seasonPercent in range(-100, 0):
					seasonMod += int(round(((seasonPercent + .0) / 100) * tempSeason))
		
		newTemperature = temperature + latMod + nightDayMod + seasonMod + atmosphereMod
		return newTemperature
	
	def adjustWeather(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE):
		
		parentPlanet = SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[self.idPlanet]
		freezeTemp = Config.FREEZE_TEMP[parentPlanet.atmosphereType]
		evaporateTemp = Config.EVAPORATE_TEMP[parentPlanet.atmosphereType]
		playerArea = getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
		playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]
		
		# Rain Evaporate #
		if self.currentTemperature >= evaporateTemp and len(self.weatherDict) > 0 and "Rain Timer" in self.weatherDict:
			self.weatherDict = {}
			if UPDATE_TYPE == "Default" and self == playerArea and not playerRoom.inside:
				Console.addDisplayLineToDictList("The rain boils away into the air.", "4w1dc3ddc24w1y")
		
		# Rain Turn To Snow #
		elif "Rain Timer" in self.weatherDict and self.currentTemperature <= freezeTemp:
			self.weatherDict["Snow Timer"] = self.weatherDict["Rain Timer"]
			del self.weatherDict["Rain Timer"]
			if UPDATE_TYPE == "Default" and self == playerArea and not playerRoom.inside:
				Console.addDisplayLineToDictList("The rain turns into snow.", "4w1dc3ddc12w1dw3ddw1y")
			
		# Snow Turn To Rain #
		elif "Snow Timer" in self.weatherDict and self.currentTemperature > freezeTemp:
			self.weatherDict["Rain Timer"] = self.weatherDict["Snow Timer"]
			del self.weatherDict["Snow Timer"]
			
			# Auto Plant Seeds <- Finish This
			
			
			if UPDATE_TYPE == "Default" and self == playerArea and not playerRoom.inside:
				Console.addDisplayLineToDictList("The snow turns into rain.", "4w1dw3ddw12w1dc3ddc1y")
	
	def createWeatherChance(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, UPDATE_TYPE, TICK_SPEED):
		
		if SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[self.idPlanet].atmosphereLevel > 0:
		
			parentPlanet = SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[self.idPlanet]
			precipChance = int((1.0 / parentPlanet.atmosphereLevel) * 10)
			freezeTemp = Config.FREEZE_TEMP[parentPlanet.atmosphereType]
			evaporateTemp = Config.EVAPORATE_TEMP[parentPlanet.atmosphereType]
			
			if UPDATE_TYPE == "Synch":
				divChance = int(TICK_SPEED * .5)
				if divChance == 0 : divChance = 1
				precipChance /= divChance
			
			#if self.currentTemperature < evaporateTemp: <- Reimplement this!
			if random.randrange(0, (precipChance+1)) == 0:
			
				precipType = "Rain"
				if self.currentTemperature <= freezeTemp : precipType = "Snow"
				weatherChoiceList = ["Cloudy Timer", precipType+" Timer"]
				for currentWeather in self.weatherDict:
					if currentWeather in weatherChoiceList:
						del weatherChoiceList[weatherChoiceList.index(currentWeather)]
				
				if len(weatherChoiceList) > 0:
					randomWeatherChoice = random.choice(weatherChoiceList)
					randomDuration = random.randrange(100, 500)
					playerArea = getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
					self.createWeather(SOLAR_SYSTEM_DICT, DATA_PLAYER, playerArea, UPDATE_ROOM_DATA_LIST, randomWeatherChoice, randomDuration, UPDATE_TYPE)
		
	def createWeather(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, PLAYER_AREA, UPDATE_ROOM_DATA_LIST, WEATHER_TYPE, WEATHER_DURATION, UPDATE_TYPE):
	
		self.weatherDict[WEATHER_TYPE] = WEATHER_DURATION
		
		# To Prevent Clouds From Finishing First #
		if WEATHER_TYPE != "Cloudy Timer":
			if "Cloudy Timer" in self.weatherDict : self.weatherDict["Cloudy Timer"] += WEATHER_DURATION
			else : self.weatherDict["Cloudy Timer"] = WEATHER_DURATION + random.randrange(30, 300)
			
		# Start Wet Timer #
		if WEATHER_TYPE == "Rain Timer" and "Water" not in self.wetTimerAreaDict:
			self.wetTimerAreaDict["Water"] = 10
			
		# Auto Plant Seeds <- Finish This
		
		
		# Weather Synch Dict #
		if WEATHER_TYPE in ["Rain Timer", "Snow Timer"]:
			self.appendSynchWeatherDict(UPDATE_ROOM_DATA_LIST, WEATHER_TYPE)
			
		# Messages #
		playerRoom = PLAYER_AREA.roomDict[DATA_PLAYER.currentRoom]
		if UPDATE_TYPE == "Default" and not playerRoom.inside and PLAYER_AREA == self:
			if WEATHER_TYPE == "Cloudy Timer" : Console.addDisplayLineToDictList("Clouds roll in overhead.", "1dw5ddw17w1y")
			elif WEATHER_TYPE == "Rain Timer" : Console.addDisplayLineToDictList("It starts to rain.", "13w1dc3ddc1y")
			elif WEATHER_TYPE == "Snow Timer" : Console.addDisplayLineToDictList("It starts to snow.", "13w1dw3ddw1y")
	
	def updateWeather(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, UPDATE_TYPE, TICK_SPEED):
	
		playerArea = getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
		playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]
		if UPDATE_TYPE == "Default" : TICK_SPEED = 10
		
		# Tick Weather Timers #
		delWeatherList = []
		for weatherType in self.weatherDict:
			if weatherType[-5::] == "Timer":
				self.weatherDict[weatherType] -= TICK_SPEED
				if self.weatherDict[weatherType] <= 0:
					delWeatherList.append(weatherType)
				
					# Add Surrounding Room Data To Synch Weather Dict #
					if weatherType in ["Rain Timer", "Snow Timer"] and UPDATE_TYPE == "Default":
						for roomDataDict in UPDATE_ROOM_DATA_LIST:
							if roomDataDict["Room Area"] == self.idArea and roomDataDict["Room Area Random"] == self.idRandom and roomDataDict["Room Solar System"] == self.idSolarSystem and roomDataDict["Room Planet"] == self.idPlanet:
								if roomDataDict["Room ID"] not in self.synchWeatherDictList[-1]["Updated Room List"]:
									self.synchWeatherDictList[-1]["Updated Room List"].append(roomDataDict["Room ID"])
									if len(self.roomDict) == len(self.synchWeatherDictList[-1]["Updated Room List"]) : del self.synchWeatherDictList[-1]
								
					# Messages #
					if UPDATE_TYPE == "Default" and not playerRoom.inside and playerArea == self:
						if weatherType == "Cloudy Timer" : Console.addDisplayLineToDictList("The clouds above dissipate.", "4w1dw5ddw16w1y")
						elif weatherType == "Rain Timer" : Console.addDisplayLineToDictList("It stops raining.", "9w1dc6ddc1y")
						elif weatherType == "Snow Timer" : Console.addDisplayLineToDictList("It stops snowing.", "9w1dw6ddw1y")
						
		# Delete Weather Data #
		for weatherType in delWeatherList:
			del self.weatherDict[weatherType]
		
	def tickAreaWetTimers(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE, TICK_SPEED):
	
		wetTimerDelList = []
		messageCheck = False
		playerArea = getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
		playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]
		if UPDATE_TYPE == "Default" : TICK_SPEED = 10
		
		for targetTimerId in self.wetTimerAreaDict:
			
			# Update Water Wet Timer During Rain #
			if targetTimerId == "Water" and "Rain Timer" in self.weatherDict:
				if self.wetTimerAreaDict[targetTimerId] < Config.WET_TIMER["Max Ground Liquid"]:
					self.wetTimerAreaDict[targetTimerId] += TICK_SPEED
			else:
				self.wetTimerAreaDict[targetTimerId] -= TICK_SPEED
				if self.wetTimerAreaDict[targetTimerId] <= 0:
					wetTimerDelList.append(targetTimerId)
					
					if UPDATE_TYPE == "Default" and not messageCheck and playerArea == self and not playerRoom.inside and "Rain Timer" not in self.weatherDict \
					and len(wetTimerDelList) == len(self.wetTimerAreaDict) and playerRoom.idNum not in self.wetTimerRoomDict:
						Console.addDisplayLineToDictList("The ground dries up.", "19w1y")
						messageCheck = True
						
		for targetTimerId in wetTimerDelList:
			del self.wetTimerAreaDict[targetTimerId]
	
	def synchData(self, TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER):
	
		TICK_SPEED = Config.SYNCH_TICK_SPEED
		tickSeconds = TICK_SYNCH - self.tickSynch
		
		print(tickSeconds / TICK_SPEED)
		for turnNum in range(tickSeconds / TICK_SPEED):
			self.update(SOLAR_SYSTEM_DICT, DATA_PLAYER, [], "Synch", TICK_SPEED)
		remainingTurns = tickSeconds % TICK_SPEED
		if remainingTurns > 0:
			self.update(SOLAR_SYSTEM_DICT, DATA_PLAYER, [], "Synch", remainingTurns)
			
	# Utility Functions #
	def appendSynchWeatherDict(self, UPDATE_ROOM_DATA_LIST, WEATHER_TYPE):

		synchWeatherDict = {}
		synchWeatherDict["Synch Num"] = self.tickSynch
		synchWeatherDict["Weather Type"] = WEATHER_TYPE
		synchWeatherDict["Timer Duration"] = self.weatherDict[WEATHER_TYPE]
		synchWeatherDict["Updated Room List"] = []
		self.synchWeatherDictList.append(synchWeatherDict)

class Room:

	# Initialization Functions #
	def __init__(self, ID_NUM, ID_SOLAR_SYSTEM, ID_PLANET, ID_AREA):
	
		# ID Variables #
		self.objectType = "Room"
		self.idNum = ID_NUM
		self.idSolarSystem = ID_SOLAR_SYSTEM
		self.idPlanet = ID_PLANET
		self.idArea = ID_AREA
		self.idAreaRandom = None
		self.tickSynch = 0
		self.flags = {}
		
		# Room Update Lists #
		self.updateSkill = None
		self.updateMobList = []
		self.updateItemList = []
		
		# Room Variables #
		self.exitDict = {}
		self.mobList = []
		self.itemList = []
		self.spaceshipDictList = []
		
		self.floorType = "Metal"
		self.inside = False
		
		# Map Screen Variables #
		self.mapLoc = [None, None]
		self.mapElevationValue = 0.5
		self.mapTileType = "Default"
		
		# Description Variables #
		self.title = "Default Room Title"
		self.titleColorCode = "18w"
		
	def loadItem(self, PREFAB_NUM, DATA_PLAYER, ITEM_IMAGE_DICT, LOAD_FLAGS={}):
	
		item = DataItem.loadPrefab(PREFAB_NUM, ITEM_IMAGE_DICT, LOAD_FLAGS)
		self.addItem(item, DATA_PLAYER)
	
	def addItem(self, TARGET_ITEM, DATA_PLAYER):
	
		# Update Item Variables #
		if True:
			TARGET_ITEM.currentSolarSystem = self.idSolarSystem
			TARGET_ITEM.currentPlanet = self.idPlanet
			TARGET_ITEM.currentArea = self.idArea
			TARGET_ITEM.currentAreaRandom = self.idAreaRandom
			TARGET_ITEM.currentRoom = self.idNum
			TARGET_ITEM.currentLoc = "Room"
			if "In Spaceship" in self.flags : TARGET_ITEM.flags["In Spaceship"] = True
			elif "In Spaceship" in TARGET_ITEM.flags : del TARGET_ITEM.flags["In Spaceship"]
			
		# Add Item #
		if True:
			addCheck = False
			if "Quantity" in TARGET_ITEM.flags:
				targetRoomIndex = -1
				for tempIndex, tempItem in enumerate(self.itemList):
					if "Quantity" in tempItem.flags and tempItem.idNum == TARGET_ITEM.idNum:
						targetRoomIndex = tempIndex
						break
				if targetRoomIndex != -1:
					self.itemList[targetRoomIndex].flags["Quantity"] += TARGET_ITEM.flags["Quantity"]
					addCheck = True
			if not addCheck : self.itemList.append(TARGET_ITEM)
		
		# UpdateList Check #
		if TARGET_ITEM.isUpdateItem():
			if TARGET_ITEM not in self.updateItemList:
				self.updateItemList.append(TARGET_ITEM)
				
		self.setEntityScreenLoc(TARGET_ITEM, DATA_PLAYER)
	
	def addItemToContainer(self, TARGET_CONTAINER, TARGET_ITEM):

		# Update Item Variables #
		if True:
			TARGET_ITEM.currentSolarSystem = TARGET_CONTAINER.currentSolarSystem
			TARGET_ITEM.currentPlanet = TARGET_CONTAINER.currentPlanet
			TARGET_ITEM.currentArea = TARGET_CONTAINER.currentArea
			TARGET_ITEM.currentAreaRandom = TARGET_CONTAINER.currentAreaRandom
			TARGET_ITEM.currentRoom = TARGET_CONTAINER.currentRoom
			TARGET_ITEM.currentLoc = "Room Container"
			if "In Spaceship" in TARGET_CONTAINER.flags : TARGET_ITEM.flags["In Spaceship"] = True
			elif "In Spaceship" in TARGET_ITEM.flags : del TARGET_ITEM.flags["In Spaceship"]
		
		# Add Item To Container #
		if True:
			addCheck = False
			if "Quantity" in TARGET_ITEM.flags:
				inContainerIndex = -1
				for tempIndex, tempItem in enumerate(TARGET_CONTAINER.flags["Container List"]):
					if "Quantity" in tempItem.flags and tempItem.idNum == TARGET_ITEM.idNum:
						inContainerIndex = tempIndex
						break
				if inContainerIndex != -1:
					TARGET_CONTAINER.flags["Container List"][inContainerIndex].flags["Quantity"] += TARGET_ITEM.flags["Quantity"]
					addCheck = True
			if not addCheck:
				TARGET_CONTAINER.flags["Container List"].append(TARGET_ITEM)
				TARGET_CONTAINER.flags["Container Current Weight"] += TARGET_ITEM.getWeight()
			
		# UpdateList Check #
		if TARGET_ITEM.isUpdateItem():
			if TARGET_ITEM not in self.updateItemList : self.updateItemList.append(TARGET_ITEM)
				
	def loadMob(self, PREFAB_NUM, DATA_PLAYER, ENTITY_IMAGE_DICT):
	
		mob = DataMob.loadPrefab(PREFAB_NUM, ENTITY_IMAGE_DICT)
		self.setEntityScreenLoc(mob, DATA_PLAYER)
		
		# Set Location Variables #
		if True:
			if "In Spaceship" in self.flags:
				if "Landed Data" in self.flags : mob.currentPlanet = self.flags["Landed Data"]["Planet"]
				else : mob.currentPlanet = None
				mob.flags["In Spaceship"] = True
			else:
				mob.currentPlanet = self.idPlanet
			mob.currentSolarSystem = self.idSolarSystem
			mob.currentArea = self.idArea
			mob.currentRoom = self.idNum
			if self.idAreaRandom != None:
				mob.currentAreaRandom = self.idAreaRandom
			mob.flags["Spawn Area"] = self.idArea
	
		# Add Mob To Room #
		self.mobList.append(mob)
		
		# UpdateList Check #
		if mob.isUpdateMob() and mob not in self.updateMobList:
			self.updateMobList.append(mob)
			
		# Draw Screen #
		if True:
			Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
		
	def addMob(self, TARGET_MOB, DATA_PLAYER):
	
		self.mobList.append(TARGET_MOB)
		
		if not (DATA_PLAYER != None and TARGET_MOB in DATA_PLAYER.groupList):
			self.setEntityScreenLoc(TARGET_MOB, DATA_PLAYER)
		
		# UpdateList Check #
		if (TARGET_MOB.isUpdateMob() or TARGET_MOB in DATA_PLAYER.mobTargetPlayerCombatList) and TARGET_MOB not in self.updateMobList:
			self.updateMobList.append(TARGET_MOB)
		
	def setEntityScreenLoc(self, TARGET_ENTITY, DATA_PLAYER):
	
		for attemptNum in range(24):
		
			# Player Area - 660, 120, 326, 250 #
			# Enemy Area - 0, 120, 650, 250 #
			
			# Set Entity X Loc #
			if True:
				if (TARGET_ENTITY.objectType == "Mob" and TARGET_ENTITY in DATA_PLAYER.groupList) \
				or (TARGET_ENTITY.objectType == "Item" and TARGET_ENTITY.dropSide == "Player"):
					minXLoc = 660 + ((TARGET_ENTITY.imageSize[0] - TARGET_ENTITY.rectArea.width) / 2)
					maxXLoc = 986 - ((TARGET_ENTITY.imageSize[0] - TARGET_ENTITY.rectArea.width) / 2) - TARGET_ENTITY.rectArea.width
				elif (TARGET_ENTITY.objectType == "Mob" and TARGET_ENTITY not in DATA_PLAYER.groupList) \
				or (TARGET_ENTITY.objectType == "Item" and TARGET_ENTITY.dropSide == "Mob"): 
					minXLoc = ((TARGET_ENTITY.imageSize[0] - TARGET_ENTITY.rectArea.width) / 2)
					maxXLoc = 650 - ((TARGET_ENTITY.imageSize[0] - TARGET_ENTITY.rectArea.width) / 2) - TARGET_ENTITY.rectArea.width
				
				if minXLoc > maxXLoc : maxXLoc = minXLoc + 1
				TARGET_ENTITY.rectArea.left = random.randrange(minXLoc, maxXLoc)
			
			# Set Entity Y Loc #
			if True:
				rowMaxRange = 9
				if TARGET_ENTITY.imageSize[1] > 25 : rowMaxRange -= TARGET_ENTITY.imageSize[1] / 25
				if rowMaxRange <= 0 : rowMaxRange = 1
				TARGET_ENTITY.rectArea.bottom = 370 - (random.randrange(rowMaxRange) * 25)
			
			# Collide Check #
			breakCheck = True
			if TARGET_ENTITY.objectType == "Mob" : targetList = self.mobList
			elif TARGET_ENTITY.objectType == "Item" : targetList = self.itemList
			
			for roomEntity in targetList:
				if roomEntity != TARGET_ENTITY:
					if Utility.rectRectCollide([TARGET_ENTITY.rectArea[0], TARGET_ENTITY.rectArea[1]], [roomEntity.rectArea[0], roomEntity.rectArea[1]], [roomEntity.rectArea.width, roomEntity.rectArea.height]):
						breakCheck = False
						break
			if breakCheck : break
		
	# Update Functions #
	def update(self, WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, UPDATE_ROOM_DATA_LIST, SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT, UPDATE_TYPE, TICK_SPEED=1):
		
		self.tickSynch += TICK_SPEED
		
		# Tick Room Wet Timers #
		if self.idNum in PARENT_AREA.wetTimerRoomDict:
			self.tickWetRoomTimers(SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, TICK_SPEED)
			
		# Tick Room Skill Timer #
		if self.updateSkill != None:
			self.updateRoomSkill(SOLAR_SYSTEM_DICT, DATA_PLAYER, SIDESCREEN_ROOM, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT)
		
		# Update Room Mobs #
		if UPDATE_TYPE == "Default":
			for targetMob in self.updateMobList:
				targetMob.update(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, ITEM_IMAGE_DICT)
			
				if UPDATE_TYPE == "Synch":
					if targetMob.currentAction != None and targetMob.currentAction["Type"] == "Attacking":
						targetMob.currentAction["Action Bar Timer"] += (.019 * TICK_SPEED)
						if targetMob.currentAction["Action Bar Timer"] > targetMob.currentAction["Attack Data"].attackTimer:
							targetMob.currentAction["Action Bar Timer"] = targetMob.currentAction["Attack Data"].attackTimer
			
		self.updateItems(SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, TICK_SPEED, UPDATE_TYPE, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT)
		
		# Synchronize Old Data - Add Room ID To Active Synch Weather Data Lists #
		if UPDATE_TYPE == "Synch":
			
			synchWeatherDelList = []
			for index, tempSynchWeatherDataDict in enumerate(PARENT_AREA.synchWeatherDictList):
				if self.tickSynch >= (tempSynchWeatherDataDict["Synch Num"] + tempSynchWeatherDataDict["Timer Duration"]) \
				and self.idNum not in tempSynchWeatherDataDict["Updated Room List"]:
					PARENT_AREA.synchWeatherDictList[index]["Updated Room List"].append(self.idNum)
					if len(PARENT_AREA.roomDict) == len(PARENT_AREA.synchWeatherDictList[index]["Updated Room List"]) : synchWeatherDelList.append(index)
				elif tempSynchWeatherDataDict["Synch Num"] > self.tickSynch : break
				
			synchWeatherDelList.reverse()
			for index in synchWeatherDelList:
				del PARENT_AREA.synchWeatherDictList[index]
		
	def tickWetRoomTimers(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, TICK_SPEED):
		
		wetTimerDelList = []
		messageCheck = False
		for targetTimerId in PARENT_AREA.wetTimerRoomDict[self.idNum]:
			
			# Update Water Timer During Rain #
			if targetTimerId == "Water" and not self.inside and "Rain Timer" in PARENT_AREA.weatherDict:
				if PARENT_AREA.wetTimerRoomDict[self.idNum][targetTimerId] < Config.WET_TIMER["Max Ground Liquid"]:
					PARENT_AREA.wetTimerRoomDict[self.idNum][targetTimerId] += TICK_SPEED
			else:
				PARENT_AREA.wetTimerRoomDict[self.idNum][targetTimerId] -= TICK_SPEED
				if PARENT_AREA.wetTimerRoomDict[self.idNum][targetTimerId] <= 0:
					wetTimerDelList.append(targetTimerId)
					
					if not messageCheck and sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self) \
					and not (self.inside == False and "Rain Timer" in PARENT_AREA.weatherDict) and not (self.inside == False and targetTimerId in PARENT_AREA.wetTimerAreaDict):
						Console.addDisplayLineToDictList("The ground dries up.", "19w1y")
						messageCheck = True			
		
		for targetTimerId in wetTimerDelList:
			del PARENT_AREA.wetTimerRoomDict[self.idNum][targetTimerId]
		if len(PARENT_AREA.wetTimerRoomDict[self.idNum]) == 0:
			del PARENT_AREA.wetTimerRoomDict[self.idNum]
		
	def updateRoomSkill(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, SIDESCREEN_ROOM, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT):
	
		if "Timer" in self.updateSkill.flags:
			self.updateSkill.flags["Timer"] -= 1
			if self.updateSkill.flags["Timer"] <= 0:
				
				# Reset Timer #
				self.updateSkill.flags["Room Ticks"] -= 1
				if self.updateSkill.flags["Room Ticks"] > 0:
					self.updateSkill.flags["Timer"] = self.updateSkill.cooldownTimer
				
				# Get Data #
				if True:
					hitPlayerCheck = False
					damageCount = 0
					healCount = 0
					skillDelList = []
					mobDelList = []
					drawList = []
					drawPlayerStatsScreen = False
					
				# Update Spell Effects #
				if self.updateSkill != None:
					
					# Get Data #
					if True:
						attackPower = self.updateSkill.basePower
						dataAttacker = self.updateSkill.flags["Attacker Data"]
						attackerRoom = getParentArea(SOLAR_SYSTEM_DICT[dataAttacker.currentSolarSystem], dataAttacker).roomDict[dataAttacker.currentRoom]
						brokenConcentrationCheck = False
						postMessageList = []
						
						playerToRoomRange = 0
						playerToRoomDir = 0
						playerToRoomMessage = None
						if not sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
							playerToRoomRange, playerToRoomDir, playerToRoomMessage = getTargetRange(SOLAR_SYSTEM_DICT, self, DATA_PLAYER, Config.PLAYER_UPDATE_RANGE)
							
						attackerToRoomRange = 0
						attackerToRoomDir = 0
						attackerToRoomMessage = None
						if not sameRoomCheck(SOLAR_SYSTEM_DICT, dataAttacker, self):
							attackerToRoomRange, attackerToRoomDir, attackerToRoomDir = getTargetRange(SOLAR_SYSTEM_DICT, self, dataAttacker, Config.PLAYER_UPDATE_RANGE)
						
						actionString1 = "hits"
						actionString2 = "damage"
						if self.updateSkill.effectType == "Heal":
							actionString1 = "heals"
							actionString2 = "points"
							
						# Get Defender Count #
						if True:
							if (dataAttacker.objectType == "Player" and self.updateSkill.effectType == "Heal") \
							or (dataAttacker.objectType == "Mob" and self.updateSkill.effectType == "Heal" and DATA_PLAYER in dataAttacker.groupList):
								healCount += 1
							if (dataAttacker.objectType == "Mob" and self.updateSkill.effectType == "Damage" and DATA_PLAYER not in dataAttacker.groupList):
								damageCount += 1
							
							for targetMob in self.mobList:
								if (targetMob == dataAttacker and self.updateSkill.effectType == "Heal") \
								or (self.updateSkill.effectType == "Heal" and targetMob in dataAttacker.groupList):
									healCount += 1
								elif (targetMob != dataAttacker and self.updateSkill.effectType == "Damage" and targetMob not in dataAttacker.groupList):
									damageCount += 1
									
						# Update Attack Power #
						if self.updateSkill.effectType == "Heal" and healCount > 1 : attackPower = int(round(attackPower / healCount))
						elif self.updateSkill.effectType == "Damage" and damageCount > 1 : attackPower = int(round(attackPower / damageCount))
						if attackPower < 1 : attackPower = 1
								
					# Target Player #
					if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						if (dataAttacker.objectType == "Player" and self.updateSkill.effectType == "Heal") \
						or (dataAttacker.objectType == "Mob" and self.updateSkill.effectType == "Heal" and DATA_PLAYER in dataAttacker.groupList) \
						or (dataAttacker.objectType == "Mob" and self.updateSkill.effectType == "Damage" and DATA_PLAYER not in dataAttacker.groupList):
						
							# Assign Damage #
							if self.updateSkill.effectType == "Heal":
								DATA_PLAYER.currentHP += attackPower
								if DATA_PLAYER.currentHP > DATA_PLAYER.maxHP : DATA_PLAYER.currentHP = DATA_PLAYER.maxHP
							else : DATA_PLAYER.currentHP -= attackPower
							hitPlayerCheck = True
							
							# Add Attacker To Player's Mob Target List If Not In It #
							if dataAttacker.objectType == "Mob" and DATA_PLAYER.currentHP > 0 and dataAttacker.currentHP > 0 and dataAttacker != DATA_PLAYER \
							and self.updateSkill.effectType == "Damage" and dataAttacker not in DATA_PLAYER.mobTargetList:
								playerToAttackerRange, playerToAttackerDir, playerToAttackerMessage = getTargetRange(SOLAR_SYSTEM_DICT, attackerRoom, DATA_PLAYER, DATA_PLAYER.getViewRange())
								if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, dataAttacker) or (playerToAttackerMessage == None and playerToAttackerRange != -1):
									DATA_PLAYER.mobTargetList.append(dataAttacker)
							
							# Remove Player Action If Taming A Target #
							if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming":
								DATA_PLAYER.currentAction = None
								brokenConcentrationCheck = True
								
							# Initiate Defender Get Hit Animation (Red Fill/Flash) #
							if self.updateSkill.effectType == "Damage" and DATA_PLAYER.currentHP > 0:
								DATA_PLAYER.animationDict["Get Hit"] = {"Timer":7}
								Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
								
							# Initiate Damage Number Animation (Numbers Bounce) #
							if self.updateSkill.effectType == "Damage" and DATA_PLAYER.currentHP > 0:
							
								# Create Number Image #
								if True:
									xDrawLoc = 0
									numberImageWidth = INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_width()
									numberImageHeight = INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_height()
									numberImage = pygame.Surface([numberImageWidth * len(str(attackPower)), numberImageHeight], pygame.SRCALPHA, 32)
									for i in str(attackPower):
										numberImage.blit(INTERFACE_IMAGE_DICT["Numbers Outline"][int(i)], [xDrawLoc, 0])
										xDrawLoc += numberImageWidth
								
								animationDict = {"Timer":150, "Draw Y Loc":0, "Number Image":numberImage, "Bounce Velocity":5.0, "Velocity Decrease":.295, "Bounce Count":0}
								
								# Initiate Damage Number Animation #
								if "Damage Number List" not in DATA_PLAYER.animationDict : DATA_PLAYER.animationDict["Damage Number List"] = []
								DATA_PLAYER.animationDict["Damage Number List"].append(animationDict)
								if "Background Bottom" not in drawList : drawList.append("Background Bottom")
								
							# Update Screen Data #
							drawPlayerStatsScreen = True
								
					# Target Room Mobs #
					for mNum, targetMob in enumerate(self.mobList):
						if targetMob.currentHP > 0:
							if (targetMob == dataAttacker and self.updateSkill.effectType == "Heal") \
							or (self.updateSkill.effectType == "Heal" and targetMob in dataAttacker.groupList) \
							or (targetMob != dataAttacker and self.updateSkill.effectType == "Damage" and targetMob not in dataAttacker.groupList):
							
								# Adjust Target Mob Health & Add To Delete List #
								if self.updateSkill.effectType == "Heal":
									targetMob.currentHP += attackPower
									if targetMob.currentHP > targetMob.maxHP : targetMob.currentHP = targetMob.maxHP
								else:
									targetMob.currentHP -= attackPower
									if targetMob.currentHP <= 0 : mobDelList.append(mNum)
								
								# Add Attacker To Defender's Combat List If Not In It #
								if targetMob.currentHP > 0 and dataAttacker.currentHP > 0 and targetMob != dataAttacker and self.updateSkill.effectType == "Damage":
									
									# Player Attacking Mob #
									if dataAttacker.objectType == "Player":
										if targetMob not in DATA_PLAYER.mobTargetPlayerCombatList and playerToRoomMessage == None and playerToRoomRange != -1 and playerToRoomRange <= targetMob.getViewRange():
											DATA_PLAYER.mobTargetPlayerCombatList.append(targetMob)
											
											# Message Data #
											if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
												postMessageList.append(targetMob.defaultTitle + " looks at you with an icy stare.")
											
									# Mob Attacking Mobs #
									elif dataAttacker.objectType == "Mob":
										if attackerToRoomMessage == None and attackerToRoomRange != -1 and attackerToRoomRange <= targetMob.getViewRange():
											if targetMob.combatTarget == None:
												targetMob.combatTarget = dataAttacker
												
												# Message Data #
												if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
													if attackerToRoomRange == 0 : postMessageList.append(targetMob.defaultTitle + " looks at " + dataAttacker.defaultTitle + " with an icy stare.")
													else : postMessageList.append(targetMob.defaultTitle + " looks " + str(attackerToRoomDir) + " with an icy stare.")
										
									# Add Idle Mob To Update Mob List #
									if targetMob not in self.updateMobList:
										self.updateMobList.append(targetMob)
										
								# Remove Player Action If Target Mob Was Being Tamed #
								if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming" and DATA_PLAYER.currentAction["Target Mob"] == targetMob:
									DATA_PLAYER.currentAction = None
									brokenConcentrationCheck = True
									
								# Initiate Defender Get Hit Animation (Red Fill/Flash) #
								if self.updateSkill.effectType == "Damage" and targetMob.currentHP > 0 and sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, targetMob):
									targetMob.animationDict["Get Hit"] = {"Timer":7}
									Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
									
								# Initiate Damage Number Animation (Numbers Bounce) #
								if self.updateSkill.effectType == "Damage" and targetMob.currentHP > 0 and sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, targetMob):
								
									# Create Number Image #
									if True:
										xDrawLoc = 0
										numberImageWidth = INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_width()
										numberImageHeight = INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_height()
										numberImage = pygame.Surface([numberImageWidth * len(str(attackPower)), numberImageHeight], pygame.SRCALPHA, 32)
										for i in str(attackPower):
											numberImage.blit(INTERFACE_IMAGE_DICT["Numbers Outline"][int(i)], [xDrawLoc, 0])
											xDrawLoc += numberImageWidth
									
									animationDict = {"Timer":150, "Draw Y Loc":0, "Number Image":numberImage, "Bounce Velocity":5.0, "Velocity Decrease":.295, "Bounce Count":0}
									
									# Initiate Damage Number Animation #
									if "Damage Number List" not in targetMob.animationDict : targetMob.animationDict["Damage Number List"] = []
									targetMob.animationDict["Damage Number List"].append(animationDict)
									if "Background Bottom" not in drawList : drawList.append("Background Bottom")
									
								# Update Screen Data #
								if targetMob in DATA_PLAYER.groupList:
									drawPlayerStatsScreen = True
									
					# Messages #
					if True:
						if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
							if hitPlayerCheck == True : Console.addDisplayLineToDictList(self.updateSkill.idSkill + " " + actionString1 + " YOU for " + str(attackPower) + " " + actionString2 + ".")
							
							# Player/Player Group Owned Spell #
							if dataAttacker.objectType == "Player" or dataAttacker in DATA_PLAYER.groupList:
								if healCount > 1 : Console.addDisplayLineToDictList(self.updateSkill.idSkill + " " + actionString1 + " your allies for " + str(attackPower) + " " + actionString2 + " each.")
								elif damageCount > 0 : Console.addDisplayLineToDictList(self.updateSkill.idSkill + " " + actionString1 + " your foes for " + str(attackPower) + " " + actionString2 + " each.")
							
							# Non-Player/Player Group Spell (Currently No Message) #
							else:
								pass
								
						if brokenConcentrationCheck == True:
							Console.addDisplayLineToDictList("Your concentration is broken.")
				
						if self.updateSkill.flags["Room Ticks"] <= 0:
							if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
								Console.addDisplayLineToDictList(self.updateSkill.idSkill + " disolves into a puff of smoke.")
							self.updateSkill = None
							
						for consoleMessage in postMessageList:
							Console.addDisplayLineToDictList(consoleMessage)
						
				# Player HP < 0 Check #
				if hitPlayerCheck and DATA_PLAYER.currentHP <= 0:
				
					# Remove All Mobs Targeting Player From Update Mob List (Resource Heavy) #
					attackingMobArea = None
					attackingMobRoom = None
					for attackingMob in DATA_PLAYER.mobTargetPlayerCombatList:
						if not attackingMob.isUpdateMob() and attackingMob.combatTarget == None:
							if attackingMobArea == None or (attackingMob.currentArea != attackingMobArea.idArea or attackingMob.currentAreaRandom != attackingMobArea.idRandom):
								attackingMobArea = getParentArea(SOLAR_SYSTEM_DICT[attackingMob.currentSolarSystem], attackingMob)
							if attackingMobRoom == None or (attackingMob.currentRoom != attackingMobRoom.idNum):
								attackingMobRoom = attackingMobArea.roomDict[attackingMob.currentRoom]
							
							if attackingMob in attackingMobRoom.updateMobList:
								del attackingMobRoom.updateMobList[attackingMobRoom.updateMobList.index(attackingMob)]
						
					DATA_PLAYER.killPlayer(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem])
					
				# Delete Mobs With < 0 HP #
				if len(mobDelList) > 0:
					mobDelList.reverse()
					for mNum in mobDelList:
						delMob = self.mobList[mNum]
						self.killMob(SOLAR_SYSTEM_DICT, DATA_PLAYER, delMob, ITEM_IMAGE_DICT)
						
						# Messages #
						if True:
							if dataAttacker.objectType == "Player" or sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, delMob):
								Console.addDisplayLineToDictList(delMob.defaultTitle + " is DEAD!", delMob.defaultTitleColorCode + "8w1y")
							else:
								delMobRoom = getParentArea(SOLAR_SYSTEM_DICT[delMob.currentSolarSystem], delMob).roomDict[delMob.currentRoom]
								distanceToPlayer, dirToPlayer, toPlayerMessage = getTargetRange(SOLAR_SYSTEM_DICT, delMobRoom, DATA_PLAYER, 3)
								if distanceToPlayer != -1 and distanceToPlayer > 0 and toPlayerMessage == None:
									oppositeDirDict = {"North":"South", "East":"West", "South":"North", "West":"East"}
									Console.addDisplayLineToDictList("You hear a death cry to the " + oppositeDirDict[dirToPlayer] + ".")
				
				# Draw Screens #
				if True:
					if len(drawList) > 0:
						for drawAreaID in drawList:
							if "Room" in Config.DRAW_SCREEN_DICT and drawAreaID not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append(drawAreaID)
							elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = [drawAreaID]
							
					if drawPlayerStatsScreen == True:
						Config.DRAW_SCREEN_DICT["Player Stats"] = True
						
	def updateItems(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, TICK_SPEED, UPDATE_TYPE, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT):
	
		updateItemDelList = []
		parentPlanet = None
		if "Spaceship Description" not in PARENT_AREA.flags : parentPlanet = SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[self.idPlanet]
		
		for iNum, targetItem in enumerate(self.updateItemList):
			updateItemDelList = targetItem.update(SOLAR_SYSTEM_DICT, iNum, DATA_PLAYER, UPDATE_TYPE, parentPlanet, PARENT_AREA, updateItemDelList, TICK_SPEED, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT)
		
		# Delete Items From UpdateItemList #
		updateItemDelList.reverse()
		for updateItemDelIndex in updateItemDelList:
			del self.updateItemList[updateItemDelIndex]
			
		# Update Display Surfaces #
		if len(updateItemDelList) > 0:
			pass
	
	def synchData(self, WINDOW, MOUSE, TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT):
	
		TICK_SPEED = Config.SYNCH_TICK_SPEED
		tickSeconds = TICK_SYNCH - self.tickSynch
		
		# Synch Rooms At A Medium Speed #
		for fastTurnNum in range(tickSeconds / TICK_SPEED):
			self.update(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, [], SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT, "Synch", TICK_SPEED)
		remainingTurns = tickSeconds % TICK_SPEED
		if remainingTurns > 0:
			self.update(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, PARENT_AREA, [], SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT, "Synch", remainingTurns)
			
	# Utility Functions #
	def displayRoom(self, PARENT_AREA, SOLAR_SYSTEM_DICT, DATA_PLAYER):
		
		if not self.lightCheck(SOLAR_SYSTEM_DICT):
			Console.addDisplayLineToDictList("It is too dark to see.", "21w1y")
		else:
			
			# Title #
			displayLine = self.title
			colorCode = self.titleColorCode
			if not self.inside and PARENT_AREA != None:
				if "Rain Timer" in PARENT_AREA.weatherDict:
					displayLine = displayLine + " [Rain]"
					colorCode = colorCode + "1w1r1dc3ddc1r"
				elif "Snow Timer" in PARENT_AREA.weatherDict:
					displayLine = displayLine + " [Snow]"
					colorCode = colorCode + "1w1r1dw3ddw1r"
			Console.addDisplayLineToDictList(displayLine, colorCode)
			
			# Exits #
			for exitDir in ["North", "East", "South", "West"]:
				if exitDir in self.exitDict:
				
					# Get Target Exit Room Data #
					exitSolarSystemId = None
					exitPlanetId = None
					exitAreaId = None
					exitRoomId = None
					if "Solar System" in self.exitDict[exitDir] : exitSolarSystemId = self.exitDict[exitDir]["Solar System"]
					if "Planet" in self.exitDict[exitDir] : exitPlanetId = self.exitDict[exitDir]["Planet"]
					if "Area" in self.exitDict[exitDir] : exitAreaId = self.exitDict[exitDir]["Area"]
					if "Room" in self.exitDict[exitDir] : exitRoomId = self.exitDict[exitDir]["Room"]
					
					# Get Target Exit Room #
					if True:
						targetExitRoom = None
						
						# Spaceship Main Exit #
						if self.exitDict[exitDir] == "Spaceship Exit":
							if PARENT_AREA.flags["Spaceship Status"] != "Landed" or PARENT_AREA.flags["Spaceship Door Status"] == "Locked":
								displayLine = exitDir + " - [Sealed] A Spaceship Door Hatch"
								colorCode = str(len(exitDir)) + "w3y1r6w2r22w"
							else:
								spaceshipExitSolarSystem = PARENT_AREA.flags["Landed Data"]["Solar System"]
								spaceshipExitPlanet = PARENT_AREA.flags["Landed Data"]["Planet"]
								spaceshipExitArea = PARENT_AREA.flags["Landed Data"]["Area"]
								spaceshipExitRoom = PARENT_AREA.flags["Landed Data"]["Room"]
								targetExitRoom = SOLAR_SYSTEM_DICT[spaceshipExitSolarSystem].planetDict[spaceshipExitPlanet].areaDict[spaceshipExitArea].roomDict[spaceshipExitRoom]
						
						# Spaceship Room #
						elif exitSolarSystemId == None and exitPlanetId == None and exitAreaId == None and PARENT_AREA != None and exitRoomId in PARENT_AREA.roomDict:
							targetExitRoom = PARENT_AREA.roomDict[exitRoomId]
						
						# Default Room #
						elif exitSolarSystemId != None and exitSolarSystemId in SOLAR_SYSTEM_DICT \
						and exitPlanetId != None and exitPlanetId in SOLAR_SYSTEM_DICT[exitSolarSystemId].planetDict \
						and exitAreaId != None and exitAreaId in SOLAR_SYSTEM_DICT[exitSolarSystemId].planetDict[exitPlanetId].areaDict \
						and exitRoomId in SOLAR_SYSTEM_DICT[exitSolarSystemId].planetDict[exitPlanetId].areaDict[exitAreaId].roomDict:
							targetExitRoom = SOLAR_SYSTEM_DICT[exitSolarSystemId].planetDict[exitPlanetId].areaDict[exitAreaId].roomDict[exitRoomId]
					
					# Door Check #
					if targetExitRoom != None:
						displayLine = exitDir + " - "
						colorCode = str(len(exitDir)) + "w3y"
						strDoorStatus = None
						if "Door Status" in self.exitDict[exitDir]:
							strDoorStatus = self.exitDict[exitDir]["Door Status"]
							if strDoorStatus == "Locked" : strDoorStatus = "Closed"
							displayLine = displayLine + "[" + strDoorStatus + "] "
							colorCode = colorCode + "1r" + str(len(strDoorStatus)) + "w2r"
						if strDoorStatus != "Closed":
							displayLine = displayLine + targetExitRoom.title
							colorCode = colorCode + targetExitRoom.titleColorCode
						
					# Write Exit Description #
					if targetExitRoom != None or self.exitDict[exitDir] == "Spaceship Exit":
						Console.addDisplayLineToDictList(displayLine, colorCode)
					else:
						Console.addDisplayLineToDictList(exitDir + " - The Void", str(len(exitDir)) + "w3y1dw7ddw")
				
					# Old Caption List #
					#displayLineDictList.append({"Display Line":displayLine, "Color Code":colorCode, "Line Count":1, "Caption List":[Caption.LoadCaption(0, 1, "Room Exit", {"Target Direction":exitDir, "Room Data":self})]})
					pass
						
			# Room Spell Message #
			if self.updateSkill != None:
				Console.addDisplayLineToDictList("There is a magical aura about the place.")
						
			# Spaceships #
			if len(self.spaceshipDictList) > 0:
				for tempSpaceshipDict in self.spaceshipDictList:
					displayLine = tempSpaceshipDict["ID"] + " is resting on the launch pad."
					colorCode = str(len(tempSpaceshipDict["ID"])) + "ddw29w1y"
					Console.addDisplayLineToDictList(displayLine, colorCode)
					
			# Control Panel #
			#if "Spaceship Control Panel" in self.flags or "Control Panel" in self.flags:
			#	Console.addDisplayLineToDictList("You see an Instrument Panel with many buttons.", "11w1dw10ddw1dw4ddw18w1y")
				
			# Mobs #
			if len(self.mobList) > 0:
				for mob in self.mobList:
					displayLinePrefix = "" ; colorCodePrefix = ""
					if mob in DATA_PLAYER.mobTargetList:
						displayLinePrefix = displayLinePrefix + "[+]"
						colorCodePrefix = colorCodePrefix + "3m"
					if "Group Leader" in mob.flags:
						displayLinePrefix = displayLinePrefix + "[L]"
						colorCodePrefix = colorCodePrefix + "3dr"
						
					displayLine = displayLinePrefix + mob.roomTitle
					colorCode = colorCodePrefix + mob.roomTitleColorCode
					
					Console.addDisplayLineToDictList(displayLine, colorCode)
					
			# Items #
			if len(self.itemList) > 0:
				
				for item in self.itemList:
					displayLine = item.roomTitle
					colorCode = item.roomTitleColorCode
					stackLineCheck = True
					
					# Planted Title Mod #
					if "Planted" in item.flags:
						displayLine = displayLine + " is planted in the ground."
						colorCode = item.defaultTitleColorCode + "25w1y"
					
					# Decaying Items #
					if ("Wilt Timer" in item.flags and item.flags["Wilt Timer"] <= 0) or "Decay Timer" in item.flags:
						displayLine = displayLine + " [Decaying]"
						colorCode = colorCode + "2r8w1r"
						
					# Quantity Check #
					if "Quantity" in item.flags and item.flags["Quantity"] > 1:
						displayLine = displayLine + " (" + str(item.flags["Quantity"]) + ")"
						colorCode = colorCode + "2r" + str(len(str(item.flags["Quantity"]))) + "w" + "1r"
						stackLineCheck = False
					
					Console.addDisplayLineToDictList(displayLine, colorCode, {"Stack Line":stackLineCheck})
	
	def addSpaceshipToRoom(self, TARGET_SPACESHIP):
	
		TARGET_SPACESHIP.flags["Spaceship Status"] = "Landed"
		TARGET_SPACESHIP.flags["Landed Data"] = {"Solar System":self.idSolarSystem, "Planet":self.idPlanet, "Area":self.idArea, "Room":self.idNum}
	
		spaceshipDict = {"ID":TARGET_SPACESHIP.idArea,
						 "Random ID":TARGET_SPACESHIP.idRandom,
						 "Key List":TARGET_SPACESHIP.flags["Spaceship Key List"],
						 "Description":TARGET_SPACESHIP.flags["Spaceship Description"]}
									   
		self.spaceshipDictList.append(spaceshipDict)
		
	def removeSpaceshipFromRoom(self, TARGET_ID, TARGET_RANDOM_ID):
	
		delNum = None
		for dNum, spaceshipDict in enumerate(self.spaceshipDictList):
			if TARGET_ID == spaceshipDict["ID"] and TARGET_RANDOM_ID == spaceshipDict["Random ID"]:
				delNum = dNum
				break
		if delNum != None:
			del self.spaceshipDictList[delNum]
	
	def killMob(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_MOB, ITEM_IMAGE_DICT, PLAYER_IS_ATTACKER=False):
	
		mobInPlayerGroup = False
		if TARGET_MOB in DATA_PLAYER.groupList : mobInPlayerGroup = True
	
		# Remove Target Mob From Room #
		self.removeMobFromRoom(TARGET_MOB)
		
		# Remove Target Mob From Player's Combat List #
		if TARGET_MOB in DATA_PLAYER.mobTargetList:
			del DATA_PLAYER.mobTargetList[DATA_PLAYER.mobTargetList.index(TARGET_MOB)]
		if TARGET_MOB in DATA_PLAYER.mobTargetPlayerCombatList:
			del DATA_PLAYER.mobTargetPlayerCombatList[DATA_PLAYER.mobTargetPlayerCombatList.index(TARGET_MOB)]
		
		# Remove Target Mob From Group #
		if len(TARGET_MOB.groupList) > 0:
			for groupEntity in TARGET_MOB.groupList:
				if TARGET_MOB in groupEntity.groupList:
					del groupEntity.groupList[groupEntity.groupList.index(TARGET_MOB)]
					
			# Assign New Group Leader #
			if "Group Leader" in TARGET_MOB.flags and len(TARGET_MOB.groupList) > 1:
				random.choice(TARGET_MOB.groupList).flags["Group Leader"] = True
				
			# Remove Leader Flag If Group Size Is 1 #
			if len(TARGET_MOB.groupList) == 1 and "Group Leader" in TARGET_MOB.groupList[0].flags:
				del TARGET_MOB.groupList[0].flags["Group Leader"]
		
		# Remove Target Mob From Surrounding Mob's Combat Target (Resource Heavy) #
		if True:
			currentUpdateArea = None
			currentRoom = None
			parentArea = getParentArea(SOLAR_SYSTEM_DICT[TARGET_MOB.currentSolarSystem], TARGET_MOB)
			surroundingAreaDataList, surroundingRoomDataList = getSurroundingRoomsDataList(SOLAR_SYSTEM_DICT, parentArea, self, Config.MOB_MOVE_CHECK_TARGET_RANGE)
			for targetRoomDataDict in surroundingRoomDataList:
				
				# Get Update Area & Room #
				if currentUpdateArea == None or (targetRoomDataDict["Room Area"] != currentUpdateArea.idArea or targetRoomDataDict["Room Area Random"] != currentUpdateArea.idRandom):
					if targetRoomDataDict["Room Area Random"] != None : currentUpdateArea = SOLAR_SYSTEM_DICT[targetRoomDataDict["Room Solar System"]].getTargetSpaceship(targetRoomDataDict["Room Area"], targetRoomDataDict["Room Area Random"])
					else : currentUpdateArea = SOLAR_SYSTEM_DICT[targetRoomDataDict["Room Solar System"]].planetDict[targetRoomDataDict["Room Planet"]].areaDict[targetRoomDataDict["Room Area"]]
				if currentRoom == None or (targetRoomDataDict["Room ID"] != currentRoom.idNum):
					currentRoom = currentUpdateArea.roomDict[targetRoomDataDict["Room ID"]]
				
				for currentMob in currentRoom.updateMobList:
					if currentMob.combatTarget == TARGET_MOB:
						currentMob.combatTarget = None
						
		# Create Corpse #
		if True:
			mobCorpse = DataItem.loadPrefab(-2, ITEM_IMAGE_DICT, {"Mob Data":TARGET_MOB})
			self.addItem(mobCorpse, DATA_PLAYER)
			
			# Add Gear And Inventory To Corpse #
			for gearSlot in TARGET_MOB.gearDict:
				if TARGET_MOB.gearDict[gearSlot] != None:
					targetGearItem = TARGET_MOB.gearDict[gearSlot]
					self.addItemToContainer(mobCorpse, targetGearItem)
			for targetItem in TARGET_MOB.inventoryList:
				self.addItemToContainer(mobCorpse, targetItem)
		
		# Generate Loot #
		if len(TARGET_MOB.lootDict) > 0:
			for iNum in range(TARGET_MOB.lootCount):
				for lootItemNum in TARGET_MOB.lootDict:
					lootItemChance = TARGET_MOB.lootDict[lootItemNum]
					if random.randrange(1, 101) <= lootItemChance:
						self.loadItem(lootItemNum, DATA_PLAYER, ITEM_IMAGE_DICT)
		
		# Draw Room Check #
		if sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_MOB):
			if mobInPlayerGroup == True : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
			elif mobInPlayerGroup == False : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
		
	def removeMobFromRoom(self, TARGET_MOB):
	
		# Mob List #
		if TARGET_MOB in self.mobList:
			del self.mobList[self.mobList.index(TARGET_MOB)]
		
		# Update Mob List #
		if TARGET_MOB in self.updateMobList:
			del self.updateMobList[self.updateMobList.index(TARGET_MOB)]
			
	def removeItemFromRoom(self, TARGET_ITEM):
	
		# Item List #
		if TARGET_ITEM in self.itemList:
			del self.itemList[self.itemList.index(TARGET_ITEM)]
		
		# Update Item List #
		if TARGET_ITEM in self.updateItemList:
			del self.updateItemList[self.updateItemList.index(TARGET_ITEM)]
	
	def createDoor(self, SOLAR_SYSTEM_DICT, TARGET_SOLAR_SYSTEM_ID, TARGET_DIR, FLAGS={}):
	
		if TARGET_DIR in self.exitDict:
			self.exitDict[TARGET_DIR]["Door Status"] = "Closed"
			if "Key Num" in FLAGS : self.exitDict[TARGET_DIR]["Key Num"] = FLAGS["Key Num"]
			if "Automatic" in FLAGS : self.exitDict[TARGET_DIR]["Door Type"] = "Automatic"
			else : self.exitDict[TARGET_DIR]["Door Type"] = "Default"
				
			# Create Other Door In Connecting Room #
			oppositeDir = None
			if TARGET_DIR == "North" : oppositeDir = "South"
			elif TARGET_DIR == "South" : oppositeDir = "North"
			elif TARGET_DIR == "East" : oppositeDir = "West"
			elif TARGET_DIR == "West" : oppositeDir = "East"
			
			if oppositeDir != None:
				connectingRoom = None	
				if "Solar System" not in self.exitDict[TARGET_DIR] and "Planet" not in self.exitDict[TARGET_DIR] and "Area" not in self.exitDict[TARGET_DIR]:
					connectingArea = SOLAR_SYSTEM_DICT[TARGET_SOLAR_SYSTEM_ID].getTargetSpaceship(self.idArea, self.idAreaRandom)
					connectingRoom = connectingArea.roomDict[self.exitDict[TARGET_DIR]["Room"]]
				elif "Solar System" in self.exitDict[TARGET_DIR] and "Planet" in self.exitDict[TARGET_DIR] and "Area" in self.exitDict[TARGET_DIR] and "Room" in self.exitDict[TARGET_DIR]:
					connectingArea = SOLAR_SYSTEM_DICT[self.exitDict[TARGET_DIR]["Solar System"]].planetDict[self.exitDict[TARGET_DIR]["Planet"]].areaDict[self.exitDict[TARGET_DIR]["Area"]]
					connectingRoom = connectingArea.roomDict[self.exitDict[TARGET_DIR]["Room"]]
					
				if connectingRoom != None and oppositeDir in connectingRoom.exitDict:
					connectingExit = connectingRoom.exitDict[oppositeDir]
					if "Solar System" not in connectingExit and "Planet" not in connectingExit and "Area" not in connectingExit and connectingExit["Room"] == self.idNum:
						connectingRoom.exitDict[oppositeDir]["Door Status"] = "Closed"
						if "Key Name" in FLAGS : connectingRoom.exitDict[oppositeDir]["Key Num"] = FLAGS["Key Num"]
						if "Automatic" in FLAGS : connectingRoom.exitDict[oppositeDir]["Door Type"] = "Automatic"
						else : connectingRoom.exitDict[oppositeDir]["Door Type"] = "Default"
					elif connectingExit["Solar System"] == self.idSolarSystem and connectingExit["Planet"] == self.idPlanet and connectingExit["Area"] == self.idArea and connectingExit["Room"] == self.idNum:
						connectingRoom.exitDict[oppositeDir]["Door Status"] = "Closed"
						if "Key Num" in FLAGS : connectingRoom.exitDict[oppositeDir]["Key Num"] = FLAGS["Key Num"]
						if "Automatic" in FLAGS : connectingRoom.exitDict[oppositeDir]["Door Type"] = "Automatic"
						else : connectingRoom.exitDict[oppositeDir]["Door Type"] = "Default"
			
	def ocluDoor(self, SOLAR_SYSTEM_DICT, TARGET_SOLAR_SYSTEM_ID, TARGET_ACTION, TARGET_DIR):
	
		if TARGET_ACTION == "Open" : targetStatus = "Open"
		elif TARGET_ACTION == "Close" : targetStatus = "Closed"
		elif TARGET_ACTION == "Lock" : targetStatus = "Locked"
		elif TARGET_ACTION == "Unlock" : targetStatus = "Closed"
		self.exitDict[TARGET_DIR]["Door Status"] = targetStatus
			
		# OCLU Other Door In Connecting Room #
		oppositeDir = None
		if TARGET_DIR == "North" : oppositeDir = "South"
		elif TARGET_DIR == "South" : oppositeDir = "North"
		elif TARGET_DIR == "East" : oppositeDir = "West"
		elif TARGET_DIR == "West" : oppositeDir = "East"
		
		if oppositeDir != None:
			connectingRoom = None
			if "Solar System" not in self.exitDict[TARGET_DIR] and "Planet" not in self.exitDict[TARGET_DIR] and "Area" not in self.exitDict[TARGET_DIR]:
				connectingArea = SOLAR_SYSTEM_DICT[TARGET_SOLAR_SYSTEM_ID].getTargetSpaceship(self.idArea, self.idAreaRandom)
				connectingRoom = connectingArea.roomDict[self.exitDict[TARGET_DIR]["Room"]]
			elif "Solar System" in self.exitDict[TARGET_DIR] and "Planet" in self.exitDict[TARGET_DIR] and "Area" in self.exitDict[TARGET_DIR] and "Room" in self.exitDict[TARGET_DIR]:
				connectingArea = SOLAR_SYSTEM_DICT[self.exitDict[TARGET_DIR]["Solar System"]].planetDict[self.exitDict[TARGET_DIR]["Planet"]].areaDict[self.exitDict[TARGET_DIR]["Area"]]
				connectingRoom = connectingArea.roomDict[self.exitDict[TARGET_DIR]["Room"]]
				
			if connectingRoom != None and oppositeDir in connectingRoom.exitDict:
				connectingExit = connectingRoom.exitDict[oppositeDir]
				if "Solar System" not in connectingExit and "Planet" not in connectingExit and "Area" not in connectingExit and connectingExit["Room"] == self.idNum:
					connectingRoom.exitDict[oppositeDir]["Door Status"] = targetStatus
				elif connectingExit["Solar System"] == self.idSolarSystem and connectingExit["Planet"] == self.idPlanet and connectingExit["Area"] == self.idArea and connectingExit["Room"] == self.idNum:
					connectingRoom.exitDict[oppositeDir]["Door Status"] = targetStatus
	
	def displayAreaText(self, PARENT_AREA):
	
		if "Spaceship Description" in PARENT_AREA.flags or self.inside:
			Console.addDisplayLineToDictList("You hear some squeaking sounds.")
		else:
			pass
		
	def lightCheck(self, SOLAR_SYSTEM_DICT):
	
		# Get Data #
		check = False
		parentPlanet = None
		if self.idSolarSystem != None and self.idPlanet != None:
			if self.idSolarSystem in SOLAR_SYSTEM_DICT and self.idPlanet in SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict:
				parentPlanet = SOLAR_SYSTEM_DICT[self.idSolarSystem].planetDict[self.idPlanet]
		
		# Checks #
		if parentPlanet != None and parentPlanet.nightCheck == False:
			check = True
		if "Light" in self.flags:
			check = True
			
		return check
	
	def wetCheck(self, PARENT_AREA, UPDATE_TYPE):
	
		wetCheck = False
		
		if UPDATE_TYPE == "Default":
		
			# Room Water #
			if self.idNum in PARENT_AREA.wetTimerRoomDict and "Water" in PARENT_AREA.wetTimerRoomDict[self.idNum]:
				wetCheck = True
			
			# Area Water #
			if not wetCheck and not self.inside and "Water" in PARENT_AREA.wetTimerAreaDict:
				wetCheck = True
				
		elif UPDATE_TYPE == "Synch":
			
			if not self.inside:
				for tempSynchWeatherDataDict in PARENT_AREA.synchWeatherDictList:
					if tempSynchWeatherDataDict["Weather Type"] == "Rain Timer" \
					and (self.tickSynch - Config.SYNCH_TICK_SPEED) >= tempSynchWeatherDataDict["Synch Num"] \
					and (self.tickSynch - Config.SYNCH_TICK_SPEED) < (tempSynchWeatherDataDict["Synch Num"] + tempSynchWeatherDataDict["Timer Duration"]):
						wetCheck = True
						break
					elif tempSynchWeatherDataDict["Synch Num"] > (self.tickSynch - Config.SYNCH_TICK_SPEED):
						break
			
		return wetCheck
	
	def emptyContainer(self, TARGET_CONTAINER, DATA_PLAYER):
	
		for containerItem in TARGET_CONTAINER.flags["Container List"]:
			self.addItem(containerItem, DATA_PLAYER)
			
		TARGET_CONTAINER.flags["Container List"] = []
	
def loadNewGalaxy(DATA_PLAYER, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT):
	
	solarSystemDict = {}
	
	# Solar System - Sol #
	if True:
	
		# ID Declarations #
		if True:
			ID_SOLAR_SYSTEM_SOL = "Sol"
			ID_STAR_SOL = "Sol"
			
			ID_PLANET_COTU = "Center Of The Universe"
			ID_AREA_COTU_SPACEPORT = "COTU Spaceport"
			
			ID_PLANET_MERCURY = "Mercury"
			ID_PLANET_VENUS = "Venus"
			
			ID_PLANET_EARTH = "Earth"
			ID_AREA_EARTH_DEBUG_FIELD = "Debug Field"
			
			ID_PLANET_MARS = "Mars"
			ID_PLANET_JUPITER = "Jupiter"
			ID_PLANET_SATURN = "Saturn"
			ID_PLANET_URANUS = "Uranus"
			ID_PLANET_NEPTUNE = "Neptune"
			ID_PLANET_PLUTO = "Pluto"
		
		# System & Parent Star - Sol #
		solarSystemDict[ID_SOLAR_SYSTEM_SOL] = SolarSystem(ID_SOLAR_SYSTEM_SOL)
		starSol = Planet(ID_SOLAR_SYSTEM_SOL, ID_STAR_SOL)
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_STAR_SOL] = starSol
		
	# Planet - Center of the Universe #
	if True:
		planetCOTU = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, "Planet", ID_STAR_SOL, 1000, 24, 8760, 20.0, .10)
		planetCOTU.keyList = ["center", "universe", "center of the universe"]
		
		# Area - Debug Spaceship #
		if True:
			ID_AREA_DEBUG_SPACESHIP = "Debug Spaceship"
			areaDebugSpaceship = Area(ID_SOLAR_SYSTEM_SOL, None, ID_AREA_DEBUG_SPACESHIP)
			solarSystemDict[ID_SOLAR_SYSTEM_SOL].spaceshipList.append(areaDebugSpaceship)
			areaDebugSpaceship.generateSpaceship(DATA_PLAYER, solarSystemDict, ID_SOLAR_SYSTEM_SOL, ITEM_IMAGE_DICT)
			
		# Area - COTU Spaceport #
		if True:
			areaCOTUSpaceport = Area(ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
			
			# Room 0 - Floating In A Void #
			if True:
				roomCOTUSpaceport0 = Room(0, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport0.title = "Floating In A Void"
				roomCOTUSpaceport0.titleColorCode = "18w"
				roomCOTUSpaceport0.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":3}
				areaCOTUSpaceport.roomDict[0] = roomCOTUSpaceport0
			
			# Room 1 - Standing On A Crystaline Platform #
			if True:
				roomCOTUSpaceport1 = Room(1, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport1.title = "Standing On A Crystaline Platform"
				roomCOTUSpaceport1.titleColorCode = "14w11lc8w"
				roomCOTUSpaceport1.exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":3}
				roomCOTUSpaceport1.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":2}
				roomCOTUSpaceport1.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":4}
				roomCOTUSpaceport1.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":6}
				for i in range(4) : roomCOTUSpaceport1.loadItem(3, DATA_PLAYER, ITEM_IMAGE_DICT)
				roomCOTUSpaceport1.loadItem(21, DATA_PLAYER, ITEM_IMAGE_DICT)
				roomCOTUSpaceport1.loadItem(22, DATA_PLAYER, ITEM_IMAGE_DICT)
				roomCOTUSpaceport1.loadItem(23, DATA_PLAYER, ITEM_IMAGE_DICT)
				roomCOTUSpaceport1.loadItem(24, DATA_PLAYER, ITEM_IMAGE_DICT, {"Quantity":50})
				roomCOTUSpaceport1.loadItem(25, DATA_PLAYER, ITEM_IMAGE_DICT, {"Quantity":50})
				roomCOTUSpaceport1.loadItem(26, DATA_PLAYER, ITEM_IMAGE_DICT, {"Quantity":50})
				roomCOTUSpaceport1.loadItem(29, DATA_PLAYER, ITEM_IMAGE_DICT, {"Quantity":50})
				areaCOTUSpaceport.roomDict[1] = roomCOTUSpaceport1
			
			# Room 2 - Item Shop At The End Of The Universe #
			if True:
				roomCOTUSpaceport2 = Room(2, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport2.title = "Item Shop At The End Of The Universe"
				roomCOTUSpaceport2.titleColorCode = "36w"
				roomCOTUSpaceport2.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":1}
				#roomCOTUSpaceport2.inside = True
				roomCOTUSpaceport2.flags["Light"] = True
				#roomCOTUSpaceport2.floorType = "Dirt"
				
				# Load Mobs & Items #
				roomCOTUSpaceport2.loadMob(1, DATA_PLAYER, ENTITY_IMAGE_DICT)
				itemChest = DataItem.loadPrefab(10, ITEM_IMAGE_DICT)
				roomCOTUSpaceport2.addItemToContainer(itemChest, DataItem.loadPrefab(1, ITEM_IMAGE_DICT))
				roomCOTUSpaceport2.addItemToContainer(itemChest, DataItem.loadPrefab(2, ITEM_IMAGE_DICT))
				roomCOTUSpaceport2.addItemToContainer(itemChest, DataItem.loadPrefab(3, ITEM_IMAGE_DICT))
				roomCOTUSpaceport2.addItem(itemChest, DATA_PLAYER)
				
				areaCOTUSpaceport.roomDict[2] = roomCOTUSpaceport2
				
			# Room 3 - A Lush Garden #
			if True:
				roomCOTUSpaceport3 = Room(3, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport3.title = "A Lush Garden"
				roomCOTUSpaceport3.titleColorCode = "13w"
				roomCOTUSpaceport3.exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":0}
				roomCOTUSpaceport3.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":1}
				roomCOTUSpaceport3.floorType = "Dirt"
				
				# Load Mobs & Items #
				roomCOTUSpaceport3.loadItem(20, DATA_PLAYER, ITEM_IMAGE_DICT)
				itemChest = DataItem.loadPrefab(10, ITEM_IMAGE_DICT)
				for i in range(10) : roomCOTUSpaceport3.addItemToContainer(itemChest, DataItem.loadPrefab(13, ITEM_IMAGE_DICT))
				for i in range(10) : roomCOTUSpaceport3.addItemToContainer(itemChest, DataItem.loadPrefab(14, ITEM_IMAGE_DICT))
				for i in range(10) : roomCOTUSpaceport3.addItemToContainer(itemChest, DataItem.loadPrefab(15, ITEM_IMAGE_DICT))
				for i in range(10) : roomCOTUSpaceport3.addItemToContainer(itemChest, DataItem.loadPrefab(16, ITEM_IMAGE_DICT))
				for i in range(10) : roomCOTUSpaceport3.addItemToContainer(itemChest, DataItem.loadPrefab(17, ITEM_IMAGE_DICT))
				for i in range(10) : roomCOTUSpaceport3.addItemToContainer(itemChest, DataItem.loadPrefab(18, ITEM_IMAGE_DICT))
				roomCOTUSpaceport3.addItem(itemChest, DATA_PLAYER)
				itemTree = DataItem.loadPrefab(13, ITEM_IMAGE_DICT)
				itemTree.setPlantStage(3, ITEM_IMAGE_DICT)
				roomCOTUSpaceport3.addItem(itemTree, DATA_PLAYER)
				
				areaCOTUSpaceport.roomDict[3] = roomCOTUSpaceport3
				
			# Room 4 - A Hallway To COTU Spaceport #
			if True:
				roomCOTUSpaceport4 = Room(4, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport4.title = "A Hallway To COTU Spaceport"
				roomCOTUSpaceport4.titleColorCode = "27w"
				roomCOTUSpaceport4.exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":1}
				roomCOTUSpaceport4.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":5}
				roomCOTUSpaceport4.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":7}
				roomCOTUSpaceport4.flags["Light"] = True
				areaCOTUSpaceport.roomDict[4] = roomCOTUSpaceport4
			
			# Room 5 - A Launch Pad #
			if True:
				roomCOTUSpaceport5 = Room(5, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport5.title = "A Launch Pad"
				roomCOTUSpaceport5.titleColorCode = "12w"
				roomCOTUSpaceport5.exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":4}
				roomCOTUSpaceport5.flags["No Mob"] = True
				roomCOTUSpaceport5.flags["Light"] = True
				areaCOTUSpaceport.roomDict[5] = roomCOTUSpaceport5
				areaCOTUSpaceport.flags["Launch Pad Room List"].append(5)
				roomCOTUSpaceport5.addSpaceshipToRoom(solarSystemDict[ID_SOLAR_SYSTEM_SOL].getTargetSpaceship(areaDebugSpaceship.idArea, areaDebugSpaceship.idRandom))
			
			# Room 6 - A Portal To Earth #
			if True:
				roomCOTUSpaceport6 = Room(6, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport6.title = "A Portal To Earth"
				roomCOTUSpaceport6.titleColorCode = "17w"
				roomCOTUSpaceport6.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":1}
				roomCOTUSpaceport6.exitDict["South"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_EARTH, "Area":"World Map", "Room":0}
				areaCOTUSpaceport.roomDict[6] = roomCOTUSpaceport6
				
			# Room 7 - A Training Center Hallway #
			if True:
				roomCOTUSpaceport7 = Room(7, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport7.title = "A Training Center Hallway"
				roomCOTUSpaceport7.titleColorCode = "25w"
				roomCOTUSpaceport7.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":8}
				roomCOTUSpaceport7.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":4}
				roomCOTUSpaceport7.inside = True
				roomCOTUSpaceport7.flags["Light"] = True
				areaCOTUSpaceport.roomDict[7] = roomCOTUSpaceport7
			
			# Room 8 - A Training Center Hallway #
			if True:
				roomCOTUSpaceport8 = Room(8, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport8.title = "A Training Center Hallway"
				roomCOTUSpaceport8.titleColorCode = "25w"
				roomCOTUSpaceport8.exitDict["East"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":9}
				roomCOTUSpaceport8.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":7}
				roomCOTUSpaceport8.inside = True
				roomCOTUSpaceport8.flags["Light"] = True
				areaCOTUSpaceport.roomDict[8] = roomCOTUSpaceport8
				
			# Room 9 - A Training Center #
			if True:
				roomCOTUSpaceport9 = Room(9, ID_SOLAR_SYSTEM_SOL, ID_PLANET_COTU, ID_AREA_COTU_SPACEPORT)
				roomCOTUSpaceport9.title = "A Training Center"
				roomCOTUSpaceport9.titleColorCode = "17w"
				roomCOTUSpaceport9.exitDict["West"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":8}
				roomCOTUSpaceport9.inside = True
				roomCOTUSpaceport9.flags["Light"] = True
				
				trainingCenterControlPanel = DataItem.loadPrefab(-3, ITEM_IMAGE_DICT)
				trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 1", "Target ID":2, "Key List":Utility.createKeyList("button 1")})
				trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 2", "Target ID":3, "Key List":Utility.createKeyList("button 2")})
				trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 3", "Target ID":4, "Key List":Utility.createKeyList("button 3")})
				trainingCenterControlPanel.flags["Button List"].append({"Button Type":"Generate", "Target Object Type":"Mob", "Button Label":"Generate Mob 4", "Target ID":5, "Key List":Utility.createKeyList("button 4")})
				roomCOTUSpaceport9.addItem(trainingCenterControlPanel, DATA_PLAYER)
				
				areaCOTUSpaceport.roomDict[9] = roomCOTUSpaceport9
			
			planetCOTU.areaDict[ID_AREA_COTU_SPACEPORT] = areaCOTUSpaceport
			
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_COTU] = planetCOTU
		
	# Planet - Mercury #
	if True:
		planetMercury = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_MERCURY, "Planet", ID_STAR_SOL, 400, 600, 2832, 2.0)
		planetMercury.keyList = ["mercury"]
		#planetMercury.generateArea(ID_SOLAR_SYSTEM_SOL)
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_MERCURY] = planetMercury
	
	# Planet - Venus #
	if True:
		planetVenus = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_VENUS, "Planet", ID_STAR_SOL, 700, 5400, 5400, 3.0, .95, "Acid")
		planetVenus.keyList = ["venus"]
		#planetVenus.generateArea(ID_SOLAR_SYSTEM_SOL)
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_VENUS] = planetVenus
		
	# Planet - Earth #
	if True:
		planetEarth = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_EARTH, "Planet", ID_STAR_SOL, 1000, 24, 8760, 20.0, .10)
		planetEarth.keyList = ["earth"]
		planetEarth.generateWorldMap(DATA_PLAYER, ID_SOLAR_SYSTEM_SOL, ITEM_IMAGE_DICT)
		
		# Exit - Portal To COTU #
		planetEarth.areaDict["World Map"].roomDict[0].exitDict["North"] = {"Solar System":ID_SOLAR_SYSTEM_SOL, "Planet":ID_PLANET_COTU, "Area":ID_AREA_COTU_SPACEPORT, "Room":6}
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_EARTH] = planetEarth
		
	# Planet - Mars #
	if True:
		planetMars = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_MARS, "Planet", ID_STAR_SOL, 1500, 25, 16500, 23.5)
		planetMars.keyList = ["mars"]
		#planetMars.generateArea(ID_SOLAR_SYSTEM_SOL)
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_MARS] = planetMars
	
	# Planet - Jupiter #
	if True:
		planetJupiter = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_JUPITER, "Planet", ID_STAR_SOL, 5200, 10, 105120, 3.0)
		planetJupiter.keyList = ["jupiter"]
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_JUPITER] = planetJupiter
	
	# Planet - Saturn #
	if True:
		planetSaturn = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_SATURN, "Planet", ID_STAR_SOL, 9600, 10, 262800, 20.0)
		planetSaturn.keyList = ["saturn"]
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_SATURN] = planetSaturn
	
	# Planet - Uranus #
	if True:
		planetUranus = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_URANUS, "Planet", ID_STAR_SOL, 19200, 18, 735840, 85)
		planetUranus.keyList = ["uranus"]
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_URANUS] = planetUranus
	
	# Planet - Neptune #
	if True:
		planetNeptune = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_NEPTUNE, "Planet", ID_STAR_SOL, 30100, 19, 1445406, 20.0)
		planetNeptune.keyList = ["neptune"]
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_NEPTUNE] = planetNeptune
	
	# Planet - Pluto #
	if True:
		planetPluto = Planet(ID_SOLAR_SYSTEM_SOL, ID_PLANET_PLUTO, "Planet", ID_STAR_SOL, 39500, 3744, 2190240, 20.0)
		planetPluto.keyList = ["pluto"]
		#planetPluto.generateArea(ID_SOLAR_SYSTEM_SOL)
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_PLUTO] = planetPluto
	
	# Load Doors - Must Be Done AFTER Loading All Galaxies #
	if True:
		
		# Planet - Center of the Universe - Area - COTU Spaceport #
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_COTU].areaDict[ID_AREA_COTU_SPACEPORT].roomDict[1].createDoor(solarSystemDict, ID_SOLAR_SYSTEM_SOL, "East", {"Key Num":1234}) # Item Shop Door #
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_COTU].areaDict[ID_AREA_COTU_SPACEPORT].roomDict[5].createDoor(solarSystemDict, ID_SOLAR_SYSTEM_SOL, "North", {"Key Num":12345, "Automatic":True}) # Launch Pad Door #
		solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_COTU].areaDict[ID_AREA_COTU_SPACEPORT].roomDict[4].createDoor(solarSystemDict, ID_SOLAR_SYSTEM_SOL, "East", {"Automatic":True}) # Training Center Door #
		#solarSystemDict[ID_SOLAR_SYSTEM_SOL].planetDict[ID_PLANET_COTU].areaDict[ID_AREA_COTU_SPACEPORT].roomDict[6].createDoor(solarSystemDict, ID_SOLAR_SYSTEM_SOL, "South", {"Automatic":True}) # Portal To Earth Door #
		
	# Zero All Areas #
	for solarSystemId in solarSystemDict:
		
		targetSolarSystem = solarSystemDict[solarSystemId]
		for targetSpaceship in targetSolarSystem.spaceshipList:
			targetSpaceship.zeroAreaCoordinates(solarSystemDict)
		
		for targetPlanetId in targetSolarSystem.planetDict:
			targetPlanet = targetSolarSystem.planetDict[targetPlanetId]
			for targetAreaId in targetPlanet.areaDict:
				targetArea = targetPlanet.areaDict[targetAreaId]
				targetArea.zeroAreaCoordinates(solarSystemDict)
		
	return solarSystemDict
	
def getParentArea(TARGET_SOLAR_SYSTEM, TARGET_OBJECT):
	
	targetArea = None
	
	if TARGET_OBJECT.objectType in ["Player", "Mob", "Item", "Room"] and "In Spaceship" in TARGET_OBJECT.flags:
		if TARGET_OBJECT.objectType == "Room" : targetArea = TARGET_SOLAR_SYSTEM.getTargetSpaceship(TARGET_OBJECT.idArea, TARGET_OBJECT.idAreaRandom)
		else : targetArea = TARGET_SOLAR_SYSTEM.getTargetSpaceship(TARGET_OBJECT.currentArea, TARGET_OBJECT.currentAreaRandom)
	else:
		if TARGET_OBJECT.objectType == "Room" : targetArea = TARGET_SOLAR_SYSTEM.planetDict[TARGET_OBJECT.idPlanet].areaDict[TARGET_OBJECT.idArea]
		else : targetArea = TARGET_SOLAR_SYSTEM.planetDict[TARGET_OBJECT.currentPlanet].areaDict[TARGET_OBJECT.currentArea]

	return targetArea
	
def getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, CURRENT_AREA, CURRENT_ROOM, TARGET_DIR, TARGET_ROOM_DISTANCE, IGNORE_DOORS=False):

	currentAreaId = CURRENT_AREA.idArea
	messageType = None
	
	for rNum in range(TARGET_ROOM_DISTANCE):
		if TARGET_DIR not in CURRENT_ROOM.exitDict:
			if messageType == None : messageType = "No Exit"
			break
		else:
			targetExit = CURRENT_ROOM.exitDict[TARGET_DIR]
			if "Door Status" in targetExit and targetExit["Door Status"] in ["Closed", "Locked"]:
				messageType = "Door Is Closed"
				if IGNORE_DOORS == False : break
			elif targetExit == "Spaceship Exit" and (CURRENT_AREA.flags["Spaceship Status"] != "Landed" or CURRENT_AREA.flags["Spaceship Door Status"] == "Locked"):
				messageType = "Door Is Closed"
				if IGNORE_DOORS == False or "Landed Data" not in CURRENT_AREA.flags : break
				
			# Spaceship Exit #
			if targetExit == "Spaceship Exit" and "Landed Data" in CURRENT_AREA.flags:
				spaceshipExitSolarSystem = CURRENT_AREA.flags["Landed Data"]["Solar System"]
				spaceshipExitPlanet = CURRENT_AREA.flags["Landed Data"]["Planet"]
				spaceshipExitArea = CURRENT_AREA.flags["Landed Data"]["Area"]
				spaceshipExitRoom = CURRENT_AREA.flags["Landed Data"]["Room"]
				CURRENT_AREA = SOLAR_SYSTEM_DICT[spaceshipExitSolarSystem].planetDict[spaceshipExitPlanet].areaDict[spaceshipExitArea]
				CURRENT_ROOM = CURRENT_AREA.roomDict[spaceshipExitRoom]
				currentAreaId = CURRENT_AREA.idArea

			# Spaceship Room #
			elif "Solar System" not in targetExit and "Planet" not in targetExit and "Area" not in targetExit:
				if "Spaceship Description" in CURRENT_AREA.flags and CURRENT_AREA.idArea == currentAreaId:
					if targetExit["Room"] in CURRENT_AREA.roomDict:
						CURRENT_ROOM = CURRENT_AREA.roomDict[targetExit["Room"]]
				
			# Area Room #
			elif targetExit["Solar System"] in SOLAR_SYSTEM_DICT and targetExit["Planet"] in SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict and targetExit["Area"] in SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict and targetExit["Room"] in SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict[targetExit["Area"]].roomDict:
				CURRENT_ROOM = SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict[targetExit["Area"]].roomDict[targetExit["Room"]]
				if currentAreaId != targetExit["Area"]:
					CURRENT_AREA = SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict[targetExit["Area"]]
					currentAreaId = targetExit["Area"]
		
	return CURRENT_AREA, CURRENT_ROOM, messageType
	
def getSurroundingRoomsDataList(SOLAR_SYSTEM_DICT, START_AREA, START_ROOM, TARGET_RANGE):

	oppositeDirDict = {"North":"South", "East":"West", "South":"North", "West":"East"}

	# Examine Room Function #
	def examineRoomData(TARGET_AREA, TARGET_ROOM, TARGET_RANGE, TARGET_DIR, EXAMINED_AREA_LIST, EXAMINED_ROOM_LIST, VIEW_LOC):
		
		# Area #
		if {"Solar System":TARGET_ROOM.idSolarSystem, "Planet":TARGET_ROOM.idPlanet, "Area":TARGET_ROOM.idArea, "Area Random":TARGET_ROOM.idAreaRandom} not in EXAMINED_AREA_LIST:
			EXAMINED_AREA_LIST.append({"Solar System":TARGET_ROOM.idSolarSystem,
									   "Planet":TARGET_ROOM.idPlanet,
									   "Area":TARGET_ROOM.idArea,
									   "Area Random":TARGET_ROOM.idAreaRandom})
		
		# Room #
		EXAMINED_ROOM_LIST.append({"Room Solar System":TARGET_ROOM.idSolarSystem,
								   "Room Planet":TARGET_ROOM.idPlanet,
								   "Room Area":TARGET_ROOM.idArea,
								   "Room Area Random":TARGET_ROOM.idAreaRandom,
								   "Room ID":TARGET_ROOM.idNum})
		
		if (VIEW_LOC[0] + VIEW_LOC[1]) < TARGET_RANGE:
		
			firstLoc = copy.deepcopy(VIEW_LOC)
			exitDirList = ["North", "East", "South", "West"]
			if TARGET_DIR != None and oppositeDirDict[TARGET_DIR] in exitDirList : del exitDirList[exitDirList.index(oppositeDirDict[TARGET_DIR])]
			for targetExitDir in exitDirList:
			
				if targetExitDir != "North":
					VIEW_LOC = copy.deepcopy(firstLoc)
			
				if targetExitDir in TARGET_ROOM.exitDict:
					tempArea, tempRoom, tempMessage = getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, TARGET_AREA, TARGET_ROOM, targetExitDir, 1, True)
					
					if targetExitDir in ["East", "West"] : VIEW_LOC[0] += 1
					elif targetExitDir in ["North", "South"] : VIEW_LOC[1] += 1
					
					if {"Room Solar System":tempRoom.idSolarSystem, "Room Planet":tempRoom.idPlanet, "Room Area":tempRoom.idArea, "Room Area Random":tempRoom.idAreaRandom, "Room ID":tempRoom.idNum} not in EXAMINED_ROOM_LIST:
						EXAMINED_AREA_LIST, EXAMINED_ROOM_LIST = examineRoomData(tempArea, tempRoom, TARGET_RANGE, targetExitDir, EXAMINED_AREA_LIST, EXAMINED_ROOM_LIST, VIEW_LOC)
						
		return EXAMINED_AREA_LIST, EXAMINED_ROOM_LIST
			
	# Get Data List #
	examinedAreaDataList, examinedRoomDataList = examineRoomData(START_AREA, START_ROOM, TARGET_RANGE, None, [], [], [0, 0])
	
	return examinedAreaDataList, examinedRoomDataList
	
def sameRoomCheck(SOLAR_SYSTEM_DICT, TARGET_OBJECT_1, TARGET_OBJECT_2):

	# Target 1 #
	if True:
		target1SpaceshipCheck = False
		if TARGET_OBJECT_1.objectType in ["Player", "Mob", "Item"]:
			target1AreaData = getParentArea(SOLAR_SYSTEM_DICT[TARGET_OBJECT_1.currentSolarSystem], TARGET_OBJECT_1)
			target1Room = TARGET_OBJECT_1.currentRoom
		elif TARGET_OBJECT_1.objectType == "Room":
			target1AreaData = getParentArea(SOLAR_SYSTEM_DICT[TARGET_OBJECT_1.idSolarSystem], TARGET_OBJECT_1)
			target1Room = TARGET_OBJECT_1.idNum
		target1Area = target1AreaData.idArea
		target1Planet = target1AreaData.idPlanet
		target1SolarSystem = target1AreaData.idSolarSystem
		if "Spaceship Description" in target1AreaData.flags : target1SpaceshipCheck = True
	
	# Target 2 #
	if True:
		target2SpaceshipCheck = False
		if TARGET_OBJECT_2.objectType in ["Player", "Mob", "Item"]:
			target2AreaData = getParentArea(SOLAR_SYSTEM_DICT[TARGET_OBJECT_2.currentSolarSystem], TARGET_OBJECT_2)
			target2Room = TARGET_OBJECT_2.currentRoom
		elif TARGET_OBJECT_2.objectType == "Room":
			target2AreaData = getParentArea(SOLAR_SYSTEM_DICT[TARGET_OBJECT_2.idSolarSystem], TARGET_OBJECT_2)
			target2Room = TARGET_OBJECT_2.idNum
		target2Area = target2AreaData.idArea
		target2Planet = target2AreaData.idPlanet
		target2SolarSystem = target2AreaData.idSolarSystem
		if "Spaceship Description" in target2AreaData.flags : target2SpaceshipCheck = True
		
	# Same Room Check #
	sameRoomCheck = False
	if target1SpaceshipCheck == target2SpaceshipCheck and target1SolarSystem == target2SolarSystem and target1Planet == target2Planet and target1Area == target2Area and target1Room == target2Room:
		sameRoomCheck = True
		
	return sameRoomCheck
		
def getTargetRange(SOLAR_SYSTEM_DICT, START_ROOM, TARGET_OBJECT, MAX_RANGE):

	targetRange = 0
	searchDir = None
	targetFoundCheck = False
	messageType = None

	# Create TargetList & First Room Check #
	if True:
		targetObjectList = START_ROOM.mobList
		if TARGET_OBJECT.objectType == "Item" : targetObjectList = START_ROOM.itemList
		elif TARGET_OBJECT.objectType in ["Player", "Room"] : targetObjectList = None
		if targetObjectList != None and TARGET_OBJECT in targetObjectList : targetFoundCheck = True
		elif TARGET_OBJECT.objectType in ["Player", "Room"] and sameRoomCheck(SOLAR_SYSTEM_DICT, TARGET_OBJECT, START_ROOM) : targetFoundCheck = True
	
	# Create Side Dir List #
	if not targetFoundCheck:
		sideDirList = {"North":["East", "West"],
					   "East":["North", "South"],
					   "South":["East", "West"],
					   "West":["North", "South"]}
	
	# Room Search #
	if not targetFoundCheck:
		for searchDir in ["North", "East", "South", "West"]:
			messageMaster = None
			currentRoom = START_ROOM
			if TARGET_OBJECT.objectType == "Room" : tempSolarSystemId = TARGET_OBJECT.idSolarSystem
			else : tempSolarSystemId = TARGET_OBJECT.currentSolarSystem
			currentArea = getParentArea(SOLAR_SYSTEM_DICT[tempSolarSystemId], TARGET_OBJECT)
			for rNum in range(MAX_RANGE):
				messageType = messageMaster
				if searchDir not in currentRoom.exitDict : break
				elif searchDir in currentRoom.exitDict:
					currentArea, currentRoom, tempMessage = getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, currentArea, currentRoom, searchDir, 1, True)
					if tempMessage == "Door Is Closed" : messageMaster = tempMessage
					
					# Room Check #
					targetObjectList = None
					if TARGET_OBJECT.objectType in ["Player", "Room"] and sameRoomCheck(SOLAR_SYSTEM_DICT, TARGET_OBJECT, currentRoom):
						messageType = messageMaster
						targetFoundCheck = True
						targetRange = rNum + 1
						break
					elif TARGET_OBJECT.objectType == "Mob" : targetObjectList = currentRoom.mobList
					elif TARGET_OBJECT.objectType == "Item" : targetObjectList = currentRoom.itemList
					if targetObjectList != None and TARGET_OBJECT in targetObjectList:
						messageType = messageMaster
						targetFoundCheck = True
						targetRange = rNum + 1
						break
					
					for sideDir in sideDirList[searchDir]:
						messageType = messageMaster
						sideRoom = currentRoom
						sideArea = currentArea
						sideRange = MAX_RANGE - (rNum + 1)
						if sideRange > (rNum + 1) : sideRange = rNum + 1
						for sideNum in range(sideRange):
							if sideDir not in sideRoom.exitDict : break
							else:
								sideArea, sideRoom, tempMessage = getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, sideArea, sideRoom, sideDir, 1, True)
								if tempMessage == "Door Is Closed" : messageType = tempMessage
								
								# Room Check #
								targetObjectList = None
								if TARGET_OBJECT.objectType in ["Player", "Room"] and sameRoomCheck(SOLAR_SYSTEM_DICT, TARGET_OBJECT, sideRoom):
									targetFoundCheck = True
									targetRange = (rNum + 1) + (sideNum + 1)
									break
								elif TARGET_OBJECT.objectType == "Mob" : targetObjectList = sideRoom.mobList
								elif TARGET_OBJECT.objectType == "Item" : targetObjectList = sideRoom.itemList
								if targetObjectList != None and TARGET_OBJECT in targetObjectList:
									targetFoundCheck = True
									targetRange = (rNum + 1) + (sideNum + 1)
									break
									
						if targetFoundCheck : break
				if targetFoundCheck : break
			if targetFoundCheck : break
			
	# Return Data #
	if not targetFoundCheck:
		return -1, None, messageType
	else:
		return targetRange, searchDir, messageType

def synchAllGameData(TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER):

	for solarSystemId in SOLAR_SYSTEM_DICT:
		targetSolarSystem = SOLAR_SYSTEM_DICT[solarSystemId]
		for planetId in targetSolarSystem.planetDict:
			targetPlanet = targetSolarSystem.planetDict[planetId]
			if targetPlanet.tickSynch < TICK_SYNCH:
				targetPlanet.synchData(TICK_SYNCH)
			
			for areaId in targetPlanet.areaDict:
				targetArea = targetPlanet.areaDict[areaId]
				if targetArea.tickSynch < TICK_SYNCH:
					targetArea.tickSynch = TICK_SYNCH
					
				for roomId in targetArea.roomDict:
					targetRoom = targetArea.roomDict[roomId]
					if targetRoom.tickSynch < TICK_SYNCH:
						targetRoom.tickSynch = TICK_SYNCH
