import pygame, random, Config, Utility, GameProcess, DataMain, DataWorld, DataSkill, DataItem, DataAttack
from Elements import Console, Caption
from pygame import *
	
class LoadMob:

	def __init__(self):
	
		# ID Variables #
		self.objectType = "Mob"
		self.type = "Mob"
		self.idNum = -1
		self.currentSolarSystem = "Sol"
		self.currentPlanet = "Center Of The Universe"
		self.currentArea = "COTU Spaceport"
		self.currentAreaRandom = None
		self.currentRoom = 1
		self.flags = {}
		
		# Mob Variables #
		self.currentWeight = 0
		self.maxWeight = 500
		self.currentHP = 10
		self.maxHP = 10
		self.currentMP = 100
		self.maxMP = 100
		self.statDict = {"Strength":10, "Dexterity":10, "Agility":10, "Spirit":10}
		
		self.currentAction = None
		self.dominantHand = "Right"
		self.dualWieldCheck = True
		
		self.combatTarget = None
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
		
		self.evolutionLevel = "Animal"
		self.lootDict = {}
		self.lootCount = 1
		
		# Image & Rect Variables #
		self.idImage = None
		self.rectArea = None
		self.imageSize = None
		self.animationDict = {}
		
		# Description Variables #
		if True:
			self.defaultTitle = "Default Mob"
			self.defaultTitleColorCode = "11w"
			self.roomTitle = "A default mob is here."
			self.roomTitleColorCode = "22w"
			self.roomTitleCaption = None
			self.lookTitle = "You see nothing special."
			self.lookTitleColorCode = "24w"
			self.keyList = []
	
	# Update Functions #
	def update(self, WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, ITEM_IMAGE_DICT):
		
		# Get Data #
		if True:
			parentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[self.currentSolarSystem], self)
			parentRoom = parentArea.roomDict[self.currentRoom]
			actionCheck = False
			
			distanceToPlayer = None
			directionToPlayer = None
			tempMessage = None
			if self in DATA_PLAYER.mobTargetPlayerCombatList:
				distanceToPlayer, directionToPlayer, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, parentRoom, DATA_PLAYER, self.getViewRange())
				
			distanceToTargetMob = None
			directionToTargetMob = None
			targetMobMessage = None
			if self.combatTarget != None:
				distanceToTargetMob, directionToTargetMob, targetMobMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, parentRoom, self.combatTarget, self.getViewRange())
		
		# Update Items #
		if True:
			updateItemDelList = []
			updateItemPlanet = None
			if "In Spaceship" not in self.flags : updateItemPlanet = SOLAR_SYSTEM_DICT[self.currentSolarSystem].planetDict[self.currentPlanet]
			
			for iNum, targetItem in enumerate(self.updateItemList):
				updateItemDelList = targetItem.update(SOLAR_SYSTEM_DICT, iNum, self, "Mob", updateItemPlanet, parentArea, updateItemDelList, 1, ITEM_IMAGE_DICT)
			updateItemDelList.reverse()
			for updateItemDelIndex in updateItemDelList:
				del self.updateItemList[updateItemDelIndex]
		
		# 1) Non-Combat Update Functions #
		if distanceToPlayer in [None, -1] and distanceToTargetMob in [None, -1]:
		
			# Heal Self #
			if actionCheck == False and self.currentAction == None and self.currentHP / (self.maxHP+0.0) <= .30:
				
				# Skill Available Check #
				healSkillIDList = []
				for skillTreeID in self.skillTreeDict:
					for targetSkillID in self.skillTreeDict[skillTreeID].skillDict:
						if (skillTreeID in ["Basic Magic", "Advanced Magic"] and targetSkillID.lower() in Config.SPELL_MASTER_KEY_LIST) or targetSkillID.lower() in Config.SKILL_MASTER_KEY_LIST:
							dataAttack = DataAttack.loadPrefab(targetSkillID)
							if dataAttack != None and dataAttack.effectType == "Heal" and self.currentMP >= dataAttack.mpCost and dataAttack.targetType == "Entity":
								healSkillIDList.append(targetSkillID)
					
				# Heal Self #
				if len(healSkillIDList) > 0:
					dataAttack = DataAttack.loadPrefab(random.choice(healSkillIDList))
					if dataAttack.effectType == "Heal":
						if dataAttack.targetType == "Entity" : dataAttack.currentCount = "Self"
						self.currentAction = {"Type":"Attacking", "Timer":dataAttack.attackTimer, "Attack Data":dataAttack}
						self.currentAction["Mob Target"] = "Mob"
						actionCheck = True
					
					# Messages #
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, self, DATA_PLAYER):
						if dataAttack.targetSkillTree in ["Basic Magic", "Advanced Magic"] : Console.addDisplayLineToDictList(self.defaultTitle + " begins casting a spell.")
						else : Console.addDisplayLineToDictList(self.defaultTitle + " prepares to attack!")

			# Reload Held Ranged Weapons (If Empty) #
			if actionCheck == False and self.currentAction == None and (self.gearDict["Left Hand"] != None or self.gearDict["Right Hand"] != None):
			
				# Get Data #
				if True:
					if self.dominantHand == "Left" : strOtherHand = "Right Hand"
					else : strOtherHand = "Left Hand"
					targetWeapon = None
					targetAmmo = None
					
					# Get Target Ranged Weapon #
					if self.gearDict[self.dominantHand + " Hand"] != None and self.gearDict[self.dominantHand + " Hand"].flags["Weapon Type"] == "Ranged" and (self.gearDict[self.dominantHand + " Hand"].flags["Loaded Ammo Object"] == None or self.gearDict[self.dominantHand + " Hand"].flags["Loaded Ammo Object"].flags["Quantity"] == 0):
						targetWeapon = self.gearDict[self.dominantHand + " Hand"]
					elif self.gearDict[strOtherHand] != None and self.gearDict[strOtherHand].flags["Weapon Type"] == "Ranged" and (self.gearDict[strOtherHand].flags["Loaded Ammo Object"] == None or self.gearDict[strOtherHand].flags["Loaded Ammo Object"].flags["Quantity"] == 0):
						targetWeapon = self.gearDict[strOtherHand]
						
					# Get Target Ammo #
					if targetWeapon != None:
						for tempItem in self.inventoryList:
							if tempItem.type == "Ammo" and tempItem.flags["Ammo Type"] == targetWeapon.flags["Ammo Type"]:
								targetAmmo = tempItem
								break
						
				# Reload #
				if targetWeapon != None and targetAmmo != None:
				
					# Get Reload Amount #
					if targetWeapon.flags["Loaded Ammo Object"] == None : reloadAmount = targetWeapon.flags["Magazine Size"]
					else : reloadAmount = targetWeapon.flags["Magazine Size"] - targetWeapon.flags["Loaded Ammo Object"].flags["Quantity"]
					if reloadAmount > targetAmmo.flags["Quantity"] : reloadAmount = targetAmmo.flags["Quantity"]
					reloadTime = reloadAmount * targetAmmo.flags["Reload Time"]
					
					self.currentAction = {"Type":"Reloading", "Timer":reloadTime, "Target Weapon":targetWeapon, "Target Ammo":targetAmmo}
					actionCheck = True
					
					# Messages #
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, self, DATA_PLAYER):
						Console.addDisplayLineToDictList(self.defaultTitle + " begins reloading " + targetWeapon.defaultTitle + ".")
			
			# Autowear Gear #
			if actionCheck == False and self.currentAction == None and "Autowear Gear" in self.flags and len(self.inventoryList) > 0:
			
				# Get Data #
				if True:
					targetGearSlot = None
					targetWearItem = None
					mobAmmoTypeList = []
					wearCheck = True
					
					if self.dominantHand == "Left" : strOtherHand = "Right Hand"
					else : strOtherHand = "Left Hand"
					
					# Get Ammo Type List #
					for tempItem in self.inventoryList:
						if tempItem.type == "Ammo" and tempItem.flags["Ammo Type"] not in mobAmmoTypeList:
							mobAmmoTypeList.append(tempItem.flags["Ammo Type"])
					
				# Get Target Gear Slot And Target Wear Item #
				for tempWearItem in self.inventoryList:
					if tempWearItem.type in ["Armor", "Weapon"]:
						
						# Get Target Gear Slot #
						if tempWearItem.type == "Armor" and self.gearDict[tempWearItem.flags["Gear Slot"]] == None:
							targetGearSlot = tempWearItem.flags["Gear Slot"]
						elif tempWearItem.type == "Weapon":
							if self.gearDict[self.dominantHand+" Hand"] == None : targetGearSlot = self.dominantHand + " Hand"
							elif (self.dualWieldCheck and ("Advanced Combat" in self.skillTreeDict and "Dual Wield" in self.skillTreeDict["Advanced Combat"].skillDict)) \
							and self.gearDict[strOtherHand] == None : targetGearSlot = strOtherHand
							
						# Get Target Wear Item #
						if targetGearSlot != None and targetGearSlot in self.gearDict and self.gearDict[targetGearSlot] == None:
							
							# Ranged Weapon Ammo Check #
							if tempWearItem.type == "Weapon" and tempWearItem.flags["Weapon Type"] == "Ranged" \
							and (tempWearItem.flags["Ammo Type"] not in mobAmmoTypeList \
							and (tempWearItem.flags["Loaded Ammo Object"] == None or tempWearItem.flags["Loaded Ammo Object"].flags["Quantity"] == 0)):
								wearCheck = False
							
							if wearCheck == True:
								targetWearItem = tempWearItem
								break
							
				# Wear Target Item #
				if wearCheck == True and targetWearItem != None and targetGearSlot != None:
					self.gearDict[targetGearSlot] = targetWearItem
					self.removeItemFromInventory(targetWearItem)
					if targetWearItem.type == "Armor" : strAction = " wears "
					else : strAction = " holds "
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						Console.addDisplayLineToDictList(self.defaultTitle + strAction + targetWearItem.defaultTitle + ".")
					actionCheck = True
			
			# Aggressive Mobs #
			if actionCheck == False and self.currentAction == None and ("Agro Player" in self.flags or "Agro Mobs" in self.flags) \
			and not (DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming" and DATA_PLAYER.currentAction["Target Mob"] == self) \
			and not (len(self.groupList) > 0 and "Group Leader" not in self.flags) and random.randrange(0, 3) == 0:
				
				# Mob Target Player #
				if "Agro Player" in self.flags and self not in DATA_PLAYER.mobTargetPlayerCombatList and DATA_PLAYER not in self.groupList:
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						DATA_PLAYER.mobTargetPlayerCombatList.append(self)
						Console.addDisplayLineToDictList(self.defaultTitle + " looks at you with an icy stare.")
						actionCheck = True
					else:
						tempDistanceToPlayer, tempDirectionToPlayer, agroMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, parentRoom, DATA_PLAYER, self.getViewRange())
						if tempDistanceToPlayer not in [None, -1] and agroMessage == None and tempDistanceToPlayer <= self.getViewRange():
							DATA_PLAYER.mobTargetPlayerCombatList.append(self)
							Console.addDisplayLineToDictList("You have a feeling someone is looking at you.")
							actionCheck = True
							
				# Mob Target Mobs #
				if actionCheck == False and "Agro Mobs" in self.flags and self.combatTarget == None and self not in DATA_PLAYER.mobTargetPlayerCombatList:
					if self.currentArea == self.flags["Spawn Area"]: # To Prevent Errors From Mob Being Inserted Into Multiple updateMobCombatList Variables If It Happens To Move Into A Different Area
						surroundingAreaDataList, surroundingRoomDataList = DataWorld.getSurroundingRoomsDataList(SOLAR_SYSTEM_DICT, parentArea, parentRoom, self.getAttackRange())
						breakCheck = False
						for currentRoomData in surroundingRoomDataList:
							if currentRoomData["Room Area"] == self.currentArea and currentRoomData["Room Area Random"] == self.currentAreaRandom:
								currentRoom = parentArea.roomDict[currentRoomData["Room ID"]]
								if len(currentRoom.mobList) > 0:
									for currentMob in currentRoom.mobList:
										if currentMob != self and currentMob != self.combatTarget and currentMob not in self.groupList:
											self.combatTarget = currentMob
											if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
												if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, self, self.combatTarget):
													Console.addDisplayLineToDictList(self.defaultTitle + " looks at " + self.combatTarget.defaultTitle + " with an icy stare.")
												else:
													tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, self, self.combatTarget, self.getViewRange())
													if tempRange != -1 and tempDir != None and tempMessage == None : Console.addDisplayLineToDictList(self.defaultTitle + " looks " + tempDir + " with an icy stare.")
											breakCheck = True
											break
							if breakCheck : break
			
			# Pick Up Items #
			if actionCheck == False and self.currentAction == None and "Pick Up Items" in self.flags and len(parentRoom.itemList) > 0:
			
				# Get Target Item Data #
				targetGetItem = None
				for tempGetItem in parentRoom.itemList:
					if "No Get" not in tempGetItem.flags and (self.currentWeight + tempGetItem.getWeight()) <= self.maxWeight:
						targetGetItem = tempGetItem
						break
					
				# Get Item #
				if targetGetItem != None:
					self.addItemToInventory(targetGetItem)
					parentRoom.removeItemFromRoom(targetGetItem)
					actionCheck = True
					
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
						Console.addDisplayLineToDictList(self.defaultTitle + " picks up " + targetGetItem.defaultTitle + ".")
					
						# Update Surface Data #
						if targetGetItem.dropSide == "Player" : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
						elif targetGetItem.dropSide == "Mob" : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
				
			# Mobile #
			if actionCheck == False and self.currentAction == None and "Mobile" in self.flags \
			and not (DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming" and DATA_PLAYER.currentAction["Target Mob"] == self) \
			and not (len(self.groupList) > 0 and "Group Leader" not in self.flags):
				
				self.flags["Mobile Timer"] -= 1
				if self.flags["Mobile Timer"] <= 0:
					self.move(SOLAR_SYSTEM_DICT, parentArea, DATA_PLAYER, UPDATE_ROOM_DATA_LIST)
					actionCheck = True
			
		# 2) Combat Update Functions #
		else:
			
			# Chase In Combat #
			if actionCheck == False and self.currentAction == None and (self in DATA_PLAYER.mobTargetPlayerCombatList or self.combatTarget != None) \
			and not (len(self.groupList) > 0 and "Group Leader" not in self.flags):
				
				# Chase Player #
				if self in DATA_PLAYER.mobTargetPlayerCombatList and distanceToPlayer not in [None, -1]:
					
					# Next Room Locked Door Check #
					if "No Chase" not in self.flags and directionToPlayer in parentRoom.exitDict and distanceToPlayer > self.getAttackRange() \
					and not ("Door Status" in parentRoom.exitDict[directionToPlayer] and parentRoom.exitDict[directionToPlayer]["Door Status"] == "Locked" and "Key Num" in parentRoom.exitDict[directionToPlayer] and self.hasKey(parentRoom.exitDict[directionToPlayer]["Key Num"]) == False):
						self.move(SOLAR_SYSTEM_DICT, parentArea, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, directionToPlayer)
						actionCheck = True
						
				# Chase Mob #
				elif self.combatTarget != None and distanceToTargetMob not in [None, -1]:
					
					# Next Room Locked Door Check #
					if "No Chase" not in self.flags and directionToTargetMob in parentRoom.exitDict and distanceToTargetMob > self.getAttackRange() \
					and not ("Door Status" in parentRoom.exitDict[directionToTargetMob] and parentRoom.exitDict[directionToTargetMob]["Door Status"] == "Locked" and "Key Num" in parentRoom.exitDict[directionToTargetMob] and self.hasKey(parentRoom.exitDict[directionToTargetMob]["Key Num"]) == False):
						self.move(SOLAR_SYSTEM_DICT, parentArea, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, directionToTargetMob)
						actionCheck = True
						
				# Move In Random Direction If In Combat But Target Is Out Of Sight #
				elif distanceToPlayer == -1 or distanceToTargetMob == -1:
					if self.flags["Mobile Timer"] > 0 : self.flags["Mobile Timer"] -= 1
					if self.flags["Mobile Timer"] <= 0:
						self.move(SOLAR_SYSTEM_DICT, parentArea, DATA_PLAYER, UPDATE_ROOM_DATA_LIST)
						actionCheck = True
			
		# 3) Combat And Non-Combat Functions #
		if actionCheck == False:
			
			# Group With Other Mobs #
			if actionCheck == False and self.currentAction == None and self.combatTarget == None and self not in DATA_PLAYER.mobTargetPlayerCombatList \
			and ("Group With ID" in self.flags or "Group With Mobs" in  self.flags) and len(self.groupList) == 0 and "Group Leader" not in self.flags and random.randrange(0, 3) == 0:
				
				# Get Target Group Mob #
				targetMob = None
				for tempMob in parentRoom.mobList:
					addCheck = False
					if tempMob != self and tempMob.combatTarget != self and self not in tempMob.groupList and len(tempMob.groupList) < 3 \
					and (len(tempMob.groupList) == 0 or "Group Leader" in tempMob.flags):
						
						# Group With ID Check #
						if "Group With ID" in self.flags and "Group With ID" in tempMob.flags and tempMob.idNum == self.idNum:
							if len(tempMob.groupList) == 0 : addCheck = True
							else:
								addCheck = True
								for tempMobGroupMember in tempMob.groupList:
									if tempMobGroupMember.objectType == "Mob" and tempMobGroupMember.idNum != self.idNum:
										addCheck = False
										break
										
						# Group With Mobs Check #
						elif "Group With Mobs" in self.flags and "Group With Mobs" in tempMob.flags:
							addCheck = True
						
						# Prevent Grouping With Player & Mobs Whose Group Targets This Mob #
						if addCheck == True and len(tempMob.groupList) > 0:
							for tempGroupEntity in tempMob.groupList:
								if tempGroupEntity.objectType == "Player":
									addCheck = False
									break
								elif tempGroupEntity.objectType == "Mob" and tempGroupEntity.combatTarget == self:
									addCheck = False
									break
						
						# Get Target Group Mob #
						if addCheck == True:
							targetMob = tempMob
							break
					
				# Group Mob #
				if targetMob != None:
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, self, DATA_PLAYER):
						Console.addDisplayLineToDictList(self.defaultTitle + " joins " + targetMob.defaultTitle + "'s group.")
					
					if len(targetMob.groupList) == 0 and "Group Leader" not in targetMob.flags : targetMob.flags["Group Leader"] = True
					self.addToGroup(targetMob, SOLAR_SYSTEM_DICT, DATA_PLAYER)
					
		# Remove Player Action If Target Mob Was Being Tamed #
		if actionCheck and DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming" and DATA_PLAYER.currentAction["Target Mob"] == self:
			DATA_PLAYER.currentAction = None
			Console.addDisplayLineToDictList("Your concentration is broken.")
			
	# Getters & Setters #
	def userExamine(self):
	
		Console.addDisplayLineToDictList(self.lookTitle, self.lookTitleColorCode)
		
		for gearSlot in self.gearDict:
			if self.gearDict[gearSlot] != None:
				targetGear = self.gearDict[gearSlot]
				strGear = "[" + gearSlot + "] " + targetGear.defaultTitle
				strCode = "1r" + str(len(gearSlot)) + "w2r" + str(len(targetGear.defaultTitle)) + "w"
				
				# Weapon Ammo Check #
				if targetGear.type == "Weapon" and targetGear.flags["Weapon Type"] == "Ranged":
					maxCount = targetGear.flags["Magazine Size"]
					ammoCount = 0
					if targetGear.flags["Loaded Ammo Object"] != None and targetGear.flags["Loaded Ammo Object"].flags["Quantity"] > 0:
						ammoCount = targetGear.flags["Loaded Ammo Object"].flags["Quantity"]
						
					strGear = strGear + " [" + str(ammoCount) + "/" + str(maxCount) + "]"
					strCode = strCode + "2r" + str(len(str(ammoCount))) + "w1r" + str(len(str(maxCount))) + "w1r"
				
				Console.addDisplayLineToDictList(strGear, strCode)
	
	def getViewRange(self):
	
		return 2
	
	def getAttackRange(self):
	
		attackRange = 0
	
		# Dominant Hand #
		targetHand = self.dominantHand + " Hand"
		if self.gearDict[targetHand] != None and "Weapon Range" in self.gearDict[targetHand].flags:
			weaponRange = self.gearDict[targetHand].flags["Weapon Range"]
			if weaponRange > attackRange : attackRange = weaponRange
			
		# Offhand #
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
	
	def getAttack(self, DATA_DEFENDER, TARGET_ROOM, TARGET_RANGE):
	
		targetAttack = None
		attackSkillIDList = []
		healSkillIDList = []
		dodgeCheck = False
		parryCheck = False
	
		# Get Attack List #
		for skillTreeID in self.skillTreeDict:
			for targetSkillID in self.skillTreeDict[skillTreeID].skillDict:
				
				# Non-Attack Data (Dodge) #
				if skillTreeID == "Basic Combat" and targetSkillID == "Dodge":
					if (DATA_DEFENDER.objectType == "Player" and len(DATA_DEFENDER.mobTargetList) > 0 and DATA_DEFENDER.mobTargetList[0] == self) \
					or (DATA_DEFENDER.objectType == "Mob" and DATA_DEFENDER.combatTarget == self):
						if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Attacking":
							dodgeCheck = True
							
				# Non-Attack Data (Parry) (Unfinished) #
				
				
				# Attack Data #
				elif (skillTreeID in ["Basic Magic", "Advanced Magic"] and targetSkillID.lower() in Config.SPELL_MASTER_KEY_LIST) or targetSkillID.lower() in Config.SKILL_MASTER_KEY_LIST:
					dataTargetAttack = DataAttack.loadPrefab(targetSkillID)
					if dataTargetAttack != None:

						# Attack Checks #
						addSkillCheck = True
						if dataTargetAttack.rangeType == "Short" and TARGET_RANGE > 0 : addSkillCheck = False
						elif dataTargetAttack.mpCost > 0 and dataTargetAttack.mpCost > self.currentMP : addSkillCheck = False
						elif dataTargetAttack.targetType == "Room" and TARGET_ROOM.updateSkill != None : addSkillCheck = False
						elif "Dual Wield Only" in dataTargetAttack.flags and not ("Advanced Combat" in self.skillTreeDict and "Dual Wield" in self.skillTreeDict["Advanced Combat"].skillDict) : addSkillCheck = False
						
						# Required Weapon Checks #
						elif "Required Weapon Type List" in dataTargetAttack.flags or "Ammo Required" in dataTargetAttack.flags:
							
							heldWeaponTypeList = []
							loadedAmmoCountList = []
							
							# Get Held Weapon Type List & Magazine Ammo Data #
							if True:
								
								# Dominant Hand #
								dominantHandCount = 0
								if self.gearDict[self.dominantHand+" Hand"] == None : heldWeaponTypeList.append(None)
								else:
									heldWeaponTypeList.append(self.gearDict[self.dominantHand+" Hand"].flags["Weapon Type"])
									if self.gearDict[self.dominantHand+" Hand"].flags["Weapon Type"] == "Ranged" and self.gearDict[self.dominantHand+" Hand"].flags["Loaded Ammo Object"] != None \
									and self.gearDict[self.dominantHand+" Hand"].flags["Loaded Ammo Object"].flags["Quantity"] > 0:
										dominantHandCount = self.gearDict[self.dominantHand+" Hand"].flags["Loaded Ammo Object"].flags["Quantity"]
										loadedAmmoCountList.append(dominantHandCount)
								
								# Offhand #
								offhandCount = 0
								if self.dominantHand == "Left" : strOffhand = "Right Hand"
								else : strOffhand = "Left Hand"
								if self.gearDict[strOffhand] == None : heldWeaponTypeList.append(None)
								else:
									heldWeaponTypeList.append(self.gearDict[strOffhand].flags["Weapon Type"])
									if self.gearDict[strOffhand].flags["Weapon Type"] == "Ranged" and self.gearDict[strOffhand].flags["Loaded Ammo Object"] != None \
									and self.gearDict[strOffhand].flags["Loaded Ammo Object"].flags["Quantity"] > 0:
										offhandCount = self.gearDict[strOffhand].flags["Loaded Ammo Object"].flags["Quantity"]
										loadedAmmoCountList.append(offhandCount)
								
							# Weapon Required Checks #
							if "Required Weapon Type List" in dataTargetAttack.flags:
								requiredWeaponCheckMain = False
								requiredWeaponCheckOffhand = False
								if heldWeaponTypeList[0] in dataTargetAttack.flags["Required Weapon Type List"]:
									requiredWeaponCheckMain = True
								if len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] in dataTargetAttack.flags["Required Weapon Type List"]:
									requiredWeaponCheckOffhand = True
									
								if ("Dual Wield Only" not in dataTargetAttack.flags and requiredWeaponCheckMain == False and requiredWeaponCheckOffhand == False) \
								or ("Dual Wield Only" in dataTargetAttack.flags and (requiredWeaponCheckMain == False or requiredWeaponCheckOffhand == False)):
									addSkillCheck = False
									
							# Ammo Check #
							if addSkillCheck == True and "Ammo Required" in dataTargetAttack.flags:
								if ("Dual Wield Only" not in dataTargetAttack.flags and loadedAmmoCountList[0] <= 0 and loadedAmmoCountList[1] <= 0) \
								or ("Dual Wield Only" in dataTargetAttack.flags and (loadedAmmoCountList[0] <= 0 or loadedAmmoCountList[1] <= 0)):
									addSkillCheck = False
						
						if addSkillCheck:
							if dataTargetAttack.effectType == "Damage":
								attackSkillIDList.append(targetSkillID)
							elif dataTargetAttack.effectType == "Heal":
								healSkillIDList.append(targetSkillID)
					
		# Choose Target Attack #
		if len(healSkillIDList) > 0 and (self.currentHP / (self.maxHP+0.0) <= .20):
			targetAttack = DataAttack.loadPrefab(random.choice(healSkillIDList))
		elif len(attackSkillIDList) > 0:
			targetAttack = DataAttack.loadPrefab(random.choice(attackSkillIDList))
		elif TARGET_RANGE <= self.getAttackRange():
			targetAttack = DataAttack.loadPrefab("Basic Attack")
		
		# Dodge Check #
		if dodgeCheck : targetAttack = "Dodge"
		elif parryCheck : targetAttack = "Parry"
		
		return targetAttack
	
	# Utility Functions #
	def addItemToInventory(self, TARGET_ITEM, ADD_WEIGHT=True):
	
		# Update Item Variables #
		if True:
			TARGET_ITEM.currentSolarSystem = self.currentSolarSystem
			TARGET_ITEM.currentPlanet = self.currentPlanet
			TARGET_ITEM.currentArea = self.currentArea
			TARGET_ITEM.currentAreaRandom = self.currentAreaRandom
			TARGET_ITEM.currentRoom = self.currentRoom
			TARGET_ITEM.currentLoc = "Mob"
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
		
	def updateMobsInView(self, SOLAR_SYSTEM_DICT, DATA_PLAYER):
	
		# Get Data #
		if True:
			playerRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
			currentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[self.currentSolarSystem], self)
			currentRoom = currentArea.roomDict[self.currentRoom]
			rangePlayerToSelf, dirPlayerToSelf, messagePlayerToSelf = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, self, DATA_PLAYER.getViewRange())
			rangeSelfToPlayer, dirSelfToPlayer, messageSelfToPlayer = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, currentRoom, DATA_PLAYER, self.getViewRange())
		
		# Remove Self From Player Target List #
		playerTargetDelMessageList = []
		if self in DATA_PLAYER.mobTargetList and (messagePlayerToSelf == "Door Is Closed" or rangePlayerToSelf == -1):
			del DATA_PLAYER.mobTargetList[DATA_PLAYER.mobTargetList.index(self)]
			playerTargetDelMessageList.append("You lose sight of " + tempMob.defaultTitle + ".")
		
		# Remove Self From Mob Target Player Combat List #
		#if self in DATA_PLAYER.mobTargetPlayerCombatList and (messageSelfToPlayer == "Door Is Closed" or rangeSelfToPlayer == -1):
		if self in DATA_PLAYER.mobTargetPlayerCombatList and rangeSelfToPlayer == -1:
			del DATA_PLAYER.mobTargetPlayerCombatList[DATA_PLAYER.mobTargetPlayerCombatList.index(self)]
		
		# Remove Self From Other Mob's View Range #
		self.removeSelfFromOtherMobsView(SOLAR_SYSTEM_DICT)
	
		# Remove Combat Target Check #
		if self.combatTarget != None:
			targetRange, targetDir, targetMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, currentRoom, self.combatTarget, self.getViewRange())
			#if targetMessage == "Door Is Closed" or targetRange == -1:
			if targetRange == -1:
				self.combatTarget = None
			
		return playerTargetDelMessageList
	
	def removeSelfFromOtherMobsView(self, SOLAR_SYSTEM_DICT):
	
		# Get Data #
		parentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[self.currentSolarSystem], self)
		parentRoom = parentArea.roomDict[self.currentRoom]
		surroundingAreaDataList, surroundingRoomDataList = DataWorld.getSurroundingRoomsDataList(SOLAR_SYSTEM_DICT, parentArea, parentRoom, Config.MOB_MOVE_CHECK_TARGET_RANGE)
		currentUpdateArea = None
		
		# Remove Self From Other Mob's Combat Target #
		for roomDataDict in surroundingRoomDataList:
			if currentUpdateArea == None or (roomDataDict["Room Area"] != currentUpdateArea.idArea or roomDataDict["Room Area Random"] != currentUpdateArea.idRandom):
				
				# Get Update Data #
				if roomDataDict["Room Area Random"] != None : currentUpdateArea = SOLAR_SYSTEM_DICT[roomDataDict["Room Solar System"]].getTargetSpaceship(roomDataDict["Room Area"], roomDataDict["Room Area Random"])
				else : currentUpdateArea = SOLAR_SYSTEM_DICT[roomDataDict["Room Solar System"]].planetDict[roomDataDict["Room Planet"]].areaDict[roomDataDict["Room Area"]]
				currentRoom = currentUpdateArea.roomDict[roomDataDict["Room ID"]]
				
				# Mob Check #
				currentDistance = None
				for currentMob in currentRoom.updateMobList:
					if currentMob.combatTarget == self:
						
						# Get Current Room Distance #
						if currentDistance == None:
							currentDistance = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, currentRoom, self, currentMob.getViewRange())
						
						if currentDistance == -1:
							currentMob.combatTarget = None
		
	def move(self, SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, UPDATE_ROOM_DATA_LIST, TARGET_DIR="Random"):
	
		# Get Data #
		if True:
			startRoom = PARENT_AREA.roomDict[self.currentRoom]
			currentRoom = PARENT_AREA.roomDict[self.currentRoom]
			openDoorCheck = False
			automaticDoorCheck = False
			moveChoiceList = []
			messageType = None
			moveCheck = False
			tameCheck = False
			
			if TARGET_DIR in ["North", "East", "South", "West"] : exitList = [TARGET_DIR]
			else : exitList = ["North", "East", "South", "West"]
			
		# Get Target Move Direction #
		for exitDir in exitList:
			if exitDir in currentRoom.exitDict:
				targetExit = currentRoom.exitDict[exitDir]
				if "Solar System" in targetExit and "Planet" in targetExit and "Area" in targetExit and "Room" in targetExit:
					if targetExit["Solar System"] == self.currentSolarSystem and targetExit["Planet"] == self.currentPlanet and targetExit["Area"] == self.currentArea:
						
						inRangeCheck = False
						for tempRoomData in UPDATE_ROOM_DATA_LIST:
							if tempRoomData["Room Solar System"] == targetExit["Solar System"] and tempRoomData["Room Planet"] == targetExit["Planet"] and tempRoomData["Room Area"] == targetExit["Area"] and tempRoomData["Room ID"] == targetExit["Room"]:
								inRangeCheck = True
						
							if inRangeCheck:
								if ("Door Status" not in targetExit or targetExit["Door Status"] in ["Open", "Closed", "Locked"]) \
								and not ("Door Status" in targetExit and "Don't Pass Closed Doors" in self.flags and targetExit["Door Status"] in ["Closed", "Locked"]):
								
									passDoorCheck = True
									if "Door Status" in targetExit and "Key Num" in targetExit and targetExit["Door Status"] == "Locked" and self.hasKey(targetExit["Key Num"]) == False:
										passDoorCheck = False
									
									if passDoorCheck == True:
										targetExitRoom = SOLAR_SYSTEM_DICT[targetExit["Solar System"]].planetDict[targetExit["Planet"]].areaDict[targetExit["Area"]].roomDict[targetExit["Room"]]
										if "No Mob" not in targetExitRoom.flags:
											targetExitDict = {"Move Dir":exitDir, "Solar System":targetExit["Solar System"], "Planet":targetExit["Planet"], "Area":targetExit["Area"], "Room":targetExit["Room"]}
											if "Door Status" in targetExit:
												targetExitDict["Door Status"] = targetExit["Door Status"]
												targetExitDict["Door Type"] = targetExit["Door Type"]
											moveChoiceList.append(targetExitDict)
			
		# Move Mob - (For Now, Mobs Move Only Within Player Update Range & Spawn Area) #
		randomChoice = None
		if len(moveChoiceList) > 0:
			randomChoice = random.choice(moveChoiceList)
			if randomChoice["Room"] != self.currentRoom:
				
				# Door Status Check #
				if "Door Status" in randomChoice and randomChoice["Door Status"] in ["Closed", "Locked"]:
					openDoorCheck = True
					if randomChoice["Door Type"] == "Default" : currentRoom.ocluDoor(SOLAR_SYSTEM_DICT, self.currentSolarSystem, "Open", randomChoice["Move Dir"])
					elif randomChoice["Door Type"] == "Automatic" : automaticDoorCheck = True
				
				# Message #
				if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
					messageType = "Move Out Of Room"
				
				# Move Mob #
				self.currentRoom = randomChoice["Room"]
				currentRoom.removeMobFromRoom(self)
				currentRoom = PARENT_AREA.roomDict[self.currentRoom]
				currentRoom.addMob(self, DATA_PLAYER)
				if self not in DATA_PLAYER.groupList : currentRoom.setEntityScreenLoc(self, DATA_PLAYER)
				self.flags["Mobile Timer"] = random.randrange(Config.MOB_TIMER["Mobile Min"], Config.MOB_TIMER["Mobile Max"])
				moveCheck = True
				
				# Mob Move Out Of View Check #
				targetDelMessageList = self.updateMobsInView(SOLAR_SYSTEM_DICT, DATA_PLAYER)
				
				# Message #
				if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
					messageType = "Move Into Room"
				
		# Being Tamed Check #
		if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming" and DATA_PLAYER.currentAction["Target Mob"] == self:
			tameCheck = DATA_PLAYER.currentAction["Target Mob"]
			DATA_PLAYER.currentAction = None
				
		# Messages #
		if messageType != None:
			oppositeDir = "None"
			if randomChoice["Move Dir"] == "North" : oppositeDir = "South"
			elif randomChoice["Move Dir"] == "East" : oppositeDir = "West"
			elif randomChoice["Move Dir"] == "South" : oppositeDir = "North"
			elif randomChoice["Move Dir"] == "West" : oppositeDir = "East"
			
			if tameCheck != False:
				Console.addDisplayLineToDictList("Your concentration on " + tameCheck.defaultTitle + " is broken.")
			
			if openDoorCheck:
				if messageType == "Move Into Room":
					if automaticDoorCheck : Console.addDisplayLineToDictList("The " + oppositeDir + "ern door opens and closes as " + self.defaultTitle + " enters the room.")
					else : Console.addDisplayLineToDictList("The " + oppositeDir + "ern door opens and " + self.defaultTitle + " enters the room.")
				elif messageType == "Move Out Of Room":
					if automaticDoorCheck : Console.addDisplayLineToDictList("The " + randomChoice["Move Dir"] + "ern door opens and closes as " + self.defaultTitle + " leaves the room.")
					else : Console.addDisplayLineToDictList(self.defaultTitle + " opens the " + randomChoice["Move Dir"] + "ern door and leaves.")
				
			else:
				if messageType == "Move Into Room":
					Console.addDisplayLineToDictList(self.defaultTitle + " arrives from the " + oppositeDir + ".")
				elif messageType == "Move Out Of Room":
					Console.addDisplayLineToDictList(self.defaultTitle + " leaves to the " + randomChoice["Move Dir"] + ".")
				
		# Post-Message Functions #
		if moveCheck:
					
			# Group Move With Mob #
			if "Group Leader" in self.flags and len(self.groupList) > 0:
				groupMoveList = []
				for groupEntity in self.groupList:
					if groupEntity.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, groupEntity, startRoom) and groupEntity.currentAction == None and groupEntity in startRoom.mobList:
						
						startRoom.removeMobFromRoom(groupEntity)
						currentRoom.addMob(groupEntity, DATA_PLAYER)
						
						groupEntity.currentSolarSystem = currentRoom.idSolarSystem
						groupEntity.currentPlanet = currentRoom.idPlanet
						groupEntity.currentArea = currentRoom.idArea
						groupEntity.currentAreaRandom = currentRoom.idAreaRandom
						groupEntity.currentRoom = currentRoom.idNum
						
						groupMoveList.append(groupEntity)
						
				# Messages #
				if True:
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, startRoom):
						if len(groupMoveList) == 1 : Console.addDisplayLineToDictList(groupMoveList[0].defaultTitle + " follows " + self.defaultTitle + " out of the room.")
						elif len(groupMoveList) > 1 : Console.addDisplayLineToDictList("A group follows " + self.defaultTitle + " out of the room.")
					elif DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, currentRoom):
						if len(groupMoveList) == 1 : Console.addDisplayLineToDictList(groupMoveList[0].defaultTitle + " follows " + self.defaultTitle + " into the room.")
						elif len(groupMoveList) > 1 : Console.addDisplayLineToDictList("A group follows " + self.defaultTitle + " into the room.")
				
			# Lose Sight Of Target Display Lines #
			if len(targetDelMessageList) > 0:
				for tempLine in targetDelMessageList:
					Console.addDisplayLineToDictList(tempLine)
		
			# Update Screen Data #
			if messageType in ["Move Out Of Room", "Move Into Room"]:
				if self in DATA_PLAYER.groupList : Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
				else : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
			
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
	
	def isUpdateMob(self):
	
		updateMobCheck = False
		
		if "Mobile" in self.flags or "Agro Player" in self.flags or "Agro Mobs" in self.flags or "Pick Up Items" in self.flags \
		or "Group With ID" in self.flags or "Group With Mobs" in self.flags:
			updateMobCheck = True
		
		return updateMobCheck
	
	def addToGroup(self, TARGET_MOB, SOLAR_SYSTEM_DICT=None, DATA_PLAYER=None):
	
		# Add Targets To Group #
		if True:
			for tempMob in TARGET_MOB.groupList:
				if tempMob not in self.groupList : self.groupList.append(tempMob)
				if self not in tempMob.groupList : tempMob.groupList.append(self)
			if TARGET_MOB not in self.groupList : self.groupList.append(TARGET_MOB)
			if self not in TARGET_MOB.groupList : TARGET_MOB.groupList.append(self)
		
		# Add Combat Target #
		if SOLAR_SYSTEM_DICT != None and DATA_PLAYER != None and self.combatTarget == None and self not in DATA_PLAYER.mobTargetPlayerCombatList:
			
			# Get Combat Target #
			groupCombatTarget = None
			for groupEntity in self.groupList:
				if groupEntity.objectType == "Mob" and (groupCombatTarget == None or "Group Leader" in groupEntity.flags):
					
					# Group Target Player #
					if groupEntity in DATA_PLAYER.mobTargetPlayerCombatList:
						playerRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
						distanceToTarget, directionToTarget, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, self, self.getViewRange())
						if distanceToTarget != -1 and tempMessage == None:
							groupCombatTarget = DATA_PLAYER
							
					# Group Target Mob #
					elif groupCombatTarget == None and groupEntity.combatTarget != None:
						groupTargetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[groupEntity.combatTarget.currentSolarSystem], groupEntity.combatTarget).roomDict[groupEntity.combatTarget.currentRoom]
						distanceToTarget, directionToTarget, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, groupTargetRoom, self, self.getViewRange())
						if distanceToTarget != -1 and tempMessage == None:
							groupCombatTarget = self.combatTarget
							
					if "Group Leader" in groupEntity.flags:
						break
						
			# Add Combat Target #
			if groupCombatTarget != None:
				if groupCombatTarget.objectType == "Player" : DATA_PLAYER.mobTargetPlayerCombatList.append(self)
				elif groupCombatTarget.objectType == "Mob" : self.combatTarget = groupEntity.combatTarget
				
				# Messages #
				if groupCombatTarget != None and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, self):
					if groupCombatTarget.objectType == "Player":
						Console.addDisplayLineToDictList(self.defaultTitle + " looks at you with an icy stare.")
					elif groupCombatTarget.objectType == "Mob":
						if distanceToTarget == 0 : Console.addDisplayLineToDictList(self.defaultTitle + " looks at " + self.combatTarget.defaultTitle + " with an icy stare.")
						elif distanceToTarget > 0 : Console.addDisplayLineToDictList(self.defaultTitle + " looks " + str(directionToTarget) + " with an icy stare.")
			
