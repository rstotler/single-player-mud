import pygame, random, Config, GameProcess, DataWorld, DataCombat, DataItem, DataSkill, DataAttack
from Elements import Console
from pygame import *

class LoadPlayer:
	
	def __init__(self):
	
		# ID Variables #
		self.objectType = "Player"
		self.currentSolarSystem = "Sol"
		self.currentPlanet = "Center Of The Universe"
		self.currentArea = "COTU Spaceport"
		self.currentAreaRandom = None
		self.currentRoom = 1
		self.flags = {}
		
		# Player Variables #
		self.level = 1
		self.currentWeight = 0
		self.maxWeight = 1200
		self.maxHP = 250
		self.currentHP = self.maxHP / 2
		self.maxMP = 200
		self.currentMP = self.maxMP
		self.statDict = {"Strength":45, "Dexterity":20, "Agility":45, "Spirit":15}
		
		self.currentAction = None
		self.dominantHand = "Right"
		self.dualWieldCheck = True
		
		self.mobTargetList = []             # Mobs Targeted By The Player
		self.mobTargetPlayerCombatList = [] # Mobs Targeting The Player
		self.groupList = []
		
		self.inventoryList = []
		self.updateItemList = []
		self.gearDict = {"Head":None,
						 "Amulet":None,
						 "Ring":None,
						 "Body":None,
						 "Legs":None,
						 "Feet":None,
						 "Left Hand":None,
						 "Right Hand":None}
		self.skillTreeDict = {}
		
		# Image & Rect Variables #
		self.idImage = "Player"
		self.rectArea = pygame.Rect([700, 145, 45, 65])
		self.imageSize = [49, 68]
		self.animationDict = {}
		
	def loadNewPlayer(self, ITEM_IMAGE_DICT):

		# Reset Variables #
		self.currentAction = None
		self.currentWeight = 0
		self.inventoryList = []
		self.skillTreeDict = {}
		
		# Load Starting Skills #
		self.learnSkillset("Basic Combat")
		self.learnSkillset("Advanced Combat")
		self.learnSkillset("Basic Magic")
		self.learnSkillset("Advanced Magic")
		self.learnSkillset("General Skills")
		
		# Load Starting Items #
		playerBag = DataItem.loadPrefab(11, ITEM_IMAGE_DICT)
		self.addItemToContainer(playerBag, DataItem.loadPrefab(9, ITEM_IMAGE_DICT))  # Key - 1234 #
		self.addItemToContainer(playerBag, DataItem.loadPrefab(12, ITEM_IMAGE_DICT)) # Key - 12345 #
		self.addItemToInventory(playerBag)
		self.addItemToInventory(DataItem.loadPrefab(3, ITEM_IMAGE_DICT))  # An Iron Sword #
		self.addItemToInventory(DataItem.loadPrefab(6, ITEM_IMAGE_DICT))  # An Ivory Pistol #
		self.addItemToInventory(DataItem.loadPrefab(27, ITEM_IMAGE_DICT)) # An Ebony Pistol  #
		self.addItemToInventory(DataItem.loadPrefab(7, ITEM_IMAGE_DICT))  # A Crossbow #
		self.addItemToInventory(DataItem.loadPrefab(30, ITEM_IMAGE_DICT)) # Silver Lance #
		for i in range(5) : self.addItemToInventory(DataItem.loadPrefab(19, ITEM_IMAGE_DICT))  # Canteen #
		for i in range(10) : self.addItemToInventory(DataItem.loadPrefab(21, ITEM_IMAGE_DICT)) # Potato #
	
	def killPlayer(self, PLAYER_SOLAR_SYSTEM):
	
		# Reset Location #
		self.currentSolarSystem = "Sol"
		self.currentPlanet = "Center Of The Universe"
		self.currentArea = "COTU Spaceport"
		self.currentAreaRandom = None
		self.currentRoom = 1
		
		self.currentAction = None
		self.mobTargetList = []
		self.mobTargetPlayerCombatList = []
		
		self.currentHP = self.maxHP
		
		# Reset Group List #
		if len(self.groupList) > 0:
			for groupMember in self.groupList : groupMember.groupList = []
			self.groupList = []
		if "Group Leader" in self.flags : del self.flags["Group Leader"]
		
		Console.addDisplayLineToDictList("You wake up in a familiar place feeling refreshed.")
		
		# Draw Screen #
		if True:
			Config.DRAW_SCREEN_DICT["Map"] = True
			if "Room" in Config.DRAW_SCREEN_DICT and "All" not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append("All")
			elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = ["All"]
			
	# Update Functions #
	def update(self, SOLAR_SYSTEM_DICT, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT):

		# Update Items #
		if True:
			updateItemDelList = []
			updateItemPlanet = None
			if "In Spaceship" not in self.flags : updateItemPlanet = SOLAR_SYSTEM_DICT[self.currentSolarSystem].planetDict[self.currentPlanet]
			parentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[self.currentSolarSystem], self)
			
			for iNum, targetItem in enumerate(self.updateItemList):
				updateItemDelList = targetItem.update(SOLAR_SYSTEM_DICT, iNum, self, "Player", updateItemPlanet, parentArea, updateItemDelList, 1, SIDESCREEN_PLAYER_UTILITY, ITEM_IMAGE_DICT)
			updateItemDelList.reverse()
			for updateItemDelIndex in updateItemDelList:
				del self.updateItemList[updateItemDelIndex]
			
		# Area Sound Message #
		if "Area Sound Cooldown Timer" in self.flags:
			self.flags["Area Sound Cooldown Timer"] -= 1
			if self.flags["Area Sound Cooldown Timer"] <= 0:
				del self.flags["Area Sound Cooldown Timer"]
		elif random.randrange(0, 800) == 0:
			parentArea.roomDict[self.currentRoom].displayAreaText(parentArea)
			self.flags["Area Sound Cooldown Timer"] = 1000
	
	# Getters & Setters #
	def displayInventory(self):

		displayList = []
		for item in self.inventoryList:
			itemInList = False
			for displayItem in displayList:
				if displayItem["Item Data"].idNum == item.idNum:
					displayItem["Count"] += 1
					itemInList = True
					break
			if itemInList == False:
				itemCount = 1
				if "Quantity" in item.flags and item.flags["Quantity"] > 1 : itemCount = item.flags["Quantity"]
				displayList.append({"Item Data":item, "Count":itemCount})
				
		Console.addDisplayLineToDictList("You are carrying:", "16w1y")
		if len(displayList) == 0:
			Console.addDisplayLineToDictList("Nothing.", "7w1y")
		
		for displayItem in displayList:
			invString = displayItem["Item Data"].defaultTitle
			invColorCode = displayItem["Item Data"].defaultTitleColorCode
			Console.addDisplayLineToDictList(invString, invColorCode, {"Count Mod":displayItem["Count"]})

	def displayGear(self):
		
		Console.addDisplayLineToDictList("You are wearing:", "15w1y")
		
		for gearSlot in ["Head", "Amulet", "Ring", "Body", "Feet", "Left Hand", "Right Hand"]:
			if gearSlot in self.gearDict:
				strLine = "[" + gearSlot + "] "
				colorCode = "1r" + str(len(gearSlot)) + "w2r"
				if self.gearDict[gearSlot] != None:
					strLine = strLine + self.gearDict[gearSlot].defaultTitle
					colorCode = colorCode + self.gearDict[gearSlot].defaultTitleColorCode
					
					# Ranged Ammo List #
					if gearSlot in ["Left Hand", "Right Hand"] and self.gearDict[gearSlot].type == "Weapon" and self.gearDict[gearSlot].flags["Weapon Type"] == "Ranged":
						loadedAmmoCount = 0
						if self.gearDict[gearSlot].flags["Loaded Ammo Object"] != None : loadedAmmoCount = self.gearDict[gearSlot].flags["Loaded Ammo Object"].flags["Quantity"]
						strLine = strLine + " [" + str(loadedAmmoCount) + "/" + str(self.gearDict[gearSlot].flags["Magazine Size"]) + "]"
						colorCode = colorCode + "2r" + str(len(str(loadedAmmoCount))) + "w1r" + str(len(str(self.gearDict[gearSlot].flags["Magazine Size"]))) + "w1r"
						
						# Ranged Ammo Type #
						if self.gearDict[gearSlot].flags["Loaded Ammo Object"] != None and self.gearDict[gearSlot].flags["Loaded Ammo Object"].flags["Quantity"] > 0:
							strLine = strLine + " [" + self.gearDict[gearSlot].flags["Loaded Ammo Object"].defaultTitle + "]"
							colorCode = colorCode + "2r" + str(len(self.gearDict[gearSlot].flags["Loaded Ammo Object"].defaultTitle)) + "w1r"
						
				else:
					strLine = strLine + "None"
					colorCode = colorCode + "4w"
				Console.addDisplayLineToDictList(strLine, colorCode)
	
	def displaySkills(self):
	
		if len(self.skillTreeDict) == 0:
			Console.addDisplayLineToDictList("No Skills Learned")
			
		else:
			for sNum, skillTreeType in enumerate(DataSkill.getMasterSkillTreeList()):
				if skillTreeType in self.skillTreeDict:
					Console.addDisplayLineToDictList("-" + skillTreeType + "-", "1r" + str(len(skillTreeType)) + "dw1r")
					displayString = ""
					displayColorCode = ""
					currentYLoc = 0
				
					for sIndex, skillId in enumerate(self.skillTreeDict[skillTreeType].skillDict):
						skillData = self.skillTreeDict[skillTreeType].skillDict[skillId]
						displayString = displayString + skillData.idSkill + " (" + str(skillData.learnPercent)[0:5] + ")"
						displayColorCode = displayColorCode + str(len(skillData.idSkill)) + "w2r" + str(len(str(skillData.learnPercent)[0:5])) + "w1r"
						
						if currentYLoc == 0:
							strBuffer = ""
							for i in range(20 - len(skillData.idSkill)) : strBuffer = strBuffer + " "
							displayString = displayString + strBuffer
							displayColorCode = displayColorCode + str(len(strBuffer)) + "w"
							currentYLoc = 1
						if sIndex % 2 == 1 or sIndex == len(self.skillTreeDict[skillTreeType].skillDict)-1:
							Console.addDisplayLineToDictList(displayString, displayColorCode, {"No Trim Check":True})
							displayString = ""
							displayColorCode = ""
							currentYLoc = 0
						
					if sNum != len(self.skillTreeDict)-1:
						Console.addDisplayLineToDictList("")
					
	def getViewRange(self):
	
        # For SAFETY PURPOSES The Player & Mobs View Distance Should Not Exceed Config.PLAYER_UPDATE_RANGE #
		return 3
	
	def getAttackRange(self):
	
		attackRange = 0
	
		targetHand = self.dominantHand + " Hand"
		if self.gearDict[targetHand] != None and "Weapon Range" in self.gearDict[targetHand].flags:
			weaponRange = self.gearDict[targetHand].flags["Weapon Range"]
			if weaponRange > attackRange : attackRange = weaponRange
		
		if self.dualWieldCheck and "Advanced Combat" in self.skillTreeDict and "Dual Wield" in self.skillTreeDict["Advanced Combat"].skillDict:
			if targetHand == "Left Hand" : otherHand = "Right Hand"
			else : otherHand = "Left Hand"
			
			if self.gearDict[otherHand] != None and "Weapon Range" in self.gearDict[otherHand].flags:
				weaponRange = self.gearDict[otherHand].flags["Weapon Range"]
				if weaponRange > attackRange : attackRange = weaponRange
		
		return attackRange
	
	def getCastRange(self):
	
		return 2
	
	def getSkillRange(self, DATA_ATTACK):
	
		skillRange = 0
		
		if DATA_ATTACK.rangeType == "Long":
			skillRange = 2
		
		return skillRange
	
	# Utility Functions #
	def addItemToInventory(self, TARGET_ITEM, ADD_WEIGHT=True):
	
		# Update Item Variables #
		if True:
			TARGET_ITEM.currentSolarSystem = self.currentSolarSystem
			TARGET_ITEM.currentPlanet = self.currentPlanet
			TARGET_ITEM.currentArea = self.currentArea
			TARGET_ITEM.currentAreaRandom = self.currentAreaRandom
			TARGET_ITEM.currentRoom = self.currentRoom
			TARGET_ITEM.currentLoc = "Player"
			if "In Spaceship" in self.flags : TARGET_ITEM.flags["In Spaceship"] = True
			
		# Add Item #
		if True:
			addCheck = False
			if "Quantity" in TARGET_ITEM.flags:
				inventoryIndex = -1
				for tempIndex, tempItem in enumerate(self.inventoryList):
					if "Quantity" in tempItem.flags and tempItem.idNum == TARGET_ITEM.idNum:
						inventoryIndex = tempIndex
						break
				if inventoryIndex != -1:
					self.inventoryList[inventoryIndex].flags["Quantity"] += TARGET_ITEM.flags["Quantity"]
					addCheck = True
			if not addCheck : self.inventoryList.append(TARGET_ITEM)
			
		# Adjust Weight #
		if ADD_WEIGHT:
			self.currentWeight += TARGET_ITEM.getWeight()
		
		if TARGET_ITEM.isUpdateItem():
			if TARGET_ITEM not in self.updateItemList:
				self.updateItemList.append(TARGET_ITEM)
			
	def addItemToContainer(self, TARGET_CONTAINER, TARGET_ITEM):
	
		# Update Item Variables #
		TARGET_ITEM.currentLoc = "Player Container"
		
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
					TARGET_CONTAINER.flags["Container Current Weight"] += TARGET_ITEM.getWeight()
					addCheck = True
			if not addCheck:
				TARGET_CONTAINER.flags["Container List"].append(TARGET_ITEM)
				TARGET_CONTAINER.flags["Container Current Weight"] += TARGET_ITEM.getWeight()
		
		# UpdateList Check #
		if TARGET_ITEM.isUpdateItem():
			if TARGET_ITEM not in self.updateItemList:
				self.updateItemList.append(TARGET_ITEM)
	
	def removeItemFromInventory(self, TARGET_ITEM, ADD_WEIGHT=True, REMOVE_UPDATE_LIST=True):
	
		# Inventory #
		if TARGET_ITEM in self.inventoryList:
			
			# Adjust Weight #
			if ADD_WEIGHT:
				if "Quantity" in TARGET_ITEM.flags and TARGET_ITEM.flags["Quantity"] > 1:
					self.currentWeight -= (TARGET_ITEM.flags["Quantity"] * TARGET_ITEM.weight)
				else : self.currentWeight -= TARGET_ITEM.getWeight()
		
			# Delete From Inventory #
			del self.inventoryList[self.inventoryList.index(TARGET_ITEM)]
	
		# Update List #
		if REMOVE_UPDATE_LIST and TARGET_ITEM in self.updateItemList:
			del self.updateItemList[self.updateItemList.index(TARGET_ITEM)]
			
	def updateMobsInView(self, SOLAR_SYSTEM_DICT):
	
		playerRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[self.currentSolarSystem], self).roomDict[self.currentRoom]
	
		# Remove Player Targets From Target List #
		playerTargetDelList = []
		playerTargetDelMessageList = []
		for mNum, tempMob in enumerate(self.mobTargetList):
			targetRange, targetDir, targetMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, tempMob, self.getViewRange())
			if targetMessage == "Door Is Closed" or targetRange == -1:
				playerTargetDelList.append(mNum)
				playerTargetDelMessageList.append("You lose sight of " + tempMob.defaultTitle + ".")
		if len(playerTargetDelList) > 0:
			playerTargetDelList.reverse()
			for mNum in playerTargetDelList : del self.mobTargetList[mNum]
			
		# Remove Action Of Mobs Targeting Player #
		mobTargetPlayerDelList = []
		for tempMob in self.mobTargetPlayerCombatList:
			if tempMob.currentAction != None and tempMob.currentAction["Type"] == "Attacking" and tempMob.combatTarget == None:
				targetRange, targetDir, targetMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, tempMob, tempMob.getViewRange())
				if targetMessage == "Door Is Closed" or targetRange == -1:
					tempMob.currentAction = None
		
		return playerTargetDelMessageList
			
	def learnSkillset(self, TARGET_SKILL_TREE):
	
		if TARGET_SKILL_TREE not in self.skillTreeDict:
			newSkillTree = DataSkill.LoadSkillTree(TARGET_SKILL_TREE)
			self.skillTreeDict[TARGET_SKILL_TREE] = newSkillTree
			
	def hasKey(self, KEY_NUM):
	
		keyCheck = False
		
		for item in self.inventoryList:
			
			if item.type == "Key" and "Key Num" in item.flags:
				if item.flags["Key Num"] == KEY_NUM:
					keyCheck = True
					break
			
			# Check Containers #
			elif item.type == "Container":
				for containerItem in item.flags["Container List"]:
					if containerItem.type == "Key" and "Key Num" in containerItem.flags:
						if containerItem.flags["Key Num"] == KEY_NUM:
							keyCheck = True
							break
			
		return keyCheck
	
	def getTargetSpellFromInputString(self, STR_TARGET_SPELL):
	
		targetSpellData = None
		breakCheck = False
		
		for skillTreeId in self.skillTreeDict:
			if skillTreeId in ["Basic Magic", "Advanced Magic"]:
				for skillId in self.skillTreeDict[skillTreeId].skillDict:
					tempAttackData = DataAttack.loadPrefab(skillId)
					if tempAttackData != None and STR_TARGET_SPELL in tempAttackData.keyList:
						targetSpellData = tempAttackData
						breakCheck = True
						break
			if breakCheck : break
		
		return targetSpellData
		
	def getTargetSkillFromInputString(self, STR_TARGET_SKILL):
	
		targetSkillData = None
		breakCheck = False
		
		for skillTreeId in self.skillTreeDict:
			if skillTreeId not in ["Basic Magic", "Advanced Magic"]:
				for skillId in self.skillTreeDict[skillTreeId].skillDict:
					tempSkillData = self.skillTreeDict[skillTreeId].skillDict[skillId]
					if tempSkillData != None and STR_TARGET_SKILL in tempSkillData.keyList:
						targetSkillData = tempSkillData
						breakCheck = True
						break
			if breakCheck : break
		
		return targetSkillData
		
