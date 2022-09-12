import pygame, random, copy, Config, GameProcess, DataWorld, DataPlayer, DataItem, DataAttack, DataSkill
from Elements import Console
from pygame import *

# Update Functions #
def updateActionTimers(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, DEL_MOB_LIST, SIDESCREEN_ROOM, INTERFACE_IMAGE_DICT):
	
	# Update Steps #
	if "Current Steps" in DATA_ATTACKER.flags:
		DATA_ATTACKER.flags["Current Steps"] -= 2
		if DATA_ATTACKER.flags["Current Steps"] <= 0:
			del DATA_ATTACKER.flags["Current Steps"]
	
	# Tick Current Action #
	if DATA_ATTACKER.currentAction != None:
		DATA_ATTACKER.currentAction["Timer"] -= .5
		
		if DATA_ATTACKER.currentAction["Timer"] <= 0:
			
			# Get Data #
			if True:
				dataAttack = None
				attackCheck = False
				clearActionCheck = True
				targetReloadWeapon = None
				targetRemoveWeapon = None
				tameTarget = None
				messageType = None
			
			# Attack #
			if DATA_ATTACKER.currentAction["Type"] == "Attacking":
				dataAttack = DATA_ATTACKER.currentAction["Attack Data"]
				
				# Get Attack Data & Attack Checks #
				if dataAttack.mpCost > 0 and dataAttack.mpCost > DATA_ATTACKER.currentMP:
					if DATA_ATTACKER.objectType == "Player" : messageType = "Player Not Enough Mana"
					elif DATA_ATTACKER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER) : messageType = "Mob Not Enough Mana"
				else:
				
					# Get Data #
					if True:
						if dataAttack.idNum == -1 : attackerAttackRange = DATA_ATTACKER.getAttackRange()
						elif dataAttack.targetSkillTree in ["Basic Magic", "Advanced Magic"] : attackerAttackRange = DATA_ATTACKER.getCastRange()
						else : attackerAttackRange = DATA_ATTACKER.getSkillRange(dataAttack)
						playerRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
						attackerRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_ATTACKER.currentSolarSystem], DATA_ATTACKER).roomDict[DATA_ATTACKER.currentRoom]
						dataDefender = None
						targetRoom = None
						oppositeDirDict = {"North":"South", "East":"West", "South":"North", "West":"East"}
						killPlayerCheck = False
						
					# Get Defender Data #
					if dataAttack.targetType == "Entity" and dataAttack.currentCount in [1, "Self"]:
						
						# Targeting Self #
						if dataAttack.currentCount == "Self":
							dataDefender = DATA_ATTACKER
						
						# Attacking Player #
						elif DATA_ATTACKER.objectType == "Player":
							if len(DATA_ATTACKER.mobTargetList) == 0 : messageType = "No Target Found"
							else : dataDefender = DATA_ATTACKER.mobTargetList[0]
						
						# Attacking Mob #
						elif DATA_ATTACKER.objectType == "Mob" and "Mob Target" in DATA_ATTACKER.currentAction:
							if DATA_ATTACKER.currentAction["Mob Target"] == "Player" : dataDefender = DATA_PLAYER
							elif DATA_ATTACKER.currentAction["Mob Target"] == "Mob" and DATA_ATTACKER.combatTarget != None : dataDefender = DATA_ATTACKER.combatTarget
							
					# Get Target Room Data #
					if dataDefender != None or dataAttack.targetType == "Room" or dataAttack.currentCount == "All":
						
						if dataAttack.targetType == "Entity":
							
							if dataAttack.currentCount in [1, "Self"]:
								targetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[dataDefender.currentSolarSystem], dataDefender).roomDict[dataDefender.currentRoom]
							
							elif dataAttack.currentCount == "All":
								
								if DATA_ATTACKER.objectType == "Player":
									targetRoom = attackerRoom
									if dataAttack.targetRoomData != None:
										targetRoom = dataAttack.targetRoomData
										
								elif DATA_ATTACKER.objectType == "Mob":
									if DATA_ATTACKER.currentAction["Mob Target"] == "Player":
										targetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
									elif DATA_ATTACKER.currentAction["Mob Target"] == "Mob" and DATA_ATTACKER.combatTarget != None:
										targetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_ATTACKER.combatTarget.currentSolarSystem], DATA_ATTACKER.combatTarget).roomDict[DATA_ATTACKER.combatTarget.currentRoom]
			
						elif dataAttack.targetType == "Room":
							
							if DATA_ATTACKER.objectType == "Player":
								targetRoom = attackerRoom
								if dataAttack.targetRoomData != None:
									targetRoom = dataAttack.targetRoomData
							
							elif DATA_ATTACKER.objectType == "Mob":
								if DATA_ATTACKER.currentAction["Mob Target"] == "Player":
									targetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
								elif DATA_ATTACKER.currentAction["Mob Target"] == "Mob":
									if DATA_ATTACKER.combatTarget != None:
										targetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_ATTACKER.combatTarget.currentSolarSystem], DATA_ATTACKER.combatTarget).roomDict[DATA_ATTACKER.combatTarget.currentRoom]
									else:
										# Should Only Fire On Heal Spells (Self Target) #
										targetRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_ATTACKER.currentSolarSystem], DATA_ATTACKER).roomDict[DATA_ATTACKER.currentRoom]
		
							if targetRoom != None and targetRoom.updateSkill != None:
								targetRoom = None
								if DATA_ATTACKER.objectType == "Player" : messageType = "Skill Already In Room"
					
					# Door & Range Checks #
					if targetRoom != None:
						if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, targetRoom):
							tempRange = 0
							tempDir = None
							attackCheck = True
						else:
							tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerRoom, targetRoom, attackerAttackRange)
							if tempMessage == "Door Is Closed":
								if DATA_ATTACKER.objectType == "Player":
									if DATA_ATTACKER.flags["Attack Data"].damageType == "Physical" : messageType = "Player Attack Hit Door"
									elif DATA_ATTACKER.flags["Attack Data"].damageType == "Magic" : messageType = "Player Spell Hit Door"
							elif tempRange == -1:
								if DATA_ATTACKER.objectType == "Player" : messageType = "Target Out Of Range"
							elif dataAttack.idNum != -1 and dataAttack.rangeType == "Short" and tempRange > 0:
								if DATA_ATTACKER.objectType == "Player" : messageType = "Target Out Of Range"
							else : attackCheck = True
						
					# Attack Target(s) #
					if attackCheck:
					
						# Cast/Use/Fire Message #
						if True:
							
							# Cast Spell Message #
							if dataAttack.targetSkillTree in ["Basic Magic", "Advanced Magic"]:
								if DATA_ATTACKER.objectType == "Player":
									if tempRange > 0 : Console.addDisplayLineToDictList("You cast " + dataAttack.idSkill + " to the " + tempDir + "!")
									else : Console.addDisplayLineToDictList("You cast " + dataAttack.idSkill + "!")
								elif DATA_ATTACKER.objectType == "Mob":
									if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
										Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " casts " + dataAttack.idSkill + "!")
									elif DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, targetRoom, DATA_PLAYER):
										Console.addDisplayLineToDictList(dataAttack.idSkill + " is cast from the " + oppositeDirDict[tempDir] + ".")
							
							# Use Skill Message #
							elif dataAttack.targetSkillTree in ["Advanced Combat"]:
								if DATA_ATTACKER.objectType == "Player":
									Console.addDisplayLineToDictList("You use " + dataAttack.idSkill + "!")
								elif DATA_ATTACKER.objectType == "Mob":
									if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
										Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " uses " + dataAttack.idSkill + "!")
									elif DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, targetRoom, DATA_PLAYER):
										Console.addDisplayLineToDictList(dataAttack.idSkill + " is cast from the " + oppositeDirDict[tempDir] + ".")
							
						# Target Entity Attack #
						if dataAttack.targetType == "Entity":
							
							# Single Target Attack #
							if dataAttack.currentCount == 1:
								if dataDefender.currentHP > 0:
								
									if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, dataDefender):
										attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, dataDefender, dataAttack, 0, None, INTERFACE_IMAGE_DICT)
									else:
										tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerRoom, dataDefender, attackerAttackRange)
										attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, dataDefender, dataAttack, tempRange, tempDir, INTERFACE_IMAGE_DICT)
										
									# Defender HP < 0 Check #
									if dataDefender.objectType == "Mob" and dataAttack.effectType != "Heal" and dataDefender.currentHP <= 0 and dataDefender not in DEL_MOB_LIST:
										DEL_MOB_LIST.append(dataDefender)
										
										# Messages #
										if True:
											if DATA_ATTACKER.objectType == "Player" or DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, dataDefender):
												Console.addDisplayLineToDictList(dataDefender.defaultTitle + " is DEAD!", dataDefender.defaultTitleColorCode + "8w1y")
											elif targetRoom != None:
												distanceToPlayer, dirToPlayer, toPlayerMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, targetRoom, DATA_PLAYER, 3)
												if distanceToPlayer != -1 and distanceToPlayer > 0 and toPlayerMessage == None:
													Console.addDisplayLineToDictList("You hear a death cry to the " + oppositeDirDict[dirToPlayer] + ".")
										
							# Target All #
							elif dataAttack.currentCount == "All":
								
								# Heal Self & Attack Player Checks #
								if True:
								
									# Get Attack All Count #
									healSelf = False
									attackAllCount = 0
									attackPlayer = False
									for tempMob in targetRoom.mobList:
										if tempMob != DATA_ATTACKER:
											if (dataAttack.effectType == "Damage" and tempMob not in DATA_ATTACKER.groupList) \
											or (dataAttack.effectType == "Heal" and tempMob in DATA_ATTACKER.groupList):
												attackAllCount += 1
									
									# Heal Self Check #
									if dataAttack.effectType == "Heal" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, targetRoom, DATA_ATTACKER) and DATA_ATTACKER.currentHP > 0:
										attackAllCount += 1
										healSelf = True
									
									# Attack/Heal Player Check #
									if DATA_ATTACKER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, targetRoom, DATA_PLAYER) and DATA_PLAYER.currentHP > 0:
										if (dataAttack.effectType == "Damage" and DATA_PLAYER not in DATA_ATTACKER.groupList) or (dataAttack.effectType == "Heal" and DATA_PLAYER in DATA_ATTACKER.groupList):
											attackAllCount += 1
											attackPlayer = True
											
									# Attack Hits No Targets #
									if attackAllCount == 0:
										messageType = "Spell Hits No Targets"
								
								# Heal Self & Attack/Heal Player #
								if healSelf : attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, DATA_ATTACKER, dataAttack, 0, None, INTERFACE_IMAGE_DICT, {"Attack All Count":attackAllCount})
								if attackPlayer : attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, DATA_PLAYER, dataAttack, tempRange, tempDir, INTERFACE_IMAGE_DICT, {"Attack All Count":attackAllCount})
								
								# Player Killed Check #
								if DATA_PLAYER.currentHP <= 0:
									DATA_PLAYER.killPlayer(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem])
									killPlayerCheck = True
								
								# Attack All Entities In Room #
								if len(targetRoom.mobList) > 0:
									for rNum, targetEntity in enumerate(targetRoom.mobList):
										if DATA_ATTACKER != targetEntity and DATA_ATTACKER.currentHP > 0 and targetEntity.currentHP > 0 \
										and ((dataAttack.effectType == "Damage" and targetEntity not in DATA_ATTACKER.groupList) or (dataAttack.effectType == "Heal" and targetEntity in DATA_ATTACKER.groupList)):
											attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, targetEntity, dataAttack, tempRange, tempDir, INTERFACE_IMAGE_DICT, {"Attack All Count":attackAllCount, "Current Mob Index":rNum})
											
											# Defender HP < 0 Check #
											if dataAttack.effectType != "Heal" and targetEntity.currentHP <= 0 and targetEntity not in DEL_MOB_LIST:
												DEL_MOB_LIST.append(targetEntity)
												
												# Messages #
												if True:
													if DATA_ATTACKER.objectType == "Player" or DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, targetEntity):
														Console.addDisplayLineToDictList(targetEntity.defaultTitle + " is DEAD!", targetEntity.defaultTitleColorCode + "8w1y")
													else:
														distanceToPlayer, dirToPlayer, toPlayerMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, targetRoom, DATA_PLAYER, 3)
														if distanceToPlayer != -1 and distanceToPlayer > 0 and toPlayerMessage == None:
															Console.addDisplayLineToDictList("You hear a death cry to the " + oppositeDirDict[dirToPlayer] + ".")
												
										if DATA_ATTACKER.currentHP <= 0:
											break
									
							# Target Self (Heal Skills) #
							elif dataAttack.currentCount == "Self":
								attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, DATA_ATTACKER, dataAttack, 0, None, INTERFACE_IMAGE_DICT)
							
						# Target Room Attack #
						elif dataAttack.targetType == "Room":
							dataAttack.flags["Timer"] = 0
							if "Room Ticks" not in dataAttack.flags : dataAttack.flags["Room Ticks"] = 5
							dataAttack.flags["Attacker Data"] = DATA_ATTACKER
							targetRoom.updateSkill = dataAttack
							
							# (Debug) Print Attack Data #
							if False:
								if DATA_ATTACKER.objectType == "Player" : print("Player: " + dataAttack.idSkill)
								else : print(DATA_ATTACKER.defaultTitle + ": " + dataAttack.idSkill)
							
						# Post-Attack Data (Subtract MP, Cooldown Timer, Counter Attack Check) #
						if True:
							
							# Subtract MP #
							if dataAttack.mpCost > 0:
								DATA_ATTACKER.currentMP -= dataAttack.mpCost
							
							# Cooldown Timer #
							if DATA_ATTACKER.currentAction != None:
								if DATA_ATTACKER.currentAction["Type"] == "Stumbling" : DATA_ATTACKER.currentAction["Timer"] = dataAttack.cooldownTimer + 2.0
								else : DATA_ATTACKER.currentAction = {"Type":"Attack Cooldown", "Timer":dataAttack.cooldownTimer, "Attack Data":dataAttack}
								clearActionCheck = False
								
							# Player/Attacker HP < 0 Checks #
							if True:
									
								# Player HP < 0 Check #
								if DATA_PLAYER.currentHP <= 0:
									DATA_PLAYER.killPlayer(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem])
									killPlayerCheck = True
									
								# Attacker HP < 0 Check (Counter Attack Check) #
								if DATA_ATTACKER.currentHP <= 0:
									if DATA_ATTACKER.objectType == "Player":
										DATA_PLAYER.killPlayer(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem])
										killPlayerCheck = True

									elif DATA_ATTACKER.objectType == "Mob" and DATA_ATTACKER not in DEL_MOB_LIST:
										DEL_MOB_LIST.append(DATA_ATTACKER)
										
										# Messages #
										if dataDefender != None:
											if dataDefender.objectType == "Player" or DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, dataDefender):
												Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " is DEAD!", DATA_ATTACKER.defaultTitleColorCode + "8w1y")
											else:
												distanceToPlayer, dirToPlayer, toPlayerMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerRoom, DATA_PLAYER, 3)
												if distanceToPlayer != -1 and distanceToPlayer > 0 and toPlayerMessage == None:
													Console.addDisplayLineToDictList("You hear a death cry to the " + oppositeDirDict[dirToPlayer] + ".")
							
						# Initiate Attacker Attack Animation (Double White Fill/Flash) #
						if not killPlayerCheck:
							DATA_ATTACKER.animationDict["Attack"] = {"Timer":5, "Timer Start":5, "Current Step":0, "Max Step":2}
							
							# Update Draw Data #
							if DATA_ATTACKER.objectType == "Player" or DATA_ATTACKER in DATA_PLAYER.groupList:
								Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
							else : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
							
				# Update Screen Data #
				Config.DRAW_SCREEN_DICT["Player Stats"] = True
								
			# Parry & Dodge #
			elif DATA_ATTACKER.currentAction["Type"] in ["Parrying", "Dodging"]:
				
				# Successful Dodge #
				if DATA_ATTACKER.currentAction["Type"] == "Dodging" and "Successful Dodge" in DATA_ATTACKER.currentAction:
					DATA_ATTACKER.currentAction = {"Type":"Attack Cooldown", "Timer":5.0}
				
				# Failed Dodge/Parry #
				else:
					DATA_ATTACKER.currentAction = {"Type":"Attack Cooldown", "Timer":3.0}
					messageType = "Lose Balance"
					clearActionCheck = False
			
			# Reload #
			elif DATA_ATTACKER.currentAction["Type"] == "Reloading" and "Target Weapon" in DATA_ATTACKER.currentAction and "Target Ammo" in DATA_ATTACKER.currentAction:
				DATA_ATTACKER.currentAction["Target Weapon"].reloadWeapon(DATA_ATTACKER, DATA_ATTACKER.currentAction["Target Ammo"])
				
			# Reload Weapon Or Remove Ranged Weapon If No More Ammo #
			elif DATA_ATTACKER.currentAction["Type"] in ["Attack Cooldown", "Stumbling"] and DATA_ATTACKER.objectType == "Mob" and "Attack Data" in DATA_ATTACKER.currentAction and (DATA_ATTACKER.currentAction["Attack Data"].idNum == -1 or "Ammo Required" in DATA_ATTACKER.currentAction["Attack Data"].flags):
				
				# Get Data #
				if True:
					targetAmmo = None
					heldAmmoTypeList = []
					for tempItem in DATA_ATTACKER.inventoryList:
						if tempItem.type == "Ammo" and tempItem.flags["Ammo Type"] not in heldAmmoTypeList:
							heldAmmoTypeList.append(tempItem.flags["Ammo Type"])
					
					if DATA_ATTACKER.dominantHand == "Left" : strOffhand = "Right Hand"
					else : strOffhand = "Left Hand"
				
				# Primary Hand Check #
				if DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"] != None and DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"].type == "Weapon" and DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"].flags["Weapon Type"] == "Ranged" \
				and (DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"].flags["Loaded Ammo Object"] == None or DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"].flags["Loaded Ammo Object"].flags["Quantity"] <= 0):
				
					# Reload Wewapon #
					if DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"].flags["Ammo Type"] in heldAmmoTypeList:
						
						# Get Weapon & Ammo Data #
						if True:
							targetReloadWeapon = DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"]
							for tempItem in DATA_ATTACKER.inventoryList:
								if tempItem.type == "Ammo" and tempItem.flags["Ammo Type"] == targetReloadWeapon.flags["Ammo Type"]:
									targetAmmo = tempItem
									break
								
						# Reload #
						if targetReloadWeapon != None and targetAmmo != None:
						
							# Get Reload Amount #
							if targetReloadWeapon.flags["Loaded Ammo Object"] == None : reloadAmount = targetReloadWeapon.flags["Magazine Size"]
							else : reloadAmount = targetReloadWeapon.flags["Magazine Size"] - targetReloadWeapon.flags["Loaded Ammo Object"].flags["Quantity"]
							if reloadAmount > targetAmmo.flags["Quantity"] : reloadAmount = targetAmmo.flags["Quantity"]
							reloadTime = reloadAmount * targetAmmo.flags["Reload Time"]
							
							DATA_ATTACKER.currentAction = {"Type":"Reloading", "Timer":reloadTime, "Target Weapon":targetReloadWeapon, "Target Ammo":targetAmmo}
							clearActionCheck = False
							
					# Unwield Weapon #
					else:
						DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"].flags["Loaded Ammo Object"] = None
						targetRemoveWeapon = DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"]
						DATA_ATTACKER.addItemToInventory(targetRemoveWeapon, False)
						DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand + " Hand"] = None
					
				# Offhand Hand Check #
				if (DATA_ATTACKER.currentAction == None or DATA_ATTACKER.currentAction["Type"] in ["Attack Cooldown", "Stumbling"]) and DATA_ATTACKER.gearDict[strOffhand] != None and DATA_ATTACKER.gearDict[strOffhand].type == "Weapon" and DATA_ATTACKER.gearDict[strOffhand].flags["Weapon Type"] == "Ranged" \
				and (DATA_ATTACKER.gearDict[strOffhand].flags["Loaded Ammo Object"] == None or DATA_ATTACKER.gearDict[strOffhand].flags["Loaded Ammo Object"].flags["Quantity"] <= 0):
					
					# Reload Weapon #
					if DATA_ATTACKER.gearDict[strOffhand].flags["Ammo Type"] in heldAmmoTypeList:
					
						# Get Weapon & Ammo Data #
						if True:
							targetReloadWeapon = DATA_ATTACKER.gearDict[strOffhand]
							for tempItem in DATA_ATTACKER.inventoryList:
								if tempItem.type == "Ammo" and tempItem.flags["Ammo Type"] == targetReloadWeapon.flags["Ammo Type"]:
									targetAmmo = tempItem
									break
								
						# Reload #
						if targetReloadWeapon != None and targetAmmo != None:
						
							# Get Reload Amount #
							if targetReloadWeapon.flags["Loaded Ammo Object"] == None : reloadAmount = targetReloadWeapon.flags["Magazine Size"]
							else : reloadAmount = targetReloadWeapon.flags["Magazine Size"] - targetReloadWeapon.flags["Loaded Ammo Object"].flags["Quantity"]
							if reloadAmount > targetAmmo.flags["Quantity"] : reloadAmount = targetAmmo.flags["Quantity"]
							reloadTime = reloadAmount * targetAmmo.flags["Reload Time"]
							
							DATA_ATTACKER.currentAction = {"Type":"Reloading", "Timer":reloadTime, "Target Weapon":targetReloadWeapon, "Target Ammo":targetAmmo}
							clearActionCheck = False
							
					# Unwield Weapon #
					else:
						DATA_ATTACKER.gearDict[strOffhand].flags["Loaded Ammo Object"] = None
						targetRemoveWeapon = DATA_ATTACKER.gearDict[strOffhand]
						DATA_ATTACKER.addItemToInventory(targetRemoveWeapon, False)
						DATA_ATTACKER.gearDict[strOffhand] = None
						if targetRemoveWeapon != None : targetRemoveWeapon = "Both"
				
			# Tame Mob #
			elif DATA_ATTACKER.currentAction["Type"] == "Taming":
				
				# Tame Checks #
				tameTarget = DATA_ATTACKER.currentAction["Target Mob"]
				if not DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, tameTarget) : messageType = "Taming Target Not There"
				elif len(tameTarget.groupList) > 0 : messageType = "Already In Group"
				elif tameTarget.currentAction != None or tameTarget.combatTarget != None or tameTarget in DATA_PLAYER.mobTargetPlayerCombatList : messageType = "Taming Target Is Busy"
				
				# Tame Animal #
				if messageType == None:
					
					# Get Tame Chance #
					if True:
						tameSkillData = DATA_ATTACKER.skillTreeDict["General Skills"].skillDict["Tame"]
						attackerTameChance = int(tameSkillData.learnPercent)
						defenderResistChance = int(round(tameTarget.statDict["Spirit"] * .45) + round(tameTarget.statDict["Strength"] * .45))
						tameChance = attackerTameChance - defenderResistChance
						
					# Successful Tame #
					if random.randrange(100) <= tameChance:
					
						# Add Target Mob To Others' In Group's List #
						for tempMob in DATA_ATTACKER.groupList:
							if tameTarget not in tempMob.groupList : tempMob.groupList.append(tameTarget)
							if tempMob not in tameTarget.groupList : tameTarget.groupList.append(tempMob)
					
						# Update Player Group And Target Mob Group Lists #
						if tameTarget not in DATA_ATTACKER.groupList : DATA_ATTACKER.groupList.append(tameTarget)
						if DATA_ATTACKER not in tameTarget.groupList : tameTarget.groupList.append(DATA_ATTACKER)
						messageType = "Tame Target"
						
						# Change Mob's Display Location & Update Draw Data #
						if True:
							playerRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER).roomDict[DATA_PLAYER.currentRoom]
							playerRoom.setEntityScreenLoc(tameTarget, DATA_PLAYER)
							
							Config.DRAW_SCREEN_DICT["Player Stats"] = True
							Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
							Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
							
					# 50% Agro Mob Chance #
					elif random.randrange(100) <= 50:
						if DATA_ATTACKER.objectType == "Player":
							DATA_PLAYER.mobTargetPlayerCombatList.append(tameTarget)
							messageType = "Agro Player"
						elif DATA_ATTACKER.objectType == "Player":
							tameTarget.combatTarget = DATA_ATTACKER
							messageType = "Agro Mob"
					else : messageType = "Tame Failed"
				
			# Messages #
			if True:
				if messageType != None:
					if messageType == "Player Not Enough Mana":
						Console.addDisplayLineToDictList("Your attack fizzles because you don't have enough mana.")
					elif messageType == "Mob Not Enough Mana":
						Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s attack fizzles out.")
					elif messageType == "No Target Found":
						Console.addDisplayLineToDictList("You don't have a target.")
					elif messageType == "Player Attack Hit Door":
						Console.addDisplayLineToDictList("Your attack hits the door.")
					elif messageType == "Player Spell Hit Door":
						Console.addDisplayLineToDictList("Your attack collides with the door.")
					elif messageType == "Target Out Of Range":
						Console.addDisplayLineToDictList("Your target is out of range.")
					elif messageType == "Spell Hits No Targets":
						if DATA_ATTACKER.objectType == "Player":
							Console.addDisplayLineToDictList("Your attack doesn't hit any targets.")
						elif DATA_ATTACKER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER):
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s attack doesn't hit any targets.")
					elif messageType == "Skill Already In Room":
						Console.addDisplayLineToDictList("There is already a skill active there.")
					elif messageType == "Lose Balance":
						Console.addDisplayLineToDictList("You lose balance for a moment.")
					elif DATA_ATTACKER.objectType == "Player" and messageType == "Taming Target Not There":
						Console.addDisplayLineToDictList("Your target is gone.")
					elif messageType == "Already In Group" and tameTarget != None and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, tameTarget):
						Console.addDisplayLineToDictList(tameTarget.defaultTitle + " seems uninterested.")
					elif messageType == "Taming Target Is Busy" and tameTarget != None and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, tameTarget):
						Console.addDisplayLineToDictList(tameTarget.defaultTitle + " is distracted.")
					elif messageType == "Tame Target" and tameTarget != None:
						Console.addDisplayLineToDictList(tameTarget.defaultTitle + " becomes sympathetic to you.")
					elif messageType == "Agro Player" and tameTarget != None:
						Console.addDisplayLineToDictList(tameTarget.defaultTitle + " looks at you with an icy stare.")	
					elif messageType == "Agro Mob" and tameTarget != None:
						Console.addDisplayLineToDictList(tameTarget.defaultTitle + " looks at " + DATA_ATTACKER.defaultTitle + " with an icy stare.")
					elif messageType == "Tame Failed" and tameTarget != None:
						Console.addDisplayLineToDictList(tameTarget.defaultTitle + " seems uninterested.")
					
				elif not attackCheck:
					if DATA_ATTACKER.objectType == "Player":
						if DATA_ATTACKER.currentAction["Type"] == "Defending" : Console.addDisplayLineToDictList("You stop defending.")
						elif DATA_ATTACKER.currentAction["Type"] == "Reloading" : Console.addDisplayLineToDictList("*Click*")
						else : Console.addDisplayLineToDictList("You regain balance.")
					
					elif DATA_ATTACKER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER):
						if DATA_ATTACKER.currentAction["Type"] == "Defending" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " stops defending.")
						elif DATA_ATTACKER.currentAction["Type"] == "Reloading" and targetReloadWeapon == None : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " finishes reloading.")
						else : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " regains balance.")
						
						if targetReloadWeapon != None:
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " begins reloading " + targetReloadWeapon.defaultTitle + ".")
						elif targetRemoveWeapon not in [None, "Both"]:
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " stops holding " + targetRemoveWeapon.defaultTitle + ".")
						elif targetRemoveWeapon == "Both":
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " stops holding their weapons.")
						
			if clearActionCheck : DATA_ATTACKER.currentAction = None
			
	# Prepare Mob Attack If Not Busy #
	elif DATA_ATTACKER.objectType == "Mob" and DATA_ATTACKER.currentAction == None:
	
		# Get Data #
		if True:
			parentArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_ATTACKER.currentSolarSystem], DATA_ATTACKER)
			parentRoom = parentArea.roomDict[DATA_ATTACKER.currentRoom]
			dataDefender = None
			mobAttackCheck = True
			
			# Nearby Target Player Data #
			if DATA_ATTACKER in DATA_PLAYER.mobTargetPlayerCombatList:
				targetRange, targetDir, targetMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, parentRoom, DATA_PLAYER, DATA_ATTACKER.getViewRange())
				if targetRange != -1 and targetMessage == None:
					dataDefender = DATA_PLAYER
					
			# Nearby Target Mob Data #
			if dataDefender == None and DATA_ATTACKER.combatTarget != None:
				targetRange, targetDir, targetMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, parentRoom, DATA_ATTACKER.combatTarget, DATA_ATTACKER.getViewRange())
				if targetRange != -1 and targetMessage == None:
					dataDefender = DATA_ATTACKER.combatTarget
					
			# Held Weapon Data #
			mainWeapon = DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"]
			if DATA_ATTACKER.dominantHand == "Left" : strOffhand = "Right Hand"
			else : strOffhand = "Left Hand"
			offhandWeapon = DATA_ATTACKER.gearDict[strOffhand]
		
		if dataDefender != None:
						
			# Get Target Attack #
			if True:
				dataAttack = DATA_ATTACKER.getAttack(dataDefender, parentRoom, targetRange)
				
				# Change Attack Data For Heal Entity Spells #
				if dataAttack not in [None, "Dodge", "Parry"] and dataAttack.targetType == "Entity" and dataAttack.effectType == "Heal":
					dataAttack.currentCount = "Self"
					dataDefender = DATA_ATTACKER
					targetRange = 0
					
			# Check & Initiate Attack #
			if dataAttack != None:
				
				# Dodge & Parry #
				if dataAttack in ["Dodge", "Parry"]:
					if dataAttack == "Dodge" : targetDodge(SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER)
					elif dataAttack == "Parry" : targetParry(SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER)
						
				# Skill Attack #
				else:
					
					# Ranged Attack Ammo Check #
					if (dataAttack.idNum == -1 or "Ammo Required" in dataAttack.flags):
						
						# Dominant Hand Check #
						if mainWeapon != None and mainWeapon.type == "Weapon" and mainWeapon.flags["Weapon Type"] == "Ranged" \
						and (mainWeapon.flags["Loaded Ammo Object"] == None or mainWeapon.flags["Loaded Ammo Object"].flags["Quantity"] <= 0):
							
							# Offhand Check #
							if not (DATA_ATTACKER.dualWieldCheck and "Advanced Combat" in DATA_ATTACKER.skillTreeDict and "Dual Wield" in DATA_ATTACKER.skillTreeDict["Advanced Combat"].skillDict) \
							or (offhandWeapon != None and offhandWeapon.type == "Weapon" and offhandWeapon.flags["Weapon Type"] == "Ranged" \
							and (offhandWeapon.flags["Loaded Ammo Object"] == None or offhandWeapon.flags["Loaded Ammo Object"].flags["Quantity"] <= 0)):
								mobAttackCheck = False
								
					# Initiate Attack #
					if mobAttackCheck and dataDefender != None and targetRange != -1 and targetMessage == None:
						DATA_ATTACKER.currentAction = {"Type":"Attacking", "Timer":dataAttack.attackTimer, "Action Bar Timer":0, "Attack Data":dataAttack}
						if dataDefender.objectType == "Player" : DATA_ATTACKER.currentAction["Mob Target"] = "Player"
						elif dataDefender.objectType == "Mob" : DATA_ATTACKER.currentAction["Mob Target"] = "Mob"
						if dataAttack.targetType == "Room" and dataAttack.effectType == "Heal" : DATA_ATTACKER.currentAction["Mob Target"] = "Mob"
						
						# Messages #
						if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
							if dataAttack.targetSkillTree in ["Basic Magic", "Advanced Magic"] : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " begins casting a spell.")
							elif dataDefender.objectType == "Mob":
								if targetRange == 0 : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " prepares to attack " + dataDefender.defaultTitle + "!")
								else : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " prepares to attack to the " + str(targetDir) + "!")
							elif dataDefender.objectType == "Player" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " prepares to attack you!")

	return DEL_MOB_LIST

def attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_ATTACKER, DATA_DEFENDER, DATA_ATTACK, TARGET_RANGE, TARGET_DIR, INTERFACE_IMAGE_DICT, FLAGS={}):	
	
	# Get Data #
	if True:
	
		# Variables #
		if True:
			hitChance = 10
			missAttackCheck = False
			attackerStumbleOnAttack = False
			defenderResetCurrentAction = False
			defenderDodgeCheck = False
			defenderStumbleCheck = False
			defenderDownCheck = False
			defenderCounterAttackCheck = False
			defenderParryCheck = False
			drawRoomList = []
			
			primaryAttackDamage = 0
			offhandDamage = 0
			defenseBonus = 0
			primaryAttackCheck = True
			dualWieldAttackCheck = False
			dualWieldSkillCheck = ("Advanced Combat" in DATA_ATTACKER.skillTreeDict and "Dual Wield" in DATA_ATTACKER.skillTreeDict["Advanced Combat"].skillDict)
				
			oppositeDirDict = {"North":"South", "East":"West", "South":"North", "West":"East"}
			if "Counter Attack" in FLAGS : strCounter = "counter "
			else : strCounter = ""
			
			defenderRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_DEFENDER.currentSolarSystem], DATA_DEFENDER).roomDict[DATA_DEFENDER.currentRoom]
			attackerArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_ATTACKER.currentSolarSystem], DATA_ATTACKER)
			attackerRoom = attackerArea.roomDict[DATA_ATTACKER.currentRoom]
			
		# Get Defender Held Weapon Data #
		if True:
			
			if DATA_DEFENDER.dominantHand == "Left" : strDefenderOffhand = "Right Hand"
			else : strDefenderOffhand = "Left Hand"
		
			# Dominant Hand #
			defenderHeldWeaponList = []
			defenderHeldWeaponTypeList = []
			if DATA_DEFENDER.gearDict[DATA_DEFENDER.dominantHand+" Hand"] == None:
				defenderHeldWeaponList.append(None)
				defenderHeldWeaponTypeList.append(None)
			else:
				defenderHeldWeaponList.append(DATA_DEFENDER.gearDict[DATA_DEFENDER.dominantHand+" Hand"])
				defenderHeldWeaponTypeList.append(DATA_DEFENDER.gearDict[DATA_DEFENDER.dominantHand+" Hand"].flags["Weapon Type"])
			
			# Offhand #
			if DATA_DEFENDER.dualWieldCheck and "Advanced Combat" in DATA_DEFENDER.skillTreeDict and "Dual Wield" in DATA_DEFENDER.skillTreeDict["Advanced Combat"].skillDict:
				if DATA_DEFENDER.gearDict[strDefenderOffhand] == None:
					defenderHeldWeaponList.append(None)
					defenderHeldWeaponTypeList.append(None)
				else:
					defenderHeldWeaponList.append(DATA_DEFENDER.gearDict[strDefenderOffhand])
					defenderHeldWeaponList.append(DATA_DEFENDER.gearDict[strDefenderOffhand].flags["Weapon Type"])
		
		# Get Defender Skill Data #
		if True:
		
			# Weapon Skill Data #
			defenderTargetWeaponSkillTree = DataSkill.getTargetWeaponSkillTree(defenderHeldWeaponTypeList[0])
			defenderTargetWeaponSkillID = DataSkill.getTargetWeaponSkillID(defenderHeldWeaponTypeList[0])
			defenderTargetWeaponSkill = None
			defenderOffhandWeaponSkill = None
			
			if defenderTargetWeaponSkillTree in DATA_DEFENDER.skillTreeDict and defenderTargetWeaponSkillID in DATA_DEFENDER.skillTreeDict[defenderTargetWeaponSkillTree].skillDict:
				defenderTargetWeaponSkill = DATA_DEFENDER.skillTreeDict[defenderTargetWeaponSkillTree].skillDict[defenderTargetWeaponSkillID]
			if len(defenderHeldWeaponTypeList) > 1:
				defenderOffhandWeaponSkillTree = DataSkill.getTargetWeaponSkillTree(defenderHeldWeaponTypeList[1])
				defenderOffhandWeaponSkillID = DataSkill.getTargetWeaponSkillID(defenderHeldWeaponTypeList[1])
				if defenderOffhandWeaponSkillTree in DATA_DEFENDER.skillTreeDict and defenderOffhandWeaponSkillID in DATA_DEFENDER.skillTreeDict[defenderOffhandWeaponSkillTree].skillDict:
					defenderOffhandWeaponSkill = DATA_DEFENDER.skillTreeDict[defenderOffhandWeaponSkillTree].skillDict[defenderOffhandWeaponSkillID]
		
			# Target Attack Skill Mods #
			defenderPrimaryAttackSkillMod = "Agility"
			defenderOffhandAttackSkillMod = "Agility"
			if defenderHeldWeaponTypeList[0] == "Ranged" : defenderPrimaryAttackSkillMod = "Dexterity"
			if len(defenderHeldWeaponTypeList) > 1 and defenderHeldWeaponTypeList[1] == "Ranged" : defenderOffhandAttackSkillMod = "Dexterity"
			
		# Get Attacker Held Weapon Data #
		if True:
			
			if DATA_ATTACKER.dominantHand == "Left" : strOffhand = "Right Hand"
			else : strOffhand = "Left Hand"
		
			# Dominant Hand #
			heldWeaponList = []
			heldWeaponTypeList = []
			if DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"] == None:
				heldWeaponList.append(None)
				heldWeaponTypeList.append(None)
			else:
				heldWeaponList.append(DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"])
				heldWeaponTypeList.append(DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"].flags["Weapon Type"])
			
			# Offhand #
			if (DATA_ATTACK.idNum == -1 and dualWieldSkillCheck and DATA_ATTACKER.dualWieldCheck) \
			or ("Dual Wield Only" in DATA_ATTACK.flags or "Required Weapon Type List" in DATA_ATTACK.flags):
				if DATA_ATTACKER.gearDict[strOffhand] == None:
					heldWeaponList.append(None)
					heldWeaponTypeList.append(None)
				else:
					heldWeaponList.append(DATA_ATTACKER.gearDict[strOffhand])
					heldWeaponTypeList.append(DATA_ATTACKER.gearDict[strOffhand].flags["Weapon Type"])
				dualWieldAttackCheck = True
				
			# Attack Descriptor Strings #
			if True:
				strAttackDescriptor = "attack"
				strOffhandAttackDescriptor = "attack"
				if DATA_ATTACK.effectType == "Heal" : strAttackDescriptor = "heal"
				elif DATA_ATTACK.weaponDamage == False and DATA_ATTACK.targetSkillTree in ["Basic Magic", "Advanced Magic"] : strAttackDescriptor = "spell"
				elif DATA_ATTACK.weaponDamage:
					
					# Primary Attack Descriptor #
					if heldWeaponTypeList[0] == None : strAttackDescriptor = "punch"
					elif heldWeaponTypeList[0] == "Sword" : strAttackDescriptor = "slash"
					elif heldWeaponTypeList[0] == "Lance" : strAttackDescriptor = "pierce"
					elif heldWeaponTypeList[0] == "Bludgeon" : strAttackDescriptor = "bash"
					elif heldWeaponTypeList[0] == "Shield" : strAttackDescriptor = "bash"
					elif heldWeaponTypeList[0] == "Ranged" : strAttackDescriptor = "shot"
					
					# Offhand Attack Descriptor #
					if len(heldWeaponTypeList) > 1:
						if heldWeaponTypeList[1] == None : strOffhandAttackDescriptor = "punch"
						elif heldWeaponTypeList[1] == "Sword" : strOffhandAttackDescriptor = "slash"
						elif heldWeaponTypeList[1] == "Lance" : strOffhandAttackDescriptor = "stab"
						elif heldWeaponTypeList[1] == "Bludgeon" : strOffhandAttackDescriptor = "bash"
						elif heldWeaponTypeList[1] == "Shield" : strOffhandAttackDescriptor = "bash"
						elif heldWeaponTypeList[1] == "Ranged" : strOffhandAttackDescriptor = "shot"
					
		# Get Attacker Skill Data #
		if True:
			attackerSkillData = None
			if DATA_ATTACK.idNum != -1 and DATA_ATTACK.targetSkillTree in DATA_ATTACKER.skillTreeDict and DATA_ATTACK.idSkill in DATA_ATTACKER.skillTreeDict[DATA_ATTACK.targetSkillTree].skillDict:
				attackerSkillData = DATA_ATTACKER.skillTreeDict[DATA_ATTACK.targetSkillTree].skillDict[DATA_ATTACK.idSkill]
			
			# Weapon Skill Data #
			targetWeaponSkillTree = DataSkill.getTargetWeaponSkillTree(heldWeaponTypeList[0])
			targetWeaponSkillID = DataSkill.getTargetWeaponSkillID(heldWeaponTypeList[0])
			targetWeaponSkill = None
			offhandWeaponSkill = None
			
			if targetWeaponSkillTree in DATA_ATTACKER.skillTreeDict and targetWeaponSkillID in DATA_ATTACKER.skillTreeDict[targetWeaponSkillTree].skillDict:
				targetWeaponSkill = DATA_ATTACKER.skillTreeDict[targetWeaponSkillTree].skillDict[targetWeaponSkillID]
			if len(heldWeaponTypeList) > 1:
				offhandWeaponSkillTree = DataSkill.getTargetWeaponSkillTree(heldWeaponTypeList[1])
				offhandWeaponSkillID = DataSkill.getTargetWeaponSkillID(heldWeaponTypeList[1])
				if offhandWeaponSkillTree in DATA_ATTACKER.skillTreeDict and offhandWeaponSkillID in DATA_ATTACKER.skillTreeDict[offhandWeaponSkillTree].skillDict:
					offhandWeaponSkill = DATA_ATTACKER.skillTreeDict[offhandWeaponSkillTree].skillDict[offhandWeaponSkillID]
		
			# Target Attack Skill Mods #
			primaryAttackSkillMod = "Strength"
			offhandAttackSkillMod = "Strength"
			if heldWeaponTypeList[0] == "Ranged" : primaryAttackSkillMod = "Dexterity"
			if len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] == "Ranged" : offhandAttackSkillMod = "Dexterity"
			
		# Get Attack Damage #
		if True:
			
			strAttackDescriptorPrimary = "nicks"
			strAttackDescriptorOffhand = "nicks"
			
			# Primary Attack #
			if True:
				
				# Primary Attack Checks #
				if (DATA_ATTACK.targetSkillTree not in ["Basic Magic", "Advanced Magic"] and TARGET_RANGE > 0 and (DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"] == None or DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"].flags["Weapon Range"] < TARGET_RANGE)) \
				or ("Required Weapon Type List" in DATA_ATTACK.flags and heldWeaponTypeList[0] not in DATA_ATTACK.flags["Required Weapon Type List"]):
					primaryAttackCheck = False
					
				# Ammo Check #
				dominantWeaponData = DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"]
				if (DATA_ATTACK.idNum == -1 or "Ammo Required" in DATA_ATTACK.flags) and dominantWeaponData != None and dominantWeaponData.flags["Weapon Type"] == "Ranged" and (dominantWeaponData.flags["Loaded Ammo Object"] == None or dominantWeaponData.flags["Loaded Ammo Object"].flags["Quantity"] <= 0):
					primaryAttackCheck = "Ranged Weapon Is Empty"
		
				# Get Attack Damage #
				if primaryAttackCheck == True:
					primaryAttackDamage = DataPlayer.getAttackPower(DATA_ATTACKER, DATA_ATTACK, "Primary Attack")
					
					# Attack All Check (Divide Damage By Defender Count) #
					if "Attack All Count" in FLAGS and FLAGS["Attack All Count"] > 1:
						primaryAttackDamage = int(round(primaryAttackDamage / FLAGS["Attack All Count"]))
					
					# Get Attack Descriptor #
					if True:
						damagePercent = int(primaryAttackDamage / (DATA_DEFENDER.maxHP * .10))
						if damagePercent == 1:
							if strAttackDescriptor == "punch" : strAttackDescriptorPrimary = "bruises"
							elif strAttackDescriptor == "slash" : strAttackDescriptorPrimary = "cuts"
							elif strAttackDescriptor == "stab" : strAttackDescriptorPrimary = "pierces"
							elif strAttackDescriptor == "bash" : strAttackDescriptorPrimary = "bruises"
							elif strAttackDescriptor == "shot" : strAttackDescriptorPrimary = "pierces"
							else : strAttackDescriptorPrimary = "damages"
						elif damagePercent == 2:
							if strAttackDescriptor == "punch" : strAttackDescriptorPrimary = "devastates"
							elif strAttackDescriptor == "slash" : strAttackDescriptorPrimary = "slices"
							elif strAttackDescriptor == "stab" : strAttackDescriptorPrimary = "pierces"
							elif strAttackDescriptor == "bash" : strAttackDescriptorPrimary = "devastates"
							elif strAttackDescriptor == "shot" : strAttackDescriptorPrimary = "pierces"
							else : strAttackDescriptorPrimary = "devastates"
						elif damagePercent == 3:
							if strAttackDescriptor == "punch" : strAttackDescriptorPrimary = "maims"
							elif strAttackDescriptor == "slash" : strAttackDescriptorPrimary = "slices through"
							elif strAttackDescriptor == "stab" : strAttackDescriptorPrimary = "pierces through"
							elif strAttackDescriptor == "bash" : strAttackDescriptorPrimary = "maims"
							elif strAttackDescriptor == "shot" : strAttackDescriptorPrimary = "pierces through"
							else : strAttackDescriptorPrimary = "maims"
						elif damagePercent in [4, 5]:
							strAttackDescriptorPrimary = "MUTILATES"
						elif damagePercent in [6, 7]:
							if strAttackDescriptor in ["punch", "bash"] : strAttackDescriptorPrimary = "DEMOLISHES"
							else : strAttackDescriptorPrimary = "DISEMBOWELS"
						elif damagePercent >= 8:
							if strAttackDescriptor in ["punch", "bash"] : strAttackDescriptorPrimary = "DESTROYS"
							else : strAttackDescriptorPrimary = "EVISCERATES"
						
			# Dual Wield Attack #
			if dualWieldAttackCheck:
				
				# Dual Wield Range Check #
				if (TARGET_RANGE > 0 and (DATA_ATTACKER.gearDict[strOffhand] == None or DATA_ATTACKER.gearDict[strOffhand].flags["Weapon Range"] < TARGET_RANGE)) \
				or ("Required Weapon Type List" in DATA_ATTACK.flags and len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] not in DATA_ATTACK.flags["Required Weapon Type List"]) \
				or ("Required Weapon Type List" in DATA_ATTACK.flags and "Dual Wield Only" not in DATA_ATTACK.flags and primaryAttackCheck in [True, "Ranged Weapon Is Empty"]):
					dualWieldAttackCheck = False
					
				# Ammo Check #
				offhandWeaponData = DATA_ATTACKER.gearDict[strOffhand]
				if (DATA_ATTACK.idNum == -1 or "Ammo Required" in DATA_ATTACK.flags) and offhandWeaponData != None and offhandWeaponData.flags["Weapon Type"] == "Ranged" and (offhandWeaponData.flags["Loaded Ammo Object"] == None or offhandWeaponData.flags["Loaded Ammo Object"].flags["Quantity"] <= 0):
					dualWieldAttackCheck = "Ranged Weapon Is Empty"
					
				if dualWieldAttackCheck == True:
					offhandDamage = DataPlayer.getAttackPower(DATA_ATTACKER, DATA_ATTACK, "Offhand Attack")
					
					# Attack All Check (Divide Damage By Defender Count) #
					if "Attack All Count" in FLAGS and FLAGS["Attack All Count"] > 1:
						offhandDamage = int(round(offhandDamage / FLAGS["Attack All Count"]))
					
					# Get Attack Descriptor #
					if True:
						offhandDamagePercent = int(offhandDamage / (DATA_DEFENDER.maxHP * .10))
						if offhandDamagePercent == 1:
							if strOffhandAttackDescriptor == "punch" : strAttackDescriptorOffhand = "bruises"
							elif strOffhandAttackDescriptor == "slash" : strAttackDescriptorOffhand = "cuts"
							elif strOffhandAttackDescriptor == "stab" : strAttackDescriptorOffhand = "pierces"
							elif strOffhandAttackDescriptor == "bash" : strAttackDescriptorOffhand = "bruises"
							elif strOffhandAttackDescriptor == "shot" : strAttackDescriptorOffhand = "pierces"
							else : strAttackDescriptorOffhand = "damages"
						elif offhandDamagePercent == 2:
							if strOffhandAttackDescriptor == "punch" : strAttackDescriptorOffhand = "devastates"
							elif strOffhandAttackDescriptor == "slash" : strAttackDescriptorOffhand = "slices"
							elif strOffhandAttackDescriptor == "stab" : strAttackDescriptorOffhand = "pierces"
							elif strOffhandAttackDescriptor == "bash" : strAttackDescriptorOffhand = "devastates"
							elif strOffhandAttackDescriptor == "shot" : strAttackDescriptorOffhand = "pierces"
							else : strAttackDescriptorOffhand = "devastates"
						elif offhandDamagePercent == 3:
							if strOffhandAttackDescriptor == "punch" : strAttackDescriptorOffhand = "maims"
							elif strOffhandAttackDescriptor == "slash" : strAttackDescriptorOffhand = "slices through"
							elif strOffhandAttackDescriptor == "stab" : strAttackDescriptorOffhand = "pierces through"
							elif strOffhandAttackDescriptor == "bash" : strAttackDescriptorOffhand = "maims"
							elif strOffhandAttackDescriptor == "shot" : strAttackDescriptorOffhand = "pierces through"
							else : strAttackDescriptorOffhand = "maims"
						elif offhandDamagePercent in [4, 5]:
							strAttackDescriptorOffhand = "MUTILATES"
						elif offhandDamagePercent in [6, 7]:
							if strOffhandAttackDescriptor in ["punch", "bash"] : strAttackDescriptorOffhand = "DEMOLISHES"
							else : strAttackDescriptorOffhand = "DISEMBOWELS"
						elif offhandDamagePercent >= 8:
							if strOffhandAttackDescriptor in ["punch", "bash"] : strAttackDescriptorOffhand = "DESTROYS"
							else : strAttackDescriptorOffhand = "EVISCERATES"
	
	# Miss Attack/Dodge Roll #
	if DATA_ATTACKER != DATA_DEFENDER and DATA_ATTACK.effectType != "Heal" \
	and not (DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] in ["Parrying", "Stumbling", "Down"]):
	
		# Get Defender Speed Data #
		if True:
			
			# Get Data #
			if True:
				defenderSpeed = 0
				
				# Wear Weight Penalty #
				defenderWearWeight = 0
				for gearSlot in DATA_DEFENDER.gearDict:
					if DATA_DEFENDER.gearDict[gearSlot] != None:
						defenderWearWeight += DATA_DEFENDER.gearDict[gearSlot].getWeight()
			
			# 1 - Defender Agility Bonus #
			defenderSpeed += DATA_DEFENDER.statDict["Agility"]
			
			# 2 - Dodge & Busy Bonus/Penalty #
			if DATA_DEFENDER.currentAction != None:
				if DATA_DEFENDER.currentAction["Type"] == "Dodging" and "Basic Combat" in DATA_DEFENDER.skillTreeDict and "Dodge" in DATA_DEFENDER.skillTreeDict["Basic Combat"].skillDict:
					defenderSpeed += (DATA_DEFENDER.skillTreeDict["Basic Combat"].skillDict["Dodge"].learnPercent * (DATA_DEFENDER.statDict["Agility"] / 100.0))
				else : defenderSpeed -= 30 # Defender Dodge Penalty If Doing Something Other Than Dodging
				
			# 3 - Wear Weight Penalty #
			defenderWearWeight -= DATA_DEFENDER.statDict["Strength"]
			if defenderWearWeight > 0:
				defenderSpeed -= (defenderWearWeight / 5.0)
				
			defenderSpeed = int(round(defenderSpeed))
			
		# Get Attacker Speed Data #
		if True:
			
			# Get Data #
			if True:
				attackerSpeed = 0
				
				# Wear Weight Penalty #
				attackerWearWeight = 0
				for gearSlot in DATA_ATTACKER.gearDict:
					if DATA_ATTACKER.gearDict[gearSlot] != None:
						attackerWearWeight += DATA_ATTACKER.gearDict[gearSlot].getWeight()
			
			# 1 - Attacker Agility/Dexterity/Spirit Bonus #
			if True:
				
				attackerStatBonus = 0
				
				# Weapon Damage Attacks (Agility/Dexterity) #
				if DATA_ATTACK.weaponDamage:
					
					# Single Hand Attack #
					if primaryAttackCheck == True and dualWieldAttackCheck != True:
						attackerStatBonus += DATA_ATTACKER.statDict[primaryAttackSkillMod]
					elif primaryAttackCheck != True and dualWieldAttackCheck == True:
						attackerStatBonus += DATA_ATTACKER.statDict[offhandAttackSkillMod]
					
					# Dual Wield Attack #
					elif primaryAttackCheck == True and dualWieldAttackCheck == True:
						attackerStatBonus += (DATA_ATTACKER.statDict[primaryAttackSkillMod] * .50)
						attackerStatBonus += (DATA_ATTACKER.statDict[offhandAttackSkillMod] * .50)
				
				# Non-Weapon Damage Attacks (Spirit) #
				elif attackerSkillData != None:
					attackerStatBonus += DATA_ATTACKER.statDict["Spirit"]
					
				attackerSpeed += attackerStatBonus
				
			# 2 - Attack Speed Bonus #
			if True:
			
				# Basic Attack #
				attackSpeedBonus = 0
				if DATA_ATTACK.idNum == -1:
					
					# Single Weapon Speed Bonus #
					if primaryAttackCheck == True and dualWieldAttackCheck != True:
						attackSpeedBonus += DATA_ATTACKER.statDict[primaryAttackSkillMod] # Stat Bonus #
						if targetWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (targetWeaponSkill.learnPercent / 100.0) # Weapon Skill % #
						
					# Single Weapon Speed Bonus (Offhand) #
					elif primaryAttackCheck != True and dualWieldAttackCheck == True:
						attackSpeedBonus += DATA_ATTACKER.statDict[offhandAttackSkillMod] # Stat Bonus #
						if offhandWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (offhandWeaponSkill.learnPercent / 100.0) # Weapon Skill % #
						
					# Dual Wield Attack Bonus #
					elif primaryAttackCheck == True and dualWieldAttackCheck == True:
						attackSpeedBonus += (DATA_ATTACKER.statDict[primaryAttackSkillMod] * .50) # Stat Bonus #
						attackSpeedBonus += (DATA_ATTACKER.statDict[offhandAttackSkillMod] * .50) # Stat Bonus #
						
						if targetWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (targetWeaponSkill.learnPercent / 100.0) # Weapon Skill % #
						if offhandWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (offhandWeaponSkill.learnPercent / 100.0) # Weapon Skill % #
						
				# Skill Attack #
				elif attackerSkillData != None:
				
					# Attack Speed On Weapon Damage Skills Is Multiplied By Weapon Skill Percent #
					if DATA_ATTACK.weaponDamage:
					
						# Attack Speed #
						attackSpeedBonus += (DATA_ATTACK.attackSpeed * .50) # 50% Attack Speed Is Given To The Attacker For Free
						attackSpeedBonus += ((DATA_ATTACK.attackSpeed * .50) * (attackerSkillData.learnPercent / 100.0))
					
						# Single Weapon Attack Bonus #
						if primaryAttackCheck == True and dualWieldAttackCheck != True:
						
							# Weapon Speed Ratio #
							if heldWeaponList[0] != None : attackSpeedBonus = attackSpeedBonus * heldWeaponList[0].flags["Attack Speed Ratio"]
							else : attackSpeedBonus = attackSpeedBonus * (DATA_ATTACKER.statDict[primaryAttackSkillMod] / 100.0)
							
							# Weapon Skill % #
							if targetWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (targetWeaponSkill.learnPercent / 100.0)
							
						# Single Weapon Attack Bonus (Offhand) #
						elif primaryAttackCheck != True and dualWieldAttackCheck == True and len(heldWeaponList) > 1:
						
							# Weapon Speed Ratio #
							if heldWeaponList[1] != None : attackSpeedBonus = attackSpeedBonus * heldWeaponList[1].flags["Attack Speed Ratio"]
							else : attackSpeedBonus = attackSpeedBonus * (DATA_ATTACKER.statDict[offhandAttackSkillMod] / 100.0)
							
							# Weapon Skill % #
							if offhandWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (offhandWeaponSkill.learnPercent / 100.0)
							
						# Dual Wield Attack Bonus #
						elif primaryAttackCheck == True and dualWieldAttackCheck == True and len(heldWeaponList) > 1:
							
							# Weapon Speed Ratio #
							if heldWeaponList[0] != None : attackSpeedBonus = attackSpeedBonus * heldWeaponList[0].flags["Attack Speed Ratio"]
							else : attackSpeedBonus = attackSpeedBonus * (DATA_ATTACKER.statDict[primaryAttackSkillMod] / 100.0)
							if heldWeaponList[1] != None : attackSpeedBonus = attackSpeedBonus * heldWeaponList[1].flags["Attack Speed Ratio"]
							else : attackSpeedBonus = attackSpeedBonus * (DATA_ATTACKER.statDict[offhandAttackSkillMod] / 100.0)
							
							# Weapon Skill % #
							if targetWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (targetWeaponSkill.learnPercent / 100.0)
							if offhandWeaponSkill != None : attackSpeedBonus = attackSpeedBonus * (offhandWeaponSkill.learnPercent / 100.0)
							
					else:
						attackSpeedBonus += (DATA_ATTACK.attackSpeed * (attackerSkillData.learnPercent / 100.0))
						attackSpeedBonus = attackSpeedBonus * (DATA_ATTACKER.statDict["Spirit"] / 100.0)
					
				attackerSpeed += attackSpeedBonus
							
			# 3 - Wear Weight Penalty #
			if DATA_ATTACK.weaponDamage:
				attackerWearWeight -= DATA_ATTACKER.statDict["Strength"]
				if attackerWearWeight > 0:
					attackerSpeed -= int(round((attackerWearWeight / 5.0)))
					
			attackerSpeed = int(round(attackerSpeed))
			
		# Miss Attack Roll #
		if True:
			dodgeChance = (defenderSpeed - attackerSpeed)
			if dodgeChance < 4 : dodgeChance = 4
			
			# (Debug) Print Defender Dodge Chance #
			if False:
				if DATA_DEFENDER.objectType == "Player" : strDefenderTitle = "Player"
				else : strDefenderTitle = DATA_DEFENDER.defaultTitle
				print(strDefenderTitle + " Dodge Chance: " + str(dodgeChance) + "%")
			
			# Successful Dodge #
			if random.randrange(100) <= dodgeChance:
				missAttackCheck = True
				if DATA_DEFENDER.currentAction != None and "Successful Dodge" not in DATA_DEFENDER.currentAction:
					DATA_DEFENDER.currentAction["Successful Dodge"] = True
				
				# Attacker Stumble (Max Chance: 80%) #
				if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Dodging":
					stumbleChance = int(round(30 + (DATA_DEFENDER.skillTreeDict["Basic Combat"].skillDict["Dodge"].learnPercent * .50)))
					if random.randrange(100) <= stumbleChance and DATA_ATTACK.currentCount == 1 and TARGET_RANGE == 0 and DATA_ATTACK.weaponDamage \
					and (heldWeaponTypeList[0] != "Ranged" or (dualWieldAttackCheck == True and len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] != "Ranged")):
						DATA_ATTACKER.currentAction = {"Type":"Stumbling"}
						attackerStumbleOnAttack = True
						
			# Failed Dodge #
			elif DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Dodging":
				defenderDodgeCheck = "Failed Dodge"
				DATA_DEFENDER.currentAction = {"Type":"Attack Cooldown", "Timer":5.0}
	
	# Attack (Parry Roll/Assign Damage/Stumble Roll/Counter Attack Roll) #
	if missAttackCheck == False:
	
		# Parry Roll #
		if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Parrying" \
		and (primaryAttackCheck == True or dualWieldAttackCheck == True):
			
			# Defender #
			if True:
			
				# Get Defender Parry Data #
				defenderParryChance = 0
				
				# 1 - Strength Bonus #
				defenderParryChance += DATA_DEFENDER.statDict["Strength"]
			
				# 2 - Parry Skill Bonus #
				defenderParryChance += (DATA_DEFENDER.skillTreeDict["Basic Combat"].skillDict["Parry"].learnPercent * (DATA_DEFENDER.statDict["Strength"] / 100.0))
				
				# 3 - Shield Bonus #
				if defenderHeldWeaponList[0] == "Shield" and defenderTargetWeaponSkill != None:
					defenderParryChance += (25 * (defenderTargetWeaponSkill.learnPercent / 100.0))
				if len(defenderHeldWeaponList) > 1 and defenderHeldWeaponList[1] == "Shield" and defenderOffhandWeaponSkill != None:
					defenderParryChance += (25 * (defenderOffhandWeaponSkill.learnPercent / 100.0))
				
				defenderParryChance = int(round(defenderParryChance))
				
			# Get Attacker Attack Data #
			if True:
			
				attackerAttackChance = 0
				
				# 1 - Strength/Dexterity/Spirit Bonus #
				if True:
					if DATA_ATTACK.weaponDamage:
						if primaryAttackCheck == True and dualWieldAttackCheck != True:
							attackerAttackChance += DATA_ATTACKER.statDict[primaryAttackSkillMod]
							
						elif primaryAttackCheck != True and dualWieldAttackCheck == True:
							attackerAttackChance += DATA_ATTACKER.statDict[offhandAttackSkillMod]
							
						elif primaryAttackCheck == True and dualWieldAttackCheck == True and len(heldWeaponList) > 1:
							attackerAttackChance += (DATA_ATTACKER.statDict[primaryAttackSkillMod] * .50)
							attackerAttackChance += (DATA_ATTACKER.statDict[offhandAttackSkillMod] * .50)
						
					else : attackerAttackChance += DATA_ATTACKER.statDict["Spirit"]
			
				# 2 - Attack Skill Bonus #
				if True:
				
					# Basic Attack #
					attackSkillBonus = 0
					if DATA_ATTACK.idNum == -1:
						
						# Single Weapon Speed Bonus #
						if primaryAttackCheck == True and dualWieldAttackCheck != True and targetWeaponSkill != None:
						
							# Stat Bonus #
							attackSkillBonus += DATA_ATTACKER.statDict[primaryAttackSkillMod]
							
							# Weapon Skill % #
							attackSkillBonus = attackSkillBonus * (targetWeaponSkill.learnPercent / 100.0)
							
						# Single Weapon Speed Bonus (Offhand) #
						elif primaryAttackCheck != True and dualWieldAttackCheck == True and offhandWeaponSkill != None:
						
							# Stat Bonus #
							attackSkillBonus += DATA_ATTACKER.statDict[offhandAttackSkillMod]
							
							# Weapon Skill % #
							attackSkillBonus = attackSkillBonus * (offhandWeaponSkill.learnPercent / 100.0)
							
						# Dual Wield Attack Bonus #
						elif primaryAttackCheck == True and dualWieldAttackCheck == True and offhandWeaponSkill != None and targetWeaponSkill != None and offhandWeaponSkill != None:
							
							# Stat Bonus #
							attackSkillBonus += (DATA_ATTACKER.statDict[primaryAttackSkillMod] * .50)
							attackSkillBonus += (DATA_ATTACKER.statDict[offhandAttackSkillMod] * .50)
							
							# Weapon Skill % #
							attackSkillBonus = attackSkillBonus * (targetWeaponSkill.learnPercent / 100.0)
							attackSkillBonus = attackSkillBonus * (offhandWeaponSkill.learnPercent / 100.0)
							
					# Skill Attack #
					elif attackerSkillData != None:
						if DATA_ATTACK.weaponDamage:
						
							# Single Weapon Speed Bonus #
							if primaryAttackCheck == True and dualWieldAttackCheck != True:
								attackSkillBonus += (attackerSkillData.learnPercent * (DATA_ATTACKER.statDict[primaryAttackSkillMod] / 100.0))
								
								# Weapon Skill % #
								if targetWeaponSkill != None : attackSkillBonus = attackSkillBonus * (targetWeaponSkill.learnPercent / 100.0)
								
							# Single Weapon Speed Bonus (Offhand) #
							elif primaryAttackCheck != True and dualWieldAttackCheck == True:
								attackSkillBonus += (attackerSkillData.learnPercent * (DATA_ATTACKER.statDict[offhandAttackSkillMod] / 100.0))
								
								# Weapon Skill % #
								if offhandWeaponSkill != None : attackSkillBonus = attackSkillBonus * (offhandWeaponSkill.learnPercent / 100.0)
								
							# Dual Wield Attack Bonus #
							elif primaryAttackCheck == True and dualWieldAttackCheck == True:
								attackSkillBonus += ((attackerSkillData.learnPercent * (DATA_ATTACKER.statDict[primaryAttackSkillMod] / 100.0)) * .50)
								attackSkillBonus += ((attackerSkillData.learnPercent * (DATA_ATTACKER.statDict[offhandAttackSkillMod] / 100.0)) * .50)
								
								# Weapon Skill % #
								if targetWeaponSkill != None : attackSkillBonus = attackSkillBonus * (targetWeaponSkill.learnPercent / 100.0)
								if offhandWeaponSkill != None : attackSkillBonus = attackSkillBonus * (offhandWeaponSkill.learnPercent / 100.0)
							
						else : attackSkillBonus += (attackerSkillData.learnPercent * (DATA_ATTACKER.statDict["Spirit"] / 100.0))
						
					attackerAttackChance += attackSkillBonus
					
				attackerAttackChance = int(round(attackerAttackChance))
			
			# (Debug) Print Defender Parry Chance #
			if False:
				if DATA_DEFENDER.objectType == "Player" : strDefenderTitle = "Player"
				else : strDefenderTitle = DATA_DEFENDER.defaultTitle
				parryChance = (defenderParryChance - attackerAttackChance)
				print(strDefenderTitle + " Parry Chance: " + str(parryChance) + "%")
			
			# Successful Parry #
			if random.randrange(100) <= defenderParryChance:
				defenderParryCheck = True
				DATA_DEFENDER.currentAction = None
				defenderResetCurrentAction = True
				
			# Failed Parry #
			else:
				defenderParryCheck = "Failed Parry"
				DATA_DEFENDER.currentAction = {"Type":"Attack Cooldown", "Timer":5.0}
		
		# Assign Damage #
		if defenderParryCheck != True:
		
			# Get Data #
			if True:
		
				# Total Damage #
				totalDamage = primaryAttackDamage
				if dualWieldAttackCheck == True : totalDamage += offhandDamage
		
				# Get Defender Defense #
				if DATA_ATTACKER != DATA_DEFENDER and DATA_ATTACK.effectType == "Damage":
					if DATA_ATTACK.damageType == "Physical" : defenseBonus = DataPlayer.getDefense(DATA_DEFENDER)
					elif DATA_ATTACK.damageType == "Magic" : defenseBonus = DataPlayer.getMagicDefense(DATA_DEFENDER)
					elif DATA_ATTACK.damageType == "Both" : defenseBonus = int((DataPlayer.getDefense(DATA_DEFENDER) * .5) + (DataPlayer.getMagicDefense(DATA_DEFENDER) * .5))
					if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Stumbling": # Defender Stumble Penalty
						defenseBonus = int(defenseBonus / 1.5)
					totalDamage -= defenseBonus
					if totalDamage < 0 : totalDamage = 0
				
			# Assign Damage #
			if DATA_ATTACK.effectType == "Damage":
				DATA_DEFENDER.currentHP -= totalDamage
			elif DATA_ATTACK.effectType == "Heal":
				DATA_DEFENDER.currentHP += totalDamage
				if DATA_DEFENDER.currentHP > DATA_DEFENDER.maxHP : DATA_DEFENDER.currentHP = DATA_DEFENDER.maxHP
		
		# Stumble/Knock Down Defender Roll #
		if defenderParryCheck != True and DATA_DEFENDER.currentHP > 0 and DATA_ATTACKER != DATA_DEFENDER and DATA_ATTACK.effectType != "Heal" and totalDamage > 0 and totalDamage >= (DATA_DEFENDER.maxHP * .08):
			
			# Stumble Check #
			if DATA_DEFENDER.currentAction == None or DATA_DEFENDER.currentAction["Type"] != "Stumbling":
			
				# Get Data #
				if True:
					stumbleChance = -1
					stumbleChance += ((totalDamage / (DATA_DEFENDER.maxHP * .10)) * 20)
					if defenderParryCheck == "Failed Parry" : stumbleChance += 25
					
					if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Parrying":
						stumbleChance -= (DATA_DEFENDER.skillTreeDict["Basic Combat"].skillDict["Parry"] * .50)
					
					stumbleChance = int(round(stumbleChance))
					
				# Stumble Defender #
				if random.randrange(100) <= stumbleChance:
					
					# Message Variables #
					if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Attacking" : defenderStumbleCheck = "Interrupt"
					else : defenderStumbleCheck = "Default"
					
					if DATA_DEFENDER.currentAction == None:
						DATA_DEFENDER.currentAction = {"Type":"Stumbling", "Timer":5.0}
					else:
						DATA_DEFENDER.currentAction["Type"] = "Stumbling"
						DATA_DEFENDER.currentAction["Timer"] = 5.0
						
			# Knock Down Check #
			elif DATA_DEFENDER.currentAction["Type"] == "Stumbling":
			
				# Get Data #
				knockdownChance = 30
				knockdownChance += ((totalDamage / (DATA_DEFENDER.maxHP * .10)) * 10)
				knockdownChance = int(round(knockdownChance))
			
				# Knock Down Defender #
				if random.randrange(100) <= knockdownChance:
					defenderDownCheck = True
					DATA_DEFENDER.currentAction["Type"] = "Down"
					DATA_DEFENDER.currentAction["Timer"] = 6.0
		
		# Defender Counter Attack Roll #
		if DATA_ATTACK.weaponDamage and defenderParryCheck != "Failed Parry" and DATA_DEFENDER.currentHP > 0 and "Counter Attack" not in FLAGS and "Advanced Combat" in DATA_DEFENDER.skillTreeDict and "Counter Attack" in DATA_DEFENDER.skillTreeDict["Advanced Combat"].skillDict \
		and TARGET_RANGE == 0 and heldWeaponTypeList[0] != "Ranged" and not (len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] == "Ranged") \
		and (DATA_DEFENDER.currentAction == None or DATA_DEFENDER.currentAction["Type"] == "Parrying"):
			
			parryBonus = 0
			if DATA_DEFENDER.currentAction != None and DATA_DEFENDER.currentAction["Type"] == "Parrying":
				parryBonus = int(round(DATA_DEFENDER.skillTreeDict["Basic Combat"].skillDict["Parry"].learnPercent))
			if random.randrange(100) <= int(round(DATA_DEFENDER.skillTreeDict["Advanced Combat"].skillDict["Counter Attack"].learnPercent)) + parryBonus:
				defenderCounterAttackCheck = True
		
	# Reduce Ammo Count #
	if DATA_ATTACK.idNum == -1 or "Ammo Required" in DATA_ATTACK.flags:

		# Primary Hand #
		if primaryAttackCheck == True and DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"] != None \
		and DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"].flags["Weapon Type"] == "Ranged" \
		and DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"].flags["Loaded Ammo Object"].flags["Quantity"] > 0:
			DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"].flags["Loaded Ammo Object"].flags["Quantity"] -= 1
			DATA_ATTACKER.currentWeight -= DATA_ATTACKER.gearDict[DATA_ATTACKER.dominantHand+" Hand"].flags["Loaded Ammo Object"].weight
			
		# Off Hand #
		if dualWieldAttackCheck == True and DATA_ATTACKER.gearDict[strOffhand] != None \
		and DATA_ATTACKER.gearDict[strOffhand].flags["Weapon Type"] == "Ranged" \
		and DATA_ATTACKER.gearDict[strOffhand].flags["Loaded Ammo Object"].flags["Quantity"] > 0:
			DATA_ATTACKER.gearDict[strOffhand].flags["Loaded Ammo Object"].flags["Quantity"] -= 1
			DATA_ATTACKER.currentWeight -= DATA_ATTACKER.gearDict[strOffhand].flags["Loaded Ammo Object"].weight
	
	# Remove (Ally) Defender From Attacker & Attacker Group's Group List #
	if DATA_ATTACK.effectType == "Damage":
		if DATA_DEFENDER in DATA_ATTACKER.groupList:
			DATA_DEFENDER.groupList = []
			del DATA_ATTACKER.groupList[DATA_ATTACKER.groupList.index(DATA_DEFENDER)]
			
		if len(DATA_ATTACKER.groupList) > 0:
			for attackerGroupEntity in DATA_ATTACKER.groupList:
				if DATA_DEFENDER in attackerGroupEntity.groupList:
					del attackerGroupEntity.groupList[attackerGroupEntity.groupList.index(DATA_DEFENDER)]
	
	# Messages (Dodge/Attack/Player HP < 0/Reeling/Knocked Down) #
	if True:
	
		# (Debug) Print Attack Data #
		if False:
			if DATA_ATTACKER.objectType == "Player" : print("Player: " + DATA_ATTACK.idSkill)
			else : print(DATA_ATTACKER.defaultTitle + ": " + DATA_ATTACK.idSkill)
	
		# Dodge Message #
		if missAttackCheck == True and (primaryAttackCheck == True or dualWieldAttackCheck == True):
			if DATA_DEFENDER.objectType == "Player":
				if attackerStumbleOnAttack : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " stumbles as you dodge their " + strAttackDescriptor + " with ease.")
				else : Console.addDisplayLineToDictList("You dodge " + DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + ".")
				if defenderResetCurrentAction : Console.addDisplayLineToDictList("You regain balance.")
				
			elif DATA_DEFENDER.objectType == "Mob":
				if DATA_ATTACKER.objectType == "Player":
					if attackerStumbleOnAttack : Console.addDisplayLineToDictList("You stumble as " + DATA_DEFENDER.defaultTitle + " dodges your " + strAttackDescriptor + " with ease.")
					else : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " dodges your " + strAttackDescriptor + ".")
				elif DATA_ATTACKER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
					if TARGET_RANGE > 0 and TARGET_DIR != None : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " shoots to the " + TARGET_DIR + "!")
					elif attackerStumbleOnAttack : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " dodges " + DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + " with ease.")
					else : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " dodges " + DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + ".")
				
		# Attack Message #
		elif missAttackCheck == False or (primaryAttackCheck == "Ranged Weapon Is Empty" or dualWieldAttackCheck == "Ranged Weapon Is Empty"):
			
			# Failed Dodge Message #
			if defenderDodgeCheck == "Failed Dodge":
				if DATA_ATTACKER.objectType == "Player" : Console.addDisplayLineToDictList("Your " + strAttackDescriptor + " finds it's mark.")
				elif DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
					Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + " finds it's mark.")
					
			# Parry Message #
			if defenderParryCheck == True and (primaryAttackCheck == True or dualWieldAttackCheck == True):
				if DATA_ATTACKER.objectType == "Player" : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " parries your " + strAttackDescriptor + ".")
				elif DATA_ATTACKER.objectType == "Mob":
					if DATA_DEFENDER.objectType == "Player" : Console.addDisplayLineToDictList("You parry " + DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + ".")
					elif DATA_DEFENDER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_DEFENDER, DATA_PLAYER):
						Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " parries " + DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + ".")
					
			# Failed Parry Message #
			if defenderParryCheck == "Failed Parry":
				if DATA_ATTACKER.objectType == "Player" : Console.addDisplayLineToDictList("Your " + strAttackDescriptor + " breaks through " + DATA_DEFENDER.defaultTitle + "'s parry!")
				elif DATA_ATTACKER.objectType == "Mob":
					if DATA_DEFENDER.objectType == "Player" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + " breaks through your parry!")
					elif DATA_DEFENDER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_DEFENDER, DATA_PLAYER):
						Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + " breaks through " + DATA_DEFENDER.defaultTitle + "'s parry!")
					
			# Attack Message #
			if defenderParryCheck != True or (primaryAttackCheck == "Ranged Weapon Is Empty" and (dualWieldAttackCheck == False or dualWieldAttackCheck == "Ranged Weapon Is Empty")):
					
				# Player Attack Message #
				if DATA_ATTACKER.objectType == "Player":
					if primaryAttackCheck == "Ranged Weapon Is Empty":
						Console.addDisplayLineToDictList("You pull the trigger and *Click*.", None)
					elif primaryAttackCheck == True and DATA_ATTACKER == DATA_DEFENDER:
						Console.addDisplayLineToDictList("You " + strAttackDescriptor + " yourself! (" + str(primaryAttackDamage) + ")")
					elif primaryAttackCheck == True:
						if DATA_ATTACK.effectType == "Damage" : Console.addDisplayLineToDictList("Your " + strCounter + strAttackDescriptor + " " + strAttackDescriptorPrimary + " " + DATA_DEFENDER.defaultTitle + "! (" + str(primaryAttackDamage) + ")")
						else : Console.addDisplayLineToDictList("You " + strCounter + strAttackDescriptor + " " + DATA_DEFENDER.defaultTitle + "! (" + str(primaryAttackDamage) + ")")
					
					if dualWieldAttackCheck == "Ranged Weapon Is Empty":
						Console.addDisplayLineToDictList("You pull the trigger and *Click*.", None)
					elif dualWieldAttackCheck == True:
						if DATA_ATTACK.effectType == "Damage" : Console.addDisplayLineToDictList("Your offhand " + strCounter + strOffhandAttackDescriptor + " " + strAttackDescriptorOffhand + " " + DATA_DEFENDER.defaultTitle + "! (" + str(offhandDamage) + ")")
						else : Console.addDisplayLineToDictList("You offhand " + strCounter + strOffhandAttackDescriptor + " " + DATA_DEFENDER.defaultTitle + "! (" + str(offhandDamage) + ")")
				
				# Mob Attack Message #
				elif DATA_ATTACKER.objectType == "Mob":
				
					# Same Room Attack #
					if TARGET_RANGE == 0 and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
						if primaryAttackCheck == "Ranged Weapon Is Empty":
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " pulls the trigger and *Click*.", None)
						elif primaryAttackCheck == True and DATA_ATTACKER == DATA_DEFENDER:
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " " + strAttackDescriptor + "s themself! (" + str(primaryAttackDamage) + ")")
						elif primaryAttackCheck == True:
							if DATA_DEFENDER.objectType == "Player":
								if DATA_ATTACK.effectType == "Damage" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s " + strCounter + strAttackDescriptor + " " + strAttackDescriptorPrimary + " you! (" + str(primaryAttackDamage) + ")")
								else : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " " + strCounter + strAttackDescriptor + "s you! (" + str(primaryAttackDamage) + ")")
							elif DATA_DEFENDER.objectType == "Mob":
								if DATA_ATTACK.effectType == "Damage" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s " + strCounter + strAttackDescriptor + " " + strAttackDescriptorPrimary + " " + DATA_DEFENDER.defaultTitle + "! (" + str(primaryAttackDamage) + ")")
								else : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " " + strCounter + strAttackDescriptor + "s " + DATA_DEFENDER.defaultTitle + "! (" + str(primaryAttackDamage) + ")")
					
						if dualWieldAttackCheck == "Ranged Weapon Is Empty":
							Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " pulls the trigger and *Click*.")
						elif dualWieldAttackCheck == True:
							if DATA_DEFENDER.objectType == "Player":
								if DATA_ATTACK.effectType == "Damage" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s offhand " + strCounter + strOffhandAttackDescriptor + " " + strAttackDescriptorOffhand + " you! (" + str(offhandDamage) + ")")
								else : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " offhand " + strCounter + strOffhandAttackDescriptor + "s you! (" + str(offhandDamage) + ")")
							elif DATA_DEFENDER.objectType == "Mob":
								if DATA_ATTACK.effectType == "Damage" : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s offhand " + strCounter + strOffhandAttackDescriptor + " " + strAttackDescriptorOffhand + " " + DATA_DEFENDER.defaultTitle + "! (" + str(offhandDamage) + ")")
								else : Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " offhand " + strCounter + strOffhandAttackDescriptor + "s " + DATA_DEFENDER.defaultTitle + "! (" + str(offhandDamage) + ")")
					
					# Distant Attack #
					elif TARGET_RANGE > 0:
						if DATA_DEFENDER.objectType == "Player":
							
							# Message Data #
							if True:
								strTempEd1 = "ed"
								strTempEd2 = "ed"
								if strAttackDescriptor == "shot" : strTempEd1 = ""
								if strOffhandAttackDescriptor == "shot" : strTempEd2 = ""
							
							if primaryAttackCheck == True : Console.addDisplayLineToDictList("You get " + strCounter + strAttackDescriptor + strTempEd1 + " from the " + oppositeDirDict[TARGET_DIR] + "! (" + str(primaryAttackDamage) + ")")
							if dualWieldAttackCheck == True : Console.addDisplayLineToDictList("You get " + strCounter + strOffhandAttackDescriptor + strTempEd2 + " from the " + oppositeDirDict[TARGET_DIR] + "! (" + str(offhandDamage) + ")")
						
						elif DATA_DEFENDER.objectType == "Mob":
							if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER): # Player In Attacker Room #
								if strAttackDescriptor == "shot" : strAttackDescriptor = "shoot"
								Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " " + strCounter + strAttackDescriptor + "s to the " + TARGET_DIR + "!")
							
							elif DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_DEFENDER, DATA_PLAYER): # Player In Defender Room #
							
								# Message Data #
								if True:
									strTempEd1 = "ed"
									strTempEd2 = "ed"
									if strAttackDescriptor == "shot" : strTempEd1 = ""
									if strOffhandAttackDescriptor == "shot" : strTempEd2 = ""
							
								Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " gets " + strCounter + strAttackDescriptor + strTempEd1 + " from from the " + oppositeDirDict[TARGET_DIR] + "! (" + str(totalDamage) + ")")
								if dualWieldAttackCheck == True : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " gets " + strCounter + strOffhandAttackDescriptor + strTempEd2 + " from from the " + oppositeDirDict[TARGET_DIR] + "! (" + str(offhandDamage) + ")")
			
		# Player HP < 0 Message #
		if missAttackCheck == False and DATA_DEFENDER.objectType == "Player" and DATA_DEFENDER.currentHP <= 0:
			Console.addDisplayLineToDictList("You are DEAD!")
		
		# Reeling Message #
		elif defenderStumbleCheck != False:
			if DATA_DEFENDER.objectType == "Player":
				if defenderStumbleCheck == "Interrupt":
					Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + " interrupts your attack and sends you reeling!")
				elif defenderStumbleCheck == "Default":
					if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_ATTACKER, DATA_PLAYER):
						Console.addDisplayLineToDictList(DATA_ATTACKER.defaultTitle + "'s " + strAttackDescriptor + " sends you reeling!")
					else : Console.addDisplayLineToDictList("You are sent reeling!")
			elif DATA_DEFENDER.objectType == "Mob" and (DATA_ATTACKER.objectType == "Player" or DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_DEFENDER, DATA_PLAYER)):
				Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " is sent reeling!")
		
		# Knocked Down Message #
		elif defenderDownCheck == True:
			if DATA_DEFENDER.objectType == "Player" : Console.addDisplayLineToDictList("You are knocked to the ground!")
			elif DATA_DEFENDER.objectType == "Mob":
				if DATA_ATTACKER.objectType == "Player" : Console.addDisplayLineToDictList("You knock " + DATA_DEFENDER.defaultTitle + " to the ground.")
				elif DATA_ATTACKER.objectType == "Mob" and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_DEFENDER, DATA_PLAYER):
					Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " is knocked to the ground.")
	
	# # # # # # # # #  # # # # # # # # #
	# # # Defender Survives Attack # # #
	# # # # # # # # #  # # # # # # # # #
	if DATA_DEFENDER.currentHP > 0 and DATA_ATTACKER != DATA_DEFENDER and DATA_ATTACK.effectType != "Heal":
		
		# Attacking Group Targets Defender #
		if len(DATA_ATTACKER.groupList) > 0:
			attackerGroupEntityRoom = None
			for attackerGroupEntity in DATA_ATTACKER.groupList:
				if attackerGroupEntity.objectType == "Mob" and attackerGroupEntity.combatTarget == None:
				
					# Get Room Data #
					if attackerGroupEntityRoom == None or not DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, attackerGroupEntityRoom, attackerGroupEntity):
						attackerGroupEntityRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[attackerGroupEntity.currentSolarSystem], attackerGroupEntity).roomDict[attackerGroupEntity.currentRoom]
					tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerGroupEntityRoom, DATA_DEFENDER, attackerGroupEntity.getViewRange())
					
					# Add Defender To Attacking Group's Combat Target #
					addCheck = False
					if tempRange != -1 and tempMessage == None:
						if DATA_DEFENDER.objectType == "Player" and attackerGroupEntity not in DATA_DEFENDER.mobTargetPlayerCombatList:
							DATA_DEFENDER.mobTargetPlayerCombatList.append(attackerGroupEntity)
							addCheck = True
						if DATA_DEFENDER.objectType == "Mob":
							attackerGroupEntity.combatTarget = DATA_DEFENDER
							addCheck = True
						
						# Add Mob To Update Mob List (If Not In It) #
						if attackerGroupEntity not in attackerGroupEntityRoom.updateMobList : attackerGroupEntityRoom.updateMobList.append(attackerGroupEntity)
						
						# Message Data #
						if addCheck == True and DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, attackerGroupEntity):
							if DATA_DEFENDER.objectType == "Player":
								Console.addDisplayLineToDictList(attackerGroupEntity.defaultTitle + " looks at you with an icy stare.")
							elif DATA_DEFENDER.objectType == "Mob":
								if tempRange == 0 : Console.addDisplayLineToDictList(attackerGroupEntity.defaultTitle + " looks at " + DATA_DEFENDER.defaultTitle + " with an icy stare.")
								elif tempRange > 0 : Console.addDisplayLineToDictList(attackerGroupEntity.defaultTitle + " looks " + str(tempDir) + " with an icy stare.")
							
		# Initiate Defender Counter Attack #
		if defenderCounterAttackCheck == True:
			counterAttackData = DataAttack.loadPrefab("Basic Attack")
			attackRound(WINDOW, MOUSE, SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_DEFENDER, DATA_ATTACKER, counterAttackData, TARGET_RANGE, None, INTERFACE_IMAGE_DICT, {"Counter Attack":True})
		
		# Initiate Defender Get Hit Animation (Red Fill/Flash) #
		if missAttackCheck == False and not (DATA_ATTACKER.objectType == "Player" and DATA_ATTACKER.currentHP <= 0):
			DATA_DEFENDER.animationDict["Get Hit"] = {"Timer":7}
			
			# Update Draw Data #
			if DATA_DEFENDER.objectType == "Player" or DATA_DEFENDER in DATA_PLAYER.groupList:
				Config.DRAW_SCREEN_DICT["Update Room Group Entity Surface"] = True
			else : Config.DRAW_SCREEN_DICT["Update Room Entity Surface"] = True
			
	# # # # # # # # # # #  # # # # # # # # # # #
	# # # Defender Does Not Survive Attack # # #
	# # # # # # # # # # #  # # # # # # # # # # #
	elif DATA_DEFENDER.currentHP <= 0 and missAttackCheck == False:
		
		# Defending Player (Clear Group & Target Lists) #
		if DATA_DEFENDER.objectType == "Player":
			
			# Disband Player Group #
			if len(DATA_DEFENDER.groupList) > 0:
				for defenderGroupEntity in DATA_DEFENDER.groupList:
					if DATA_DEFENDER in defenderGroupEntity.groupList:
						del defenderGroupEntity.groupList[defenderGroupEntity.groupList.index(DATA_DEFENDER)]
					defenderGroupEntity.groupList = []
				DATA_DEFENDER.groupList = []
			
			# Remove All Idle Mobs Targeting Player From Update Mob List (Resource Heavy) #
			attackingMobArea = None
			attackingMobRoom = None
			for attackingMob in DATA_DEFENDER.mobTargetPlayerCombatList:
				if not attackingMob.isUpdateMob() and attackingMob.combatTarget == None:
					if attackingMobArea == None or (attackingMob.currentArea != attackingMobArea.idArea or attackingMob.currentAreaRandom != attackingMobArea.idRandom):
						attackingMobArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[attackingMob.currentSolarSystem], attackingMob)
					if attackingMobRoom == None or (attackingMob.currentRoom != attackingMobRoom.idNum):
						attackingMobRoom = attackingMobArea.roomDict[attackingMob.currentRoom]
					
					if attackingMob in attackingMobRoom.updateMobList:
						del attackingMobRoom.updateMobList[attackingMobRoom.updateMobList.index(attackingMob)]
				
			# Clear Player Targets & Mobs Targeting Player #
			DATA_DEFENDER.mobTargetList = []
			DATA_DEFENDER.mobTargetPlayerCombatList = []
		
		# Defending Mob (Set/Clear Next Group Target) #
		elif DATA_DEFENDER.objectType == "Mob":
			
			# Set Next Target & Set Next Group Target #
			if len(DATA_DEFENDER.groupList) > 0:
				playerSetNextTargetCheck = False
				for attackerGroupEntity in ([DATA_ATTACKER] + DATA_ATTACKER.groupList):
					if (DATA_ATTACKER.objectType == "Player" and attackerGroupEntity.objectType == "Player" and len(attackerGroupEntity.mobTargetList) > 0 and DATA_DEFENDER in attackerGroupEntity.mobTargetList) \
					or (attackerGroupEntity.objectType == "Mob" and attackerGroupEntity.combatTarget in [None, DATA_DEFENDER]):
						
						# Clear Old Target #
						if True:
							defenderIsPrimaryTarget = False
							if attackerGroupEntity.objectType == "Player":
								if DATA_DEFENDER == attackerGroupEntity.mobTargetList[0] : defenderIsPrimaryTarget = True
								if DATA_DEFENDER in attackerGroupEntity.mobTargetList : del attackerGroupEntity.mobTargetList[attackerGroupEntity.mobTargetList.index(DATA_DEFENDER)]
								if DATA_DEFENDER in attackerGroupEntity.mobTargetPlayerCombatList : del attackerGroupEntity.mobTargetPlayerCombatList[attackerGroupEntity.mobTargetPlayerCombatList.index(DATA_DEFENDER)]
							elif attackerGroupEntity.objectType == "Mob":
								attackerGroupEntity.combatTarget = None
								
								# Remove Idle Mob From Update Mob List (If In It) #
								if not attackerGroupEntity.isUpdateMob() and attackerGroupEntity in attackerGroupEntityRoom.updateMobList:
									del attackerGroupEntityRoom.updateMobList[attackerGroupEntityRoom.updateMobList.index(attackerGroupEntity)]
							
						# Set Next Target #
						attackerGroupEntityRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[attackerGroupEntity.currentSolarSystem], attackerGroupEntity).roomDict[attackerGroupEntity.currentRoom]
						for defenderGroupEntity in DATA_DEFENDER.groupList:
							if defenderGroupEntity.currentHP > 0:
								defenderRange, defenderDir, defenderMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerGroupEntityRoom, defenderGroupEntity, attackerGroupEntity.getViewRange())
								if defenderRange != -1 and defenderMessage == None:
									
									# Player Attacking Group Member #
									if attackerGroupEntity.objectType == "Player" and playerSetNextTargetCheck == False and defenderIsPrimaryTarget == True and defenderGroupEntity not in attackerGroupEntity.mobTargetList:
										attackerGroupEntity.mobTargetList.append(defenderGroupEntity)
										Console.addDisplayLineToDictList("You shift your focus to " + defenderGroupEntity.defaultTitle + ".")
										playerSetNextTargetCheck = True
									
									# Mob Attacking Group Member #
									elif attackerGroupEntity.objectType == "Mob" and attackerGroupEntity.combatTarget == None:
										attackerGroupEntity.combatTarget = defenderGroupEntity
										
										# Add Mob To Update Mob List (If Not In It) #
										if attackerGroupEntity not in attackerGroupEntityRoom.updateMobList : attackerGroupEntityRoom.updateMobList.append(attackerGroupEntity)
						
										# Message Data #
										if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, attackerGroupEntity):
											if defenderGroupEntity.objectType == "Player" : Console.addDisplayLineToDictList(attackerGroupEntity.defaultTitle + " shifts their focus to you.")
											elif defenderGroupEntity.objectType == "Mob":
												if defenderRange == 0 : Console.addDisplayLineToDictList(attackerGroupEntity.defaultTitle + " shifts their focus to " + defenderGroupEntity.defaultTitle + ".")
												elif defenderRange > 0 : Console.addDisplayLineToDictList(attackerGroupEntity.defaultTitle + " shifts their focus " + str(defenderDir) + ".")
					
			# No Next Target - Clear Combat Target #
			elif len(DATA_DEFENDER.groupList) == 0:
				
				# Attacker #
				if DATA_ATTACKER.objectType == "Player":
					if DATA_DEFENDER in DATA_ATTACKER.mobTargetList : del DATA_ATTACKER.mobTargetList[DATA_ATTACKER.mobTargetList.index(DATA_DEFENDER)]
					if DATA_DEFENDER in DATA_ATTACKER.mobTargetPlayerCombatList : del DATA_ATTACKER.mobTargetPlayerCombatList[DATA_ATTACKER.mobTargetPlayerCombatList.index(DATA_DEFENDER)]
				elif DATA_ATTACKER.objectType == "Mob" and DATA_ATTACKER.combatTarget == DATA_DEFENDER:
					DATA_ATTACKER.combatTarget = None
					
					# Remove Idle Mob From Update Mob List #
					if not DATA_ATTACKER.isUpdateMob() and DATA_ATTACKER.combatTarget == None and DATA_ATTACKER in attackerRoom.mobList:
						del attackerRoom.mobList[attackerRoom.mobList.index(DATA_ATTACKER)]
				
				# Attacker's Group #
				for groupEntity in DATA_ATTACKER.groupList:
					if groupEntity.objectType == "Player":
						if DATA_DEFENDER in groupEntity.mobTargetList : del groupEntity.mobTargetList[groupEntity.mobTargetList.index(DATA_DEFENDER)]
						if DATA_DEFENDER in groupEntity.mobTargetPlayerCombatList : del groupEntity.mobTargetPlayerCombatList[groupEntity.mobTargetPlayerCombatList.index(DATA_DEFENDER)]
					elif groupEntity.objectType == "Mob" and groupEntity.combatTarget == DATA_DEFENDER:
						groupEntity.combatTarget = None
						
						# Remove Idle Mob From Update Mob List #
						groupEntityRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[groupEntity.currentSolarSystem], groupEntity).roomDict[groupEntity.currentRoom]
						if not groupEntity.isUpdateMob() and groupEntity.combatTarget == None and groupEntity in groupEntityRoom.mobList:
							del groupEntityRoom.mobList[groupEntityRoom.mobList.index(groupEntity)]
		
		DATA_DEFENDER.currentAction = None
	
	# Add Attacker To Defender & Defending Group's Combat List If Not In It & Defender Has No Combat Target #
	if DATA_ATTACKER.currentHP > 0 and DATA_ATTACKER != DATA_DEFENDER and DATA_ATTACK.effectType != "Heal":
	
		if DATA_ATTACKER.objectType == "Player":
			
			# Defender Target Player - Player Target Mob List & Mob Target Player List #
			if DATA_DEFENDER.currentHP > 0 and TARGET_RANGE <= DATA_DEFENDER.getViewRange() and DATA_DEFENDER.combatTarget == None:
				if DATA_DEFENDER not in DATA_PLAYER.mobTargetList:
					DATA_PLAYER.mobTargetList.append(DATA_DEFENDER)
				if DATA_DEFENDER not in DATA_PLAYER.mobTargetPlayerCombatList and TARGET_RANGE <= DATA_DEFENDER.getViewRange():
					DATA_PLAYER.mobTargetPlayerCombatList.append(DATA_DEFENDER)
					if TARGET_RANGE == 0 : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " looks at you with an icy stare.")
					
					# Add Idle Defending Mob To Update Mob List #
					if DATA_DEFENDER.objectType == "Mob" and DATA_DEFENDER not in defenderRoom.updateMobList : defenderRoom.updateMobList.append(DATA_DEFENDER)
				
			# Defender Group Target Player #
			if len(DATA_DEFENDER.groupList) > 0:
				for groupMob in DATA_DEFENDER.groupList:
					if groupMob.objectType == "Mob" and groupMob.currentHP > 0 and groupMob not in DATA_ATTACKER.mobTargetPlayerCombatList:
						tempRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[groupMob.currentSolarSystem], groupMob).roomDict[groupMob.currentRoom]
						tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerRoom, tempRoom, groupMob.getViewRange())
						if tempRange != -1 and tempMessage == None:
							DATA_ATTACKER.mobTargetPlayerCombatList.append(groupMob)
							if tempRange == 0 : Console.addDisplayLineToDictList(groupMob.defaultTitle + " looks at you with an icy stare.")
							
							# Add Idle Defending Mob To Update Mob List #
							if groupMob not in tempRoom.updateMobList : tempRoom.updateMobList.append(groupMob)
							
		elif DATA_ATTACKER.objectType == "Mob":
			
			# Defender Target Attacking Mob #
			if DATA_DEFENDER.currentHP > 0 and TARGET_RANGE <= DATA_DEFENDER.getViewRange():
		
				# Mob Attacking Player #
				if DATA_DEFENDER.objectType == "Player":
					if DATA_ATTACKER not in DATA_DEFENDER.mobTargetList:
						DATA_DEFENDER.mobTargetList.append(DATA_ATTACKER)
					
				# Mob Attacking Mob #
				elif DATA_DEFENDER.objectType == "Mob":
					if DATA_DEFENDER.combatTarget == None:
						DATA_DEFENDER.combatTarget = DATA_ATTACKER
						
					# Add Idle Defending Mob To Update Mob List #
					if DATA_DEFENDER not in defenderRoom.updateMobList : defenderRoom.updateMobList.append(DATA_DEFENDER)
					
			# Defender Group Target Attacking Mob #
			if len(DATA_DEFENDER.groupList) > 0:
				for groupEntity in DATA_DEFENDER.groupList:
					if groupEntity.currentHP > 0:
						tempRange, tempDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, attackerRoom, groupEntity, groupEntity.getViewRange())
						if tempRange != -1 and tempMessage == None:
						
							if groupEntity.objectType == "Player" and DATA_ATTACKER not in groupEntity.mobTargetList:
								groupEntity.mobTargetList.append(DATA_ATTACKER)
								#Console.addDisplayLineToDictList("You focus on " + DATA_ATTACKER.defaultTitle + " attacking your group.")
							
							elif groupEntity.objectType == "Mob" and groupEntity.combatTarget == None:
								groupEntity.combatTarget = DATA_ATTACKER
								
								# Add Idle Defending Mob To Update Mob List #
								tempRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[groupEntity.currentSolarSystem], groupEntity).roomDict[groupEntity.currentRoom]
								if groupEntity not in tempRoom.updateMobList : tempRoom.updateMobList.append(groupEntity)
								
								# Message Data #
								if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, groupEntity, DATA_PLAYER):
									if tempRange == 0 : Console.addDisplayLineToDictList(groupEntity.defaultTitle + " looks at " + DATA_ATTACKER.defaultTitle + " with an icy stare.")
									else : Console.addDisplayLineToDictList(groupEntity.defaultTitle + " looks " + str(tempDir) + " with an icy stare.")
		
	# Regain Balance Message (After Successful Parry, Display After Counter Messages) #
	if defenderParryCheck == True and defenderResetCurrentAction:
		if DATA_DEFENDER.objectType == "Player" : Console.addDisplayLineToDictList("You regain balance.")
		elif DATA_DEFENDER.objectType == "Mob" : Console.addDisplayLineToDictList(DATA_DEFENDER.defaultTitle + " regains balance.")

	# Remove Player Action If Target Mob Was Being Tamed #
	if DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Taming" and DATA_PLAYER.currentAction["Target Mob"] == DATA_DEFENDER:
		DATA_PLAYER.currentAction = None
		if DATA_PLAYER.currentHP > 0 : Console.addDisplayLineToDictList("Your concentration on " + DATA_DEFENDER.defaultTitle + " is broken.")
	
	# Initiate Damage Number Animation (Numbers Bounce) #
	if missAttackCheck == False and DATA_PLAYER.currentHP > 0:
	
		# Create Number Image #
		if True:
			xDrawLoc = 0
			numberImageWidth = INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_width()
			numberImageHeight = INTERFACE_IMAGE_DICT["Numbers Outline"][0].get_height()
			numberImage = pygame.Surface([numberImageWidth * len(str(totalDamage)), numberImageHeight], pygame.SRCALPHA, 32)
			for i in str(totalDamage):
				numberImage.blit(INTERFACE_IMAGE_DICT["Numbers Outline"][int(i)], [xDrawLoc, 0])
				xDrawLoc += numberImageWidth
		
		animationDict = {"Timer":150, "Draw Y Loc":0, "Number Image":numberImage, "Bounce Velocity":5.0, "Velocity Decrease":.295, "Bounce Count":0}
		
		# Initiate Damage Number Animation #
		if "Damage Number List" not in DATA_DEFENDER.animationDict : DATA_DEFENDER.animationDict["Damage Number List"] = []
		DATA_DEFENDER.animationDict["Damage Number List"].append(animationDict)
		
		if DATA_DEFENDER.objectType == "Player" or DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, DATA_DEFENDER):
			if "Background Bottom" not in drawRoomList : drawRoomList.append("Background Bottom")
		
	# Draw Room Check #
	if len(drawRoomList) > 0:
		for drawAreaID in drawRoomList:
			if "Room" in Config.DRAW_SCREEN_DICT and drawAreaID not in Config.DRAW_SCREEN_DICT["Room"] : Config.DRAW_SCREEN_DICT["Room"].append(drawAreaID)
			elif "Room" not in Config.DRAW_SCREEN_DICT : Config.DRAW_SCREEN_DICT["Room"] = [drawAreaID]
		
