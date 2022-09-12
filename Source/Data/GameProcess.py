import random, copy, Config, Utility, DataMain, DataWorld, DataItem, DataCombat
from Elements import Console

# User Input - Room Commands #
if True:
	def userLookDir(WINDOW, MOUSE, TICK_SYNCH, PARENT_AREA, SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_DIR, TARGET_DIR_NUM, SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT):
		
		playerViewDistance = DATA_PLAYER.getViewRange()
		startRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
		endRoom = None
		
		if TARGET_DIR_NUM > playerViewDistance : messageType = "Too Far"
		else : endArea, endRoom, messageType = DataWorld.getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, PARENT_AREA, startRoom, TARGET_DIR, TARGET_DIR_NUM)
		
		# Synch Unsynched Data #
		if endRoom != None and startRoom != endRoom:
			if endRoom.idSolarSystem != startRoom.idSolarSystem or endRoom.idPlanet != startRoom.idPlanet or endRoom.idArea != startRoom.idArea or endRoom.idAreaRandom != startRoom.idAreaRandom:
				
				# Get Data #
				endRoomPlanet = None
				if endRoom.idPlanet != None : endRoomPlanet = SOLAR_SYSTEM_DICT[endRoom.idSolarSystem].planetDict[endRoom.idPlanet]
				
				# Synch Checks #
				if endRoomPlanet != None and endRoomPlanet.tickSynch < TICK_SYNCH:
					endRoomPlanet.synchData(TICK_SYNCH)
				if endArea.tickSynch < TICK_SYNCH:
					endArea.synchData(TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER)
				if endRoom.tickSynch < TICK_SYNCH:
					endRoom.synchData(WINDOW, MOUSE, TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER, endArea, SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT)
		
		# Messages #
		if True:
			if endRoom != None and startRoom != endRoom:
				endRoom.displayRoom(PARENT_AREA, SOLAR_SYSTEM_DICT, DATA_PLAYER)
				if messageType == "No Exit":
					Console.addDisplayLineToDictList("You can't see any further.", "25w1y")
				elif messageType == "Door Is Closed":
					Console.addDisplayLineToDictList("You can't see past the door.", "27w1y")
			elif messageType == "Too Far":
				Console.addDisplayLineToDictList("You can't see that far.")
			elif messageType == "No Exit":
				Console.addDisplayLineToDictList("There is nothing there.", "22w1y")
			elif messageType == "Door Is Closed":
				Console.addDisplayLineToDictList("The door is closed.", "18w1y")

	def userExamine(PARENT_AREA, DATA_PLAYER, STR_TARGET_OBJECT, TARGET_INDEX, STR_TARGET_CONTAINER, CONTAINER_INDEX):

		targetObject = None
		targetLoc = None
		targetContainer = None
		containerLoc = None
		
		# Get Data #
		currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
		if STR_TARGET_CONTAINER == None : targetObject, targetObjectIndex, targetLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET_OBJECT, TARGET_INDEX, ["Room Items", "Player Inventory", "Room Mobs"])
		else : targetObject, targetContainer, containerLoc = getTargetInContainer(DATA_PLAYER, currentRoom, STR_TARGET_OBJECT, TARGET_INDEX, STR_TARGET_CONTAINER, CONTAINER_INDEX)
		
		# Examine Target #
		if STR_TARGET_CONTAINER == None and targetObject != None:
			targetObject.userExamine()
		
		# Examine Target In Container #
		elif targetObject != None and targetContainer != None:
			if containerLoc == "Room" : itemList = currentRoom.itemList
			elif containerLoc == "Player Inventory" : itemList = DATA_PLAYER.inventoryList
			
			containerIndex = 0
			targetCount = 0
			breakCheck = False
			for cNum, item in enumerate(itemList):
				if item.type == "Container" and item.idNum == targetContainer.idNum:
					if CONTAINER_INDEX == -1 or CONTAINER_INDEX == containerIndex:
						
						for iNum, itemInContainer in enumerate(item.flags["Container List"]):
							if itemInContainer.idNum == targetObject.idNum:
								if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
									itemInContainer.userExamine()
									breakCheck = True
									break
								targetCount += 1
						if breakCheck : break
					containerIndex += 1
					
			if breakCheck == False:
				Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")
		
		# Other - Instrument Panel #
		elif STR_TARGET_OBJECT in ["instrument", "control", "panel", "instrument panel", "control panel"]:
			
			# Spaceship Control Panel #
			if "Spaceship Control Panel" in currentRoom.flags:
				
				Console.addDisplayLineToDictList("There are several flashing lights and buttons on the Panel.", "58w1y")
				
				if "Manual Control" in currentRoom.flags["Spaceship Control Panel"]:
					Console.addDisplayLineToDictList("It is equipped with a Manual Control module.", "22w1dw6ddw1dw6ddw7w1y")
				if "Autopilot" in currentRoom.flags["Spaceship Control Panel"]:
					Console.addDisplayLineToDictList("There is a light labeled \"Autopilot\".", "25w1y9w2y")
				if "Scanner Module" in currentRoom.flags["Spaceship Control Panel"]:
					Console.addDisplayLineToDictList("It is capable of scanning the planet surface.", "44w1y")
				if "Radar" in currentRoom.flags["Spaceship Control Panel"]:
					Console.addDisplayLineToDictList("It is able to scan the local system for celestial bodies.", "56w1y")
			
			# Default Control Panel #
			elif "Control Panel" in currentRoom.flags:
				currentRoom.flags["Control Panel"].userExamine()
				
			else:
				Console.addDisplayLineToDictList("You don't see anything like that.", "7w1y24w1y")
		
		# Examine Spaceship #
		else:
			targetSpaceshipDescription = None
			for spaceshipDict in currentRoom.spaceshipDictList:
				if STR_TARGET_OBJECT in spaceshipDict["Key List"]:
					targetSpaceshipDescription = spaceshipDict["Description"]
			if targetSpaceshipDescription != None:
				Console.addDisplayLineToDictList(targetSpaceshipDescription)
			else:
				Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")

	def userMove(TICK_SYNCH, WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_DIR, SIDESCREEN_ROOM, SIDESCREEN_MAP, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT):

		# Get Data #
		if True:
			startArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
			startRoom = startArea.roomDict[DATA_PLAYER.currentRoom]
			playerArea = startArea
			playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]
			messageType = None
			moveCheck = False
			moveInsideCheck = False
			moveOutsideCheck = False
			leaveSpaceshipCheck = False
			groupMoveList = []
		
		# Checks #
		if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] in Config.COMBAT_ACTION_LIST : messageType = "Already Busy"
		elif ("Current Steps" in DATA_PLAYER.flags and (DATA_PLAYER.flags["Current Steps"] + 1) > 4) : messageType = "Can't Move That Fast"
		
		# Move Player #
		if messageType == None:
			if TARGET_DIR not in playerRoom.exitDict : messageType = "No Exit"
			else:
				targetMoveArea, targetMoveRoom, targetMoveMessage = DataWorld.getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, startArea, playerRoom, TARGET_DIR, 1)
				if targetMoveRoom.mapTileType == "Mountain" : messageType = "Can't Move There"
				else:
				
					# Update Current Steps #
					if "Current Steps" in DATA_PLAYER.flags : DATA_PLAYER.flags["Current Steps"] += 1
					else : DATA_PLAYER.flags["Current Steps"] = 1
				
					# Open/Unlock Doors #
					targetExit = playerRoom.exitDict[TARGET_DIR]
					openDoorCheck = False
					automaticDoorCheck = False
					if "Door Status" in targetExit and targetExit["Door Status"] in ["Closed", "Locked"]:
						if targetExit["Door Status"] == "Closed":
							if targetExit["Door Type"] == "Default":
								playerRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, "Open", TARGET_DIR)
								openDoorCheck = True
							elif targetExit["Door Type"] == "Automatic" : automaticDoorCheck = True
						elif targetExit["Door Status"] == "Locked":
							if not DATA_PLAYER.hasKey(targetExit["Key Num"]) : messageType = "Door Is Locked"
							else:
								if targetExit["Door Type"] == "Default":
									playerRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, "Open", TARGET_DIR)
									openDoorCheck = True
								elif targetExit["Door Type"] == "Automatic" : automaticDoorCheck = True
								
					# Move Player #
					if messageType == None:
						
						# Exit Spaceship #
						if "In Spaceship" in DATA_PLAYER.flags and targetExit == "Spaceship Exit":
							unlockShipCheck = False
							if playerArea.flags["Spaceship Status"] != "Landed" or ("Spaceship Door Status" in playerArea.flags and playerArea.flags["Spaceship Door Status"] == "Locked" and not DATA_PLAYER.hasKey(playerArea.flags["Spaceship Door Key Num"])):
								messageType = "Door Is Locked"
							else:
							
								# Get Target Room Data #
								spaceshipExitSolarSystem = playerArea.flags["Landed Data"]["Solar System"]
								spaceshipExitPlanet = playerArea.flags["Landed Data"]["Planet"]
								spaceshipExitArea = playerArea.flags["Landed Data"]["Area"]
								spaceshipExitRoom = playerArea.flags["Landed Data"]["Room"]
								
								# Update Player & Held Item Location #
								DATA_PLAYER.currentSolarSystem = spaceshipExitSolarSystem
								DATA_PLAYER.currentPlanet = spaceshipExitPlanet
								DATA_PLAYER.currentArea = spaceshipExitArea
								DATA_PLAYER.currentAreaRandom = None
								DATA_PLAYER.currentRoom = spaceshipExitRoom
								del DATA_PLAYER.flags["In Spaceship"]
									
								if "Spaceship Door Status" in playerArea.flags and playerArea.flags["Spaceship Door Status"] == "Locked":
									playerArea.flags["Spaceship Door Status"] = "Unlocked"
									unlockShipCheck = True
								leaveSpaceshipCheck = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].getTargetSpaceship(DATA_PLAYER.currentArea, DATA_PLAYER.currentAreaRandom)
								
								playerRoom = SOLAR_SYSTEM_DICT[spaceshipExitSolarSystem].planetDict[spaceshipExitPlanet].areaDict[spaceshipExitArea].roomDict[spaceshipExitRoom]
								playerArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
								moveCheck = True
								
						# Spaceship Movement #
						elif "In Spaceship" in DATA_PLAYER.flags and "Solar System" not in targetExit and "Planet" not in targetExit and "Area" not in targetExit and "Room" in targetExit and targetExit["Room"] in playerArea.roomDict:
							DATA_PLAYER.currentRoom = targetExit["Room"]
							playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]
							moveCheck = True
							
						# Area Movement #
						elif "Solar System" in targetExit and targetExit["Solar System"] in SOLAR_SYSTEM_DICT and "Planet" in targetExit and targetExit["Planet"] in SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict and "Area" in targetExit and targetExit["Area"] in SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict and "Room" in targetExit and targetExit["Room"] in SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict[targetExit["Area"]].roomDict:
							DATA_PLAYER.currentSolarSystem = targetExit["Solar System"]
							DATA_PLAYER.currentPlanet = targetExit["Planet"]
							DATA_PLAYER.currentArea = targetExit["Area"]
							DATA_PLAYER.currentRoom = targetExit["Room"]
							
							playerRoom = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[DATA_PLAYER.currentPlanet].areaDict[DATA_PLAYER.currentArea].roomDict[DATA_PLAYER.currentRoom]
							playerArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
							moveCheck = True
							
							# Inside/Outside Check #
							if startRoom.inside != playerRoom.inside:
								if playerRoom.inside : moveInsideCheck = True
								else : moveOutsideCheck = True
				
		# Movement Updates #
		if moveCheck:
		
			# Get Data #
			if True:
				newSurroundingAreaDataList, newSurroundingRoomDataList = DataWorld.getSurroundingRoomsDataList(SOLAR_SYSTEM_DICT, playerArea, playerRoom, Config.PLAYER_UPDATE_RANGE)
				currentPlanet = None
				currentArea = None
			
			# Synch Unsynched Solar Systems/Planets/Areas/Rooms In New Player Update Range #
			for roomDataDict in newSurroundingRoomDataList:
				
				# Synch Planet #
				if roomDataDict["Room Planet"] != None and (currentPlanet == None or currentPlanet.idPlanet != roomDataDict["Room Planet"]):
					currentPlanet = SOLAR_SYSTEM_DICT[roomDataDict["Room Solar System"]].planetDict[roomDataDict["Room Planet"]]
					if currentPlanet.tickSynch < TICK_SYNCH : currentPlanet.synchData(TICK_SYNCH)
					
				# Synch Area #
				if currentArea == None or (currentArea.idArea != roomDataDict["Room Area"] or currentArea.idRandom != roomDataDict["Room Area Random"]):
					if roomDataDict["Room Area Random"] != None : currentArea = SOLAR_SYSTEM_DICT[roomDataDict["Room Solar System"]].getTargetSpaceship(roomDataDict["Room Area"], roomDataDict["Room Area Random"])
					else : currentArea = SOLAR_SYSTEM_DICT[roomDataDict["Room Solar System"]].planetDict[roomDataDict["Room Planet"]].areaDict[roomDataDict["Room Area"]]
					if currentArea.tickSynch < TICK_SYNCH : currentArea.synchData(TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER)
					
				# Synch Room #
				currentRoom = currentArea.roomDict[roomDataDict["Room ID"]]
				if currentRoom.tickSynch < TICK_SYNCH : currentRoom.synchData(WINDOW, MOUSE, TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER, currentArea, SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT)
			
			# Clear CERTAIN Actions #
			if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] in ["Taming"]:
				DATA_PLAYER.currentAction = None
				Console.addDisplayLineToDictList("You break your concentration and move.")
				
			# Remove Far Away Player Targets #
			playerTargetDelMessageList = DATA_PLAYER.updateMobsInView(SOLAR_SYSTEM_DICT)
			
		# Messages #
		if True:
			if moveCheck:
				if openDoorCheck:
					if moveInsideCheck or moveOutsideCheck:
						if moveInsideCheck : insideOutsideStr = "inside"
						else : insideOutsideStr = "outside"
						Console.addDisplayLineToDictList("You open the door and step " + insideOutsideStr + ".", "27w"+str(len(insideOutsideStr))+"w1y")
					else : Console.addDisplayLineToDictList("You open the door.", "17w1y")
				elif automaticDoorCheck:
					Console.addDisplayLineToDictList("The door opens and closes behind you.", "36w1y")
				elif moveInsideCheck or moveOutsideCheck:
					if moveInsideCheck : Console.addDisplayLineToDictList("You step inside.")
					elif moveOutsideCheck : Console.addDisplayLineToDictList("You step outside.")
				elif leaveSpaceshipCheck:
					displayLinePart = "You step down from "
					if unlockShipCheck : displayLinePart = "You unlock the door and step off of "
					Console.addDisplayLineToDictList(displayLinePart + targetSpaceship.idArea + ".", str(len(displayLinePart)) + "w" + str(len(targetSpaceship.idArea)) + "w1y")
				
				# Lose Sight Of Target Display Lines #
				if len(playerTargetDelMessageList) > 0:
					for tempLine in playerTargetDelMessageList:
						Console.addDisplayLineToDictList(tempLine)
				
				playerRoom.displayRoom(playerArea, SOLAR_SYSTEM_DICT, DATA_PLAYER)
				
				if messageType == "No Exit":
					Console.addDisplayLineToDictList("You can't go any further.", "7w1y16w1y")
				elif messageType == "Door Is Locked":
					Console.addDisplayLineToDictList("The door is locked.", "18w1y")
				elif messageType == "In Combat":
					Console.addDisplayLineToDictList("You are in combat!", "17w1y")
			
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "No Exit":
				Console.addDisplayLineToDictList("You can't go that way.", "7w1y13w1y")
			elif messageType == "Door Is Locked":
				Console.addDisplayLineToDictList("The door is locked.", "18w1y")
			elif messageType == "In Combat":
				Console.addDisplayLineToDictList("You are in combat!", "17w1y")
			elif messageType == "Can't Move That Fast":
				Console.addDisplayLineToDictList("You can't move that fast.", "24w1y")
			elif messageType == "Can't Move There":
				Console.addDisplayLineToDictList("You can't move there.", "7w1y12w1y")
				
		# Post-Message Functions #
		if moveCheck:
			
			# Move Player Group With Player #
			if len(DATA_PLAYER.groupList) > 0:
				for groupMob in DATA_PLAYER.groupList:
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, groupMob, startRoom) and groupMob.currentAction == None and groupMob in startRoom.mobList:
						
						startRoom.removeMobFromRoom(groupMob)
						playerRoom.addMob(groupMob, DATA_PLAYER)
						
						groupMob.currentSolarSystem = playerRoom.idSolarSystem
						groupMob.currentPlanet = playerRoom.idPlanet
						groupMob.currentArea = playerRoom.idArea
						groupMob.currentAreaRandom = playerRoom.idAreaRandom
						groupMob.currentRoom = playerRoom.idNum
						
						groupMoveList.append(groupMob)
						
				if len(groupMoveList) == 1:
					Console.addDisplayLineToDictList(groupMoveList[0].defaultTitle + " follows you into the room.")
				elif len(groupMoveList) > 1:
					Console.addDisplayLineToDictList("Your group moves with you into the room.")
				
			# Move To Different Area Check #
			if startRoom != playerRoom and startRoom.idArea != playerRoom.idArea:
				SIDESCREEN_MAP.initMap(playerArea)
			
			# Update Room/Map/Target Stats Surfaces #
			if True:
				Config.DRAW_SCREEN_DICT["Map"] = True
				
				if "Room" in Config.DRAW_SCREEN_DICT and "All" not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append("All")
				elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = ["All"]
				
				if MOUSE.hoverScreen != None and MOUSE.hoverScreen.id == "Room":
					Config.DRAW_SCREEN_DICT["Target Stats"] = MOUSE.hoverElement
				
	def userOCLUDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_ACTION, TARGET_COUNT, TARGET_DIR):

		# Get Data #
		if True:
			currentRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
			playerTargetDelMessageList = []
			doorStatus = None
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# OCLU Door #
		if messageType == None:
			for exitDir in currentRoom.exitDict:
				if (TARGET_COUNT == "All" or TARGET_DIR == exitDir) and "Door Status" in currentRoom.exitDict[exitDir]:
					
					doorStatus = copy.deepcopy(currentRoom.exitDict[exitDir]["Door Status"])
					
					if TARGET_ACTION == "Open":
						if doorStatus == "Open" and messageType == None : messageType = "Already Opened"
						elif doorStatus == "Closed":
							currentRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, TARGET_ACTION, exitDir)
							messageType = "Open Door"
							if TARGET_COUNT == "All" : messageType = "Open All Doors"
						elif doorStatus == "Locked":
							keyCheck = DATA_PLAYER.hasKey(currentRoom.exitDict[exitDir]["Key Num"])
							if keyCheck == False and messageType == None : messageType = "Lack Key"	
							elif keyCheck:
								currentRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, TARGET_ACTION, exitDir)
								messageType = "Unlock And Open Door"
								if TARGET_COUNT == "All" : messageType = "Open All Doors"
					
					elif TARGET_ACTION == "Close":
						if doorStatus in ["Closed", "Locked"] and messageType == None : messageType = "Already Closed"
						elif doorStatus == "Open":
							currentRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, TARGET_ACTION, exitDir)
							messageType = "Close Door"
							if TARGET_COUNT == "All" : messageType = "Close All Doors"
					
					elif TARGET_ACTION == "Lock":
						if "Key Num" not in currentRoom.exitDict[exitDir] and messageType == None : messageType = "No Lock"
						elif doorStatus == "Locked" and messageType == None : messageType = "Already Locked"
						elif "Key Num" in currentRoom.exitDict[exitDir] and doorStatus in ["Open", "Closed"]:
							keyCheck = DATA_PLAYER.hasKey(currentRoom.exitDict[exitDir]["Key Num"])
							if keyCheck == False and messageType == None : messageType = "Lack Key"	
							elif keyCheck:
								currentRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, TARGET_ACTION, exitDir)
								messageType = "Lock Door"
								if TARGET_COUNT == "All" : messageType = "Lock All Doors"
								if doorStatus == "Open":
									messageType = "Close And Lock Door"
									if TARGET_COUNT == "All" : messageType = "Lock All Doors"
					
					elif TARGET_ACTION == "Unlock":
						if "Key Num" not in currentRoom.exitDict[exitDir] and messageType == None : messageType = "No Lock"
						elif "Key Num" in currentRoom.exitDict[exitDir] and doorStatus in ["Open", "Closed"] and messageType == None : messageType = "Already Unlocked"
						elif doorStatus == "Locked":
							keyCheck = DATA_PLAYER.hasKey(currentRoom.exitDict[exitDir]["Key Num"])
							if keyCheck == False and messageType == None : messageType = "Lack Key"	
							elif keyCheck:
								currentRoom.ocluDoor(SOLAR_SYSTEM_DICT, DATA_PLAYER.currentSolarSystem, TARGET_ACTION, exitDir)
								messageType = "Unlock Door"
								if TARGET_COUNT == "All" : messageType = "Unlock All Doors"
					
					if TARGET_COUNT != "All":
						break
			
			# Update Player Targets #
			playerTargetDelMessageList = DATA_PLAYER.updateMobsInView(SOLAR_SYSTEM_DICT)
			
		# Messages #
		if messageType == "Already Busy":
			Console.addDisplayLineToDictList("You are busy.")
		elif doorStatus != None and messageType != None:
			if messageType == "Open All Doors":
				Console.addDisplayLineToDictList("You open every door.", "19w1y")
			elif messageType == "Open Door":
				Console.addDisplayLineToDictList("You open the door.", "17w1y")
			elif messageType == "Unlock And Open Door":
				Console.addDisplayLineToDictList("You unlock and open the door.", "28w1y")
			elif messageType == "Already Opened":
				Console.addDisplayLineToDictList("It is already open.", "18w1y")
			elif messageType == "Close All Doors":
				Console.addDisplayLineToDictList("You close every door.", "20w1y")
			elif messageType == "Close Door":
				Console.addDisplayLineToDictList("You close the door.", "18w1y")
			elif messageType == "Already Closed":
				Console.addDisplayLineToDictList("It is already closed.", "20w1y")
			elif messageType == "Lock All Doors":
				Console.addDisplayLineToDictList("You lock every door.", "19w1y")
			elif messageType == "Lock Door":
				Console.addDisplayLineToDictList("You lock the door.", "17w1y")
			elif messageType == "Close And Lock Door":
				Console.addDisplayLineToDictList("You close and lock the door.", "27w1y")
			elif messageType == "Already Locked":
				Console.addDisplayLineToDictList("It is already locked.", "20w1y")
			elif messageType == "Unlock All Doors":
				Console.addDisplayLineToDictList("You unlock every door.", "21w1y")
			elif messageType == "Unlock Door":
				Console.addDisplayLineToDictList("You unlock the door.", "19w1y")
			elif messageType == "Already Unlocked":
				Console.addDisplayLineToDictList("It is already unlocked.", "22w1y")
			elif messageType == "No Lock":
				Console.addDisplayLineToDictList("It doesn't have a lock.", "8w1y13w1y")
			elif messageType == "Lack Key":
				Console.addDisplayLineToDictList("You lack the key.", "17w")
		else : Console.addDisplayLineToDictList("You don't see a door.", "7w1y12w1y")
		
		# Lose Sight Of Target Display Lines #
		if len(playerTargetDelMessageList) > 0:
			for tempLine in playerTargetDelMessageList:
				Console.addDisplayLineToDictList(tempLine)

	def userEnterSpaceship(WINDOW, MOUSE, TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER, STR_TARGET, SIDESCREEN_MAP, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT):

		messageType = None
		
		# Wear Checks #
		if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] in Config.COMBAT_ACTION_LIST : messageType = "Already Busy"
		elif "In Spaceship" in DATA_PLAYER.flags : messageType = "Already In Spaceship"
		
		# Enter Spaceship #
		if messageType == None:
			currentRoom = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[DATA_PLAYER.currentPlanet].areaDict[DATA_PLAYER.currentArea].roomDict[DATA_PLAYER.currentRoom]
			targetSpaceship = None
		
			for spaceshipDict in currentRoom.spaceshipDictList:
				if STR_TARGET == None or STR_TARGET in spaceshipDict["Key List"]:
					targetSpaceship = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].getTargetSpaceship(spaceshipDict["ID"], spaceshipDict["Random ID"])
					if targetSpaceship != None:
						
						# Find Main Door On Spaceship #
						mainDoorRoomNum = None
						for spaceshipRoomID in targetSpaceship.roomDict:
							spaceshipRoom = targetSpaceship.roomDict[spaceshipRoomID]
							if "Spaceship Main Door" in spaceshipRoom.flags:
								mainDoorRoomNum = spaceshipRoomID
								break
								
						if mainDoorRoomNum != None:
							if targetSpaceship.flags["Spaceship Door Status"] == "Locked" \
							and ("Spaceship Door Key Num" in targetSpaceship.flags and not DATA_PLAYER.hasKey(targetSpaceship.flags["Spaceship Door Key Num"])):
								messageType = "Door Is Locked"
							else:
								unlockShipCheck = False
								if targetSpaceship.flags["Spaceship Door Status"] == "Locked":
									targetSpaceship.flags["Spaceship Door Status"] = "Unlocked"
									unlockShipCheck = True
									
								# Update Player Data #
								oldAreaId = DATA_PLAYER.currentArea
								DATA_PLAYER.currentArea = targetSpaceship.idArea
								DATA_PLAYER.currentAreaRandom = targetSpaceship.idRandom
								DATA_PLAYER.currentRoom = mainDoorRoomNum
								DATA_PLAYER.flags["In Spaceship"] = True
								
								# Synch Data #
								if targetSpaceship.tickSynch < TICK_SYNCH : targetSpaceship.synchData(TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER)
								currentRoom = targetSpaceship.roomDict[DATA_PLAYER.currentRoom]
								#if currentRoom.tickSynch < TICK_SYNCH : currentRoom.synchData(WINDOW, MOUSE, TICK_SYNCH, SOLAR_SYSTEM_DICT, DATA_PLAYER, targetSpaceship, SIDESCREEN_ROOM, SIDESCREEN_PLAYER_UTILITY, INTERFACE_IMAGE_DICT, ITEM_IMAGE_DICT)
								
								# Display Room Message #
								displayLinePart = "You climb aboard "
								if unlockShipCheck : displayLinePart = "You unlock the door and climb aboard "
								Console.addDisplayLineToDictList(displayLinePart + targetSpaceship.idArea + ".", str(len(displayLinePart))+"w" + str(len(targetSpaceship.idArea)) + "w1y")
								currentRoom.displayRoom(targetSpaceship, SOLAR_SYSTEM_DICT, DATA_PLAYER)
								
								# Load Map Data #
								currentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
								SIDESCREEN_MAP.initMap(currentArea)
								
								# Update Display Data #
								pass
					break
		
		# Messages #
		if True:
			if messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.", "12w1y")
			elif messageType == "Already In Spaceship":
				Console.addDisplayLineToDictList("You are already in a spaceship.", "30w1y")
			elif messageType == "Door Is Locked":
				Console.addDisplayLineToDictList("The door is locked.", "18w1y")
			elif targetSpaceship == None:
				Console.addDisplayLineToDictList("You don't see it.", "7w1y8w1y")

	def userControlSpaceship(PARENT_AREA, SOLAR_SYSTEM_DICT, DATA_PLAYER, USER_INPUT_LIST):

		# Get Data #
		if True:
			playerRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetControlPanel = None
			launchModuleCheck = False
			landingModuleCheck = False
			scanPlanetModuleCheck = False
			radarModuleCheck = False
			manualControlModuleCheck = False
			autopilotModuleCheck = False
			throttleModuleCheck = False
			
			# Get Target Control Panel #
			for tempItem in playerRoom.itemList:
				if tempItem.type == "Control Panel":
					targetControlPanel = tempItem
					break
					
			# Module Checks #
			if "Spaceship Module List" in PARENT_AREA.flags:
				for spaceshipModule in PARENT_AREA.flags["Spaceship Module List"]:
					if spaceshipModule.idModule == "Launch Module" : launchModuleCheck = True
					elif spaceshipModule.idModule == "Landing Module" : landingModuleCheck = True
					elif spaceshipModule.idModule == "Scan Planet Module" : scanPlanetModuleCheck = True
					elif spaceshipModule.idModule == "Radar Module" : radarModuleCheck = True
					elif spaceshipModule.idModule == "Manual Control Module" : manualControlModuleCheck = True
					elif spaceshipModule.idModule == "Autopilot Module" : autopilotModuleCheck = True
					elif spaceshipModule.idModule == "Throttle Module" : throttleModuleCheck = True
		
		# Checks #
		if DATA_PLAYER.currentAction != None:
			Console.addDisplayLineToDictList("You are busy.")
		elif "In Spaceship" not in DATA_PLAYER.flags or "In Spaceship" not in playerRoom.flags:
			Console.addDisplayLineToDictList("You must be in a spaceship to do that.")
		elif targetControlPanel == None or "Spaceship Control Panel" not in targetControlPanel.flags:
			Console.addDisplayLineToDictList("You must be at a Spaceship Control Panel to do that.")
			
		# Spaceship Commands #
		else:

			# Launch Spaceship #
			if len(USER_INPUT_LIST) == 1 and USER_INPUT_LIST[0] in ["launch", "launc", "laun", "lau"]:
				
				if launchModuleCheck == False:
					Console.addDisplayLineToDictList("There is no module to do so.")
				elif PARENT_AREA.flags["Spaceship Status"] != "Landed":
					Console.addDisplayLineToDictList("You must be landed to do that.")
				else:
					PARENT_AREA.flags["Spaceship Status"] = "Launching"
					PARENT_AREA.flags["Spaceship Launch Timer"] = 1
					PARENT_AREA.flags["Spaceship Launch Stage"] = 0
					Console.addDisplayLineToDictList("You push a button on the Panel.")
				
			# Land Spaceship #
			elif USER_INPUT_LIST[0] in ["land", "lan"]:
				
				if landingModuleCheck == False:
					Console.addDisplayLineToDictList("There is no module to do so.")
				elif PARENT_AREA.flags["Spaceship Status"] != "Orbit":
					Console.addDisplayLineToDictList("You must be in orbit to do that.")
				elif len(USER_INPUT_LIST) > 1 and not Utility.stringIsNumber(USER_INPUT_LIST[1]):
					Console.addDisplayLineToDictList("You must choose a landing site.")
				else:
				
					# Check If Target Landing Site Index Is In List #
					targetLandingSiteIndex = 0
					if len(USER_INPUT_LIST) > 1 : targetLandingSiteIndex = int(USER_INPUT_LIST[1]) - 1
					landingSiteDictList = []
					for tempAreaName in SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[PARENT_AREA.flags["Spaceship Orbit Target"]].areaDict:
						tempArea = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[PARENT_AREA.flags["Spaceship Orbit Target"]].areaDict[tempAreaName]
						if "Launch Pad Room List" in tempArea.flags:
							for idRoom in tempArea.flags["Launch Pad Room List"]:
								landingSiteDict = {"Area ID":tempArea.idArea, "Room ID":idRoom}
								landingSiteDictList.append(landingSiteDict)
								
					if targetLandingSiteIndex < 0 or targetLandingSiteIndex >= len(landingSiteDictList):
						Console.addDisplayLineToDictList("That is not a valid selection.")
					else:
						PARENT_AREA.flags["Spaceship Status"] = "Landing"
						PARENT_AREA.flags["Spaceship Landing Target Planet"] = PARENT_AREA.flags["Spaceship Orbit Target"]
						PARENT_AREA.flags["Spaceship Landing Target Area"] = landingSiteDictList[targetLandingSiteIndex]["Area ID"]
						PARENT_AREA.flags["Spaceship Landing Target Room"] = landingSiteDictList[targetLandingSiteIndex]["Room ID"]
						PARENT_AREA.flags["Spaceship Landing Timer"] = 3
						PARENT_AREA.flags["Spaceship Landing Stage"] = 0
						del PARENT_AREA.flags["Spaceship Orbit Target"]
						Console.addDisplayLineToDictList("A computerized voice says, \"Initiating landing sequence.\"")
			
			# Scan Planet #
			elif len(USER_INPUT_LIST) == 1 and USER_INPUT_LIST[0] in ["scan", "sca"]:
			
				if scanPlanetModuleCheck == False:
					Console.addDisplayLineToDictList("There is no module to do so.")
				elif PARENT_AREA.flags["Spaceship Status"] != "Orbit":
					Console.addDisplayLineToDictList("You must be in orbit to do that.")
				else:
					Console.addDisplayLineToDictList("The ship computer scans the planet surface.")
					
					# Get Landing Site List #
					masterLandingList = []
					for tempAreaName in SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[PARENT_AREA.flags["Spaceship Orbit Target"]].areaDict:
						tempArea = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[PARENT_AREA.flags["Spaceship Orbit Target"]].areaDict[tempAreaName]
						if "Launch Pad Room List" in tempArea.flags:
							for idRoom in tempArea.flags["Launch Pad Room List"]:
								tempRoom = tempArea.roomDict[idRoom]
								displayLine = tempAreaName + " - " + tempRoom.title
								masterLandingList.append(displayLine)
					for lNum, displayLine in enumerate(masterLandingList):
						Console.addDisplayLineToDictList(str(lNum+1) + " - " + displayLine)
							
			# Radar #
			elif len(USER_INPUT_LIST) == 1 and USER_INPUT_LIST[0] in ["radar", "rada", "rad"]:
				
				if radarModuleCheck == False:
					Console.addDisplayLineToDictList("There is no module to do so.")
				elif PARENT_AREA.flags["Spaceship Status"] not in ["Orbit", "Flight"]:
					Console.addDisplayLineToDictList("You must be in space to do that.")
				else:
					targetSolarSystem = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem]
				
					Console.addDisplayLineToDictList("You check the ship radar.")
					Console.addDisplayLineToDictList(str(len(targetSolarSystem.planetDict)-1) + " planets have been detected in this system.")
					
					# Get Planet List #
					for pNum, tempPlanetDict in enumerate(targetSolarSystem.getPlanetDataList()):
						Console.addDisplayLineToDictList(str(pNum + 1) + " - " + tempPlanetDict["ID"])
						
			# Set Course #
			elif USER_INPUT_LIST[0] in ["course", "cours", "cour", "cou"]:
				
				if PARENT_AREA.flags["Spaceship Status"] not in ["Orbit", "Flight"]:
					Console.addDisplayLineToDictList("You must be in space to do that.")
				else:					
					setCourseType = "Autopilot"
					if len(USER_INPUT_LIST) == 4 and Utility.stringIsNumber(USER_INPUT_LIST[1]) and Utility.stringIsNumber(USER_INPUT_LIST[2]) and Utility.stringIsNumber(USER_INPUT_LIST[3]):
						if manualControlModuleCheck == False : Console.addDisplayLineToDictList("There is no module to do so.")
						else : setCourseType = "Manual Control"
					elif radarModuleCheck == False or autopilotModuleCheck == False:
						Console.addDisplayLineToDictList("There is no module to do so.")
					else:
						
						# Set Autopilot #
						if setCourseType == "Autopilot":
							targetPlanetString = ' '.join(USER_INPUT_LIST[1::])
							targetSolarSystem = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem]
							targetPlanet = None
							for tempPlanetDict in targetSolarSystem.getPlanetDataList():
								if targetPlanetString in tempPlanetDict["Key List"]:
									targetPlanet = targetSolarSystem.planetDict[tempPlanetDict["ID"]]
									break
							if targetPlanet == None:
								Console.addDisplayLineToDictList("The ship's radar detects no such planet.")
							else:
								PARENT_AREA.flags["Spaceship Flight Timer"] = Config.SPACESHIP_TIMER["Update"]
								PARENT_AREA.flags["Spaceship Status"] = "Flight"
								PARENT_AREA.flags["Spaceship Flight Type"] = "Autopilot"
								PARENT_AREA.flags["Spaceship Speed"] = 1.0
								PARENT_AREA.flags["Spaceship Flight Target"] = targetPlanet
								
								if "Spaceship Orbit Target" in PARENT_AREA.flags:
									orbitingPlanet = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[PARENT_AREA.flags["Spaceship Orbit Target"]]
									del PARENT_AREA.flags["Spaceship Orbit Target"]
									PARENT_AREA.flags["Spaceship X Loc"] = orbitingPlanet.x
									PARENT_AREA.flags["Spaceship Y Loc"] = orbitingPlanet.y
									
								Console.addDisplayLineToDictList("The ship lurches forward as it changes course.")
							
						# Set Manual Control #
						elif setCourseType == "Manual":
							pass
			
			# Adjust Throttle #
			elif USER_INPUT_LIST[0] in ["throttle", "throttl", "thrott", "throt", "thro", "thr"]:
			
				if throttleModuleCheck == False or (manualControlModuleCheck == False and autopilotModuleCheck == False):
					Console.addDisplayLineToDictList("There is no module to do so.")
				elif PARENT_AREA.flags["Spaceship Status"] != "Flight":
					Console.addDisplayLineToDictList("You must be in flight to do that.")
				elif len(USER_INPUT_LIST) == 1 or not Utility.stringIsNumber(USER_INPUT_LIST[1]) or int(USER_INPUT_LIST[1]) not in range(101):
					Console.addDisplayLineToDictList("A computerized voice says, \"Please enter an input from 0-100.\"")
				else:
					targetThrottle = int(USER_INPUT_LIST[1])
					oldSpeed = PARENT_AREA.flags["Spaceship Speed"]
					PARENT_AREA.flags["Spaceship Speed"] = targetThrottle * .01
					
					if PARENT_AREA.flags["Spaceship Speed"] > oldSpeed:
						Console.addDisplayLineToDictList("The ship accelerates under your command.")
					elif PARENT_AREA.flags["Spaceship Speed"] < oldSpeed:
						Console.addDisplayLineToDictList("The ship begins to slow down.")
					else : Console.addDisplayLineToDictList("Speed is already at " + oldSpeed + "%.")