# Shared Entity Functions (Player & Mob) #	
def getAttackPower(DATA_ATTACKER, DATA_ATTACK, TARGET_ATTACK_TYPE):

	# Get Data #
	if True:
		if DATA_ATTACKER.dominantHand == "Left" : strOffhand = "Right Hand"
		else : strOffhand = "Left Hand"
	
		totalDamage = 0
		totalWeaponDamage = 0
		if TARGET_ATTACK_TYPE == "Primary Attack" : heldWeapon = DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"]
		elif TARGET_ATTACK_TYPE == "Offhand Attack" : heldWeapon = DATA_ATTACKER.gearDict[strOffhand]
		weaponTargetSkill = DATA_ATTACKER.statDict["Strength"]
		if heldWeapon != None and heldWeapon.flags["Weapon Type"] == "Ranged" : weaponTargetSkill = DATA_ATTACKER.statDict["Dexterity"]
		
		totalSkillDamage = 0
		skillTargetSkill = DATA_ATTACKER.statDict["Strength"]
		if DATA_ATTACK.damageType == "Magic" : skillTargetSkill = DATA_ATTACKER.statDict["Spirit"]
		
	# Weapon Damage #
	if DATA_ATTACK.weaponDamage:
		heldWeaponDamage = 0
		if heldWeapon != None : heldWeaponDamage = heldWeapon.flags["Base Power"]
		totalWeaponDamage = heldWeaponDamage * (1 + (weaponTargetSkill / 10.0))

	# Skill Damage #
	if DATA_ATTACK.damageType in ["Physical", "Magic"]:
		totalSkillDamage = DATA_ATTACK.basePower * (1 + (skillTargetSkill / 10.0))
	elif DATA_ATTACK.damageType == "Both":
		totalSkillDamage = (((DATA_ATTACK.basePower * .5) * (1 + (DATA_ATTACKER.statDict["Strength"] / 10.0))) \
						  + ((DATA_ATTACK.basePower * .5) * (1 + (DATA_ATTACKER.statDict["Spirit"] / 10.0))))
						 
	# Total Damage #
	totalDamage = (totalWeaponDamage + totalSkillDamage)
	if DATA_ATTACK.damageType == "Physical" : totalDamage += DATA_ATTACKER.statDict["Strength"]
	elif DATA_ATTACK.damageType == "Magic" : totalDamage += DATA_ATTACKER.statDict["Spirit"]
	elif DATA_ATTACK.damageType == "Both" : totalDamage += ((DATA_ATTACKER.statDict["Strength"] * .5) + (DATA_ATTACKER.statDict["Spirit"] * .5))
	totalDamage = int(round(totalDamage * random.uniform(0.85, 1.15)))
	if totalDamage < 0 : totalDamage = 0
	
	return totalDamage
	