# Utility Functions #
def userAttack(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE):

	# Get Data #
	if True:
		playerRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
		playerAttackRange = DATA_PLAYER.getAttackRange()
		primaryAttackCheck = True
		dualWieldSkillCheck = ("Advanced Combat" in DATA_PLAYER.skillTreeDict and "Dual Wield" in DATA_PLAYER.skillTreeDict["Advanced Combat"].skillDict)
		dualWieldAttackCheck = False
		heldWeaponTypeList = []
		targetMob = None
		messageType = None
				
	# Pre-Attack Checks #
	if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
	elif TARGET_DIR != None and TARGET_ROOM_DISTANCE != None and TARGET_ROOM_DISTANCE > DATA_PLAYER.getViewRange() : messageType = "Room Not In View"
	elif TARGET_DIR != None and TARGET_ROOM_DISTANCE != None and TARGET_ROOM_DISTANCE > playerAttackRange : messageType = "Target Not In Attack Range"
	else:
		
		# Get Target Room #
		if TARGET_DIR == None and TARGET_ROOM_DISTANCE == None : targetMobRoom = playerRoom
		else : targetMobArea, targetMobRoom, messageType = DataWorld.getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, PARENT_AREA, playerRoom, TARGET_DIR, TARGET_ROOM_DISTANCE)
		
		# Get Target Mob #
		if messageType == None:
			
			# Get Target Mob - No Target Input (Input: Attack) #
			if STR_TARGET == None:
				if len(DATA_PLAYER.mobTargetList) == 0 : messageType = "No Target"
				else:
				
					# Range Check #
					firstTargetMob = DATA_PLAYER.mobTargetList[0]
					targetRange, targetDir, rangeMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, firstTargetMob, playerAttackRange)
					if targetRange == -1 : messageType = "Target Not In Attack Range"
					elif rangeMessage == "Door Is Closed" : messageType = "Door Is Closed"
					else : targetMob = firstTargetMob
					
			# Get Target Mob - Target Input #
			else:
				tempMob, mobIndex, mobLoc = GameProcess.getTarget(DATA_PLAYER, targetMobRoom, STR_TARGET, TARGET_INDEX, ["Room Mobs"])
				
				# Door Check #
				if TARGET_DIR != None and TARGET_ROOM_DISTANCE != None:
					targetRange, targetDir, messageType = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, tempMob, playerAttackRange)
					if messageType == None : targetMob = tempMob
				else:
					targetMob = tempMob
					targetRange = 0
				
		# Prepare Attack Data #
		if messageType == None and targetMob != None:
		
			dataAttack = DataAttack.loadPrefab("Basic Attack")
			DATA_PLAYER.currentAction = {"Type":"Attacking", "Timer":dataAttack.attackTimer, "Action Bar Timer":0, "Attack Data":dataAttack}
	
			# Put Defender In Player MobTargetList #
			if targetMob not in DATA_PLAYER.mobTargetList:
				DATA_PLAYER.mobTargetList.insert(0, targetMob)
			elif targetMob != DATA_PLAYER.mobTargetList[0]:
				del DATA_PLAYER.mobTargetList[DATA_PLAYER.mobTargetList.index(targetMob)]
				DATA_PLAYER.mobTargetList.insert(0, targetMob)
				
			# Get Defender Held Weapon Data #
			if True:
				
				if DATA_PLAYER.dominantHand == "Left" : strOffhand = "Right Hand"
				else : strOffhand = "Left Hand"
			
				# Dominant Hand #
				if DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"] == None : heldWeaponTypeList.append(None)
				else : heldWeaponTypeList.append(DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"].flags["Weapon Type"])
				
				# Offhand #
				if (dataAttack.idNum == -1 and dualWieldSkillCheck and DATA_PLAYER.dualWieldCheck) \
				or ("Dual Wield Only" in dataAttack.flags or "Required Weapon Type List" in dataAttack.flags):
					if DATA_PLAYER.gearDict[strOffhand] == None : heldWeaponTypeList.append(None)
					else : heldWeaponTypeList.append(DATA_PLAYER.gearDict[strOffhand].flags["Weapon Type"])
					dualWieldAttackCheck = True
					
					# Get Attack Data # 
					if dataAttack.weaponDamage:
					
						# Primary Attack Checks #
						if (dataAttack.targetSkillTree not in ["Basic Magic", "Advanced Magic"] and TARGET_ROOM_DISTANCE > 0 and (DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"] == None or DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"].flags["Weapon Range"] < TARGET_ROOM_DISTANCE)) \
						or ("Required Weapon Type List" in dataAttack.flags and heldWeaponTypeList[0] not in dataAttack.flags["Required Weapon Type List"]):
							primaryAttackCheck = False
							
						# Ammo Check #
						dominantWeaponData = DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"]
						if (dataAttack.idNum == -1 or "Ammo Required" in dataAttack.flags) and dominantWeaponData != None and dominantWeaponData.flags["Weapon Type"] == "Ranged" and (dominantWeaponData.flags["Loaded Ammo Object"] == None or dominantWeaponData.flags["Loaded Ammo Object"].flags["Quantity"] <= 0):
							primaryAttackCheck = "Ranged Weapon Is Empty"
				
						# Dual Wield Range Check #
						if (TARGET_ROOM_DISTANCE != None and TARGET_ROOM_DISTANCE > 0 and (DATA_PLAYER.gearDict[strOffhand] == None or DATA_PLAYER.gearDict[strOffhand].flags["Weapon Range"] < TARGET_ROOM_DISTANCE)) \
						or ("Required Weapon Type List" in dataAttack.flags and len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] not in dataAttack.flags["Required Weapon Type List"]) \
						or ("Required Weapon Type List" in dataAttack.flags and "Dual Wield Only" not in dataAttack.flags and primaryAttackCheck in [True, "Ranged Weapon Is Empty"]):
							dualWieldAttackCheck = False
				
	# Messages #
	if True:
		if targetMob != None and dataAttack != None:
			if dataAttack.weaponDamage and ((primaryAttackCheck != False and heldWeaponTypeList[0] == "Ranged") or (dualWieldAttackCheck != False and heldWeaponTypeList[1] == "Ranged")):
				Console.addDisplayLineToDictList("You aim at " + targetMob.defaultTitle + ".")
			else : Console.addDisplayLineToDictList("You prepare to attack.")
		elif messageType == "Already Busy":
			Console.addDisplayLineToDictList("You are busy.")
		elif messageType == "Target Not In Attack Range":
			Console.addDisplayLineToDictList("You are not in range.")
		elif messageType == "Room Not In View":
			Console.addDisplayLineToDictList("You can't see that far.")
		elif messageType == "No Target":
			Console.addDisplayLineToDictList("You don't have a target.")
		elif messageType == "Door Is Closed":
			Console.addDisplayLineToDictList("The door is closed.")
		elif messageType == "No Exit":
			Console.addDisplayLineToDictList("There is no exit there.")
		elif targetMob == None:
			Console.addDisplayLineToDictList("You don't see anyone like that.")

