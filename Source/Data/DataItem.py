import pygame, random, Config, Utility, DataWorld, DataSkill
from Elements import Console, Caption
from pygame import *

class LoadItem:

	# Initialization Functions #
	def __init__(self):
	
		# ID Variables #
		self.objectType = "Item"
		self.idNum = -1
		self.idRandom = Utility.generateRandomId() # NOT Used For Spaceships!
		self.type = None
		self.currentSolarSystem = None
		self.currentPlanet = None
		self.currentArea = None
		self.currentAreaRandom = None
		self.currentRoom = None
		self.currentLoc = None
		self.flags = {}
		
		# Item Variables #
		self.weight = 0
		self.value = 0
		self.physicalDefense = 0
		self.magicDefense = 0
	
		# Image & Rect Variables #
		self.idImage = None
		self.idIcon = None
		self.rectArea = None
		self.imageSize = None
		self.dropSide = "Mob"
	
		# Description Variables #
		if True:
			self.keyList = []
			self.defaultTitle = "Default Item"
			self.defaultTitleColorCode = "12w"
			self.roomTitle = "A default item is on the ground."
			self.roomTitleColorCode = "32w"
			self.roomTitleCaption = None
			self.lookTitle = "You see nothing special."
			self.lookTitleColorCode = "24w"
	
	def loadControlPanel(self, FLAGS):
	
		self.type = "Control Panel"
		self.defaultTitle = "A Control Panel"
		self.defaultTitleColorCode = "2w1dw7ddw1dw4ddw"
		self.roomTitle = "You see a Control Panel with many buttons."
		self.roomTitleColorCode = "8w2w1dw7ddw1dw4ddw18w1y"
	
		self.flags["No Get"] = True
		self.flags["Button List"] = []
		
		if "Spaceship Control Panel" in FLAGS:
			self.flags["Spaceship Control Panel"] = True
		
	def loadWeapon(self, WEAPON_TYPE, BASE_POWER, FLAGS={}):
	
		self.type = "Weapon"
		self.flags["Gear Slot"] = "Weapon"
		self.flags["Weapon Type"] = WEAPON_TYPE
		self.flags["Base Power"] = BASE_POWER
		self.flags["Weapon Range"] = 0
		self.flags["Attack Speed Ratio"] = 1.0
		if "Two Handed" in FLAGS : self.flags["Two Handed"] = True
		if "Attack Speed Ratio" in FLAGS : self.flags["Attack Speed Ratio"] = FLAGS["Attack Speed Ratio"]
		
		# Ranged Weapons #
		if WEAPON_TYPE == "Ranged":
			self.flags["Weapon Range"] = 1
			if "Weapon Range" in FLAGS : self.flags["Weapon Range"] = FLAGS["Weapon Range"]
			self.flags["Ammo Type"] = "Basic Ammo"
			if "Ammo Type" in FLAGS : self.flags["Ammo Type"] = FLAGS["Ammo Type"]
			
			self.flags["Loaded Ammo Object"] = None
			self.flags["Magazine Size"] = 2
			if "Magazine Size" in FLAGS : self.flags["Magazine Size"] = FLAGS["Magazine Size"]
		
	def loadAmmo(self, AMMO_TYPE, FLAGS={}):
	
		# Ammo Data #
		self.type = "Ammo"
		self.flags["Ammo Type"] = AMMO_TYPE
		self.flags["Quantity"] = 1
		if "Quantity" in FLAGS : self.flags["Quantity"] = FLAGS["Quantity"]
		self.flags["Reload Time"] = 0.4
		if "Reload Time" in FLAGS : self.flags["Reload Time"] = FLAGS["Reload Time"]
		
		# Load Description #
		self.roomTitle = "A pile of " + self.defaultTitle + " is on the ground."
		self.roomTitleColorCode = str(len(self.roomTitle)-1) + "w1y"
		
	def loadArmor(self, GEAR_SLOT):
	
		self.type = "Armor"
		self.flags["Gear Slot"] = GEAR_SLOT
		
	def loadContainer(self, FLAGS={}):
	
		self.type = "Container"
		self.flags["Container Max Weight"] = 1000
		self.flags["Container Current Weight"] = 0
		self.flags["Container List"] = []
		
		if "Container Max Weight" in FLAGS:
			self.flags["Container Max Weight"] = FLAGS["Container Max Weight"]
			
		if "Closable" in FLAGS:
			self.flags["Container Status"] = "Closed"
			
		if "Key Num" in FLAGS:
			self.flags["Key Num"] = FLAGS["Key Num"]
			self.flags["Container Status"] = "Closed"
			
		if "No Get" in FLAGS:
			self.flags["No Get"] = True
		
	def loadLiquidContainer(self, FLAGS={}):
	
		self.type = "Liquid Container"
		self.flags["Max Liquid Capacity"] = 200
		self.flags["Current Liquid Capacity"] = 0
		self.flags["Liquid Type"] = None
		
		if "Max Liquid Capacity" in FLAGS:
			self.flags["Max Liquid Capacity"] = FLAGS["Max Liquid Capacity"]
		
	def loadSeed(self, PLANT_NAME, PLANT_TYPE, FLAGS={}):
	
		self.type = "Seed"
		
		# Update Description Variables #
		stringPrefix = "A "
		if "A/An Check" in FLAGS:
			self.flags["A/An Check"] = FLAGS["A/An Check"]
			stringPrefix = FLAGS["A/An Check"] + " "
		if "Fruit Name" in FLAGS:
			targetName = stringPrefix + FLAGS["Fruit Name"]
			stringName = targetName
			if stringName.split()[0].lower() in ["a", "an"]:
				stringName = ' '.join(stringName.split()[1::])
			self.defaultTitle = targetName
			self.defaultTitleColorCode = str(len(self.defaultTitle)) + "w"
			self.roomTitle = "A small " + stringName + " is on the ground."
			self.roomTitleColorCode = str(len(self.roomTitle)) + "w"
			self.flags["Fruit Name"] = FLAGS["Fruit Name"]
		else:
			self.defaultTitle = stringPrefix + PLANT_NAME + " " + PLANT_TYPE +" Seed"
			self.defaultTitleColorCode = str(len(self.defaultTitle)) + "w"
			self.roomTitle = "A small " + PLANT_NAME + " " + PLANT_TYPE + " Seed is on the ground."
			self.roomTitleColorCode = str(len(self.roomTitle)) + "w"
		
		self.flags["Max Age Timer"] = Config.PLANT_MAX_AGE_TIMER[PLANT_TYPE]
		self.flags["Germinate Timer"] = Config.PLANT_STAGE_TIMER["Germinate"]
		self.flags["Plant Stage"] = "Seed"
		self.flags["Edible"] = True
		
		self.flags["Plant Name"] = PLANT_NAME
		self.flags["Plant Type"] = PLANT_TYPE # Tree / Bush / Plant / Flower #
		self.flags["Fruit Num"] = None
		
		if PLANT_TYPE != "Root":
			self.flags["Quantity"] = 1
			if "Quantity" in FLAGS : self.flags["Quantity"] = FLAGS["Quantity"]
		
		if self.flags["Plant Type"] == "Root":
			self.flags["Wilt Timer"] = Config.PLANT_MAX_LIQUID_TIMER["Root"]
		
		if "Fruit Num" in FLAGS:
			self.flags["Fruit Num"] = FLAGS["Fruit Num"]
			self.flags["Fruit List"] = []
			
		if "Fruit Type" in FLAGS:
			self.flags["Fruit Type"] = FLAGS["Fruit Type"]
			
		if PLANT_TYPE == "Flower" and self.flags["Fruit Num"] == None:
			self.flags["Produce Item On Decay"] = self.idNum
		
	def loadMaterium(self, PREFAB_NUM):
	
		self.idImage = "Crystal 1"
		self.type = "Materium"
	
		# Load Prefab #
		if PREFAB_NUM != None:
			
			if PREFAB_NUM == 1:
				self.flags["Skill Data List"] = [DataSkill.loadPrefab("Magic", "Fire"), DataSkill.loadPrefab("Magic", "Fira"), DataSkill.loadPrefab("Magic", "Firestorm")]
				self.flags["XP Unlock Level"] = [0, 100, 1000]
				self.flags["Total Experience"] = 0
				self.flags["Learn Timer Max"] = 5
				self.flags["Learn Timer"] = 0
				
			elif PREFAB_NUM == 2:
				self.flags["Skill Data List"] = [DataSkill.loadPrefab("Magic", "Attack All")]
				self.flags["XP Unlock Level"] = [0]
				self.flags["Total Experience"] = 0
				self.flags["Learn Timer Max"] = 10
				self.flags["Learn Timer"] = 0
		
	def loadCorpse(self, MOB_DATA):
	
		self.idImage = "Bone 1"
		self.idNum = MOB_DATA.idNum + 200000
		self.defaultTitle = "The Corpse of " + MOB_DATA.defaultTitle
		self.defaultTitleColorCode = "14w" + MOB_DATA.defaultTitleColorCode
		self.roomTitle = "The corpse of " + MOB_DATA.defaultTitle + " lies on the ground."
		self.roomTitleColorCode = "14w" + str(len(MOB_DATA.defaultTitle)) + "w19w1y"
		self.flags["Wilt Timer"] = Config.MOB_TIMER["Corpse Decay"]
		self.loadContainer()
		
	def loadImageData(self, ITEM_IMAGE):
	
		if self.type == "Plant" and self.flags["Plant Type"] == "Tree":
			self.rectArea = pygame.Rect([0, 0, 70, 200])
		else:
			self.rectArea = pygame.Rect([0, 0, ITEM_IMAGE.get_width() - (ITEM_IMAGE.get_width() * .15), ITEM_IMAGE.get_height() - (ITEM_IMAGE.get_height() * .15)])
		
		self.imageSize = [ITEM_IMAGE.get_width(), ITEM_IMAGE.get_height()]
		
	# Update Functions #
	def update(self, SOLAR_SYSTEM_DICT, ITEM_INDEX, DATA_PLAYER, UPDATE_TYPE, PARENT_PLANET, PARENT_AREA, UPDATE_ITEM_DEL_LIST, TICK_SPEED, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT):
	
		if self.currentLoc in ["Player", "Mob"] : parentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
		else : parentRoom = PARENT_AREA.roomDict[self.currentRoom]
	
		# Materia Learn Timer # (Unfinished) # Add to isUpdateItem()
		if False:
			#if UPDATE_TYPE == "Player" and "Magic" in DATA_PLAYER.skillDict and self.type == "Materia" and "Learn Timer" in self.flags:
			#	self.flags["Learn Timer"] += 1
			#	if self.flags["Learn Timer"] >= self.flags["Learn Timer Max"]:
			#		self.flags["Learn Timer"] = 0
					
			#		self.flags["Total Experience"] += 1
			#		for index, targetSkill in enumerate(self.flags["Skill Data List"]):
			#			if self.flags["Total Experience"] >= self.flags["XP Unlock Level"][index]:
							
			#				if targetSkill.strId not in DATA_PLAYER.skillDict["Magic"]:
			#					DATA_PLAYER.skillDict["Magic"][targetSkill.strId] = random.uniform(2.5, 5.5)
			#				elif DATA_PLAYER.skillDict["Magic"][targetSkill.strId] < 100:
			#					DATA_PLAYER.skillDict["Magic"][targetSkill.strId] += random.uniform(0.5, 1.5)
			#					if DATA_PLAYER.skillDict["Magic"][targetSkill.strId] > 100 : DATA_PLAYER.skillDict["Magic"][targetSkill.strId] = 100
			pass
		
		# Tick Max Age - Stage 3 #
		if "Plant Stage" in self.flags and self.flags["Plant Stage"] == 3 and "Max Age Timer" in self.flags and self.flags["Max Age Timer"] > 0:
			self.flags["Max Age Timer"] -= TICK_SPEED
			if self.flags["Max Age Timer"] <= 0:
				self.flags["Wilt Timer"] = 0
				self.flags["Decay Timer"] = Config.ITEM_TIMER["Decay"]
				
				# Drop Remaining Fruits #
				if "Fruit List" in self.flags and len(self.flags["Fruit List"]) > 0:
					roomDropCount = 0
					for targetFruit in self.flags["Fruit List"]:
						if self.currentLoc == "Room":
							if self.flags["Plant Type"] == "Root":
								targetFruit.flags["Planted"] = True
							else:
								parentRoom.addItem(targetFruit, DATA_PLAYER)
								roomDropCount += 1
					self.flags["Fruit List"] = []
						
					if UPDATE_TYPE == "Default" and roomDropCount > 0 and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = targetFruit.defaultTitle + " falls off the vine."
						Console.addDisplayLineToDictList(displayLine, str(len(displayLine))+"w", {"Count Mod":roomDropCount, "Stack Line":True})
							
				if UPDATE_TYPE == "Player" or (UPDATE_TYPE == "Default" and self.currentLoc == "Room" and not ("Planted" in self.flags and "Plant Stage" in self.flags and self.flags["Plant Stage"] == "Seed") and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self)):
					displayLineMod = ""
					if UPDATE_TYPE == "Player" : displayLineMod = " in your inventory"
					displayLine = self.defaultTitle + displayLineMod + " wilts and dries up."
					Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
					
		# Wilt Timer #
		if "Wilt Timer" in self.flags and self.flags["Wilt Timer"] > 0 and not ("Planted" in self.flags and parentRoom.wetCheck(PARENT_AREA, UPDATE_TYPE)):
			self.flags["Wilt Timer"] -= TICK_SPEED
			if self.flags["Wilt Timer"] <= 0:
				self.flags["Decay Timer"] = Config.ITEM_TIMER["Decay"]
				
				# Drop Remaining Fruits #
				if "Fruit List" in self.flags and len(self.flags["Fruit List"]) > 0:
					roomDropCount = 0
					for targetFruit in self.flags["Fruit List"]:
						if self.currentLoc == "Room":
							if self.flags["Plant Type"] == "Root":
								targetFruit.flags["Planted"] = True
							else:
								parentRoom.addItem(targetFruit, DATA_PLAYER)
								roomDropCount += 1
					self.flags["Fruit List"] = []
						
					if UPDATE_TYPE == "Default" and roomDropCount > 0 and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = targetFruit.defaultTitle + " falls off the vine."
						Console.addDisplayLineToDictList(displayLine, str(len(displayLine))+"w", {"Count Mod":roomDropCount, "Stack Line":True})
				
				if UPDATE_TYPE == "Player" or (UPDATE_TYPE == "Default" and self.currentLoc == "Room" and not ("Planted" in self.flags and "Plant Stage" in self.flags and self.flags["Plant Stage"] == "Seed") and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self)):
					displayLineMod = ""
					if UPDATE_TYPE == "Player" : displayLineMod = " in your inventory"
					displayLine = self.defaultTitle + displayLineMod + " wilts and dries up."
					Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
	
		# Decay Timer #
		if "Decay Timer" in self.flags:
			self.flags["Decay Timer"] -= TICK_SPEED
			if self.flags["Decay Timer"] <= 0:
				
				# Produce Item On Decay #
				if "Produce Item On Decay" in self.flags:
					targetItem = loadPrefab(self.flags["Produce Item On Decay"])
					
					if self.currentLoc == "Room":
						parentRoom.addItem(targetItem, DATA_PLAYER)
					
					elif self.currentLoc in ["Player", "Mob"]:
						DATA_PLAYER.addItemToInventory(targetItem)
						
					elif self.currentLoc == "Room Container":
						targetContainer = None
						breakCheck = False
						for tempContainer in parentRoom.itemList:
							if tempContainer.type == "Container" and "Container List" in tempContainer.flags and len(tempContainer.flags["Container List"]) > 0:
								for tempContainerItem in tempContainer.flags["Container List"]:
									if tempContainerItem == self:
										targetContainer = tempContainer
										breakCheck = True
										break
								if breakCheck : break
						if targetContainer != None:
							parentRoom.addItemToContainer(targetContainer, targetItem)
					
					elif self.currentLoc == "Player Container":
						targetContainer = None
						breakCheck = False
						for tempContainer in DATA_PLAYER.inventoryList:
							if tempContainer.type == "Container" and "Container List" in tempContainer.flags and len(tempContainer.flags["Container List"]) > 0:
								for tempContainerItem in tempContainer.flags["Container List"]:
									if tempContainerItem == self:
										targetContainer = tempContainer
										breakCheck = True
										break
								if breakCheck : break
						if targetContainer != None:
							DATA_PLAYER.addItemToContainer(targetContainer, targetItem)
							DATA_PLAYER.currentWeight += targetItem.getWeight()
                            
                            # Break Container If Capacity Breached (?) #
						
				# Delete Item #
				if True:
					deleteIndex = None
					UPDATE_ITEM_DEL_LIST.append(ITEM_INDEX)
							
					if self.currentLoc == "Room":
						for iNum, tempItem in enumerate(parentRoom.itemList):
							if self == tempItem:
								deleteIndex = iNum
								break
						if deleteIndex != None:
							
							# Delete Container Update Items From Room Update Item List #
							if True:
								containerDelList = []
								if parentRoom.itemList[deleteIndex].type == "Container":
									for tempContainerItem in parentRoom.itemList[deleteIndex].flags["Container List"]:
										if tempContainerItem in parentRoom.updateItemList:
											containerDelList.append(parentRoom.updateItemList.index(tempContainerItem))
								if len(containerDelList) > 0:
									containerDelList.reverse()
									for containerDelNum in containerDelList:
										del parentRoom.updateItemList[containerDelNum]
							
							del parentRoom.itemList[deleteIndex]
					
					elif self.currentLoc in ["Player", "Mob"]:
						for iNum, tempItem in enumerate(DATA_PLAYER.inventoryList):
							if self == tempItem:
								deleteIndex = iNum
								break
						if deleteIndex != None:
							targetItem = DATA_PLAYER.inventoryList[deleteIndex]
							DATA_PLAYER.currentWeight -= targetItem.getWeight()
							del DATA_PLAYER.inventoryList[deleteIndex]
					
					elif self.currentLoc == "Room Container":
						targetContainerIndex = None
						targetItemIndex = 0
						breakCheck = False
						for cNum, tempContainer in enumerate(parentRoom.itemList):
							if tempContainer.type == "Container" and "Container List" in tempContainer.flags and len(tempContainer.flags["Container List"]) > 0:
								for iNum, tempContainerItem in enumerate(tempContainer.flags["Container List"]):
									if tempContainerItem == self:
										targetContainerIndex = cNum
										targetItemIndex = iNum
										breakCheck = True
										break
								if breakCheck : break
						if targetContainerIndex != None and targetItemIndex != None:
							parentRoom.itemList[targetContainerIndex].flags["Container Current Weight"] -= tempContainerItem.getWeight()
							del parentRoom.itemList[targetContainerIndex].flags["Container List"][targetItemIndex]
						
					elif self.currentLoc == "Player Container":
						targetContainerIndex = None
						targetItemIndex = 0
						for cNum, tempContainer in enumerate(DATA_PLAYER.inventoryList):
							if tempContainer.type == "Container" and "Container List" in tempContainer.flags and len(tempContainer.flags["Container List"]) > 0:
								for iNum, tempContainerItem in enumerate(tempContainer.flags["Container List"]):
									if tempContainerItem == self:
										targetContainerIndex = cNum
										targetItemIndex = iNum
										breakCheck = True
										break
								if breakCheck : break
						if targetContainerIndex != None and targetItemIndex != None:
							DATA_PLAYER.currentWeight -= tempContainerItem.getWeight()
							DATA_PLAYER.inventoryList[targetContainerIndex].flags["Container Current Weight"] -= tempContainerItem.getWeight()
							del DATA_PLAYER.inventoryList[targetContainerIndex].flags["Container List"][targetItemIndex]
						
				# Decay Message #
				if UPDATE_TYPE == "Player" or (UPDATE_TYPE == "Default" and self.currentLoc == "Room" and not ("Planted" in self.flags and "Plant Stage" in self.flags and self.flags["Plant Stage"] == "Seed") and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self)):
					displayLineMod = ""
					if UPDATE_TYPE == "Player" : displayLineMod = " in your inventory"
					displayLine = self.defaultTitle + displayLineMod + " crumbles and turns to dust."
					Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
		
				# Update Draw Data #
				if self.currentLoc == "Player":
					Config.DRAW_SCREEN_DICT["Player Utility"] = True
					SIDESCREEN_PLAYER_UTILITY.updateDisplayItemList(self, "Remove")
				elif self.currentLoc == "Room":
					if self.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
					elif self.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
		
		if "Planted" in self.flags:
			self.updatePlantInGround(SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE, PARENT_PLANET, PARENT_AREA, TICK_SPEED, ITEM_IMAGE_DICT)
	
		return UPDATE_ITEM_DEL_LIST
	
	def updatePlantInGround(self, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_TYPE, PARENT_PLANET, PARENT_AREA, TICK_SPEED, ITEM_IMAGE_DICT):
	
		parentRoom = PARENT_AREA.roomDict[self.currentRoom]
		previousTitle = self.defaultTitle
		previousTitleColorCode = self.defaultTitleColorCode
					
		# Tick With Water During Rain #
		if parentRoom.wetCheck(PARENT_AREA, UPDATE_TYPE) and "Wilt Timer" in self.flags and self.flags["Wilt Timer"] > 0 and self.flags["Wilt Timer"] < Config.PLANT_MAX_LIQUID_TIMER[self.flags["Plant Type"]]:
			self.flags["Wilt Timer"] += TICK_SPEED
		
		# Plant & Fruit Growth #
		freezeTemp = Config.FREEZE_TEMP["Default"]
		if PARENT_PLANET != None : freezeTemp = Config.FREEZE_TEMP[PARENT_PLANET.atmosphereType]
		#if PARENT_AREA.currentTemperature > freezeTemp <- Needs to be added back in!
		if parentRoom.wetCheck(PARENT_AREA, UPDATE_TYPE) and not ("Wilt Timer" in self.flags and self.flags["Wilt Timer"] <= 0):
		
			# Stage Seed To Stage 1 - Seedling #
			if self.type == "Seed":
			
				self.flags["Germinate Timer"] -= TICK_SPEED
				if self.flags["Germinate Timer"] <= 0:
					
					self.setPlantStage(1, ITEM_IMAGE_DICT)
					
					if UPDATE_TYPE == "Default" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = self.defaultTitle + " sprouts out of the ground."
						Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
						
					parentRoom.itemList.append(self)
					
			# Stage 1 To Stage 2 - Sapling #
			elif self.flags["Plant Stage"] == 1 and ("Light" in parentRoom.flags or (PARENT_PLANET != None and PARENT_PLANET.nightCheck == False)):
			
				self.flags["Stage 1 Timer"] -= TICK_SPEED
				if self.flags["Stage 1 Timer"] <= 0:
					
					self.setPlantStage(2, ITEM_IMAGE_DICT)
					
					if UPDATE_TYPE == "Default" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = previousTitle + " grows into " + self.defaultTitle[0].lower() + self.defaultTitle[1::] + "."
						Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
			
			# Stage 2 To Stage 3 #
			elif self.flags["Plant Stage"] == 2 and ("Light" in parentRoom.flags or (PARENT_PLANET != None and PARENT_PLANET.nightCheck == False)):
			
				self.flags["Stage 2 Timer"] -= TICK_SPEED
				if self.flags["Stage 2 Timer"] <= 0:
					
					self.setPlantStage(3, ITEM_IMAGE_DICT)
					
					if UPDATE_TYPE == "Default" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = previousTitle + " grows into " + self.defaultTitle[0].lower() + self.defaultTitle[1::] + "."
						Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
				
			# Stage 3 - Generate Fruit Blossoms #
			if self.flags["Plant Stage"] == 3 and ("Light" in parentRoom.flags or (PARENT_PLANET != None and PARENT_PLANET.nightCheck == False)) and "Blossom Timer" not in self.flags and "Unripe Fruit Timer" not in self.flags:
				if "Fruit List" not in self.flags or len(self.flags["Fruit List"]) < 10:
					if random.randrange(0, (100 / TICK_SPEED)) == 0:
						self.flags["Blossom Timer"] = Config.PLANT_TIMER["Blossom"]
						if self.flags["Plant Type"] == "Flower" : self.flags["Blossom Timer"] += 500
						
						if UPDATE_TYPE == "Default" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
							fruitName = self.flags["Plant Name"]
							if "Fruit Name" in self.flags : fruitName = self.flags["Fruit Name"]
							displayLine = fruitName + " blossoms start to grow on " + self.defaultTitle + "."
							Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
				
			# Stage 3 - Blossoms To Unripe Fruit/Seeds #
			if "Blossom Timer" in self.flags and ("Light" in parentRoom.flags or (PARENT_PLANET != None and PARENT_PLANET.nightCheck == False)):
				self.flags["Blossom Timer"] -= TICK_SPEED
				if self.flags["Blossom Timer"] <= 0:
					
					if UPDATE_TYPE == "Default" and self.flags["Plant Type"] in ["Root", "Flower"] and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = "Blossoms fall from " + self.defaultTitle + "."
						Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
					
					if self.flags["Fruit Num"] != None:
						self.flags["Unripe Fruit Timer"] = Config.PLANT_TIMER["Unripe"] - abs(self.flags["Blossom Timer"])
						
						if UPDATE_TYPE == "Default" and self.flags["Plant Type"] != "Root" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
							fruitName = self.flags["Plant Name"]
							if "Fruit Name" in self.flags : fruitName = self.flags["Fruit Name"]
							displayLine = "Small " + fruitName + "s start growing on " + self.defaultTitle + "."
							Console.addDisplayLineToDictList(displayLine, None, {"Stack Line":True})
							
					del self.flags["Blossom Timer"]
		
			# Stage 3 - Unripe Fruit To Ripe Fruit/Seeds #
			if "Unripe Fruit Timer" in self.flags and ("Light" in parentRoom.flags or (PARENT_PLANET != None and PARENT_PLANET.nightCheck == False)):	
				self.flags["Unripe Fruit Timer"] -= TICK_SPEED
				if self.flags["Unripe Fruit Timer"] <= 0:
					
					if self.flags["Plant Type"] != "Root" and "Fall Off Vine Timer" not in self.flags:
						self.flags["Fall Off Vine Timer"] = Config.PLANT_TIMER["Fall Off Vine"] - abs(self.flags["Unripe Fruit Timer"])
					del self.flags["Unripe Fruit Timer"]
					
					growCount = 5
					if self.flags["Plant Type"] == "Root":
						growCount = random.randrange(15, 20)
					for fNum in range(growCount):
						if self.flags["Fruit Num"] == "Default":
							fruitName = self.flags["Plant Name"]
							if "Fruit Name" in self.flags : fruitName = self.flags["Fruit Name"]
							fruitType = "Fruit"
							if "Fruit Type" in self.flags : fruitType = self.flags["Fruit Type"]
							targetFruitFlags = {"Parent ID Num":self.idNum, "Fruit Type":fruitType, "Fruit Name":fruitName, "Fruit Num":self.flags["Fruit Num"]}
							if fruitType == "Seed":
								targetFruitFlags["Plant Name"] = self.flags["Plant Name"]
								targetFruitFlags["Plant Type"] = self.flags["Plant Type"]
							targetFruit = loadPrefab(-1, targetFruitFlags)
						else:
							targetFruit = loadPrefab(self.flags["Fruit Num"])
						targetFruit.currentSolarSystem = self.currentSolarSystem
						targetFruit.currentPlanet = self.currentPlanet
						targetFruit.currentArea = self.currentArea
						targetFruit.currentRoom = self.currentRoom
						targetFruit.currentLoc = "Room"
						self.flags["Fruit List"].append(targetFruit)
						
					if UPDATE_TYPE == "Default" and self.flags["Plant Type"] != "Root" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						displayLine = targetFruit.defaultTitle+" ripens on "+self.defaultTitle+"."
						Console.addDisplayLineToDictList(displayLine, str(len(displayLine))+"w", {"Count Mod":growCount, "Stack Line":True})
		
		# Fruit Fall Off Vine Timer #
		if "Fall Off Vine Timer" in self.flags:
			self.flags["Fall Off Vine Timer"] -= TICK_SPEED
			if self.flags["Fall Off Vine Timer"] <= 0:
				
				# Add Ripe Fruit To Room ItemList & UpdateItemList & Delete From Plant Fruit List #
				if "Fruit List" in self.flags and len(self.flags["Fruit List"]) > 0:
					maxFallCount = len(self.flags["Fruit List"])
					if maxFallCount > 1 : maxFallCount /= 2
					fallOffVineCount = random.randrange(1, maxFallCount + 1)
					for fNum in range(fallOffVineCount):
						tempFruit = self.flags["Fruit List"][fNum]
						if self.currentLoc == "Room":
							parentRoom.addItem(tempFruit, DATA_PLAYER)
					for fNum in range(fallOffVineCount):
						del self.flags["Fruit List"][0]
						
					if len(self.flags["Fruit List"]) > 0:
						self.flags["Fall Off Vine Timer"] = Config.PLANT_TIMER["Fall Off Vine"] - abs(self.flags["Fall Off Vine Timer"])
						
					if UPDATE_TYPE == "Player" or (UPDATE_TYPE == "Default" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self)):
						displayLine = tempFruit.defaultTitle+" falls off the vine."
						Console.addDisplayLineToDictList(displayLine, str(len(displayLine))+"w", {"Count Mod":fallOffVineCount, "Stack Line":True})
						
				del self.flags["Fall Off Vine Timer"]
		
	# Getters & Setters #
	def getWeight(self):
	
		totalWeight = self.weight
		
		if self.type == "Container" and "Container List" in self.flags:
			for containerItem in self.flags["Container List"]:
				totalWeight += containerItem.getWeight()
				
		if "Fruit List" in self.flags:
			for fruitItem in self.flags["Fruit List"]:
				totalWeight += fruitItem.getWeight()
				
		if self.type == "Weapon" and self.flags["Weapon Type"] == "Ranged" and self.flags["Loaded Ammo Object"] != None and self.flags["Loaded Ammo Object"].flags["Quantity"] > 0:
			totalWeight += (self.flags["Loaded Ammo Object"].getWeight() * self.flags["Loaded Ammo Object"].flags["Quantity"])
		
		if "Quantity" in self.flags and self.flags["Quantity"] > 1:
			totalWeight = self.weight * self.flags["Quantity"]
		
		return totalWeight
	
	def userExamine(self):
	
		Console.addDisplayLineToDictList(self.lookTitle, self.lookTitleColorCode)
		
		# Control Panel Description #
		Console.addDisplayLineToDictList("There are flashing lights and buttons on the Panel.", "50w1y")
		#for panelButton in self.flags["Button List"]:
		#	Console.addDisplayLineToDictList("There is a button labled \"" + panelButton["Button Label"] + "\".", "25w1y" + str(len(panelButton["Button Label"])) + "w2y")
	
		# Container Description #
		if self.type == "Container":
			if "Container Status" in self.flags and self.flags["Container Status"] in ["Closed", "Locked"]:
				Console.addDisplayLineToDictList("It is closed.", "12w1y")
			elif "Container List" in self.flags:
				displayList = []
				for containerItem in self.flags["Container List"]:
					inDisplayDict = False
					for displayDict in displayList:
						if displayDict["ID_NUM"] == containerItem.idNum:
							inDisplayDict = True
							displayDict["Count"] += 1
							break
					if inDisplayDict == False:
						containerItemCount = 1
						if "Quantity" in containerItem.flags and containerItem.flags["Quantity"] > 1 : containerItemCount = containerItem.flags["Quantity"]
						displayList.append({"ID_NUM":containerItem.idNum, "Count":containerItemCount, "Default Title":containerItem.defaultTitle})
					
				if len(displayList) == 0:
					Console.addDisplayLineToDictList("It is empty.", "11w1y")
				else:
					STR_LINE = "It contains "
					for iNum, displayItemDict in enumerate(displayList):
						STR_LINE = STR_LINE + str(displayItemDict["Count"]) + " "
						gatherItemTitle = displayItemDict["Default Title"]
						if len(gatherItemTitle.split()) > 1 and gatherItemTitle.split()[0] in ["A", "An"]:
							gatherItemTitle = ' '.join(gatherItemTitle.split()[1::])
						STR_LINE = STR_LINE + gatherItemTitle
						if displayItemDict["Count"] > 1 : STR_LINE = STR_LINE + "s"
							
						if len(displayList) > 2 and iNum+1 < len(displayList) : STR_LINE = STR_LINE + ", "
						if iNum+2 == len(displayList) : STR_LINE = STR_LINE + " and "
					STR_LINE = STR_LINE + "."
					Console.addDisplayLineToDictList(STR_LINE)
		
		# Timer Description #
		if True:
			if "Wilt Timer" in self.flags and self.flags["Wilt Timer"] <= 0:
				Console.addDisplayLineToDictList("It is wilted.", "12w1y")
			elif "Blossom Timer" in self.flags:
				Console.addDisplayLineToDictList("It is covered in blossoms.", "25w1y")
			elif "Unripe Fruit Timer" in self.flags:
				Console.addDisplayLineToDictList("There is unripe fruit on the vine.", "33w1y")
				
		# Plant Description #
		if self.type == "Plant" and self.flags["Plant Type"] != "Root" and "Fruit List" in self.flags and len(self.flags["Fruit List"]) > 0:
			targetFruit = self.flags["Fruit List"][0]
			displayLine = targetFruit.defaultTitle + " is on the vine."
			Console.addDisplayLineToDictList(displayLine, str(len(displayLine))+"w", {"Count Mod":len(self.flags["Fruit List"])})
	
	# Utility Functions #
	def unloadRangedWeapon(self, DATA_PLAYER=None):
	
		# Unload Checks #
		messageType = None
		if self.flags["Loaded Ammo Object"] == None : messageType = "Already Unloaded"
	
		# Unload Weapon #
		if messageType == None:
	
			# Add Old Ammo To Player Inventory #
			if self.flags["Loaded Ammo Object"].flags["Quantity"] > 0 and DATA_PLAYER != None:
				targetAmmo = self.flags["Loaded Ammo Object"]
				tempIndex = -1
				for tempIndex, tempItem in enumerate(DATA_PLAYER.inventoryList):
					if tempItem.type == "Ammo" and tempItem.idNum == targetAmmo.idNum:
						targetAmmoIndex = tempIndex
						break
				
				if tempIndex != -1 : DATA_PLAYER.inventoryList[tempIndex].flags["Quantity"] += self.flags["Loaded Ammo Object"].flags["Quantity"]
				else : DATA_PLAYER.inventoryList.append(targetAmmo)
				
			# Reset Ammo Object Data #
			self.flags["Loaded Ammo Object"] = None
			messageType = "Unload Weapon"
			
		return messageType
		
	def isUpdateItem(self):
	
		updateItemCheck = False
		
		if "Wilt Timer" in self.flags or "Decay Timer" in self.flags or "Learn Timer" in self.flags:
			updateItemCheck = True
		
		return updateItemCheck
		
	def reloadWeapon(self, DATA_ATTACKER, TARGET_AMMO):
	
		# Get Data #
		if True:
			targetAmmo = None
			targetAmmoIndex = -1
			messageType = None
	
		# Get Target Ammo - Check If Target Ammo Is In Attacker's Inventory #
		for tempIndex, tempItem in enumerate(DATA_ATTACKER.inventoryList):
			if tempItem.type == "Ammo" and tempItem.idNum == TARGET_AMMO.idNum:
				targetAmmo = tempItem
				targetAmmoIndex = tempIndex
				break
		
		# Reload Checks #
		if targetAmmo == None and targetAmmoIndex == -1 : messageType = "Ammo Not Found"
		elif self.flags["Loaded Ammo Object"] != None and self.flags["Loaded Ammo Object"].idNum == targetAmmo.idNum and self.flags["Loaded Ammo Object"].flags["Quantity"] >= self.flags["Magazine Size"] : messageType = "Magazine Already Full"
		
		# Reload Weapon #
		if messageType == None:
			
			# Unload Different Ammo Into Attacker Inventory #
			if self.flags["Loaded Ammo Object"] != None and self.flags["Loaded Ammo Object"].idNum != targetAmmo.idNum and self.flags["Loaded Ammo Object"].flags["Quantity"] > 0:
				ammoInInvCheck = False
				for tempIndex, tempItem in enumerate(DATA_ATTACKER.inventoryList):
					if tempItem.idNum == self.flags["Loaded Ammo Object"].idNum:
						DATA_ATTACKER.inventoryList[tempIndex].flags["Quantity"] += self.flags["Loaded Ammo Object"].flags["Quantity"]
						ammoInInvCheck = True
						break
				if not ammoInInvCheck:
					tempAmmo = loadPrefab(self.flags["Loaded Ammo Object"].idNum)
					tempAmmo.flags["Quantity"] = self.flags["Loaded Ammo Count"]
					DATA_ATTACKER.addItemToInventory(tempAmmo, False)
				self.flags["Loaded Ammo Object"] = None
				
			# Load New Ammo #
			if True:
			
				# Get Reload Amount #
				if self.flags["Loaded Ammo Object"] == None : reloadAmount = self.flags["Magazine Size"]
				else : reloadAmount = self.flags["Magazine Size"] - self.flags["Loaded Ammo Object"].flags["Quantity"]
				if reloadAmount > targetAmmo.flags["Quantity"] : reloadAmount = targetAmmo.flags["Quantity"]
				
				# Put Ammo In Weapon #
				if self.flags["Loaded Ammo Object"] != None:
					self.flags["Loaded Ammo Object"].flags["Quantity"] += reloadAmount
				else:
					tempAmmo = loadPrefab(targetAmmo.idNum)
					tempAmmo.flags["Quantity"] = reloadAmount
					self.flags["Loaded Ammo Object"] = tempAmmo
					
				# Remove Ammo From Attacker Inventory #
				if DATA_ATTACKER.inventoryList[targetAmmoIndex].flags["Quantity"] > reloadAmount:
					DATA_ATTACKER.inventoryList[targetAmmoIndex].flags["Quantity"] -= reloadAmount
					DATA_ATTACKER.currentWeight -= (DATA_ATTACKER.inventoryList[targetAmmoIndex].weight * reloadAmount)
				else:
					targetDelAmmo = DATA_ATTACKER.inventoryList[targetAmmoIndex]
					DATA_ATTACKER.removeItemFromInventory(targetDelAmmo, False)
					
		# Messages #
		if messageType != None and DATA_ATTACKER.objectType == "Player":
			if messageType == "Ammo Not Found":
				Console.addDisplayLineToDictList("You don't have ammo.")
			elif messageType == "Magazine Already Full":
				Console.addDisplayLineToDictList("The magazine is full.")

	def getTargetControlPanelButton(self, STR_TARGET):
	
		targetButtonDict = None
		
		if "Button List" in self.flags and len(self.flags["Button List"]) > 0:
			for tempButtonDict in self.flags["Button List"]:
				if "Key List" in tempButtonDict and STR_TARGET in tempButtonDict["Key List"]:
					targetButtonDict = tempButtonDict
					break
		
		return targetButtonDict

	def setPlantStage(self, TARGET_STAGE, ITEM_IMAGE_DICT):
		
		if self.type == "Seed" and self.flags["Plant Type"] != "Root":
			self.flags["Wilt Timer"] = Config.PLANT_MAX_LIQUID_TIMER[self.flags["Plant Type"]]
		
		# Stage Seed To Stage 1 - Seedling #
		if TARGET_STAGE == 1 and self.type == "Seed":
			germinateTimer = 0
			if "Germinate Timer" in self.flags : germinateTimer = self.flags["Germinate Timer"]
			self.flags["Stage 1 Timer"] = Config.PLANT_STAGE_TIMER[self.flags["Plant Type"]] - abs(germinateTimer)
			self.flags["Plant Stage"] = 1
			
			plantName = self.flags["Plant Name"]
			plantType = self.flags["Plant Type"]
			stringPrefix = "A "
			if "A/An Check" in self.flags : stringPrefix = self.flags["A/An Check"] + " "
			
			self.idNum = self.flags["ID Num"] + 100000
			self.defaultTitle = stringPrefix + plantName + " " + plantType + " Seedling"
			self.defaultTitleColorCode = str(len(self.defaultTitle)) + "w"
			self.roomTitle = stringPrefix + plantName + " " + plantType + " Seedling is on the ground."
			self.roomTitleColorCode = str(len(self.roomTitle)) + "w"
			self.keyList = Utility.createKeyList(self.defaultTitle)
			self.idImage = self.flags["Plant Type"]
			
		# Stage 1 To Stage 2 - Sapling #
		elif TARGET_STAGE == 2:
			stage1Timer = 0
			if "Stage 1 Timer" in self.flags : stage1Timer = self.flags["Stage 1 Timer"]
			self.flags["Stage 2 Timer"] = Config.PLANT_STAGE_TIMER[self.flags["Plant Type"]] - abs(stage1Timer)
			self.flags["Plant Stage"] = 2
			if "Stage 1 Timer" in self.flags : del self.flags["Stage 1 Timer"]
			
			plantName = self.flags["Plant Name"]
			plantType = self.flags["Plant Type"]
			stringPrefix = "A "
			if "A/An Check" in self.flags : stringPrefix = self.flags["A/An Check"] + " "
			
			self.idNum = self.flags["ID Num"] + 20000
			self.defaultTitle = stringPrefix + plantName + " " + plantType + " Sapling"
			self.defaultTitleColorCode = str(len(self.defaultTitle)) + "w"
			self.roomTitle = stringPrefix + plantName + " " + plantType + " Sapling is planted in the ground."
			self.roomTitleColorCode = str(len(self.roomTitle)) + "w"
			self.keyList = Utility.createKeyList(self.defaultTitle)
			self.idImage = self.flags["Plant Type"]
			
		# Stage 2 To Stage 3 #
		elif TARGET_STAGE == 3:
			if "Stage 1 Timer" in self.flags : del self.flags["Stage 1 Timer"]
			if "Stage 2 Timer" in self.flags : del self.flags["Stage 2 Timer"]
			self.flags["Plant Stage"] = 3
			
			if self.flags["Plant Type"] not in ["Flower", "Root"] : self.flags["No Get"] = True
			if "Quantity" in self.flags : del self.flags["Quantity"]
			
			plantName = self.flags["Plant Name"]
			plantType = self.flags["Plant Type"]
			stringPrefix = "A "
			if "A/An Check" in self.flags : stringPrefix = self.flags["A/An Check"] + " "
			
			self.idNum = self.flags["ID Num"] + 30000
			self.defaultTitle = stringPrefix + plantName + " " + plantType
			self.defaultTitleColorCode = str(len(self.defaultTitle)) + "w"
			self.roomTitle = stringPrefix + plantName + " " + plantType + " is planted in the ground."
			self.roomTitleColorCode = str(len(self.roomTitle)) + "w"
			self.keyList = Utility.createKeyList(self.defaultTitle)
			self.idImage = self.flags["Plant Type"]
			
		# Update Item Data #
		self.type = "Plant"
		if "Germinate Timer" in self.flags : del self.flags["Germinate Timer"]
			
		# Update Image Data #
		if self.idImage in ITEM_IMAGE_DICT : itemImage = ITEM_IMAGE_DICT[self.idImage]
		else : itemImage = ITEM_IMAGE_DICT["Default"]
		self.loadImageData(itemImage)
			