def getDefense(DATA_ENTITY):
	
	totalDefense = 0
	totalGearDefense = 0
	
	for gearSlot in DATA_ENTITY.gearDict:
		if DATA_ENTITY.gearDict[gearSlot] != None:
			totalGearDefense += DATA_ENTITY.gearDict[gearSlot].physicalDefense
	
	totalDefense = int(round((totalGearDefense * .7) * (1 + (DATA_ENTITY.statDict["Strength"] / 15))) \
						  + ((totalGearDefense * .3) * (1 + (DATA_ENTITY.statDict["Dexterity"] / 15))))
	
	return totalDefense
	
def getMagicDefense(DATA_ENTITY):

	totalMagicDefense = 0
	totalGearMagicDefense = 0
	
	for gearSlot in DATA_ENTITY.gearDict:
		if DATA_ENTITY.gearDict[gearSlot] != None:
			totalGearMagicDefense += DATA_ENTITY.gearDict[gearSlot].magicDefense
			
	totalMagicDefense = int(round((totalGearMagicDefense * .7) * (1 + (DATA_ENTITY.statDict["Spirit"] / 15))) \
							   + ((totalGearMagicDefense * .3) * (1 + (DATA_ENTITY.statDict["Dexterity"] / 15))))
	
	return totalMagicDefense
	