def userUseSkillEntity(SOLAR_SYSTEM_DICT, PARENT_AREA, DATA_PLAYER, STR_TARGET_SKILL, STR_TARGET_MOB, TARGET_INDEX, TARGET_DIR, TARGET_ROOM_DISTANCE, INPUT_TYPE):
	
	# Get Data #
	if True:
		STR_TARGET_SKILL = str(STR_TARGET_SKILL)
		if STR_TARGET_MOB != None : STR_TARGET_MOB = str(STR_TARGET_MOB)
		if INPUT_TYPE == "Cast Spell" : masterKeyList = Config.SPELL_MASTER_KEY_LIST
		elif INPUT_TYPE == "Use Skill" : masterKeyList = Config.SKILL_MASTER_KEY_LIST
		castAllSkillCheck = (INPUT_TYPE == "Use Skill" or ("Advanced Magic" in DATA_PLAYER.skillTreeDict and "Cast All" in DATA_PLAYER.skillTreeDict["Advanced Magic"].skillDict))
		playerRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
		targetMobRoom = None
		targetMob = None
		heldWeaponTypeList = []
		strRequiredWeaponType = ""
		messageType = None
		
	# String & Skill Check #
	if STR_TARGET_SKILL != "" and STR_TARGET_MOB != "" and STR_TARGET_SKILL in masterKeyList:
		
		# Get Attack & Attack Range Data #
		if True:
			if INPUT_TYPE == "Cast Spell" : targetAttack = DATA_PLAYER.getTargetSpellFromInputString(STR_TARGET_SKILL)
			elif INPUT_TYPE == "Use Skill":
				targetSkill = DATA_PLAYER.getTargetSkillFromInputString(STR_TARGET_SKILL)
				targetAttack = DataAttack.loadPrefab(targetSkill.idSkill)
			
			if targetAttack != None:
				STR_TARGET_SKILL = targetAttack.idSkill.lower()
				if INPUT_TYPE == "Cast Spell" : playerAttackRange = DATA_PLAYER.getCastRange()
				elif INPUT_TYPE == "Use Skill":
					if targetAttack.targetSkillTree in DATA_PLAYER.skillTreeDict and targetAttack.idSkill in DATA_PLAYER.skillTreeDict[targetAttack.targetSkillTree].skillDict:
						playerAttackRange = DATA_PLAYER.getSkillRange(targetAttack)
					else : messageType = "Skill Not Found"
				
		# Get Held Weapon Type List #
		if True:
		
			# Dominant Hand #
			if DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"] == None : heldWeaponTypeList.append(None)
			else : heldWeaponTypeList.append(DATA_PLAYER.gearDict[DATA_PLAYER.dominantHand+" Hand"].flags["Weapon Type"])
			
			# Offhand #
			if DATA_PLAYER.dualWieldCheck or "Required Weapon Type List" in targetAttack.flags or "Dual Wield Only" in targetAttack.flags:
				if DATA_PLAYER.dominantHand == "Left" : strOffhand = "Right Hand"
				else : strOffhand = "Left Hand"
				if DATA_PLAYER.gearDict[strOffhand] == None : heldWeaponTypeList.append(None)
				else : heldWeaponTypeList.append(DATA_PLAYER.gearDict[strOffhand].flags["Weapon Type"])
				
		# Skill Checks #
		if True:
			if DATA_PLAYER.currentAction != None : messageType = "Already Busy"
			elif INPUT_TYPE == "Cast Spell" and "Basic Magic" not in DATA_PLAYER.skillTreeDict : messageType = "Don't Know Magic"
			elif targetAttack == None or targetAttack.targetSkillTree not in DATA_PLAYER.skillTreeDict or targetAttack.idSkill not in DATA_PLAYER.skillTreeDict[targetAttack.targetSkillTree].skillDict : messageType = "Skill Not Found"
			elif STR_TARGET_MOB == "All" and targetAttack.targetSize == "Single Only" : messageType = "Single Target Only"
			elif STR_TARGET_MOB == "All" and targetAttack.targetSize == "Single Or All" and not castAllSkillCheck : messageType = "Cast All Not Known"
			elif STR_TARGET_MOB not in [None, "All"] and targetAttack.targetSize == "All Only" : messageType = "All Target Only"
			elif STR_TARGET_MOB == "Self" and (targetAttack.targetType == "Room" or targetAttack.effectType != "Heal") : messageType = "Can't Use On Self"
			elif STR_TARGET_MOB not in ["All", None] and targetAttack.targetType == "Room" : messageType = "Wrong Target Type"
			elif targetAttack.mpCost > DATA_PLAYER.currentMP : messageType = "Not Enough Mana"
			elif "Dual Wield Only" in targetAttack.flags and not ("Advanced Combat" in DATA_PLAYER.skillTreeDict and "Dual Wield" in DATA_PLAYER.skillTreeDict["Advanced Combat"].skillDict) : messageType = "Dual Wield Only"
			
		# Weapon Required Checks #
		if "Required Weapon Type List" in targetAttack.flags:
		
			requiredWeaponCheckMain = False
			requiredWeaponCheckOffhand = False
			if heldWeaponTypeList[0] in targetAttack.flags["Required Weapon Type List"]:
				requiredWeaponCheckMain = True
			if len(heldWeaponTypeList) > 1 and heldWeaponTypeList[1] in targetAttack.flags["Required Weapon Type List"]:
				requiredWeaponCheckOffhand = True
				
			if ("Dual Wield Only" not in targetAttack.flags and requiredWeaponCheckMain == False and requiredWeaponCheckOffhand == False) \
			or ("Dual Wield Only" in targetAttack.flags and (requiredWeaponCheckMain == False or requiredWeaponCheckOffhand == False)):
				messageType = "Weapon Type Not Held"
				
				# Message Data #
				strRequiredWeaponType = targetAttack.flags["Required Weapon Type List"][0]
				if "Dual Wield Only" not in targetAttack.flags:
					if strRequiredWeaponType == None : strRequiredWeaponType = "empty handed"
					elif strRequiredWeaponType == "Ranged" : strRequiredWeaponType = "holding a Ranged weapon"
					else : strRequiredWeaponType = "holding a " + strRequiredWeaponType
				else:
					if strRequiredWeaponType == None : strRequiredWeaponType = "empty handed"
					elif strRequiredWeaponType == "Ranged" : strRequiredWeaponType = "holding two Ranged weapons"
					else : strRequiredWeaponType = "holding two " + strRequiredWeaponType + "s"
					
		# Get Target Room #
		if messageType == None and targetAttack != None:
		
			if targetAttack.targetType == "Entity":
				
				# Input: Cast/Use Spell/Skill #
				if TARGET_ROOM_DISTANCE == None:
				
					# Player Has No Targets #
					if len(DATA_PLAYER.mobTargetList) == 0:
						if targetAttack.targetSize == "All Only" or targetAttack.effectType == "Heal":
							targetMobRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
							if targetAttack.effectType == "Heal" and targetAttack.targetSize != "All Only" : targetAttack.currentCount = "Self"
						elif targetAttack.targetSize in ["Single Only", "Single Or All"] : messageType = "No Target"
					
					# Player Has Targets #
					else:
					
						# Target Mob Room Is Defaulted To Player Room If Attack Will Heal A Non-Grouped Mob #
						if targetAttack.effectType == "Heal" and DATA_PLAYER.mobTargetList[0] not in DATA_PLAYER.groupList:
							targetMobRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
							if targetAttack.effectType == "Heal" and targetAttack.targetSize != "All Only" : targetAttack.currentCount = "Self"
					
						else:
							tempMobRange, tempMobDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, playerRoom, DATA_PLAYER.mobTargetList[0], playerAttackRange)
							if tempMessage == "Door Is Closed" : messageType = "Door Is Closed"
							elif tempMobRange == -1 : messageType = "Not In Range"
							elif tempMobRange > 0 and targetAttack.rangeType == "Short" : messageType = "Spell Range Is Short"
							else:
								targetMobRoom = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.mobTargetList[0].currentSolarSystem], DATA_PLAYER.mobTargetList[0]).roomDict[DATA_PLAYER.mobTargetList[0].currentRoom]
								if targetAttack.targetSize == "All Only" : targetAttack.targetRoomData = targetMobRoom
					
				# Input: Cast/Use Spell/Skill All, Cast/Use Spell/Skill @Target, Cast/Use Spell/Skill @Target @Index, Cast/Use Spell/Skill Self
				elif TARGET_ROOM_DISTANCE == 0:
					targetMobRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
					if targetAttack.targetSize == "Single Or All" and STR_TARGET_MOB == "All" : targetAttack.currentCount = "All"
					elif STR_TARGET_MOB == "Self" and targetAttack.effectType == "Heal" : targetAttack.currentCount = "Self"
				
				# Input: Cast/Use Spell/Skill @Dir/@Num, Cast/Use Spell/Skill @Target @Dir/@Num, Cast/Use Spell/Skill @Target @Index @Dir/@Num, Cast/Use Spell/Skill All @Dir/@Num, Cast/Use Spell/Skill Self @Dir/Num #
				elif TARGET_ROOM_DISTANCE > 0 and targetAttack.rangeType == "Short" : messageType = "Skill Range Is Short"
				elif TARGET_ROOM_DISTANCE > 0 and targetAttack.rangeType == "Long" and TARGET_ROOM_DISTANCE > playerAttackRange : messageType = "Not In Range"
				elif TARGET_ROOM_DISTANCE > 0:
					tempMobArea, tempMobRoom, tempMessage = DataWorld.getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, PARENT_AREA, playerRoom, TARGET_DIR, TARGET_ROOM_DISTANCE)
					if tempMessage == "Door Is Closed" : messageType = "Door Is Closed"
					elif tempMessage == "No Exit" : messageType = "Room Not There"
					else:
						targetMobRoom = tempMobRoom
						if targetAttack.targetSize == "All Only" : targetAttack.targetRoomData = targetMobRoom
						elif targetAttack.targetSize == "Single Or All" and STR_TARGET_MOB == "All":
							targetAttack.currentCount = "All"
							targetAttack.targetRoomData = targetMobRoom
						elif STR_TARGET_MOB == "Self" and targetAttack.effectType == "Heal":
							targetAttack.currentCount = "Self"
							targetMobRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
					
			elif targetAttack.targetType == "Room":
			
				if TARGET_ROOM_DISTANCE == None : targetMobRoom = PARENT_AREA.roomDict[DATA_PLAYER.currentRoom]
				elif TARGET_ROOM_DISTANCE > 0 and targetAttack.rangeType == "Short" : messageType = "Skill Range Is Short"
				elif TARGET_ROOM_DISTANCE > 0 and targetAttack.rangeType == "Long" and TARGET_ROOM_DISTANCE > playerAttackRange : messageType = "Not In Range"
				elif TARGET_ROOM_DISTANCE > 0:
					tempRoomArea, tempRoom, tempMessage = DataWorld.getTargetRoomFromStartRoom(SOLAR_SYSTEM_DICT, PARENT_AREA, playerRoom, TARGET_DIR, TARGET_ROOM_DISTANCE)
					if tempMessage == "Door Is Closed" : messageType = "Door Is Closed"
					elif tempMessage == "No Exit" : messageType = "Room Not There"
					else:
						targetMobRoom = tempRoom
						targetAttack.targetRoomData = targetMobRoom
						
				# Skill Already In Room Check #
				if messageType == None and targetMobRoom != None and targetMobRoom.updateSkill != None:
					targetMobRoom = None
					messageType = "Skill Already In Room"
			
		# Get Target Mob #
		if messageType == None and targetMobRoom != None and targetAttack.targetType == "Entity" and targetAttack.currentCount == 1:
			
			# No Input Target Mob (Input: Cast/Use Spell/Skill, Cast/Use Spell/Skill @Dir/@Num) #
			if STR_TARGET_MOB == None:
			
				# No Active Targets #
				if len(DATA_PLAYER.mobTargetList) == 0:
					if targetAttack.targetSize == "Single Only":
						messageType = "No Target"
					elif targetAttack.targetSize == "All Only" or (targetAttack.targetSize == "Single Or All" and castAllSkillCheck):
						targetAttack.currentCount = "All"
						STR_TARGET_MOB = "All"
						if targetAttack.targetSize == "Single Or All" : targetAttack.targetRoomData = targetMobRoom
				
				# Player Has Active Targets #
				else:
					tempMob = DATA_PLAYER.mobTargetList[0]
					
					# No Input Target Direction (Input: Cast/Use Spell/Skill) #
					if TARGET_DIR == None and TARGET_ROOM_DISTANCE == None:
						
						# Target Mob Is Defaulted To Player Room If Attack Will Heal A Non-Grouped Mob #
						if targetAttack.effectType == "Heal" and DATA_PLAYER.mobTargetList[0] not in DATA_PLAYER.groupList:
							pass
						else:
							tempMobRange, tempMobDir, tempMessage = DataWorld.getTargetRange(SOLAR_SYSTEM_DICT, targetMobRoom, tempMob, playerAttackRange)
							if tempMessage == "Door Is Closed" : messageType = "Door Is Closed"
							elif tempMobRange == -1 : messageType = "Not In Range"
							elif targetAttack.rangeType == "Short" and tempMobRange > 0 : messageType = "Spell Range Is Short"
							elif targetAttack.rangeType == "Long" and tempMobRange > playerAttackRange : messageType = "Not In Range"
							else : targetMob = tempMob
						
					# Input Target Direction (Input: Cast/Use Spell/Skill @Dir/@Num) #
					elif TARGET_DIR != None or TARGET_ROOM_DISTANCE != None:
						if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, targetMobRoom, tempMob):
							targetMob = tempMob
						elif targetAttack.targetSize == "Single Or All" and castAllSkillCheck:
							targetAttack.currentCount = "All"
							targetAttack.targetRoomData = targetMobRoom
						else:
							messageType = "Target Not Found"
						
			# Input Target Mob (Input: Cast/Use Spell/Skill @Target, Cast/Use Spell/Skill @Target @Index, Cast/Use Spell/Skill All, Cast/Use Spell/Skill @Target @Dir/@Num, Cast/Use Spell/Skill @Target @Index @Dir/@Num, Cast/Use Spell/Skill All @Dir/@Num) #
			else:
				tempMob, mobIndex, mobLoc = GameProcess.getTarget(DATA_PLAYER, targetMobRoom, STR_TARGET_MOB, TARGET_INDEX, ["Room Mobs"])
				if targetAttack.targetSize == "All Only":
					targetAttack.currentCount = "All"
					STR_TARGET_MOB = "All"
				elif tempMob == None:
					messageType = "Target Not Found"
				else:
					targetMob = tempMob
		
		# Initiate Skill #
		if messageType == None and targetAttack != None \
		and (targetMob != None or (targetMobRoom != None and targetAttack.currentCount in ["All", "Self"]) or targetAttack.targetType == "Room"):
			
			DATA_PLAYER.currentAction = {"Type":"Attacking", "Timer":targetAttack.attackTimer, "Action Bar Timer":0, "Attack Data":targetAttack}
			
			# Put Defender In Player MobTargetList #
			if targetMob != None:
				if targetMob not in DATA_PLAYER.mobTargetList:
					DATA_PLAYER.mobTargetList.insert(0, targetMob)
				elif targetMob != DATA_PLAYER.mobTargetList[0]:
					del DATA_PLAYER.mobTargetList[DATA_PLAYER.mobTargetList.index(targetMob)]
					DATA_PLAYER.mobTargetList.insert(0, targetMob)
			
	# Messages #
	if True:
		if messageType == None and DATA_PLAYER.currentAction != None and DATA_PLAYER.currentAction["Type"] == "Attacking":
			if INPUT_TYPE == "Cast Spell" : Console.addDisplayLineToDictList("You begin casting " + targetAttack.idSkill + ".")
			elif INPUT_TYPE == "Use Skill" : Console.addDisplayLineToDictList("You prepare to attack.")
		elif messageType == "Already Busy":
			Console.addDisplayLineToDictList("You are busy.")
		elif messageType == "Don't Know Magic":
			Console.addDisplayLineToDictList("You don't know how to cast magic.")
		elif messageType == "Skill Not Found":
			Console.addDisplayLineToDictList("That doesn't sound familiar.")
		elif messageType == "Door Is Closed":
			Console.addDisplayLineToDictList("The door is closed.")
		elif messageType == "Room Not There":
			Console.addDisplayLineToDictList("There is no room there.")
		elif messageType == "Skill Already In Room":
			Console.addDisplayLineToDictList("There is already a skill active there.")
		elif messageType == "Skill Range Is Short":
			Console.addDisplayLineToDictList("You can't use it from afar.")
		elif messageType == "Not In Range":
			Console.addDisplayLineToDictList("You are not in range.")
		elif messageType == "No Target":
			Console.addDisplayLineToDictList("You don't have a target.")
		elif messageType == "Target Not Found":
			Console.addDisplayLineToDictList("Your target is not there.")
		elif messageType == "Wrong Target Type":
			Console.addDisplayLineToDictList("You can't use that on an someone.")
		elif messageType == "Single Target Only":
			Console.addDisplayLineToDictList("That attack only has one target.")
		elif messageType == "All Target Only":
			Console.addDisplayLineToDictList("That attack can only target everyone in the room.")
		elif messageType == "Cast All Not Known":
			Console.addDisplayLineToDictList("You can't cast all yet.")
		elif messageType == "Can't Use On Self":
			Console.addDisplayLineToDictList("You can't use that on yourself.")
		elif messageType == "Not Enough Mana":
			Console.addDisplayLineToDictList("You don't have enough mana.")
		elif messageType == "Weapon Type Not Held":
			Console.addDisplayLineToDictList("You need to be " + strRequiredWeaponType + " to do that.")
		elif messageType == "Can't Use Attack With That":
			Console.addDisplayLineToDictList("You can't use that attack with that weapon.")
		elif messageType == "Dual Wield Only":
			Console.addDisplayLineToDictList("Dual wielding is required for this attack.")

