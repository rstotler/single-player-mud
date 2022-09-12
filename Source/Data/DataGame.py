import Config, DataWorld, DataCombat, DataPlayer

class LoadGame:
	
	def __init__(self, DATA_SCREEN):
		
		self.solarSystemDict = None
		self.dataPlayer = None
		
		self.tickMillisecond = 60
		self.tickSecond = 60
		self.tickSynch = 0
		
		# Load New Game Data #
		self.loadNewGame(DATA_SCREEN)
		
	def loadNewGame(self, DATA_SCREEN):
		
		# Load Start Data #
		self.dataPlayer = DataPlayer.LoadPlayer()
		self.dataPlayer.loadNewPlayer(DATA_SCREEN.imageDict["Item"])
		self.solarSystemDict = DataWorld.loadNewGalaxy(self.dataPlayer, DATA_SCREEN.imageDict["Entity"], DATA_SCREEN.imageDict["Item"])
		
		# Advance Time Half A COTU (Earth) Day #
		planetCOTU = self.solarSystemDict["Sol"].planetDict["Center Of The Universe"]
		addMinutes = (planetCOTU.totalHoursInDay * 30) - 1
		self.tickSynch += addMinutes
		DataWorld.synchAllGameData(self.tickSynch, self.solarSystemDict, self.dataPlayer)
		planetCOTU.updateNightDayMinutes()
		
		# Initialize Room & Map Screens #
		playerArea = DataWorld.getParentArea(self.solarSystemDict[self.dataPlayer.currentSolarSystem], self.dataPlayer)
		DATA_SCREEN.sidescreenMap.initMap(playerArea)
		
		# Set Display Room Start Room #
		playerRoom = DataWorld.getParentArea(self.solarSystemDict[self.dataPlayer.currentSolarSystem], self.dataPlayer).roomDict[self.dataPlayer.currentRoom]
		
	def updateGame(self, WINDOW, MOUSE, DATA_SCREEN, UPDATE_TYPE):
		
		# Tick Game Clock #
		self.tickMillisecond += Config.GAME_TICK_SPEED
		if self.tickMillisecond >= 60:
			self.tickMillisecond = 0
			self.tickSynch += 1
			self.tickSecond += 1
			if self.tickSecond >= 60 : self.tickSecond = 0
		
		# Get Area & Room Update Data List #
		if self.tickMillisecond in [0, 30]:
			playerSolarSystem = self.solarSystemDict[self.dataPlayer.currentSolarSystem]
			playerArea = DataWorld.getParentArea(playerSolarSystem, self.dataPlayer)
			playerRoom = playerArea.roomDict[self.dataPlayer.currentRoom]
			updateAreaDataList, updateRoomDataList = DataWorld.getSurroundingRoomsDataList(self.solarSystemDict, playerArea, playerRoom, Config.PLAYER_UPDATE_RANGE)
			
		# Update - Every Minute - Player Solar System - All Planet Constant Positions #
		if self.tickMillisecond == 0 and self.tickSecond == 0:
			for constantPlanetId in playerSolarSystem.planetDict:
				constantPlanet = playerSolarSystem.planetDict[constantPlanetId]
				constantPlanet.tickConstantTime()
			
		# Update - Every Second - Local Planets/Areas/Rooms/Player #
		if self.tickMillisecond == 0:
			
			# Get Data #
			if True:
				currentPlanet = None
				currentArea = None
				updatedPlanetList = []
				updatedArealist = []
		
			# Update Local Planets/Areas/Rooms #
			for roomDataDict in updateRoomDataList:
				
				# Update Planet #
				if roomDataDict["Room Planet"] != None and (currentPlanet == None or currentPlanet.idPlanet != roomDataDict["Room Planet"]):
					currentPlanet = self.solarSystemDict[roomDataDict["Room Solar System"]].planetDict[roomDataDict["Room Planet"]]
					if currentPlanet.idPlanet not in updatedPlanetList:
						currentPlanet.update(self.solarSystemDict, self.dataPlayer, UPDATE_TYPE)
						updatedPlanetList.append(roomDataDict["Room Planet"])
				
				# Update Area #
				if currentArea == None or (currentArea.idArea != roomDataDict["Room Area"] or currentArea.idRandom != roomDataDict["Room Area Random"]):
					if roomDataDict["Room Area Random"] != None : currentArea = self.solarSystemDict[roomDataDict["Room Solar System"]].getTargetSpaceship(roomDataDict["Room Area"], roomDataDict["Room Area Random"])
					else : currentArea = self.solarSystemDict[roomDataDict["Room Solar System"]].planetDict[roomDataDict["Room Planet"]].areaDict[roomDataDict["Room Area"]]
					if {"Solar System":roomDataDict["Room Solar System"], "Planet":roomDataDict["Room Planet"], "Area":roomDataDict["Room Area"], "Area Random":roomDataDict["Room Area Random"]} not in updatedArealist:
						currentArea.update(self.solarSystemDict, self.dataPlayer, updateRoomDataList, UPDATE_TYPE)
						updatedArealist.append({"Solar System":roomDataDict["Room Solar System"], "Planet":roomDataDict["Room Planet"], "Area":roomDataDict["Room Area"], "Area Random":roomDataDict["Room Area Random"]})
				
				# Update Room #
				currentRoom = currentArea.roomDict[roomDataDict["Room ID"]]
				currentRoom.update(WINDOW, MOUSE, self.solarSystemDict, self.dataPlayer, currentArea, updateRoomDataList, DATA_SCREEN.sidescreenRoom, DATA_SCREEN.sidescreenPlayerUtility, DATA_SCREEN.imageDict["Interface"], DATA_SCREEN.imageDict["Item"], UPDATE_TYPE)
				
			# Update - Every Second - Player #
			self.dataPlayer.update(self.solarSystemDict, DATA_SCREEN.sidescreenPlayerUtility, DATA_SCREEN.imageDict["Item"])
			
		# Player & Mob Action - Updates Twice Per Second #
		if self.tickMillisecond in [0, 30]:
		
			# Update Player #
			delMobList = []
			if self.dataPlayer.currentHP > 0:
				delMobList = DataCombat.updateActionTimers(WINDOW, MOUSE, self.solarSystemDict, self.dataPlayer, self.dataPlayer, delMobList, DATA_SCREEN.sidescreenRoom, DATA_SCREEN.imageDict["Interface"])
				if len(delMobList) > 0:
					
					# Killed Mobs Check #
					targetMobRoom = None
					for delMob in delMobList:
						if targetMobRoom == None or targetMobRoom != DataWorld.getParentArea(self.solarSystemDict[delMob.currentSolarSystem], delMob).roomDict[delMob.currentRoom]:
							targetMobRoom = DataWorld.getParentArea(self.solarSystemDict[delMob.currentSolarSystem], delMob).roomDict[delMob.currentRoom]
						if delMob in targetMobRoom.mobList or delMob in targetMobRoom.updateMobList:
							targetMobRoom.killMob(self.solarSystemDict, self.dataPlayer, delMob, DATA_SCREEN.imageDict["Item"], True)
				
			# Mobs In Update Range Rooms #
			currentUpdateArea = None
			for targetRoomDataDict in updateRoomDataList:
			
				# Get Update Area #
				if currentUpdateArea == None or (targetRoomDataDict["Room Area"] != currentUpdateArea.idArea or targetRoomDataDict["Room Area Random"] != currentUpdateArea.idRandom):
					if targetRoomDataDict["Room Area Random"] != None : currentUpdateArea = self.solarSystemDict[targetRoomDataDict["Room Solar System"]].getTargetSpaceship(targetRoomDataDict["Room Area"], targetRoomDataDict["Room Area Random"])
					else : currentUpdateArea = self.solarSystemDict[targetRoomDataDict["Room Solar System"]].planetDict[targetRoomDataDict["Room Planet"]].areaDict[targetRoomDataDict["Room Area"]]
				
				# Update Room Mobs #
				if currentUpdateArea != None:
					delMobList = []
					currentUpdateRoom = currentUpdateArea.roomDict[targetRoomDataDict["Room ID"]]
					for currentMob in currentUpdateRoom.updateMobList:
						if currentMob.currentHP > 0:
							delMobList = DataCombat.updateActionTimers(WINDOW, MOUSE, self.solarSystemDict, self.dataPlayer, currentMob, delMobList, DATA_SCREEN.sidescreenRoom, DATA_SCREEN.imageDict["Interface"])
							
					# Killed Mobs Check #
					targetMobRoom = None
					if len(delMobList) > 0:
						for delMob in delMobList:
							if targetMobRoom == None or targetMobRoom != DataWorld.getParentArea(self.solarSystemDict[delMob.currentSolarSystem], delMob).roomDict[delMob.currentRoom]:
								targetMobRoom = DataWorld.getParentArea(self.solarSystemDict[delMob.currentSolarSystem], delMob).roomDict[delMob.currentRoom]
							if delMob in targetMobRoom.mobList or delMob in targetMobRoom.updateMobList:
								targetMobRoom.killMob(self.solarSystemDict, self.dataPlayer, delMob, DATA_SCREEN.imageDict["Item"])
								