def loadPrefab(ID_NUM, ENTITY_IMAGE_DICT):

	mob = LoadMob()
	mob.idNum = ID_NUM
	tempKeywordList = []
	
	# A Shopkeeper #
	if ID_NUM == 1:
		tempKeywordList = ["shop"]
		mob.idImage = "Shopkeeper"
		mob.defaultTitle = "A Shopkeeper"
		mob.defaultTitleColorCode = "12w"
		mob.roomTitle = "A Shopkeeper is here, waiting to take your order."
		mob.roomTitleColorCode = "20w2y26w1y"
		mob.roomTitleCaption = Caption.LoadCaption(1, 1, "Undefined")
		mob.evolutionLevel = "Human"
		mob.flags["Shop List"] = [1, 2, 3, 4]
		mob.flags["Pick Up Items"] = True
		mob.flags["Autowear Gear"] = True
		mob.flags["No Chase"] = True
		mob.maxHP = 6000
		mob.learnSkillset("Basic Combat")
		#mob.learnSkillset("Advanced Combat")
		mob.learnSkillset("Basic Magic")
		
	# A Mouse #
	elif ID_NUM == 2:
		tempKeywordList = ["rat"]
		mob.idImage = "Mouse"
		mob.defaultTitle = "A Mouse"
		mob.defaultTitleColorCode = "7w"
		mob.roomTitle = "A Mouse is here scuttling about."
		mob.roomTitleColorCode = "15w16w1y"
		mob.flags["Mobile"] = True
		mob.flags["Don't Pass Closed Doors"] = True
		mob.flags["Group With Mobs"] = True
		mob.maxHP = 32
		mob.lootDict = {1:75}
		
	# A Zombie #
	elif ID_NUM == 3:
		mob.idImage = "Zombie"
		mob.defaultTitle = "A Zombie"
		mob.defaultTitleColorCode = "2w1dg5ddw"
		mob.roomTitle = "A Zombie is here looking for brains."
		mob.roomTitleColorCode = "2w1dg5ddg27w1y"
		mob.flags["Agro Player"] = True
		mob.flags["Group With ID"] = True
		mob.maxHP = 50
		#mob.learnSkillset("Advanced Combat")
		pass
		
	# A Knight #
	elif ID_NUM == 4:
		mob.idImage = "Knight"
		mob.defaultTitle = "A Knight"
		mob.defaultTitleColorCode = "2w1dw5w"
		mob.roomTitle = "A Knight is here."
		mob.roomTitleColorCode = "2w1dw5w8w1y"
		#mob.flags["Agro Mobs"] = True
		mob.maxHP = 75
		
	# A Dragon #
	elif ID_NUM == 5:
		mob.idImage = "Dragon"
		mob.defaultTitle = "A Dragon"
		mob.defaultTitleColorCode = "8w"
		mob.roomTitle = "A Dragon is here spitting hot fire."
		mob.roomTitleColorCode = "8w26w1y"
		mob.flags["Mobile"] = True
		mob.flags["Group With Mobs"] = True
		mob.maxHP = 1500
		
	# A Debug Mob #
	else:
		mob.defaultTitle = "A Debug Mob"
		mob.defaultTitleColorCode = "11w"
		mob.roomTitle = "A Debug Mob is here."
		mob.roomTitleColorCode = "40w"
	
	# Load Mob Data #
	if True:
		mob.keyList = Utility.createKeyList(mob.defaultTitle)
		for tempKeyword in tempKeywordList:
			if tempKeyword not in mob.keyList : mob.keyList.append(tempKeyword)
		roomTitleLength = len(mob.roomTitle.split())
		mob.roomTitleCaption = Caption.LoadCaption(0, roomTitleLength, "Undefined")
		mob.flags["Mobile Timer"] = 0
		if "Mobile" in mob.flags : mob.flags["Mobile Timer"] = Config.MOB_TIMER["Mobile Max"]
		
		# Dire Mob Roll #
		if random.randrange(0, 100) <= 20:
			mob.flags["Dire Mob"] = True
			mob.maxHP = (mob.maxHP * 1.5)
			mob.maxMP = (mob.maxMP * 1.5)
		
		mob.currentHP = mob.maxHP
		mob.currentMP = mob.maxMP
		
		# Load Area Rect #
		if mob.idImage in ENTITY_IMAGE_DICT : mobImage = ENTITY_IMAGE_DICT[mob.idImage]
		else : mobImage = ENTITY_IMAGE_DICT["Default"]
		mob.rectArea = pygame.Rect([0, 0, mobImage.get_width() - (mobImage.get_width() * .15), mobImage.get_height() - (mobImage.get_height() * .15)])
		mob.imageSize = [mobImage.get_width(), mobImage.get_height()]
		
	return mob

def listWares(PARENT_AREA, DATA_PLAYER):

	currentRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
	
	targetMob = None
	for mob in currentRoom.mobList:
		if "Shop List" in mob.flags:
			targetMob = mob
			break
			
	if targetMob == None:
		Console.addDisplayLineToDictList("Nobody seems to be selling anything.", "35w1y")
	else:
		Console.addDisplayLineToDictList("For Sale:", "8w1y")
		for itemIdNum in targetMob.flags["Shop List"]:
			item = DataItem.loadPrefab(itemIdNum)
			if item.idNum != -1:
				strLine = item.defaultTitle + " - " + str(item.value) + " Gold"
				colorCode = item.defaultTitleColorCode + "3y" + str(len(str(item.value))) + "w5w"
				Console.addDisplayLineToDictList(strLine, colorCode)
		