def loadPrefab(ID_NUM, ITEM_IMAGE_DICT, FLAGS={}):

	item = LoadItem()
	item.flags["ID Num"] = ID_NUM
	tempKeyList = []
	
	if ID_NUM == -3: # Control Panel #
		item.idNum = ID_NUM
		item.loadControlPanel(FLAGS)
	
	elif ID_NUM == -2: # Corpse #
		mobData = None
		if "Mob Data" in FLAGS : mobData = FLAGS["Mob Data"]
		item.loadCorpse(mobData)
	
	elif ID_NUM == -1: # Default Fruit #
		if FLAGS["Fruit Type"] == "Seed":
			item.idNum = FLAGS["Parent ID Num"] - 120000
			seedFlags = {"Fruit Num":FLAGS["Fruit Num"]}
			if "Fruit Name" in FLAGS : seedFlags["Fruit Name"] = FLAGS["Fruit Name"]
			if "Fruit Type" in FLAGS : seedFlags["Fruit Type"] = FLAGS["Fruit Type"]
			item.loadSeed(FLAGS["Plant Name"], FLAGS["Plant Type"], seedFlags)
		elif FLAGS["Fruit Type"] == "Fruit":
			item.idNum = FLAGS["Parent ID Num"] + 100000
			fruitName = FLAGS["Fruit Name"]
			item.defaultTitle = "A " + fruitName
			item.defaultTitleColorCode = str(len(item.defaultTitle)) + "w"
			item.roomTitle = "A " + fruitName + " has been dropped on the ground."
			item.roomTitleColorCode = str(len(item.roomTitle)) + "w"
			item.flags["Wilt Timer"] = Config.ITEM_TIMER["Wilt"]
			item.flags["Produce Item On Decay"] = FLAGS["Parent ID Num"] - 120000
			item.flags["Edible"] = True
	
	elif ID_NUM == 0: # A Debug Item #
		item.idNum = ID_NUM
		item.defaultTitle = "A Debug Item"
		item.defaultTitleColorCode = "12w"
		item.roomTitle = "A debug item lies on the ground."
		item.roomTitleColorCode = "42w"
	
	elif ID_NUM == 1: # A Leather Helmet #
		item.idImage = "Helmet 1"
		item.idIcon = "Helmet"
		item.idNum = ID_NUM
		item.weight = 100
		item.value = 100
		item.physicalDefense = 5
		item.defaultTitle = "A Leather Helmet"
		item.defaultTitleColorCode = "2w1do6ddo7w"
		item.roomTitle = "A Leather Helmet has been dropped here."
		item.roomTitleColorCode = "2w1do6ddo7w22w1y"
		item.loadArmor("Head")
	
	elif ID_NUM == 2: # Leather Armor #
		item.idImage = "Armor 1"
		item.idIcon = "Armor"
		item.idNum = ID_NUM
		item.weight = 200
		item.value = 250
		item.physicalDefense = 17
		item.defaultTitle = "Leather Armor"
		item.defaultTitleColorCode = "1do6ddo6w"
		item.roomTitle = "Some Leather Armor is here collecting dust."
		item.roomTitleColorCode = "5w1do6ddo30w1y"
		item.loadArmor("Body")
	
	elif ID_NUM == 3: # An Iron Sword #
		item.idImage = "Sword 1"
		item.idIcon = "Sword"
		item.idNum = ID_NUM
		item.weight = 100
		item.value = 300
		item.defaultTitle = "An Iron Sword"
		item.defaultTitleColorCode = "3w1dw3ddw6w"
		item.roomTitle = "An Iron Sword has been left here."
		item.roomTitleColorCode = "3w1dw3ddw25w1y"
		item.loadWeapon("Sword", 5)
	
	elif ID_NUM == 4: # An Iron Helmet #
		item.idImage = "Helmet 2"
		item.idIcon = "Helmet"
		item.idNum = ID_NUM
		item.weight = 101
		item.value = 100
		item.physicalDefense = 15
		item.defaultTitle = "An Iron Helmet"
		item.defaultTitleColorCode = "3w1dw3ddw7w"
		item.roomTitle = "An Iron Helmet has been dropped here."
		item.roomTitleColorCode = "3w1dw3ddw29w1y"
		item.loadArmor("Head")
	
	elif ID_NUM == 5: # A Steel Sword #
		item.idImage = "Sword 2"
		item.idIcon = "Sword"
		item.idNum = ID_NUM
		item.weight = 300
		item.value = 300
		item.defaultTitle = "A Steel Sword"
		item.defaultTitleColorCode = "2w1dw4ddw6w"
		item.roomTitle = "A Steel Sword has been left here."
		item.roomTitleColorCode = "2w1dw4ddw25w1y"
		item.loadWeapon("Sword", 25)
	
	elif ID_NUM == 6: # An Ivory Pistol #
		item.idImage = "Gun 1"
		item.idNum = ID_NUM
		item.weight = 175
		item.value = 1250
		item.defaultTitle = "An Ivory Pistol"
		item.defaultTitleColorCode = "3w1dw5ddw1dw5ddw"
		item.roomTitle = "An Ivory Pistol has been dropped on the ground."
		item.roomTitleColorCode = "3w1dw5ddw1dw5ddw31w1y"
		item.loadWeapon("Ranged", 42, {"Weapon Range":2, "Ammo Type":"Pistol Ammo", "Attack Speed Ratio":1.60})
		
	elif ID_NUM == 7: # A Crossbow #
		item.idImage = "Bow 1"
		item.idIcon = "Bow"
		item.idNum = ID_NUM
		item.weight = 125
		item.value = 250
		item.defaultTitle = "A Crossbow"
		item.defaultTitleColorCode = "2w1do7ddo"
		item.roomTitle = "There is A Crossbow on the ground."
		item.roomTitleColorCode = "11w1do7ddo14w1y"
		item.loadWeapon("Ranged", 14, {"Two Handed":True, "Ammo Type":"Bolts", "Magazine Size":1, "Attack Speed Ratio":1.20, "Parry Bonus":10})
		
	elif ID_NUM == 8: # Unused #
		item.idNum = ID_NUM
	
	elif ID_NUM == 9: # Rusty Key - Code: 1234 #
		item.idImage = "Key 1"
		item.idNum = ID_NUM
		item.type = "Key"
		item.defaultTitle = "A Rusty Key"
		item.defaultTitleColorCode = "2w1do4ddo4w"
		item.roomTitle = "A Rusty Key is on the ground."
		item.roomTitleColorCode = "2w1do4ddo21w1y"
		item.flags["Key Num"] = 1234
	
	elif ID_NUM == 10: # A Chest - Code: 1234 #
		item.idImage = "Chest"
		item.idNum = ID_NUM
		item.defaultTitle = "A Chest"
		item.defaultTitleColorCode = "7w"
		item.roomTitle = "A Chest is here on the ground."
		item.roomTitleColorCode = "29w1y"
		item.loadContainer({"Closable":True, "Key Num":1234, "No Get":True})
	
	elif ID_NUM == 11: # A Bag #
		item.idImage = "Bag 1"
		item.idNum = ID_NUM
		item.defaultTitle = "A Bag"
		item.defaultTitleColorCode = "2w1do2ddo"
		item.roomTitle = "A Bag is here on the ground."
		item.roomTitleColorCode = "2w1do2ddo22w1y"
		item.loadContainer({"Container Max Weight":750})
	
	elif ID_NUM == 12: # Silver Keycard - Code: 12345 #
		item.idImage = "Key 2"
		item.idNum = ID_NUM
		item.type = "Key"
		tempKeyList = ["key", "card"]
		item.defaultTitle = "A Silver Keycard"
		item.defaultTitleColorCode = "2w1dw5ddw8w"
		item.roomTitle = "A Silver Keycard is on the ground."
		item.roomTitleColorCode = "2w1dw5ddw25w1y"
		item.flags["Key Num"] = 12345
	
	elif ID_NUM == 13: # An Acorn #
		item.idImage = "Seed"
		item.idNum = ID_NUM
		item.loadSeed("Oak", "Tree", {"Fruit Num":13,
									  "Fruit Name":"Acorn",
									  "A/An Check":"An"})
	
	elif ID_NUM == 14: # A Blackberry Seed #
		item.idImage = "Seed"
		item.idNum = ID_NUM
		item.weight = 500
		item.loadSeed("Blackberry", "Bush", {"Fruit Num":"Default"})
	
	elif ID_NUM == 15: # A Tomato Seed #
		item.idImage = "Seed"
		item.idNum = ID_NUM
		item.loadSeed("Tomato", "Plant", {"Fruit Num":"Default"})
	
	elif ID_NUM == 16: # A Tulip Seed #
		item.idImage = "Seed"
		item.idNum = ID_NUM
		item.loadSeed("Tulip", "Flower")
	
	elif ID_NUM == 17: # A Pinecone #
		item.idImage = "Seed"
		item.idNum = ID_NUM
		item.loadSeed("Pine", "Tree", {"Fruit Num":"Default",
									   "Fruit Name":"Pinecone",
									   "Fruit Type":"Seed"})
	
	elif ID_NUM == 18: # A Melon Seed #
		item.idImage = "Seed"
		item.idNum = ID_NUM
		item.loadSeed("Melon", "Vine", {"Fruit Num":"Default"})
	
	elif ID_NUM == 19: # A Canteen #
		item.idNum = ID_NUM
		item.defaultTitle = "A Canteen"
		item.defaultTitleColorCode = "2w1dw6ddw"
		item.roomTitle = "A Canteen has been dropped on the ground."
		item.roomTitleColorCode = "2w1dw6ddw31w1y"
		item.loadLiquidContainer()
	
	elif ID_NUM == 20: # A Fountain #
		item.idNum = ID_NUM
		item.type = "Fountain"
		item.defaultTitle = "A Fountain"
		item.defaultTitleColorCode = "2w1c7dw"
		item.roomTitle = "An endless flow of liquid streams from a Fountain here."
		item.roomTitleColorCode = "41w1c7dc5w1y"
		item.weight = 2000
		item.flags["No Get"] = True
		item.flags["Liquid Type"] = "Water"
	
	elif ID_NUM == 21: # A Potato #
		item.idImage = "Potato"
		item.idNum = ID_NUM
		item.weight = 1
		item.loadSeed("Potato", "Root", {"Fruit Num":21,
										 "Fruit Name":"Potato"})
	
	elif ID_NUM == 22: # Fire Materium #
		item.idNum = ID_NUM
		item.defaultTitle = "A Fire Materium"
		item.roomTitle = "A Fire Materium is on the ground."
		item.loadMaterium(1)
		
	elif ID_NUM == 23: # Attack All Materium #
		item.idNum = ID_NUM
		item.defaultTitle = "An Attack All Materium"
		item.roomTitle = "An Attack All Materium is on the ground."
		item.loadMaterium(2)
		
	elif ID_NUM == 24: # Bolts #
		item.idNum = ID_NUM
		item.weight = 1
		item.defaultTitle = "Bolts"
		item.defaultTitleColorCode = str(len(item.defaultTitle)) + "w"
		item.loadAmmo("Bolts", FLAGS)
		
	elif ID_NUM == 25: # Pistol Ammo #
		item.idNum = ID_NUM
		item.weight = 1
		item.defaultTitle = "Pistol Ammo"
		item.defaultTitleColorCode = str(len(item.defaultTitle)) + "w"
		item.loadAmmo("Pistol Ammo", FLAGS)
		
	elif ID_NUM == 26: # Basic Ammo #
		item.idNum = ID_NUM
		item.weight = 1
		item.defaultTitle = "Basic Ammo"
		item.defaultTitleColorCode = str(len(item.defaultTitle)) + "w"
		item.loadAmmo("Basic Ammo", FLAGS)
		
	elif ID_NUM == 27: # An Ebony Pistol #
		item.idImage = "Gun 2"
		item.idNum = ID_NUM
		item.weight = 175
		item.value = 1250
		item.defaultTitle = "An Ebony Pistol"
		item.defaultTitleColorCode = "3w1da5dda1da5dda"
		item.roomTitle = "An Ebony Pistol has been dropped on the ground."
		item.roomTitleColorCode = "3w1da5dda1da5dda31w1y"
		item.loadWeapon("Ranged", 50, {"Weapon Range":2, "Ammo Type":"Pistol Ammo", "Attack Speed Ratio":1.60})
		
	elif ID_NUM == 28: # Rocket Ammo #
		item.idNum = ID_NUM
		item.weight = 200
		item.defaultTitle = "Rocket Ammo"
		item.defaultTitleColorCode = str(len(item.defaultTitle)) + "w"
		item.loadAmmo("Rocket Ammo", FLAGS)
		
	elif ID_NUM == 29: # Firestorm Ammo #
		item.idNum = ID_NUM
		item.weight = 1
		item.defaultTitle = "Firestorm Ammo"
		item.defaultTitleColorCode = str(len(item.defaultTitle)) + "w"
		item.loadAmmo("Pistol Ammo", FLAGS)
		
	elif ID_NUM == 30: # A Silver Lance #
		item.idImage = "Spear 1"
		item.idIcon = "Spear"
		item.idNum = ID_NUM
		item.weight = 30
		item.value = 1000
		item.defaultTitle = "A Silver Lance"
		item.defaultTitleColorCode = "2w1dw11w"
		item.roomTitle = "A Silver Lance has been left here."
		item.roomTitleColorCode = "2w1dw30w1y"
		item.loadWeapon("Lance", 55)
		
	elif ID_NUM == 31: # A Silver Shield #
		item.idImage = "Shield 1"
		item.idIcon = "Shield"
		item.idNum = ID_NUM
		item.weight = 55
		item.value = 1000
		item.physicalDefense = 16
		item.defaultTitle = "A Silver Shield"
		item.defaultTitleColorCode = "2w1dw12w"
		item.roomTitle = "A Silver Shield has been dropped here."
		item.roomTitleColorCode = "2w1dw12w22w1y"
		item.loadWeapon("Shield", 10)
		
	elif ID_NUM == 32: # A Warhammer #
		item.idNum = ID_NUM
		item.weight = 120
		item.value = 500
		item.defaultTitle = "A Warhammer"
		item.defaultTitleColorCode = "2w1dw8w"
		item.roomTitle = "A Warhammer is lying on the floor."
		item.roomTitleColorCode = "2w1d8w22w1y"
		item.loadWeapon("Bludgeon", 100, {"Attack Speed Ratio":.40})
		
	elif ID_NUM == 33: # A Gold Shield #
		item.idImage = "Shield 2"
		item.idIcon = "Shield"
		item.idNum = ID_NUM
		item.weight = 35
		item.value = 10000
		item.physicalDefense = 26
		item.defaultTitle = "A Gold Shield"
		item.defaultTitleColorCode = "2w1dy3y7w"
		item.roomTitle = "A Gold Shield has been dropped here."
		item.roomTitleColorCode = "2w1dy3y29w1y"
		item.loadWeapon("Shield", 10)
		
	# Load Item Data #
	if True:
		
		# Quantity Data #
		if "Quantity" in FLAGS and "Quantity" in item.flags:
			item.flags["Quantity"] = FLAGS["Quantity"]
		
		# Load Keylist & Caption Data #
		item.keyList = Utility.createKeyList(item.defaultTitle)
		for tempKeyword in tempKeyList:
			if tempKeyword not in item.keyList : item.keyList.append(tempKeyword)
			
		roomTitleLength = len(item.roomTitle.split())
		item.roomTitleCaption = Caption.LoadCaption(0, roomTitleLength, "Get Item")
		
		# Load Area Rect & Image Data #
		itemImage = None
		if item.idImage in ITEM_IMAGE_DICT : itemImage = ITEM_IMAGE_DICT[item.idImage]
		elif item.type == "Container" and item.idImage == "Chest":
			if item.idImage + " Open" in ITEM_IMAGE_DICT : itemImage = ITEM_IMAGE_DICT[item.idImage + " Open"]
			if "Container Status" in item.flags and item.flags["Container Status"] in ["Closed", "Locked"]:
				if item.idImage + " Closed" in ITEM_IMAGE_DICT : itemImage = ITEM_IMAGE_DICT[item.idImage + " Closed"]
		else : itemImage = ITEM_IMAGE_DICT["Default"]
		if itemImage != None : item.loadImageData(itemImage)
		
	return item
		