def targetStopAttack(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_OBJECT):

	if TARGET_OBJECT.objectType == "Player":
		if TARGET_OBJECT.currentAction == None:
			Console.addDisplayLineToDictList("You are already resting.")
		elif TARGET_OBJECT.currentAction["Type"] != "Attacking":
			Console.addDisplayLineToDictList("You can only stop an attack.")
		else:
			Console.addDisplayLineToDictList("You stop preparing to attack.")
	
	elif TARGET_OBJECT.objectType == "Mob":
		if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_OBJECT):
			Console.addDisplayLineToDictList(TARGET_OBJECT.defaultTitle + " stops preparing to attack.")
		
	if TARGET_OBJECT.currentAction != None and TARGET_OBJECT.currentAction["Type"] == "Attacking":
		TARGET_OBJECT.currentAction = None

def targetParry(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_ENTITY):

	# Player #
	if TARGET_ENTITY.objectType == "Player":
		if TARGET_ENTITY.currentAction != None:
			Console.addDisplayLineToDictList("You are busy.")
		elif "Basic Combat" not in TARGET_ENTITY.skillTreeDict or "Parry" not in TARGET_ENTITY.skillTreeDict["Basic Combat"].skillDict:
			Console.addDisplayLineToDictList("You don't know how.")
		else:
			TARGET_ENTITY.currentAction = {"Type":"Parrying", "Timer":3.0}
			Console.addDisplayLineToDictList("You prepare for an incoming attack.")
			
	# Mob #
	elif TARGET_ENTITY.objectType == "Mob":
		TARGET_ENTITY.currentAction = {"Type":"Parrying", "Timer":3.0}
		if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_ENTITY):
			Console.addDisplayLineToDictList(TARGET_ENTITY.defaultTitle + " prepares for an incoming attack.")

def targetDodge(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_ENTITY):

	# Player #
	if TARGET_ENTITY.objectType == "Player":
		if TARGET_ENTITY.currentAction != None:
			Console.addDisplayLineToDictList("You are busy.")
		elif "Basic Combat" not in TARGET_ENTITY.skillTreeDict or "Dodge" not in TARGET_ENTITY.skillTreeDict["Basic Combat"].skillDict:
			Console.addDisplayLineToDictList("You don't know how.")
		else:
			TARGET_ENTITY.currentAction = {"Type":"Dodging", "Timer":3.0}
			Console.addDisplayLineToDictList("You start moving out of the way.")
			
	# Mob #
	elif TARGET_ENTITY.objectType == "Mob":
		TARGET_ENTITY.currentAction = {"Type":"Dodging", "Timer":3.0}
		if DataWorld.sameRoomCheck(SOLAR_SYSTEM_DICT, DATA_PLAYER, TARGET_ENTITY):
			Console.addDisplayLineToDictList(TARGET_ENTITY.defaultTitle + " starts to moving out of the way.")