# User Input - Item Commands #
if True:
	def userPutIn(PARENT_AREA, DATA_PLAYER, TARGET_NUM, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, ITEM_IMAGE_DICT):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET_ITEM, TARGET_ITEM_INDEX, ["Player Inventory"])
			targetContainer, containerIndex, containerLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, ["Room Items", "Player Inventory"])
			itemList = currentRoom.itemList
			if containerLoc == "Player Inventory" : itemList = DATA_PLAYER.inventoryList
			containerCount = 0
			objectCount = 0
			putCount = 0
			delList = []
			playerItem = None
			openContainerCheck = False
			messageType = None
			
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
			
		# Put Item In Container #
		if messageType == None:
			if targetContainer != None and targetContainer.type == "Container" and (STR_TARGET_ITEM == "All" or targetItem != None):
				if targetItem != None and targetItem.type == "Container" : messageType = "Can't Put Container In Container"
				elif "Container Status" in targetContainer.flags and targetContainer.flags["Container Status"] == "Locked" and "Key Num" in targetContainer.flags and not DATA_PLAYER.hasKey(targetContainer.flags["Key Num"]) : messageType = "Container Is Locked"
				else:
					for cNum, containerItem in enumerate(itemList):
						if containerItem.idNum == targetContainer.idNum:
							if TARGET_CONTAINER_INDEX == containerCount:
								for iNum, playerItem in enumerate(DATA_PLAYER.inventoryList):
									if STR_TARGET_ITEM == "All" or playerItem.idNum == targetItem.idNum:
										if (containerLoc == "Room Items" or iNum != containerIndex):
											if TARGET_ITEM_INDEX == -1 or TARGET_ITEM_INDEX == objectCount:
											
												# Create New Quantity Item #
												if "Quantity" in playerItem.flags:
													targetPutCount = TARGET_NUM
													if targetPutCount == "All" or targetPutCount > playerItem.flags["Quantity"] : targetPutCount = playerItem.flags["Quantity"]
													newQuantityItem = DataItem.loadPrefab(playerItem.idNum, ITEM_IMAGE_DICT, {"Quantity":targetPutCount})
													if targetPutCount > 1 and targetContainer.flags["Container Current Weight"] + newQuantityItem.getWeight() > targetContainer.flags["Container Max Weight"]:
														newPutCount = (targetContainer.flags["Container Max Weight"] - targetContainer.flags["Container Current Weight"]) / newQuantityItem.weight
														if newPutCount > targetPutCount : newPutCount = targetPutCount
														if newPutCount > 0:
															targetPutCount = newPutCount
															newQuantityItem.flags["Quantity"] = targetPutCount
													playerItem = newQuantityItem
											
												# Pre Put In Checks #
												if playerItem.getWeight() + targetContainer.flags["Container Current Weight"] > targetContainer.flags["Container Max Weight"] : messageType = "Bag Overweight"
												else:
													
													# Add Item To Container #
													if containerLoc == "Room Items" : currentRoom.addItemToContainer(targetContainer, playerItem)
													elif containerLoc == "Player Inventory" : DATA_PLAYER.addItemToContainer(targetContainer, playerItem)
													
													# Update Delete List #
													if "Quantity" in playerItem.flags:
														putCount += playerItem.flags["Quantity"]
														delList.append([iNum, playerItem.flags["Quantity"]])
													else:
														putCount += 1
														delList.append([iNum, 1])
													
												if TARGET_NUM != "All" and putCount >= TARGET_NUM:
													break
											
										objectCount += 1
							containerCount += 1
			
			# Open Closed/Locked Container #
			if putCount > 0 and "Container Status" in targetContainer.flags and targetContainer.flags["Container Status"] in ["Closed", "Locked"]:
				targetContainer.flags["Container Status"] = "Open"
				openContainerCheck = True
				Console.addDisplayLineToDictList("You open " + targetContainer.defaultTitle + ".")
			
		# Messages #
		if True:
			if len(delList) > 0:
				if STR_TARGET_ITEM == "All" : targetItemTitle = "everything you can"
				else: targetItemTitle = targetItem.defaultTitle
				if STR_TARGET_ITEM != "All" and len(delList) > 1 : addCountMod = len(delList)
				else : addCountMod = 1
				strQuantity = ""
				strQuantityCode = ""
				if STR_TARGET_ITEM != "All" and playerItem != None and "Quantity" in playerItem.flags and playerItem.flags["Quantity"] > 1:
					strQuantity = " (" + str(targetPutCount) + ")"
					strQuantityCode = "2r" + str(len(str(targetPutCount))) + "w1r"
				Console.addDisplayLineToDictList("You put "+targetItemTitle+" in "+targetContainer.defaultTitle+"."+strQuantity, "8w"+str(len(targetItemTitle))+"w4w"+targetContainer.defaultTitleColorCode+"1y"+strQuantityCode, {"Count Mod":addCountMod})
			
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Container Is Locked":
				Console.addDisplayLineToDictList("It is locked.", "13w")
			elif targetContainer != None and targetContainer.type != "Container":
				Console.addDisplayLineToDictList("It is not a container.", "23w")
			elif messageType == "Can't Put Container In Container":
				Console.addDisplayLineToDictList("You can't put a container in another container.")
			elif messageType == "Bag Overweight":
				Console.addDisplayLineToDictList("It won't fit.", "14w")
			else:
				Console.addDisplayLineToDictList("You can't find it.", "18w")
		
		# Delete Items From Player Inventory #
		if len(delList) > 0:
			delList.reverse()
			for delData in delList:
				delItem = DATA_PLAYER.inventoryList[delData[0]]
				
				if "Quantity" in delItem.flags:
					if delData[1] > DATA_PLAYER.inventoryList[delData[0]].flags["Quantity"] : delData[1] = DATA_PLAYER.inventoryList[delData[0]].flags["Quantity"]
					DATA_PLAYER.inventoryList[delData[0]].flags["Quantity"] -= delData[1]
					if containerLoc == "Room Items" : DATA_PLAYER.currentWeight -= (delItem.weight * delData[1])
					
					if DATA_PLAYER.inventoryList[delData[0]].flags["Quantity"] <= 0:
						if containerLoc == "Player Inventory" : DATA_PLAYER.removeItemFromInventory(delItem, False, False)
						else : DATA_PLAYER.removeItemFromInventory(delItem, False)
								
				else:
					if containerLoc == "Player Inventory" : DATA_PLAYER.removeItemFromInventory(delItem, False, False)
					else : DATA_PLAYER.removeItemFromInventory(delItem)
								
	def userGetFrom(PARENT_AREA, DATA_PLAYER, TARGET_NUM, STR_TARGET_ITEM, TARGET_ITEM_INDEX, CONTAINER_NUM, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, ITEM_IMAGE_DICT):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetContainer, containerLoc = getTargetInContainer(DATA_PLAYER, currentRoom, STR_TARGET_ITEM, TARGET_ITEM_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, ["Container", "Plant"])
			itemList = currentRoom.itemList
			if containerLoc == "Player Inventory" : itemList = DATA_PLAYER.inventoryList
			containerIndex = 0
			targetContainerCount = 0
			getCount = 0
			delList = []
			itemInContainer = None
			openContainerCheck = False
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Get Item(s) From Container #
		if messageType == None:
			if targetContainer != None or STR_TARGET_CONTAINER == "All":
				for cNum, item in enumerate(itemList):
					if (STR_TARGET_CONTAINER == "All" and item.type in ["Container", "Plant"]) or (targetContainer != None and item.type == targetContainer.type and item.idNum == targetContainer.idNum):
						if "Container Status" in item.flags and item.flags["Container Status"] == "Locked" and "Key Num" in targetContainer.flags and not DATA_PLAYER.hasKey(targetContainer.flags["Key Num"]) : messageType = "Container Is Locked"
						elif item.type == "Plant" and ("Fruit List" not in item.flags or len(item.flags["Fruit List"]) == 0) : messageType = "No Fruit To Get"
						elif TARGET_CONTAINER_INDEX == -1 or TARGET_CONTAINER_INDEX == containerIndex:
							targetCount = 0
							getCheck = False
							breakCheck = False
							if item.type == "Container" : containerItemList = item.flags["Container List"]
							elif item.type == "Plant" : containerItemList = item.flags["Fruit List"]
							for iNum, itemInContainer in enumerate(containerItemList):
								if STR_TARGET_ITEM == "All" or (targetItem != None and itemInContainer.idNum == targetItem.idNum):
								
									# Create New Quantity Item #
									if "Quantity" in itemInContainer.flags:
										targetGetCount = TARGET_NUM
										if targetGetCount == "All" or targetGetCount > itemInContainer.flags["Quantity"] : targetGetCount = itemInContainer.flags["Quantity"]
										newQuantityItem = DataItem.loadPrefab(itemInContainer.idNum, ITEM_IMAGE_DICT, {"Quantity":targetGetCount})
										if containerLoc == "Room" and targetGetCount > 1 and (DATA_PLAYER.currentWeight + newQuantityItem.getWeight() > DATA_PLAYER.maxWeight):
											newGetCount = (DATA_PLAYER.maxWeight - DATA_PLAYER.currentWeight) / newQuantityItem.weight
											if newGetCount > targetGetCount : newGetCount = targetGetCount
											if newGetCount > 0:
												targetGetCount = newGetCount
												newQuantityItem.flags["Quantity"] = targetGetCount
										itemInContainer = newQuantityItem
								
									# Pre Get From Checks #
									if containerLoc == "Room" and DATA_PLAYER.currentWeight + itemInContainer.getWeight() > DATA_PLAYER.maxWeight : messageType = "Overweight"
									elif TARGET_ITEM_INDEX == -1 or TARGET_ITEM_INDEX == targetCount:
									
										# Add Item To Player Inventory #
										if containerLoc == "Room" : DATA_PLAYER.addItemToInventory(itemInContainer)
										else : DATA_PLAYER.addItemToInventory(itemInContainer, False)
										
										# Update Delete List #
										if "Quantity" in itemInContainer.flags:
											delList.append([cNum, iNum, itemInContainer.flags["Quantity"]])
											getCount += itemInContainer.flags["Quantity"]
											getCheck = True
										else:
											delList.append([cNum, iNum, 1])
											getCount += 1
											getCheck = True
										
									targetCount += 1
									if TARGET_NUM != "All" and getCount >= TARGET_NUM:
										breakCheck = True
										break
							if getCheck : targetContainerCount += 1
							if breakCheck or (TARGET_CONTAINER_INDEX != -1 and containerIndex >= TARGET_CONTAINER_INDEX) or (CONTAINER_NUM != "All" and targetContainerCount >= CONTAINER_NUM):
								break
						containerIndex += 1
			
			# Open Container Check #
			if targetContainer != None and getCount > 0 and "Container Status" in targetContainer.flags and targetContainer.flags["Container Status"] in ["Closed", "Locked"]:
				targetContainer.flags["Container Status"] = "Open"
				openContainerCheck = True
				Console.addDisplayLineToDictList("You open " + targetContainer.defaultTitle + ".")
			
		# Messages #
		if True:
			if len(delList) > 0:
				
				addCountMod = 1
				strQuantity = ""
				strQuantityCode = ""
				
				# Item Title Mods #
				if True:
					if itemInContainer != None and "Quantity" in itemInContainer.flags and itemInContainer.flags["Quantity"] > 1:
						strQuantity = " (" + str(itemInContainer.flags["Quantity"]) + ")"
						strQuantityCode = "2r" + str(len(str(itemInContainer.flags["Quantity"]))) + "w1r"
					if targetItem != None:
						itemTitle = targetItem.defaultTitle
						if len(delList) > 1 : addCountMod = len(delList)
					if targetContainer != None:
						containerTitle = targetContainer.defaultTitle
						if targetContainerCount > 1:
							containerTitleMod = " (" + str(targetContainerCount) + ") "
							containerColorCodeMod = "2r" + str(len(str(targetContainerCount))) + "w2r" 
					
				if len(delList) > 1 and STR_TARGET_ITEM == "All" and STR_TARGET_CONTAINER == "All":
					Console.addDisplayLineToDictList("You get everything you can.", "26w1y")
				elif STR_TARGET_ITEM != "All" and STR_TARGET_CONTAINER == "All":
					Console.addDisplayLineToDictList("You search all containers and retrieve "+itemTitle+"."+strQuantity, "39w"+targetItem.defaultTitleColorCode+"1y"+strQuantityCode, {"Count Mod":addCountMod})
					
				elif targetContainer.type == "Container":
					if STR_TARGET_ITEM == "All" and STR_TARGET_CONTAINER != "All":
						Console.addDisplayLineToDictList("You get everything you can from "+containerTitle+".", "32w"+targetContainer.defaultTitleColorCode+"1y")
					elif targetContainerCount > 1:
						Console.addDisplayLineToDictList("You get "+itemTitle+" from "+containerTitleMod+containerTitle+"."+strQuantity, "8w"+targetItem.defaultTitleColorCode+"6w"+targetContainer.defaultTitleColorCode+containerColorCodeMod+"1y"+strQuantityCode, {"Count Mod":addCountMod})
					else : Console.addDisplayLineToDictList("You get "+itemTitle+" from "+containerTitle+"."+strQuantity, "8w"+targetItem.defaultTitleColorCode+"6w"+targetContainer.defaultTitleColorCode+"1y"+strQuantityCode, {"Count Mod":addCountMod})
				
				elif targetContainer.type == "Plant":
					if STR_TARGET_ITEM == "All" and STR_TARGET_CONTAINER != "All":
						Console.addDisplayLineToDictList("You pick everything you can from "+containerTitle+".", "33w"+targetContainer.defaultTitleColorCode+"1y")
					elif targetContainerCount > 1:
						Console.addDisplayLineToDictList("You pick "+itemTitle+" from "+containerTitleMod+containerTitle+".", "9w"+targetItem.defaultTitleColorCode+"6w"+targetContainer.defaultTitleColorCode+containerColorCodeMod+"1y", {"Count Mod":addCountMod})
					else : Console.addDisplayLineToDictList("You pick "+itemTitle+" from "+containerTitle+".", "9w"+targetItem.defaultTitleColorCode+"6w"+targetContainer.defaultTitleColorCode+"1y", {"Count Mod":addCountMod})
				
			else:
				if messageType == "Already Busy":
					Console.addDisplayLineToDictList("You are busy.")
				elif messageType == "Container Is Locked":
					Console.addDisplayLineToDictList("It is locked.", "13w")
				elif messageType == "Overweight":
					Console.addDisplayLineToDictList("You can't hold that much.", "25w")
				elif messageType == "No Fruit To Get":
					Console.addDisplayLineToDictList("There is no fruit to get.")
				elif targetContainer != None and STR_TARGET_ITEM == "All":
					Console.addDisplayLineToDictList("There is nothing left to get.", "29w")
				else : Console.addDisplayLineToDictList("You can't find it.", "18w")
			
		# Delete From Container #
		if len(delList) > 0:
			delList.reverse()
			for delData in delList:
			
				if containerLoc == "Room":
					
					# Get Delete Item #
					tempContainer = currentRoom.itemList[delData[0]]
					tempItemInContainer = None
					if tempContainer.type == "Container" : tempItemInContainer = tempContainer.flags["Container List"][delData[1]]
					elif tempContainer.type == "Plant" : tempItemInContainer = tempContainer.flags["Fruit List"][delData[1]]
					
					# Delete Target Item #
					if tempItemInContainer != None:
					
						if "Quantity" in tempItemInContainer.flags:
							if delData[2] > tempItemInContainer.flags["Quantity"] : delData[2] = tempItemInContainer.flags["Quantity"]
							tempItemInContainer.flags["Quantity"] -= delData[2]
							if tempItemInContainer.flags["Quantity"] <= 0:
								if tempContainer.type == "Container" : del currentRoom.itemList[delData[0]].flags["Container List"][delData[1]]
								elif tempContainer.type == "Plant" : del currentRoom.itemList[delData[0]].flags["Fruit List"][delData[1]]
								if tempItemInContainer in currentRoom.updateItemList:
									del currentRoom.updateItemList[currentRoom.updateItemList.index(tempItemInContainer)]
						
						else:
							if tempContainer.type == "Container" : del currentRoom.itemList[delData[0]].flags["Container List"][delData[1]]
							elif tempContainer.type == "Plant" : del currentRoom.itemList[delData[0]].flags["Fruit List"][delData[1]]
							if tempItemInContainer in currentRoom.updateItemList:
								del currentRoom.updateItemList[currentRoom.updateItemList.index(tempItemInContainer)]
								
						if tempContainer.type == "Container":
							if "Quantity" in tempItemInContainer.flags:
								tempContainer.flags["Container Current Weight"] -= (tempItemInContainer.weight * delData[2])
							else:
								tempContainer.flags["Container Current Weight"] -= tempItemInContainer.getWeight()
					
				elif containerLoc == "Player Inventory":
					
					tempContainer = DATA_PLAYER.inventoryList[delData[0]]
					delItem = tempContainer.flags["Container List"][delData[1]]
				
					if "Quantity" in delItem.flags:
						if delData[2] > delItem.flags["Quantity"] : delData[2] = delItem.flags["Quantity"]
						delItem.flags["Quantity"] -= delData[2]
						tempContainer.flags["Container Current Weight"] -= (delItem.weight * delData[2])
						if delItem.flags["Quantity"] <= 0:
							del DATA_PLAYER.inventoryList[delData[0]].flags["Container List"][delData[1]]
					
					else:
						tempContainer.flags["Container Current Weight"] -= delItem.getWeight()
						del DATA_PLAYER.inventoryList[delData[0]].flags["Container List"][delData[1]]
					
	def userGet(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Room Items"])
			targetCount = 0
			getCount = 0
			fruitGetCount = 0
			delList = []
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Get Item(s) #
		if messageType == None and (targetItem != None or STR_TARGET == "All"):		
			for iNum, item in enumerate(currentRoom.itemList):
				if STR_TARGET == "All" or item.idNum == targetItem.idNum:
					
					# Create New Quantity Item #
					oldItem = item
					targetGetCount = TARGET_COUNT
					if "Quantity" in item.flags:
						if targetGetCount == "All" or (targetGetCount == 1 and TARGET_INDEX == 0) or targetGetCount > item.flags["Quantity"] : targetGetCount = item.flags["Quantity"]
						newQuantityItem = DataItem.loadPrefab(item.idNum, ITEM_IMAGE_DICT, {"Quantity":targetGetCount})
						if targetGetCount > 1 and DATA_PLAYER.currentWeight + newQuantityItem.getWeight() > DATA_PLAYER.maxWeight:
							newGetCount = (DATA_PLAYER.maxWeight - DATA_PLAYER.currentWeight) / newQuantityItem.weight
							if newGetCount > targetGetCount : newGetCount = targetGetCount
							if newGetCount > 0:
								targetGetCount = newGetCount
								newQuantityItem.flags["Quantity"] = targetGetCount
						item = newQuantityItem
						item.dropSide = oldItem.dropSide
						
					# Pre Get Checks #
					if "No Get" in oldItem.flags : messageType = "No Get"
					elif DATA_PLAYER.currentWeight + item.getWeight() > DATA_PLAYER.maxWeight : messageType = "Overweight"
					elif TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
						
						addItemToEntityInventory(DATA_PLAYER, item, currentRoom, targetGetCount, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT)
						
						# Get Fruit Count #
						if "Fruit List" in item.flags and len(item.flags["Fruit List"]) > 0:
							fruitGetCount += len(item.flags["Fruit List"])
							
						# Update Delete List #
						if "Quantity" in item.flags:
							getCount += item.flags["Quantity"]
							delList.append([iNum, item.flags["Quantity"]])
						else:
							getCount += 1
							delList.append([iNum, 1])
						
						# Update Screen Data #
						if True:
							if item.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
							elif item.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
							
					targetCount += 1
					if TARGET_COUNT != "All" and getCount >= TARGET_COUNT:
						break

		# Messages #
		if True:
			if len(delList) > 0:
			
				# Item Title Mods #
				if targetItem != None:
					itemTitle = targetItem.defaultTitle
					if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
						itemTitle = itemTitle[0].lower() + itemTitle[1::]
				
				# Pick Up Fruits #
				if STR_TARGET != "All" and fruitGetCount > 0:
					displayLine = "You get " + tempFruit.defaultTitle + " from " + targetItem.defaultTitle + "."
					colorCode = "8w" + tempFruit.defaultTitleColorCode + "6w" + targetItem.defaultTitleColorCode + "1y"
					Console.addDisplayLineToDictList(displayLine, colorCode, {"Count Mod":fruitGetCount})
				
				if TARGET_COUNT == 1:
					strQuantity = ""
					strQuantityCode = ""
					if "Quantity" in item.flags and item.flags["Quantity"] > 1:
						strQuantity = " (" + str(item.flags["Quantity"]) + ")"
						strQuantityCode = "2r" + str(len(str(item.flags["Quantity"]))) + "w1r"
					Console.addDisplayLineToDictList("You pick up " + itemTitle + "." + strQuantity, "12w" + targetItem.defaultTitleColorCode + "1w" + strQuantityCode)
				elif STR_TARGET != "All" and TARGET_COUNT > 1:
					colorCode = targetItem.defaultTitleColorCode
					if "Quantity" in item.flags and item.flags["Quantity"] > 1:
						Console.addDisplayLineToDictList("You pick up " + itemTitle + ".", "12w" + colorCode + "1w", {"Count Mod":getCount})
					else : Console.addDisplayLineToDictList("You pick up " + itemTitle + ".", "12w" + colorCode + "1w", {"Count Mod":len(delList)})
				else : Console.addDisplayLineToDictList("You pick up everything you can.", "30w1y")
					
			elif len(delList) == 0 and messageType != None:
				if messageType == "Already Busy":
					Console.addDisplayLineToDictList("You are busy.")
				elif messageType == "No Get":
					Console.addDisplayLineToDictList("You can't pick that up.", "7w1y14w1y")
				elif messageType == "Overweight":
					Console.addDisplayLineToDictList("You can't hold that much.", "7w1y16w1y")
					
			else : Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")
			
		# Delete From Room #
		if len(delList) > 0:
			delList.reverse()
			for delData in delList:
				delItem = currentRoom.itemList[delData[0]]
				
				if "Quantity" in delItem.flags:
					currentRoom.itemList[delData[0]].flags["Quantity"] -= delData[1]
					if currentRoom.itemList[delData[0]].flags["Quantity"] <= 0:
						currentRoom.removeItemFromRoom(currentRoom.itemList[delData[0]])
				else:
					currentRoom.removeItemFromRoom(currentRoom.itemList[delData[0]])

	def userDrop(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT):
		
		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Player Inventory"])
			targetCount = 0
			dropCount = 0
			delList = []
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Drop Item(s) #
		if messageType == None and (targetItem != None or STR_TARGET == "All"):
			for iNum, item in enumerate(DATA_PLAYER.inventoryList):
				if STR_TARGET == "All" or item.idNum == targetItem.idNum:
					if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
						
						# Create New Quantity Item #
						if "Quantity" in item.flags:
							targetDropCount = TARGET_COUNT
							if targetDropCount == "All" or (targetDropCount == 1 and TARGET_INDEX == 0) or targetDropCount > item.flags["Quantity"] : targetDropCount = item.flags["Quantity"]
							item = DataItem.loadPrefab(item.idNum, ITEM_IMAGE_DICT, {"Quantity":targetDropCount})
							
						# Update Container Objects #
						if "Container List" in item.flags:
							for containerItem in item.flags["Container List"]:
								containerItem.currentLoc = "Room"
								
								# Remove Container Item From Player Update Item List #
								if containerItem in DATA_PLAYER.updateItemList:
									del DATA_PLAYER.updateItemList[DATA_PLAYER.updateItemList.index(containerItem)]
								
								# Add Container Item To Room Update Item List #
								if containerItem.isUpdateItem() and containerItem not in currentRoom.updateItemList:
									currentRoom.updateItemList.append(containerItem)
								
						# Add Item To Room & Update Delete List #
						currentRoom.addItem(item, DATA_PLAYER)
						if "Quantity" in item.flags:
							dropCount += item.flags["Quantity"]
							delList.append([iNum, item.flags["Quantity"]])
						else:
							dropCount += 1
							delList.append([iNum, 1])
							
						# Update Screen Data #
						if True:
							if item.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
							elif item.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
							
							SIDESCREEN_PLAYER_UTILITY.updateDisplayItemList(item, "Remove")
							Config.DRAW_SCREEN_DICT["Player Utility"] = True
						
					targetCount += 1
					if TARGET_COUNT != "All" and dropCount >= TARGET_COUNT:
						break
		
		# Messages #
		if True:
			if len(delList) > 0:
				if STR_TARGET != "All":
					itemTitle = targetItem.defaultTitle
					colorCode = targetItem.defaultTitleColorCode
					if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
						itemTitle = itemTitle[0].lower() + itemTitle[1::]
					if "Quantity" in item.flags and item.flags["Quantity"] > 1:
						Console.addDisplayLineToDictList("You drop " + itemTitle + ".", "9w" + colorCode + "1y", {"Count Mod":item.flags["Quantity"]})
					else : Console.addDisplayLineToDictList("You drop " + itemTitle + ".", "9w" + colorCode + "1y", {"Count Mod":len(delList)})
				elif STR_TARGET == "All":
					Console.addDisplayLineToDictList("You drop everything you have.", "28w1y")
					
			else:
				if messageType == "Already Busy":
					Console.addDisplayLineToDictList("You are busy.")
				elif len(DATA_PLAYER.inventoryList) == 0:
					Console.addDisplayLineToDictList("You don't have anything.", "7w1y15w1y")
				else : Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")

		# Delete From Player #
		if len(delList) > 0:
			delList.reverse()
			for delData in delList:
				delItem = DATA_PLAYER.inventoryList[delData[0]]
			
				if "Quantity" in delItem.flags:
					if DATA_PLAYER.inventoryList[delData[0]].flags["Quantity"] - delData[1] <= 0:
						DATA_PLAYER.removeItemFromInventory(delItem)
					else:
						DATA_PLAYER.inventoryList[delData[0]].flags["Quantity"] -= delData[1]
						DATA_PLAYER.currentWeight -= delItem.weight * delData[1]
				else : DATA_PLAYER.removeItemFromInventory(delItem)
					
	def userOCLUItem(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_ACTION, CONTAINER_NUM, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX):

		# Get Data #
		if True:
			currentRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
			targetContainer, containerIndex, containerLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, ["Room Items", "Player Inventory", "Room Spaceships"])
			targetSpaceshipDict = None
			if targetContainer != None and containerLoc == "Room Spaceships" : targetSpaceshipDict = targetContainer
			elif targetContainer == None and "In Spaceship" in DATA_PLAYER.flags : targetSpaceshipDict = {"ID":DATA_PLAYER.currentArea, "Random ID":DATA_PLAYER.currentAreaRandom}
			containerCount = 0
			ocluCount = 0
			itemList = currentRoom.itemList
			if containerLoc == "Player Inventory" : itemList = DATA_PLAYER.inventoryList
			if STR_TARGET_CONTAINER == "All" : itemList = currentRoom.itemList + DATA_PLAYER.inventoryList
			containerStatus = None
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# OCLU Item #
		if messageType == None:
			if targetSpaceshipDict != None:
				targetSpaceship = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].getTargetSpaceship(targetSpaceshipDict["ID"], targetSpaceshipDict["Random ID"])
				if TARGET_ACTION  == "Open" : messageType = "Does Not Open"
				elif TARGET_ACTION == "Close" : messageType = "Does Not Close"
				elif "Spaceship Door Key Num" not in targetSpaceship.flags : messageType = "No Lock"
				elif not DATA_PLAYER.hasKey(targetSpaceship.flags["Spaceship Door Key Num"]) : messageType = "Lack Key"
				else:
					if TARGET_ACTION == "Lock" and targetSpaceship.flags["Spaceship Door Status"] == "Locked" : messageType = "Already Locked"
					elif TARGET_ACTION == "Unlock" and targetSpaceship.flags["Spaceship Door Status"] == "Unlocked" : messageType = "Already Unlocked"
					else:
						targetSpaceship.flags["Spaceship Door Status"] = TARGET_ACTION + "ed"
						messageType = TARGET_ACTION + " Spaceship"
				
			elif (targetContainer != None and targetContainer.type == "Container") or STR_TARGET_CONTAINER == "All":
				for iNum, item in enumerate(itemList):
					if item.type == "Container" and(STR_TARGET_CONTAINER == "All" or item.idNum == targetContainer.idNum):
						if (CONTAINER_NUM == "All" or TARGET_CONTAINER_INDEX == containerCount):
							
							if "Container Status" not in item.flags:
								if TARGET_ACTION in ["Open", "Close"] and messageType == None:
									messageType = "Does Not " + TARGET_ACTION
								elif TARGET_ACTION in ["Lock", "Unlock"] and messageType == None:
									messageType = "No Lock"
									
							else:
								containerStatus = copy.deepcopy(item.flags["Container Status"])
								
								if TARGET_ACTION == "Open":
									if containerStatus == "Open" and messageType == None:
										messageType = "Already Open"
									elif containerStatus == "Closed":
										item.flags["Container Status"] = "Open"
										messageType = "Open Container"
										if STR_TARGET_CONTAINER == "All" : messageType = "Open All Containers"
										ocluCount += 1
									elif containerStatus == "Locked":
										keyCheck = DATA_PLAYER.hasKey(item.flags["Key Num"])
										if keyCheck == False and messageType == None : messageType = "Lack Key"	
										else:
											item.flags["Container Status"] = "Open"
											messageType = "Unlock And Open Container"
											if STR_TARGET_CONTAINER == "All" : messageType = "Open All Containers"
											ocluCount += 1
											
								elif TARGET_ACTION == "Close":
									if containerStatus in ["Closed", "Locked"] and messageType == None:
										messageType = "Already Closed"
									elif containerStatus == "Open":
										item.flags["Container Status"] = "Closed"
										messageType = "Close Container"
										if STR_TARGET_CONTAINER == "All" : messageType = "Close All Containers"
										ocluCount += 1
										
								elif TARGET_ACTION == "Lock":
									if "Key Num" not in item.flags and messageType == None:
										messageType = "No Lock"
									elif containerStatus == "Locked" and messageType == None:
										messageType = "Already Locked"
									elif containerStatus in ["Open", "Closed"] and "Key Num" in item.flags:
										keyCheck = DATA_PLAYER.hasKey(item.flags["Key Num"])
										if keyCheck == False and messageType == None : messageType = "Lack Key"	
										elif keyCheck:
											item.flags["Container Status"] = "Locked"
											messageType = "Lock Container"
											if STR_TARGET_CONTAINER == "All" : messageType = "Lock All Containers"
											if containerStatus == "Open":
												messageType = "Close And Lock Container"
												if STR_TARGET_CONTAINER == "All" : messageType = "Lock All Containers"
											ocluCount += 1

								elif TARGET_ACTION == "Unlock":
									if "Key Num" not in item.flags and messageType == None:
										messageType = "No Lock"
									elif containerStatus in ["Open", "Closed"] and messageType == None:
										messageType = "Already Unlocked"
									elif containerStatus == "Locked" and "Key Num" in item.flags:
										keyCheck = DATA_PLAYER.hasKey(item.flags["Key Num"])
										if keyCheck == False and messageType == None : messageType = "Lack Key"	
										elif keyCheck:
											item.flags["Container Status"] = "Closed"
											messageType = "Unlock Container"
											if STR_TARGET_CONTAINER == "All" : messageType = "Unlock All Containers"
											ocluCount += 1
								
								if STR_TARGET_CONTAINER != "All" and CONTAINER_NUM != "All" and TARGET_CONTAINER_INDEX == containerCount:
									break
							
						containerCount += 1
			
		# Messages #
		if messageType != None:
			
			# Title Mods #
			if STR_TARGET_CONTAINER != "All" and targetSpaceshipDict == None:
				itemTitle = targetContainer.defaultTitle
				if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
					itemTitle = itemTitle[0].lower() + itemTitle[1::]
			
			if messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Open All Containers":
				Console.addDisplayLineToDictList("You open all containers.", "23w1y")
			elif messageType == "Open Container":
				Console.addDisplayLineToDictList("You open "+itemTitle+".", "9w"+targetContainer.defaultTitleColorCode+"1w", {"Cound Mod":ocluCount})
			elif messageType == "Already Open":
				Console.addDisplayLineToDictList("It is already open.", "18w1y")
			elif messageType == "Close All Containers":
				Console.addDisplayLineToDictList("You close all containers.", "24w1y")
			elif messageType == "Close Container":
				Console.addDisplayLineToDictList("You close "+itemTitle+".", "10w"+targetContainer.defaultTitleColorCode+"1w", {"Cound Mod":ocluCount})
			elif messageType == "Close And Lock Container":
				Console.addDisplayLineToDictList("You close and lock "+itemTitle+".", "19w"+targetContainer.defaultTitleColorCode+"1w", {"Cound Mod":ocluCount})
			elif messageType == "Already Closed":
				Console.addDisplayLineToDictList("It is already closed.", "21w")
			elif messageType == "Lock All Containers":
				Console.addDisplayLineToDictList("You lock all containers.", "24w")
			elif messageType == "Lock Container":
				Console.addDisplayLineToDictList("You lock "+itemTitle+".", "9w"+targetContainer.defaultTitleColorCode+"1w", {"Cound Mod":ocluCount})
			elif messageType == "Already Locked":
				Console.addDisplayLineToDictList("It is already locked.", "21w")
			elif messageType == "Unlock All Containers":
				Console.addDisplayLineToDictList("You unlock all containers.", "26w")
			elif messageType == "Unlock Container":
				Console.addDisplayLineToDictList("You unlock "+itemTitle+".", "11w"+targetContainer.defaultTitleColorCode+"1w", {"Cound Mod":ocluCount})
			elif messageType == "Unlock And Open Container":
				Console.addDisplayLineToDictList("You unlock and open "+itemTitle+".", "20w"+targetContainer.defaultTitleColorCode+"1w", {"Cound Mod":ocluCount})
			elif messageType == "Already Unlocked":
				Console.addDisplayLineToDictList("It is already unlocked.", "23w")
			elif messageType == "No Lock":
				Console.addDisplayLineToDictList("It doesn't have a lock.", "23w")
			elif messageType == "Lack Key":
				Console.addDisplayLineToDictList("You lack the key.", "17w")
			elif messageType == "Does Not Open":
				Console.addDisplayLineToDictList("It doesn't open.")
			elif messageType == "Does Not Close":
				Console.addDisplayLineToDictList("It doesn't close.")
			elif messageType in ["Lock Spaceship", "Unlock Spaceship"]:
				Console.addDisplayLineToDictList("The ship beeps in response to your command.")
				
		elif targetContainer != None and targetContainer.type != "Container":
			Console.addDisplayLineToDictList("It is not a container.", "22w")
		else : Console.addDisplayLineToDictList("You can't find it.", "18w")

	def userFillLiquidContainer(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Player Inventory"])
			targetCount = 0
			fillCount = 0
			fillList = []
			fountainCheck = False
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Fill Liquid Container #
		if messageType == None and (STR_TARGET == "All" or targetItem != None):
			if STR_TARGET != "All" and targetItem.type != "Liquid Container" : messageType = "Not Fillable"
			else:
				for fNum, targetFountain in enumerate(currentRoom.itemList):
					if targetFountain.type == "Fountain":
						fountainCheck = True
						for iNum, item in enumerate(DATA_PLAYER.inventoryList):
							if STR_TARGET == "All" or item.idNum == targetItem.idNum:
								if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
									if item.type == "Liquid Container":
										if item.flags["Current Liquid Capacity"] >= item.flags["Max Liquid Capacity"]:
											messageType = "Already Full"
										else:
											item.flags["Current Liquid Capacity"] = item.flags["Max Liquid Capacity"]
											item.flags["Liquid Type"] = targetFountain.flags["Liquid Type"]
											fillList.append(iNum)
											fillCount += 1
									
								targetCount += 1
								if TARGET_COUNT != "All" and fillCount >= TARGET_COUNT:
									break
						break

		# Messages #
		if True:
			if len(fillList) > 1 and STR_TARGET == "All":
				Console.addDisplayLineToDictList("You fill all your containers with " + targetFountain.flags["Liquid Type"] + ".")
				
			elif len(fillList) > 0:
				targetItem = DATA_PLAYER.inventoryList[fillList[0]]
				itemTitle = targetItem.defaultTitle
				if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
					itemTitle = itemTitle[0].lower() + itemTitle[1::]
				itemTitleMod = ""
				if len(fillList) > 1:
					itemTitleMod = " (x" + str(len(fillList)) + ")"
				Console.addDisplayLineToDictList("You fill " + targetItem.defaultTitle + " with " + targetFountain.flags["Liquid Type"] + "." + itemTitleMod)
				
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Not Fillable":
				Console.addDisplayLineToDictList("You can't fill it.")
			elif messageType == "Already Full":
				Console.addDisplayLineToDictList("It is already full.")
			elif targetItem != None and fountainCheck == False:
				Console.addDisplayLineToDictList("There is nowhere to fill it.")
			else : Console.addDisplayLineToDictList("You can't find it.")

	def userEmpty(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Player Inventory", "Room Items"])
			targetCount = 0
			emptyCount = 0
			emptyList = []
			fountainCheck = False
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Empty Container #
		if messageType == None and (STR_TARGET == "All" or targetItem != None):
			if STR_TARGET != "All" and targetItem.type not in ["Container", "Liquid Container"] : messageType = "Can't Empty"
			else:
				targetItemList = DATA_PLAYER.inventoryList
				if targetItemLoc == "Room Items" : targetItemList = currentRoom.itemList
				if TARGET_COUNT == "All" and STR_TARGET == "All" : targetItemList = DATA_PLAYER.inventoryList + currentRoom.itemList
				
				for iNum, item in enumerate(targetItemList):
					if STR_TARGET == "All" or item.idNum == targetItem.idNum:
						if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
						
							if item.type in ["Container", "Liquid Container"]:
								if (item.type == "Container" and len(item.flags["Container List"]) == 0) or (item.type == "Liquid Container" and item.flags["Current Liquid Capacity"] == 0):
									messageType = "Already Empty"
								elif item.type == "Container" and "Container Status" in item.flags and item.flags["Container Status"] == "Locked" and "Key Num" in item.flags and not DATA_PLAYER.hasKey(item.flags["Key Num"]):
									if messageType == None : messageType = "Container Locked"
								
								elif item.type == "Container":
									for containerItem in item.flags["Container List"]:
									
										# Set Drop Side Data #
										if targetItemLoc in ["Player Gear", "Player Inventory"] or item.dropSide == "Player":
											containerItem.dropSide = "Player"
										else : containerItem.dropSide = "Mob"
										
										currentRoom.addItem(containerItem, DATA_PLAYER)
										if containerItem in DATA_PLAYER.updateItemList:
											del DATA_PLAYER.updateItemList[DATA_PLAYER.updateItemList.index(containerItem)]
										
									if item.currentLoc == "Player":
										DATA_PLAYER.currentWeight -= item.flags["Container Current Weight"]
									if "Container Status" in item.flags:
										item.flags["Container Status"] = "Open"
									item.flags["Container Current Weight"] = 0
									item.flags["Container List"] = []
									
									emptyList.append(iNum)
									emptyCount += 1
									
								elif item.type == "Liquid Container":
									if currentRoom.floorType == "Grass":
										if currentRoom.idNum not in PARENT_AREA.wetTimerRoomDict:
											PARENT_AREA.wetTimerRoomDict[currentRoom.idNum] = {}
										if item.flags["Liquid Type"] in PARENT_AREA.wetTimerRoomDict[currentRoom.idNum]:
											PARENT_AREA.wetTimerRoomDict[currentRoom.idNum][item.flags["Liquid Type"]] += item.flags["Current Liquid Capacity"]
										else : PARENT_AREA.wetTimerRoomDict[currentRoom.idNum][item.flags["Liquid Type"]] = item.flags["Current Liquid Capacity"]
										if PARENT_AREA.wetTimerRoomDict[currentRoom.idNum][item.flags["Liquid Type"]] > Config.WET_TIMER["Max Ground Liquid"]:
											PARENT_AREA.wetTimerRoomDict[currentRoom.idNum][item.flags["Liquid Type"]] = Config.WET_TIMER["Max Ground Liquid"]
											
									item.flags["Current Liquid Capacity"] = 0
									item.flags["Liquid Type"] = None
									
									emptyList.append(iNum)
									emptyCount += 1
							
								# Update Screen Data #
								if targetItemLoc in ["Player Gear", "Player Inventory"] or item.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
								elif item.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
							
								Config.DRAW_SCREEN_DICT["Player Utility"] = True
							
						targetCount += 1
						if TARGET_COUNT != "All" and emptyCount >= TARGET_COUNT:
							break

		# Messages #
		if True:
			if len(emptyList) > 1 and STR_TARGET == "All":
				Console.addDisplayLineToDictList("You empty every container you can on the ground.")
			elif len(emptyList) > 0:
				targetItem = targetItemList[emptyList[0]]
				Console.addDisplayLineToDictList("You empty " + targetItem.defaultTitle + " on the ground.", "10w"+targetItem.defaultTitleColorCode+"14w1y", {"Count Mod":len(emptyList)})
				
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Can't Empty":
				Console.addDisplayLineToDictList("You can't empty it.")
			elif messageType == "Already Empty":
				Console.addDisplayLineToDictList("It is already empty.")
			elif messageType == "Container Locked":
				Console.addDisplayLineToDictList("It is locked.")
			else : Console.addDisplayLineToDictList("You can't find it.")

	def userEat(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Player Inventory"])
			targetCount = 0
			eatCount = 0
			delList = []
			messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Get Del List #
		eatCount = 0
		if messageType == None and (STR_TARGET == "All" or targetItem != None):
			for iNum, item in enumerate(DATA_PLAYER.inventoryList):
				if STR_TARGET == "All" or item.idNum == targetItem.idNum:
					if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
						if "Edible" not in item.flags:
							messageType = "Not Edible"
							if STR_TARGET != "All" : break
						else:
							delList.append(iNum)
							
							# Get Eat Count #
							if "Quantity" in item.flags:
								if TARGET_COUNT == "All" : eatCount = item.flags["Quantity"]
								elif isinstance(TARGET_COUNT, int) and TARGET_COUNT > item.flags["Quantity"] : eatCount = item.flags["Quantity"]
								elif isinstance(TARGET_COUNT, int) : eatCount = TARGET_COUNT
							else : eatCount += 1
							
					targetCount += 1
					if (TARGET_COUNT != "All" and eatCount >= TARGET_COUNT) \
					or "Quantity" in item.flags:
						break

		# Heal Player - Temp Effect #
		if eatCount > 0:
			if DATA_PLAYER.currentHP < DATA_PLAYER.maxHP:
				DATA_PLAYER.currentHP += eatCount
		
		# Messages #
		if True:
			if len(delList) > 1 and STR_TARGET == "All":
				Console.addDisplayLineToDictList("You eat everything you can.", "26w1y")
				
			elif len(delList) > 0:
				itemTitle = targetItem.defaultTitle
				if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
					itemTitle = itemTitle[0].lower() + itemTitle[1::]
				Console.addDisplayLineToDictList("You eat " + itemTitle + ".", "8w" + targetItem.defaultTitleColorCode + "1y", {"Count Mod":len(delList)})
				
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Not Edible":
				Console.addDisplayLineToDictList("You can't eat that.", "7w1y10w1y")
			else : Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")
		
		# Delete From Player #
		if len(delList) > 0:
			delList.reverse()
			for i in delList:
				targetItem = DATA_PLAYER.inventoryList[i]
				if "Quantity" in targetItem.flags:
					if eatCount >= targetItem.flags["Quantity"] : DATA_PLAYER.removeItemFromInventory(targetItem)
					else:
						targetItem.flags["Quantity"] -= eatCount
						DATA_PLAYER.currentWeight -= targetItem.getWeight() * eatCount
				else : DATA_PLAYER.removeItemFromInventory(targetItem)
				
		# Update Draw Data #
		Config.DRAW_SCREEN_DICT["Player Stats"] = True

	def userDrink(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX):

		pass

	def userWear(PARENT_AREA, DATA_PLAYER, STR_TARGET, TARGET_INDEX, TARGET_SLOT):

		# Get Data #
		if True:
			targetItem = None
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			if STR_TARGET != "All" : targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Player Inventory"])
			targetCount = 0
			wornItem = None
			secondWornItem = None
			delList = []
			targetGearSlot = None
			messageType = None
		
		# Wear Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Wear Item #
		if messageType == None and (STR_TARGET == "All" or targetItem != None):
			if DATA_PLAYER.dominantHand == "Left" : strOffhand = "Right Hand"
			else : strOffhand = "Left Hand"
			for iNum, item in enumerate(DATA_PLAYER.inventoryList):
				wearCheck = False
				if STR_TARGET == "All" or item.idNum == targetItem.idNum:
					if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
						if "Gear Slot" in item.flags and item.flags["Gear Slot"] != None and (item.flags["Gear Slot"] == "Weapon" or item.flags["Gear Slot"] in DATA_PLAYER.gearDict):
							
							# Get Target Gear Slot #
							targetGearSlot = item.flags["Gear Slot"]
							
							# Get Weapon Gear Slot #
							if item.flags["Gear Slot"] == "Weapon":
								targetGearSlot = DATA_PLAYER.dominantHand + " Hand"
								
								if item.flags["Weapon Type"] == "Shield":
									shieldWornCheck = False
									if DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand + " Hand"] != None and DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand + " Hand"].flags["Weapon Type"] == "Shield":
										shieldWornCheck = "Dominant Hand"
									elif DATA_PLAYER.gearDict[strOffhand] != None and DATA_PLAYER.gearDict[strOffhand].flags["Weapon Type"] == "Shield":
										shieldWornCheck = "Off Hand"
									
									if shieldWornCheck == False:
										if DATA_PLAYER.gearDict[strOffhand] == None : targetGearSlot = strOffhand
									elif shieldWornCheck == "Off Hand" : targetGearSlot = strOffhand
								
								if DATA_PLAYER.gearDict[targetGearSlot] != None and DATA_PLAYER.gearDict[targetGearSlot].flags["Weapon Type"] != "Shield" \
								and DATA_PLAYER.gearDict[strOffhand] == None and "Two Handed" not in DATA_PLAYER.gearDict[targetGearSlot].flags and "Two Handed" not in item.flags:
									targetGearSlot = strOffhand
								if TARGET_SLOT != None : targetGearSlot = TARGET_SLOT
								
								# Get Other Hand Data #
								if targetGearSlot == "Left Hand" : strNonTargetHand = "Right Hand"
								else : strNonTargetHand = "Left Hand"
								
							# Remove Worn Item #
							if DATA_PLAYER.gearDict[targetGearSlot] != None and STR_TARGET != "All":
								wornItem = DATA_PLAYER.gearDict[targetGearSlot]
								DATA_PLAYER.inventoryList.append(wornItem)
								DATA_PLAYER.gearDict[targetGearSlot] = item
								delList.append(iNum)
								wearCheck = True
							
							# Wear Item #
							elif DATA_PLAYER.gearDict[targetGearSlot] == None:
								DATA_PLAYER.gearDict[targetGearSlot] = item
								delList.append(iNum)
								wearCheck = True
								
							# Two-Handed Weapon Check #
							if wearCheck and STR_TARGET != "All":
								
								# Remove Other Item If Two Handed Weapon Is Worn #
								if item.flags["Gear Slot"] == "Weapon" and "Two Handed" in item.flags:
									if DATA_PLAYER.gearDict[strNonTargetHand] != None:
										secondWornItem = DATA_PLAYER.gearDict[strNonTargetHand]
										DATA_PLAYER.inventoryList.append(secondWornItem)
										DATA_PLAYER.gearDict[strNonTargetHand] = None
								
								# Remove Other Item If It Is A Two Handed Weapon #
								elif item.flags["Gear Slot"] == "Weapon":
									otherHandGear = DATA_PLAYER.gearDict[strNonTargetHand]
									if otherHandGear != None and "Two Handed" in otherHandGear.flags:
										wornItem = DATA_PLAYER.gearDict[strNonTargetHand]
										DATA_PLAYER.inventoryList.append(wornItem)
										DATA_PLAYER.gearDict[strNonTargetHand] = None
							
							# Double Shield Check #
							if DATA_PLAYER.gearDict[strNonTargetHand] != None and DATA_PLAYER.gearDict[strNonTargetHand].flags["Weapon Type"] == "Shield":
								wornItem = DATA_PLAYER.gearDict[strNonTargetHand]
								DATA_PLAYER.inventoryList.append(DATA_PLAYER.gearDict[strNonTargetHand])
								DATA_PLAYER.gearDict[strNonTargetHand] = None
							
							if STR_TARGET != "All" : break
					targetCount += 1
				
		# Messages #
		if True:
			if len(delList) > 1:
				Console.addDisplayLineToDictList("You wear everything you can.", "27w1y")
				
			elif len(delList) == 1:
				
				targetItemTitle = DATA_PLAYER.inventoryList[delList[0]].defaultTitle
				targetItemColorCode = DATA_PLAYER.inventoryList[delList[0]].defaultTitleColorCode
				if len(targetItemTitle.split()) > 1 and targetItemTitle.split()[0] in ["A", "An"] : targetItemTitle = targetItemTitle[0].lower() + targetItemTitle[1::]
				strAction = "wear"
				if item.flags["Gear Slot"] == "Weapon" : strAction = "hold"
				
				strOffhand = "."
				wearOffhandCheck = False
				if STR_TARGET != "All" and "Two Handed" not in item.flags and targetGearSlot != None and targetGearSlot in ["Left Hand", "Right Hand"]:
					if targetGearSlot != (DATA_PLAYER.dominantHand + " Hand") : strOffhand = " in your off-hand."
				
				if wornItem != None:
					wornItemTitle = wornItem.defaultTitle
					if len(wornItemTitle.split()) > 1 and wornItemTitle.split()[0] in ["A", "An"] : wornItemTitle = wornItemTitle[0].lower() + wornItemTitle[1::]
					if secondWornItem != None : Console.addDisplayLineToDictList("You remove your weapons and " + strAction + " " + targetItemTitle + strOffhand)
					else : Console.addDisplayLineToDictList("You remove " + wornItemTitle + " and " + strAction + " " + targetItemTitle + strOffhand, "11w" + wornItem.defaultTitleColorCode + "10w" + targetItemColorCode + str(len(strOffhand)-1) + "w1y")
				
				else : Console.addDisplayLineToDictList("You " + strAction + " " + targetItemTitle + strOffhand, "9w" + targetItemColorCode + str(len(strOffhand)-1) + "w1y")
				
			else:
				if messageType == "Already Busy":
					Console.addDisplayLineToDictList("You are busy.")
				elif targetItem != None and "Gear Slot" not in targetItem.flags:
					Console.addDisplayLineToDictList("You can't wear it.", "7w1y9w1y")
				elif STR_TARGET == "All":
					Console.addDisplayLineToDictList("You don't have anything to wear.", "7w1y23w1y")
				else : Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")
					
		# Delete Items #
		if len(delList) > 0:
			delList.reverse()
			for iNum in delList:
				del DATA_PLAYER.inventoryList[iNum]

	def userRemove(PARENT_AREA, DATA_PLAYER, STR_TARGET, TARGET_SLOT):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, -1, ["Player Gear"])
			removeList = []
			messageType = None
		
		# Remove Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Remove Item(s) #
		if messageType == None and (STR_TARGET == "All" or targetItem != None):
			for gearSlot in DATA_PLAYER.gearDict:
				if DATA_PLAYER.gearDict[gearSlot] != None:
					gearItem = DATA_PLAYER.gearDict[gearSlot]
					if STR_TARGET == "All" or gearItem.idNum == targetItem.idNum:
						if TARGET_SLOT == None or (gearSlot in ["Left Hand", "Right Hand"] and gearSlot == TARGET_SLOT):
							
							removeList.append(gearItem)
							DATA_PLAYER.inventoryList.append(gearItem)
							DATA_PLAYER.gearDict[gearSlot] = None
							
							if STR_TARGET != "All" : break
		
		# Update Attack Range If Charging A Default Attack #
		if messageType == None and "Attack Data" in DATA_PLAYER.flags and DATA_PLAYER.flags["Attack Data"].id == -1:
			if DATA_PLAYER.flags["Attack Data"].rangeType == "Long" and DATA_PLAYER.getAttackRange() == 0:
				DATA_PLAYER.flags["Attack Data"].rangeType = "Short"
		
		# Messages #
		if True:
			
			if len(removeList) > 1:
				Console.addDisplayLineToDictList("You remove everything you can.", "29w1y")
			
			elif len(removeList) == 1:
				targetItem = removeList[0]
				itemTitle = targetItem.defaultTitle
				if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
					itemTitle = itemTitle[0].lower() + itemTitle[1::]
				Console.addDisplayLineToDictList("You remove " + itemTitle + ".", "11w" + targetItem.defaultTitleColorCode + "1y")
			
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif STR_TARGET == "All":
				Console.addDisplayLineToDictList("You aren't wearing anything.", "8w1y18w1y")
			else : Console.addDisplayLineToDictList("You can't find it.", "7w1y9w1y")

	def userPressButton(PARENT_AREA, DATA_PLAYER, STR_TARGET, ENTITY_IMAGE_DICT, ITEM_IMAGE_DICT):

		# Get Data #
		playerRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
		targetControlPanel = None
		
		# Get Target Control Panel #
		for tempItem in playerRoom.itemList:
			if tempItem.type == "Control Panel":
				targetControlPanel = tempItem
				break
		
		# Checks #
		if DATA_PLAYER.currentAction != None:
			Console.addDisplayLineToDictList("You are busy.")
		elif targetControlPanel == None:
			Console.addDisplayLineToDictList("You don't see a control panel.")
		elif STR_TARGET == None:
			Console.addDisplayLineToDictList("Press which button?")
			
		# Press Button #
		else:
			
			# Get & Press Target Button #
			targetButtonDict = targetControlPanel.getTargetControlPanelButton(STR_TARGET)
			if targetButtonDict == None : Console.addDisplayLineToDictList("You see no such button.")
			else:
				
				if targetButtonDict["Button Type"] == "Generate":
			
					if targetButtonDict["Target Object Type"] == "Item":
						targetItemID = 0
						if "Target ID" in targetButtonDict : targetItemID = targetButtonDict["Target ID"]
						playerRoom.loadItem(targetItemID, ITEM_IMAGE_DICT)
						
						targetItem = playerRoom.itemList[-1]
						Console.addDisplayLineToDictList("You press a button and " + targetItem.defaultTitle + " materializes on the floor.")
				
					elif targetButtonDict["Target Object Type"] == "Mob":
						targetMobID = 0
						if "Target ID" in targetButtonDict : targetMobID = targetButtonDict["Target ID"]
						playerRoom.loadMob(targetMobID, DATA_PLAYER, ENTITY_IMAGE_DICT)
						
						targetMob = playerRoom.mobList[-1]
						Console.addDisplayLineToDictList("You press a button and " + targetMob.defaultTitle + " materializes before you.")
						
	def userPlantSeed(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX):

		# Get Data #
		if True:
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetItem, targetItemIndex, targetItemLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Player Inventory"])
			targetCount = 0
			plantCount = 0
			delList = []
			messageType = None
			
		# Wear Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Plant Seed #
		if messageType == None and (STR_TARGET == "All" or targetItem != None):
			for iNum, item in enumerate(DATA_PLAYER.inventoryList):
				if item.type in ["Seed", "Plant"]:
					if STR_TARGET == "All" or item.idNum == targetItem.idNum:
						if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
							if currentRoom.floorType != "Grass":
								messageType = "Not Dirt"
								break
							else:
								item.currentSolarSystem = currentRoom.idSolarSystem
								item.currentPlanet = currentRoom.idPlanet
								item.currentArea = currentRoom.idArea
								item.currentAreaRandom = currentRoom.idAreaRandom
								item.currentRoom = currentRoom.idNum
								item.currentLoc = "Room"
								item.flags["Planted"] = True
								
								if "In Spaceship" in currentRoom.flags : item.flags["In Spaceship"] = True
								elif "In Spaceship" in item.flags : del item.flags["In Spaceship"]
								
								if item.type == "Plant" : currentRoom.itemList.append(item)
								currentRoom.updateItemList.append(item)
								delList.append(iNum)
								plantCount += 1
							
						targetCount += 1
						if TARGET_COUNT != "All" and plantCount >= TARGET_COUNT:
							break

		# Messages #
		if True:
			if len(delList) > 1 and STR_TARGET == "All":
				Console.addDisplayLineToDictList("You plant all of your seeds.", "28w")
				
			elif len(delList) > 0:
				itemTitle = targetItem.defaultTitle
				if len(itemTitle.split()) > 1 and itemTitle.split()[0] in ["A", "An"]:
					itemTitle = itemTitle[0].lower() + itemTitle[1::]
				Console.addDisplayLineToDictList("You plant " + itemTitle + " in the ground.", "10w" + targetItem.defaultTitleColorCode + "14w1y", {"Count Mod":len(delList)})
				
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Not Dirt":
				Console.addDisplayLineToDictList("You can't plant anything here.", "30w")
			elif targetItem != None:
				Console.addDisplayLineToDictList("You can't plant that.", "25w")
			else : Console.addDisplayLineToDictList("You can't find it.", "18w")

		# Delete From Player #
		if len(delList) > 0:
			delList.reverse()
			for i in delList:
				delItem = DATA_PLAYER.inventoryList[i]
				DATA_PLAYER.removeItemFromInventory(delItem)

	def switchHands(DATA_PLAYER):

		# Checks #
		if DATA_PLAYER.currentAction != None:
			Console.addDisplayLineToDictList("You are busy.")

		# Switch Hands #
		else:
			if DATA_PLAYER.dominantHand == "Left" : DATA_PLAYER.dominantHand = "Right"
			else : DATA_PLAYER.dominantHand = "Left"
			
			Console.addDisplayLineToDictList("You switch your handedness.")

	def switchWeapons(DATA_PLAYER):

		# Get Data #
		leftWeapon = None
		rightWeapon = None
		messageType = None
		
		# Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Switch Weapons #
		if messageType == None:
			if DATA_PLAYER.gearDict["Left Hand"] != None : leftWeapon = DATA_PLAYER.gearDict["Left Hand"]
			if DATA_PLAYER.gearDict["Right Hand"] != None : rightWeapon = DATA_PLAYER.gearDict["Right Hand"]
			if leftWeapon == None and rightWeapon == None : messageType = "Holding Nothing"
			else:
				DATA_PLAYER.gearDict["Left Hand"] = rightWeapon
				DATA_PLAYER.gearDict["Right Hand"] = leftWeapon
		
		# Messages #
		if messageType == "Already Busy":
			Console.addDisplayLineToDictList("You are busy.")
		elif messageType == "Holding Nothing":
			Console.addDisplayLineToDictList("You aren't holding anything.")
		else:
			Console.addDisplayLineToDictList("You switch hands with what you are holding.")

	def userReloadWeapon(DATA_PLAYER, STR_TARGET_WEAPON, STR_TARGET_AMMO):

		# Get Data #
		if True:
			targetWeapon = None
			targetAmmo = None
			targetAmmoIndex = -1
			backupAmmo = None
			backupAmmoIndex = -1
			messageType = None

		# Wear Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Get Target Weapon #
		if messageType == None:
			
			# No Target Weapon #
			if STR_TARGET_WEAPON == None:
				
				# Dominant Hand Check #
				targetHand = DATA_PLAYER.dominantHand + " Hand"
				if DATA_PLAYER.gearDict[targetHand] != None:
					targetWeapon = DATA_PLAYER.gearDict[targetHand]
				
				# Other Hand Check #
				if targetHand == "Left Hand" : otherHand = "Right Hand"
				else : otherHand = "Left Hand"
				
				if (targetWeapon == None or targetWeapon.type != "Weapon" or targetWeapon.flags["Weapon Type"] != "Ranged" \
				or (targetWeapon.type == "Weapon" and targetWeapon.flags["Weapon Type"] == "Ranged" and targetWeapon.flags["Loaded Ammo Object"] != None and targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"] >= targetWeapon.flags["Magazine Size"])) \
				and DATA_PLAYER.gearDict[otherHand] != None and DATA_PLAYER.gearDict[otherHand].type == "Weapon" and DATA_PLAYER.gearDict[otherHand].flags["Weapon Type"] == "Ranged":
					targetWeapon = DATA_PLAYER.gearDict[otherHand]
				
			# Left/Right #
			elif STR_TARGET_WEAPON in ["Left", "Right"]:
				if STR_TARGET_WEAPON == "Left" and DATA_PLAYER.gearDict["Left Hand"] != None:
					targetWeapon = DATA_PLAYER.gearDict["Left Hand"]
				elif STR_TARGET_WEAPON == "Right" and DATA_PLAYER.gearDict["Right Hand"] != None:
					targetWeapon = DATA_PLAYER.gearDict["Right Hand"]
				
			# TargetWeapon #
			else:
			
				# Dominant Hand Check #
				targetHand = DATA_PLAYER.dominantHand + " Hand"
				if DATA_PLAYER.gearDict[targetHand] != None and STR_TARGET_WEAPON in DATA_PLAYER.gearDict[targetHand].keyList:
					targetWeapon = DATA_PLAYER.gearDict[targetHand]
				
				# Other Hand Check #
				if targetHand == "Left Hand" : otherHand = "Right Hand"
				else : otherHand = "Left Hand"
				
				if (targetWeapon == None or targetWeapon.type != "Weapon" or targetWeapon.flags["Weapon Type"] != "Ranged" \
				or (targetWeapon.type == "Weapon" and targetWeapon.flags["Weapon Type"] == "Ranged" and targetWeapon.flags["Loaded Ammo Object"] != None and targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"] >= targetWeapon.flags["Magazine Size"])) \
				and DATA_PLAYER.gearDict[otherHand] != None and STR_TARGET_WEAPON in DATA_PLAYER.gearDict[otherHand].keyList:
					targetWeapon = DATA_PLAYER.gearDict[otherHand]
				
				# Inventory Check #
				if targetWeapon == None or not (targetWeapon.type == "Weapon" and targetWeapon.flags["Weapon Type"] == "Ranged"):
					for tempItem in DATA_PLAYER.inventoryList:
						if STR_TARGET_WEAPON in tempItem.keyList:
							targetWeapon = tempItem
							break
				
		# Get Target Ammo #
		if messageType == None and targetWeapon != None and targetWeapon.type == "Weapon" and targetWeapon.flags["Weapon Type"] == "Ranged":
			
			# No Target Ammo #
			if STR_TARGET_AMMO == None:
				
				# Get Already Loaded Ammo Data #
				alreadyLoadedAmmo = None
				if targetWeapon.flags["Loaded Ammo Object"] != None:
					alreadyLoadedAmmo = targetWeapon.flags["Loaded Ammo Object"]
				
				# Get Target Ammo Index #
				for tempIndex, tempItem in enumerate(DATA_PLAYER.inventoryList):
					if alreadyLoadedAmmo != None and tempItem.type == "Ammo" and tempItem.idNum == alreadyLoadedAmmo.idNum:
						targetAmmoIndex = tempIndex
						targetAmmo = tempItem
						break
					if backupAmmo == None and tempItem.type == "Ammo" and tempItem.flags["Ammo Type"] == targetWeapon.flags["Ammo Type"]:
						backupAmmoIndex = tempIndex
						backupAmmo = tempItem
						if alreadyLoadedAmmo == None : break
				if targetAmmoIndex == -1 and backupAmmoIndex != -1:
					targetAmmoIndex = backupAmmoIndex
					targetAmmo = backupAmmo
					
			# TargetAmmo #
			elif STR_TARGET_AMMO != None:
				for tempIndex, tempItem in enumerate(DATA_PLAYER.inventoryList):
					if tempItem.type == "Ammo" and STR_TARGET_AMMO in tempItem.keyList:
						targetAmmoIndex = tempIndex
						targetAmmo = tempItem
						break
					
		# Reload Checks #
		if messageType == None:
			if "Basic Combat" not in DATA_PLAYER.skillTreeDict or "Ranged" not in DATA_PLAYER.skillTreeDict["Basic Combat"].skillDict : messageType = "Skill Not Learned"
			elif targetWeapon == None : messageType = "No Weapon Found"
			elif targetWeapon.type != "Weapon" or targetWeapon.flags["Weapon Type"] != "Ranged" : messageType = "Weapon Not Ranged"
			elif targetAmmo == None : messageType = "Ammo Not Found"
			elif targetAmmo.flags["Ammo Type"] != targetWeapon.flags["Ammo Type"] : messageType = "Wrong Ammo Type"
			elif targetWeapon.flags["Loaded Ammo Object"] != None and targetWeapon.flags["Loaded Ammo Object"].idNum == targetAmmo.idNum and targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"] >= targetWeapon.flags["Magazine Size"] : messageType = "Magazine Already Full"
		
		# Reload Weapon #
		if messageType == None:

			# Get Reload Amount #
			if targetWeapon.flags["Loaded Ammo Object"] == None : reloadAmount = targetWeapon.flags["Magazine Size"]
			else : reloadAmount = targetWeapon.flags["Magazine Size"] - targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"]
			if reloadAmount > targetAmmo.flags["Quantity"] : reloadAmount = targetAmmo.flags["Quantity"]
			reloadTime = reloadAmount * targetAmmo.flags["Reload Time"]
		
			# Update Player Status #
			DATA_PLAYER.currentAction = {"Type":"Reloading", "Timer":reloadTime, "Target Weapon":targetWeapon, "Target Ammo":targetAmmo}
			messageType = "Reload Weapon"
			
		# Messages #
		if True:
			if messageType == "Reload Weapon":
				Console.addDisplayLineToDictList("You begin reloading " + targetWeapon.defaultTitle + "..")
			elif messageType == "Skill Not Learned":
				Console.addDisplayLineToDictList("You don't know how.")
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "No Weapon Found":
				Console.addDisplayLineToDictList("You can't find it.")
			elif messageType == "Weapon Not Ranged":
				Console.addDisplayLineToDictList("You can't reload it.")
			elif messageType == "Ammo Not Found":
				Console.addDisplayLineToDictList("You don't have ammo.")
			elif messageType == "Wrong Ammo Type":
				Console.addDisplayLineToDictList("Wrong ammo type.")
			elif messageType == "Magazine Already Full":
				Console.addDisplayLineToDictList("The magazine is full.")

	def userUnloadWeapon(DATA_PLAYER, STR_TARGET_WEAPON):

		# Get Data #
		if True:
			targetWeapon = None
			currentUnloadedWeapon = None
			unloadCount = 0
			messageType = None
		
		# Wear Checks #
		if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
		
		# Get Target Weapon #
		if messageType == None:
			
			# No Target Weapon #
			if STR_TARGET_WEAPON == None:
				
				# Dominant Hand Check #
				targetHand = DATA_PLAYER.dominantHand + " Hand"
				if DATA_PLAYER.gearDict[targetHand] != None and DATA_PLAYER.gearDict[targetHand].type == "Weapon" and DATA_PLAYER.gearDict[targetHand].flags["Weapon Type"] == "Ranged":
					targetWeapon = DATA_PLAYER.gearDict[targetHand]
				
				# Other Hand Check #
				if targetHand == "Left Hand" : otherHand = "Right Hand"
				else : otherHand = "Left Hand"
				
				if targetWeapon == None or (targetWeapon.flags["Loaded Ammo Object"] != None and targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"] == 0) \
				and DATA_PLAYER.gearDict[otherHand] != None and DATA_PLAYER.gearDict[otherHand].type == "Weapon" and DATA_PLAYER.gearDict[otherHand].flags["Weapon Type"] == "Ranged":
					targetWeapon = DATA_PLAYER.gearDict[otherHand]
			
			# Left/Right #
			elif STR_TARGET_WEAPON in ["Left", "Right"]:
				if STR_TARGET_WEAPON == "Left" and DATA_PLAYER.gearDict["Left Hand"] != None:
					targetWeapon = DATA_PLAYER.gearDict["Left Hand"]
				elif STR_TARGET_WEAPON == "Right" and DATA_PLAYER.gearDict["Right Hand"] != None:
					targetWeapon = DATA_PLAYER.gearDict["Right Hand"]
					
			# TargetWeapon #
			elif STR_TARGET_WEAPON != "All":
			
				# Dominant Hand Check #
				targetHand = DATA_PLAYER.dominantHand + " Hand"
				if DATA_PLAYER.gearDict[targetHand] != None and STR_TARGET_WEAPON in DATA_PLAYER.gearDict[targetHand].keyList:
					targetWeapon = DATA_PLAYER.gearDict[targetHand]
					
				# Other Hand Check #
				if targetHand == "Left Hand" : otherHand = "Right Hand"
				else : otherHand = "Left Hand"
					
				if not (targetWeapon != None and targetWeapon.type == "Weapon" and targetWeapon.flags["Weapon Type"] == "Ranged") \
				and DATA_PLAYER.gearDict[otherHand] != None and STR_TARGET_WEAPON in DATA_PLAYER.gearDict[otherHand].keyList:
					targetWeapon = DATA_PLAYER.gearDict[otherHand]
				
				# Inventory Check #
				if targetWeapon == None or not (targetWeapon.type == "Weapon" and targetWeapon.flags["Weapon Type"] == "Ranged"):
					for tempItem in DATA_PLAYER.inventoryList:
						if STR_TARGET_WEAPON in tempItem.keyList:
							targetWeapon = tempItem
							break
				
		# Unload All #
		if messageType == None and STR_TARGET_WEAPON == "All":
			
			if DATA_PLAYER.gearDict["Left Hand"] != None and DATA_PLAYER.gearDict["Left Hand"].type == "Weapon" and DATA_PLAYER.gearDict["Left Hand"].flags["Weapon Type"] == "Ranged":
				targetWeapon = DATA_PLAYER.gearDict["Left Hand"]
				unloadMessage = targetWeapon.unloadRangedWeapon(DATA_PLAYER)
				if unloadMessage == "Unload Weapon":
					unloadCount += 1
					currentUnloadedWeapon = targetWeapon
		
			if DATA_PLAYER.gearDict["Right Hand"] != None and DATA_PLAYER.gearDict["Right Hand"].type == "Weapon" and DATA_PLAYER.gearDict["Right Hand"].flags["Weapon Type"] == "Ranged":
				targetWeapon = DATA_PLAYER.gearDict["Right Hand"]
				unloadMessage = targetWeapon.unloadRangedWeapon(DATA_PLAYER)
				if unloadMessage == "Unload Weapon":
					unloadCount += 1
					currentUnloadedWeapon = targetWeapon
				
			if unloadCount == 0:
				for tempItem in DATA_PLAYER.inventoryList:
					if tempItem.type == "Weapon" and tempItem.flags["Weapon Type"] == "Ranged":
						targetWeapon = tempItem
						unloadMessage = targetWeapon.unloadRangedWeapon(DATA_PLAYER)
						if unloadMessage == "Unload Weapon":
							unloadCount += 1
							currentUnloadedWeapon = targetWeapon
						
		# Pre Unload Checks #
		if messageType == None:
			if "Basic Combat" not in DATA_PLAYER.skillTreeDict or "Ranged" not in DATA_PLAYER.skillTreeDict["Basic Combat"].skillDict : messageType = "Skill Not Learned"
			elif DATA_PLAYER.currentAction != None : messageType = "Already Busy"
			elif targetWeapon == None : messageType = "No Weapon Found"
			elif targetWeapon.type != "Weapon" or targetWeapon.flags["Weapon Type"] != "Ranged" : messageType = "Target Weapon Not Ranged"
			elif targetWeapon.flags["Loaded Ammo Object"] == None or targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"] == 0 : messageType = "Already Unloaded"
		
		# Unload Weapon #
		if messageType in [None, "Already Unloaded"] and STR_TARGET_WEAPON != "All":
			messageType = targetWeapon.unloadRangedWeapon(DATA_PLAYER)
			if messageType == "Unload Weapon":
				unloadCount += 1
				currentUnloadedWeapon = targetWeapon
		
		# Messages #
		if True:
			if unloadCount == 1:
				Console.addDisplayLineToDictList("You unload " + currentUnloadedWeapon.defaultTitle + ".")
			elif unloadCount > 1:
				Console.addDisplayLineToDictList("You unload all your weapons.")
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Skill Not Learned":
				Console.addDisplayLineToDictList("You don't know how.")
			elif messageType == "No Weapon Found":
				Console.addDisplayLineToDictList("You can't find it.")
			elif messageType == "Target Weapon Not Ranged":
				Console.addDisplayLineToDictList("You can't unload that.")
			elif STR_TARGET_WEAPON == "All":
				Console.addDisplayLineToDictList("All of your magazines are empty.")
			elif messageType == "Already Unloaded":
				Console.addDisplayLineToDictList("It is already unloaded.")
		
# User Input - Player Commands #	
if True:
	def userUseSkill(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE):
		
		# String & Skill Check #
		STR_TARGET_SKILL = str(STR_TARGET_SKILL)
		if STR_TARGET_SKILL != "":
			targetSkill = DATA_PLAYER.getTargetSkillFromInputString(STR_TARGET_SKILL)
			
			if targetSkill != None:
				
				# Target Entity Skill #
				if targetSkill.useTarget == "Entity":
					DataCombat.userUseSkillEntity(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE, "Use Skill")
				
				# Item Skill #
				elif targetSkill.useTarget == "Item":
					userUseSkillItem(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE)
				
				# Room Skill #
				elif targetSkill.useTarget == "Room":
					userUseSkillRoom(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE)
				
				else : Console.addDisplayLineToDictList("You don't know how.")
			else : Console.addDisplayLineToDictList("You don't know how.")
				
	def userUseSkillItem(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE):
		
		print("Item Skill")

	def userUseSkillRoom(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE):
		
		print("Room Skill")
			
# User Input - Mob Commands #
if True:
	def userTargetMob(PARENT_ROOM, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX):

		targetMob, mobIndex, mobLoc = getTarget(DATA_PLAYER, PARENT_ROOM, STR_TARGET, TARGET_INDEX, ["Room Mobs"])
		targetCount = 0
		targetMobCount = 0
		messageType = None
		
		# Target Mobs #
		if STR_TARGET == "All" or targetMob != None:
			for mNum, tempMob in enumerate(PARENT_ROOM.mobList):
				if STR_TARGET == "All" or tempMob.idNum == targetMob.idNum:
					if TARGET_INDEX == -1 or TARGET_INDEX == targetCount:
						
						# Target Mob #
						if tempMob not in DATA_PLAYER.mobTargetList:
							if TARGET_COUNT == 1 : DATA_PLAYER.mobTargetList.insert(0, tempMob)
							else : DATA_PLAYER.mobTargetList.append(tempMob)
							targetMobCount += 1
						elif tempMob in DATA_PLAYER.mobTargetList:
							if TARGET_COUNT == 1 and tempMob != DATA_PLAYER.mobTargetList[0]:
								del DATA_PLAYER.mobTargetList[DATA_PLAYER.mobTargetList.index(tempMob)]
								DATA_PLAYER.mobTargetList.insert(0, tempMob)
								targetMobCount += 1
							else : messageType = "Already Targeting"
							
					targetCount += 1
					if TARGET_COUNT != "All" and targetMobCount >= TARGET_COUNT:
						break

		# Messages #
		if True:
			if (targetMobCount > 0 and STR_TARGET != "All") or (targetMobCount == 1 and STR_TARGET == "All"):
				if targetMob == None : targetMob = DATA_PLAYER.mobTargetList[0]
				Console.addDisplayLineToDictList("You focus your attention on " + targetMob.defaultTitle + ".", "28w"+targetMob.defaultTitleColorCode+"1y", {"Count Mod":targetMobCount})
			elif targetMobCount > 1 and STR_TARGET == "All":
				Console.addDisplayLineToDictList("You focus on everyone in the room.")
			elif messageType == "Already Targeting":
				strTarget = "everyone"
				if targetMob != None : strTarget = targetMob.defaultTitle
				Console.addDisplayLineToDictList("You are already targeting " + strTarget + ".")
			else:
				Console.addDisplayLineToDictList("You don't see anyone like that.")

		# Update Display Surfaces #
		pass

	def userTargetMobInRoom(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE):

		# Get Data #
		currentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
		startRoom = currentArea.roomDict[DATA_PLAYER.currentRoom]
		
		# Get Target Room #
		if TARGET_ROOM_DISTANCE > DATA_PLAYER.getViewRange():
			Console.addDisplayLineToDictList("You can't see that far.")
		else:
			endArea, endRoom, messageType = DataWorld.getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, currentArea, startRoom, TARGET_DIR, TARGET_ROOM_DISTANCE)
		
		# Target Mobs #
		if startRoom != endRoom and messageType == None:
			userTargetMob(endRoom, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX)
			
		# Messages #
		if messageType != None:
			if messageType == "No Exit":
				Console.addDisplayLineToDictList("There is nothing there.", "22w1y")
			elif messageType == "Door Is Closed":
				Console.addDisplayLineToDictList("The door is closed.", "18w1y")

		# Update Display Surfaces #
		pass

	def userStopTargeting(PARENT_AREA, DATA_PLAYER, TARGET_COUNT, STR_TARGET, TARGET_INDEX, COMMAND_TYPE):

		if COMMAND_TYPE == "Stop Targeting All":
			if len(DATA_PLAYER.mobTargetList) == 0:
				Console.addDisplayLineToDictList("You aren't focusing on anyone.")
			else:
				if len(DATA_PLAYER.mobTargetList) > 1:
					Console.addDisplayLineToDictList("You stop focusing on your targets.")
				else:
					tempMob = DATA_PLAYER.mobTargetList[0]
					Console.addDisplayLineToDictList("You stop focusing on " + tempMob.defaultTitle + ".")
				DATA_PLAYER.mobTargetList = []
		
		elif COMMAND_TYPE == "Stop Targeting All Mob":
			if len(DATA_PLAYER.mobTargetList) == 0:
				Console.addDisplayLineToDictList("You aren't focusing on anyone.")
			else:
				delList = []
				targetNum = -1
				for mNum, tempMob in enumerate(DATA_PLAYER.mobTargetList):
					if STR_TARGET in tempMob.keyList and (targetNum == -1 or targetNum == tempMob.idNum):
						delList.append(mNum)
						targetNum = tempMob.idNum
				if len(delList) > 0:
					delList.reverse()
					for dNum in delList:
						tempMob = DATA_PLAYER.mobTargetList[dNum]
						del DATA_PLAYER.mobTargetList[dNum]
						
				if len(delList) > 1:
					Console.addDisplayLineToDictList("You stop focusing on your targets.")
				elif len(delList) == 1:
					Console.addDisplayLineToDictList("You stop focusing on " + tempMob.defaultTitle + ".")
				else:
					Console.addDisplayLineToDictList("You don't see anyone like that.")
		
		elif COMMAND_TYPE == "Stop Targeting Count#":
			if len(DATA_PLAYER.mobTargetList) == 0:
				Console.addDisplayLineToDictList("You aren't focusing on anyone.")
			else:
				delCount = 0
				for delNum in range(TARGET_COUNT):
					delCount += 1
					tempMob = DATA_PLAYER.mobTargetList[0]
					del DATA_PLAYER.mobTargetList[0]
					if len(DATA_PLAYER.mobTargetList) == 0 : break
				if delCount > 1:
					Console.addDisplayLineToDictList("You stop focusing on some targets.")
				else:
					Console.addDisplayLineToDictList("You stop focusing on " + tempMob.defaultTitle + ".")
		
		elif COMMAND_TYPE in ["Stop Targeting Count# Mob", "Stop Targeting Mob"]:
			if len(DATA_PLAYER.mobTargetList) == 0:
				Console.addDisplayLineToDictList("You aren't focusing on anyone.")
			else:
				delList = []
				targetNum = -1
				for mNum, tempMob in enumerate(DATA_PLAYER.mobTargetList):
					if STR_TARGET in tempMob.keyList and (targetNum == -1 or targetNum == tempMob.idNum):
						delList.append(mNum)
						targetNum = tempMob.idNum
						if len(delList) >= TARGET_COUNT : break
				if len(delList) > 0:
					delList.reverse()
					for dNum in delList:
						tempMob = DATA_PLAYER.mobTargetList[dNum]
						del DATA_PLAYER.mobTargetList[dNum]
						
				if len(delList) > 1:
					Console.addDisplayLineToDictList("You stop focusing on some targets.")
				elif len(delList) == 1:
					Console.addDisplayLineToDictList("You stop focusing on " + tempMob.defaultTitle + ".")
				else:
					Console.addDisplayLineToDictList("You don't see anyone like that.")
		
		elif COMMAND_TYPE == "Stop Targeting":
			if len(DATA_PLAYER.mobTargetList) == 0:
				Console.addDisplayLineToDictList("You aren't focusing on anyone.")
			else:
				Console.addDisplayLineToDictList("You stop focusing on " + DATA_PLAYER.mobTargetList[0].defaultTitle + ".")
				del DATA_PLAYER.mobTargetList[0]
		
		elif COMMAND_TYPE == "Stop Targeting Mob @Index":
			
			# Get Data #
			currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
			targetMob, mobIndex, mobLoc = getTarget(DATA_PLAYER, currentRoom, STR_TARGET, TARGET_INDEX, ["Room Mobs"])
			targetCount = 0
			removeCheck = False
			messageType = None

			# Stop Targeting Mobs #
			if targetMob != None:
				for mNum, tempMob in enumerate(currentRoom.mobList):
					if tempMob.idNum == targetMob.idNum:
						if TARGET_INDEX == targetCount:
							if tempMob not in DATA_PLAYER.mobTargetList : messageType = "Not Target"
							else:
								removeCheck = True
								del DATA_PLAYER.mobTargetList[DATA_PLAYER.mobTargetList.index(tempMob)]
							break
						targetCount += 1
			
			# Messages #
			if True:
				if removeCheck:
					Console.addDisplayLineToDictList("You stop focusing on " + tempMob.defaultTitle + ".")
				elif messageType == "Not Target":
					Console.addDisplayLineToDictList("You aren't focused on " + tempMob.defaultTitle + ".")
				else:
					Console.addDisplayLineToDictList("You don't see anyone like that.")

		# Update Display Surfaces #
		pass

	def userTame(SOLAR_SYSTEM_DICT, DATA_PLAYER, STR_TARGET, TARGET_INDEX):

		# Get Data #
		if True:
			parentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
			parentRoom = parentArea.roomDict[DATA_PLAYER.currentRoom]
			targetMob = None
			targetCount = 0
			messageType = None

		# Get Target Mob #
		if STR_TARGET == None and TARGET_INDEX == None:
			if len(DATA_PLAYER.mobTargetList) == 0 : messageType = "Can't Find Target"
			else:
				tempMob = DATA_PLAYER.mobTargetList[0]
				tempMobRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[tempMob.currentSolarSystem], tempMob).roomDict[tempMob.currentRoom]
				tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, parentRoom, tempMobRoom, 1)
				if tempRange == 0 : targetMob = tempMob
				else : messageType = "Target Too Far"
				
		else:
			for tempMob in parentRoom.mobList:
				if STR_TARGET in tempMob.keyList:
					targetMob = tempMob
					if targetCount < TARGET_INDEX : targetCount += 1
					else : break
		
		# Tame Checks #
		if targetMob == None : messageType = "Can't Find Target"
		if messageType == None and targetMob != None:
			if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
			elif "General Skills" not in DATA_PLAYER.skillTreeDict or "Tame" not in DATA_PLAYER.skillTreeDict["General Skills"].skillDict : messageType = "Don't Know How"
			elif targetMob in DATA_PLAYER.groupList : messageType = "Already In Your Group"
			elif len(targetMob.groupList) > 0 : messageType = "Already In Group"
			elif len(DATA_PLAYER.groupList) >= 3 : messageType = "Group Is Full"
			elif targetMob.currentAction != None or targetMob.combatTarget != None or targetMob in DATA_PLAYER.mobTargetPlayerCombatList : messageType = "Target Is Busy"
			elif targetMob.evolutionLevel != "Animal" : messageType = "Can Only Tame Animals"
			
		# Initiate Tame Mob #
		if targetMob != None and messageType == None:
			DATA_PLAYER.currentAction = {"Type":"Taming", "Timer":2.0, "Target Mob":targetMob}
			if "Group Leader" not in DATA_PLAYER.flags : DATA_PLAYER.flags["Group Leader"] = True
			if "Group Leader" in targetMob.flags : del targetMob.flags["Group Leader"]
			messageType = "Initiate Tame Target"
			
		# Messages #
		if messageType != None:
			if messageType == "Can't Find Target":
				Console.addDisplayLineToDictList("You don't see them.")
			elif messageType == "Target Too Far":
				Console.addDisplayLineToDictList("Your target is too far.")
			elif messageType == "Already Busy":
				Console.addDisplayLineToDictList("You are busy.")
			elif messageType == "Don't Know How":
				Console.addDisplayLineToDictList("You don't know how!")
			elif messageType == "Already In Your Group":
				Console.addDisplayLineToDictList(targetMob.defaultTitle + " is already sympathetic to you.")
			elif messageType == "Already In Group":
				Console.addDisplayLineToDictList(targetMob.defaultTitle + " seems uninterested.")
			elif messageType == "Group Is Full":
				Console.addDisplayLineToDictList("Your group is already full.")
			elif messageType == "Target Is Busy":
				Console.addDisplayLineToDictList(targetMob.defaultTitle + " is distracted.")
			elif messageType == "Can Only Tame Animals":
				Console.addDisplayLineToDictList("Only animals can be tamed.")
			elif messageType == "Initiate Tame Target":
				Console.addDisplayLineToDictList("You gaze deeply into the eyes of " + targetMob.defaultTitle + "..")
		
	def userDisband(SOLAR_SYSTEM_DICT, DATA_PLAYER, STR_TARGET, TARGET_INDEX):

		# Get Data #
		if True:
			targetCount = 0
			disbandList = []
			
		# Remove Target Mobs From Group Mob's Group List #
		for targetGroupMember in DATA_PLAYER.groupList:
			if STR_TARGET == "All" or STR_TARGET in targetGroupMember.keyList:
				if STR_TARGET == "All" or TARGET_INDEX == targetCount:
				
					# Remove Target Mob From Other Group Members List #
					for tempEntity in targetGroupMember.groupList:
						if tempEntity.objectType == "Mob" and tempEntity != targetGroupMember and targetGroupMember in tempEntity.groupList:
							del tempEntity.groupList[tempEntity.groupList.index(targetGroupMember)]
					
					targetGroupMember.groupList = []
					disbandList.append(targetGroupMember)
				targetCount += 1
				
		# Remove Target Mobs From Player Group List #
		for targetGroupMember in disbandList:
			if targetGroupMember in DATA_PLAYER.groupList:
				del DATA_PLAYER.groupList[DATA_PLAYER.groupList.index(targetGroupMember)]
		if len(DATA_PLAYER.groupList) == 0 and "Group Leader" in DATA_PLAYER.flags:
			del DATA_PLAYER.flags["Group Leader"]
		
		# Messages #
		if len(disbandList) > 0 and STR_TARGET == "All":
			Console.addDisplayLineToDictList("You disband your group.")
		elif len(disbandList) == 1 and STR_TARGET != "All":
			Console.addDisplayLineToDictList("You remove " + disbandList[0].defaultTitle + " from the group.")
		elif len(disbandList) == 0 and STR_TARGET == "All":
			Console.addDisplayLineToDictList("You don't have a group.")
		elif len(disbandList) == 0 and STR_TARGET != "All":
			Console.addDisplayLineToDictList("You aren't grouped with anyone like that.")
			
# User Input - God Commands #
def userGodCommand(PARENT_AREA, SOLAR_SYSTEM_DICT, DATA_PLAYER, USER_INPUT_LIST):

	# Get Data #
	playerArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
	playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]

	# Weather #
	if "In Spaceship" in DATA_PLAYER.flags:
		Console.addDisplayLineToDictList("You can't create weather in a spaceship!")
	else:
		updateAreaDataList, updateRoomDataList = DataWorld.getSurroundingRoomsDataList(SOLAR_SYSTEM_DICT, playerArea, playerRoom, Config.PLAYER_UPDATE_RANGE)
		userInputString = ' '.join(USER_INPUT_LIST)
		if userInputString == "rain":
			PARENT_AREA.createWeather(SOLAR_SYSTEM_DICT, DATA_PLAYER, playerArea, updateRoomDataList, "Rain Timer", 500, "Default")
		elif userInputString in ["cloud", "cloudy", "clouds"]:
			PARENT_AREA.createWeather(SOLAR_SYSTEM_DICT, DATA_PLAYER, playerArea, updateRoomDataList, "Cloudy Timer", 500, "Default")
		elif userInputString in ["stop weather", "no weather", "stopweather", "noweather"]: # Use With Caution! (Does Not Synch With Game)
			PARENT_AREA.weatherDict = {}
			Console.addDisplayLineToDictList("The weather comes to a halt.", "27w1y")
		
# Utility Commands #
def getTarget(DATA_PLAYER, CURRENT_ROOM, STR_TARGET, TARGET_INDEX, SEARCH_LIST=["All"]):

	targetObject = None
	targetObjectIndex = -1
	targetObjectLoc = None
	targetCount = 0
	targetId = -1

	# Room Items #
	if "All" in SEARCH_LIST or "Room Items" in SEARCH_LIST:
		for iNum, item in enumerate(CURRENT_ROOM.itemList):
			if STR_TARGET in item.keyList and (targetId == item.idNum or targetId == -1):
				targetId = item.idNum
				targetObject = item
				targetObjectIndex = iNum
				targetObjectLoc = "Room Items"
				if targetCount < TARGET_INDEX : targetCount += 1
				else : break
		
	# Player Inventory #
	if "All" in SEARCH_LIST or "Player Inventory" in SEARCH_LIST:
		if targetObject == None:
			for iNum, item in enumerate(DATA_PLAYER.inventoryList):
				if STR_TARGET in item.keyList and (targetId == item.idNum or targetId == -1):
					targetId = item.idNum
					targetObject = item
					targetObjectIndex = iNum
					targetObjectLoc = "Player Inventory"
					if targetCount < TARGET_INDEX : targetCount += 1
					else : break
		
	# Player Gear #
	if "All" in SEARCH_LIST or "Player Gear" in SEARCH_LIST:
		if targetObject == None:
			for gearSlot in DATA_PLAYER.gearDict:
				if DATA_PLAYER.gearDict[gearSlot] != None:
					item = DATA_PLAYER.gearDict[gearSlot]
					if STR_TARGET in item.keyList:
						targetObject = item
						targetObjectIndex = -1
						targetObjectLoc = "Player Gear"
						break
		
	# Room Mob List #
	if "All" in SEARCH_LIST or "Room Mobs" in SEARCH_LIST:
		if targetObject == None:
			for mNum, mob in enumerate(CURRENT_ROOM.mobList):
				if STR_TARGET in mob.keyList and (targetId == mob.idNum or targetId == -1):
					targetId = mob.idNum
					targetObject = mob
					targetObjectIndex = mNum
					targetObjectLoc = "Room Mobs"
					if targetCount < TARGET_INDEX : targetCount += 1
					else : break
					
	# Spaceship List #
	if "Room Spaceships" in SEARCH_LIST:
		if STR_TARGET != "All" and targetObject == None:
			for sNum, targetSpaceshipDict in enumerate(CURRENT_ROOM.spaceshipDictList):
				if STR_TARGET in targetSpaceshipDict["Key List"]:
					targetObject = targetSpaceshipDict
					targetObjectIndex = sNum
					targetObjectLoc = "Room Spaceships"
					break
					
	return targetObject, targetObjectIndex, targetObjectLoc;

def getTargetInContainer(DATA_PLAYER, CURRENT_ROOM, STR_TARGET_OBJECT, TARGET_OBJECT_INDEX, STR_TARGET_CONTAINER, TARGET_CONTAINER_INDEX, SEARCH_LIST=["Container"]):

	targetItem = None
	targetContainer = None
	containerLoc = None
	targetCount = 0
	containerCount = 0
	targetId = -1
	containerId = -1

	# Room Items #
	for item in CURRENT_ROOM.itemList:
		if (STR_TARGET_CONTAINER == "All" or STR_TARGET_CONTAINER in item.keyList) and (item.idNum == containerId or containerId == -1) and item.type in SEARCH_LIST and ((item.type == "Container" and "Container List" in item.flags) or (item.type == "Plant")):
			
			containerLoc = "Room"
			if STR_TARGET_CONTAINER != "All":
				if containerId == -1 : containerId = item.idNum
				if targetContainer != item : targetContainer = item
				
			# Get Target Container List #
			targetContainerList = None
			if item.type == "Container" : targetContainerList = item.flags["Container List"]
			elif item.type == "Plant" and "Fruit List" in item.flags : targetContainerList = item.flags["Fruit List"]
			if targetContainerList != None:
				
				for itemInContainer in targetContainerList:
					if (STR_TARGET_OBJECT == "All" or STR_TARGET_OBJECT in itemInContainer.keyList) and (itemInContainer.idNum == targetId or targetId == -1):
						if STR_TARGET_OBJECT != "All":
							if targetId == -1 : targetId = itemInContainer.idNum
							targetItem = itemInContainer
							
						if TARGET_OBJECT_INDEX == -1 : pass
						elif targetCount < TARGET_OBJECT_INDEX : targetCount += 1
						else : break
						
			if TARGET_CONTAINER_INDEX == -1 : pass
			elif containerCount < TARGET_CONTAINER_INDEX : containerCount += 1
			else : break
			
	# Player Inventory #
	if targetContainer == None:
		for item in DATA_PLAYER.inventoryList:
			if (STR_TARGET_CONTAINER == "All" or STR_TARGET_CONTAINER in item.keyList) and (item.idNum == containerId or containerId == -1) and item.type == "Container" and "Container List" in item.flags:
				
				containerLoc = "Player Inventory"
				if STR_TARGET_CONTAINER != "All":
					if containerId == -1 : containerId = item.idNum
					if targetContainer != item : targetContainer = item
					
				for itemInContainer in item.flags["Container List"]:
					if (STR_TARGET_OBJECT == "All" or STR_TARGET_OBJECT in itemInContainer.keyList) and (itemInContainer.idNum == targetId or targetId == -1):
						if STR_TARGET_OBJECT != "All":
							if targetId == -1 : targetId = itemInContainer.idNum
							targetItem = itemInContainer
							
						if TARGET_OBJECT_INDEX == -1 : pass
						elif targetCount < TARGET_OBJECT_INDEX : targetCount += 1
						else : break
				if TARGET_CONTAINER_INDEX == -1 : pass
				elif containerCount < TARGET_CONTAINER_INDEX : containerCount += 1
				else : break
		
	return targetItem, targetContainer, containerLoc;

# Non-Input Commands #
def addItemToEntityInventory(DATA_ENTITY, TARGET_ITEM, TARGET_ROOM, TARGET_GET_COUNT, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT, FLAGS={}):

	getCheck = True
	
	# Create New Quantity Item #
	oldItem = TARGET_ITEM
	targetWeight = oldItem.getWeight()
	if "Quantity" in TARGET_ITEM.flags:
		if TARGET_GET_COUNT == "All" or TARGET_GET_COUNT > TARGET_ITEM.flags["Quantity"] : TARGET_GET_COUNT = TARGET_ITEM.flags["Quantity"]
		newQuantityItem = DataItem.loadPrefab(TARGET_ITEM.idNum, ITEM_IMAGE_DICT, {"Quantity":TARGET_GET_COUNT})
		if TARGET_GET_COUNT > 1 and DATA_ENTITY.currentWeight + newQuantityItem.getWeight() > DATA_ENTITY.maxWeight:
			newGetCount = (DATA_ENTITY.maxWeight - DATA_ENTITY.currentWeight) / newQuantityItem.weight
			if newGetCount > TARGET_GET_COUNT : newGetCount = TARGET_GET_COUNT
			if newGetCount > 0 : newQuantityItem.flags["Quantity"] = newGetCount
		TARGET_ITEM = newQuantityItem
		TARGET_ITEM.dropSide = oldItem.dropSide
		targetWeight = TARGET_ITEM.getWeight()
		
	# Checks #
	if DATA_ENTITY.currentWeight + targetWeight > DATA_ENTITY.maxWeight : getCheck = False
		
	# Add Item To Entity Inventory #
	if getCheck == True:
		
		# Update Item Loc #
		TARGET_ITEM.currentLoc = DATA_ENTITY.objectType
			
		# Remove Planted Flag #
		if "Planted" in TARGET_ITEM.flags:
			del TARGET_ITEM.flags["Planted"]
		
		# Add Fruits To Inventory #
		if "Fruit List" in TARGET_ITEM.flags and len(TARGET_ITEM.flags["Fruit List"]) > 0:
			for tempFruit in TARGET_ITEM.flags["Fruit List"]:
				DATA_ENTITY.addItemToInventory(tempFruit)
			TARGET_ITEM.flags["Fruit List"] = []
			
		# Update Container Objects #
		if "Container List" in TARGET_ITEM.flags:
			for containerItem in TARGET_ITEM.flags["Container List"]:
				containerItem.currentLoc = DATA_ENTITY.objectType
				
				# Remove Container Item From Room Update Item List #
				if containerItem in TARGET_ROOM.updateItemList:
					del TARGET_ROOM.updateItemList[TARGET_ROOM.updateItemList.index(containerItem)]
					
				# Add Container Item To Entity Update Item List #
				if DATA_ENTITY.objectType == "Player" and containerItem.isUpdateItem() and containerItem not in DATA_ENTITY.updateItemList:
					DATA_ENTITY.updateItemList.append(containerItem)
		
		# Add Item To Entity Inventory #
		DATA_ENTITY.addItemToInventory(TARGET_ITEM)
		
		# Delete From Room #
		if "Delete Check" in FLAGS:
			
			# Get Data #
			if True:
				deleteCheck = False
				updateUtilityScreenCheck = True
				
				# Room Update Checks #
				if "Quantity" in oldItem.flags:
					if oldItem.flags["Quantity"] > TARGET_ITEM.flags["Quantity"]:
						oldItem.flags["Quantity"] -= TARGET_ITEM.flags["Quantity"]
					else:
						TARGET_ROOM.removeItemFromRoom(oldItem)
						deleteCheck = True
				else:
					TARGET_ROOM.removeItemFromRoom(TARGET_ITEM)
					deleteCheck = True
					
			# Update Room Screen #
			if deleteCheck == True:
				if oldItem.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
				elif oldItem.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True

		# Update Player Utility Screen #
		SIDESCREEN_PLAYER_UTILITY.updateDisplayItemList(TARGET_ITEM, "Add")
		Config.DRAW_SCREEN_DICT["Player Utility"] = True
		