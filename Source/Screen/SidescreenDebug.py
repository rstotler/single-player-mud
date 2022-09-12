import pygame, Config, Utility
from Data import DataWorld
from pygame import *

class LoadSidescreenDebug:

	def __init__(self):
	
		self.objectType = "Sidescreen"
		
		self.rect = pygame.Rect([0, 0, 540, 280])
		self.surfaceDefault = pygame.Surface([540, 280])
		self.surfaceDefault.fill([0, 0, 0])
		
	def draw(self, TICK_SYNCH, SCREEN, SOLAR_SYSTEM_DICT, DATA_PLAYER):
	
		SCREEN.blit(self.surfaceDefault, [0, 0])
		
		# Get Data #
		if True:
			playerArea = DataWorld.getParentArea(SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem], DATA_PLAYER)
			playerRoom = playerArea.roomDict[DATA_PLAYER.currentRoom]
			displayLoc = [7, 7]
			
			# Room/Time Data #
			strInsideOutside = "Outside"
			if playerRoom.inside : strInsideOutside = "Inside"
			
			strPlanetTickSynch = ""
			if DATA_PLAYER.currentPlanet != None:
				playerPlanet = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[DATA_PLAYER.currentPlanet]
				strPlanetTickSynch = str(playerPlanet.tickSynch)
			
		# Write To Screen #
		if True:
			
			# Time Data #
			if True:
				Utility.writeFast("-Time/Synch Data-", displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("*:" + str(TICK_SYNCH) + " P:" + strPlanetTickSynch + " A:" + str(playerArea.tickSynch) + " R:" + str(playerRoom.tickSynch), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast(playerPlanet.getTimeString() + " - " + playerPlanet.getDateString(), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				displayLoc[1] += 12
			
			# Room Data #
			if True:
				Utility.writeFast("-Room Data-", displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("[" + str(playerRoom.idNum) + "] " + playerRoom.title, displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast(str(playerArea.currentTemperature) + "F (" + strInsideOutside + ")", displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("W: (" + str(len(playerArea.synchWeatherDictList)) + ") " + str(playerArea.weatherDict), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("A Wet: " + str(playerArea.wetTimerAreaDict), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("R Wet: " + str(playerArea.wetTimerRoomDict), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				displayLoc[1] += 12
				
			# Room Update Data #
			if True:
				Utility.writeFast("-Room Update Data-", displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				if playerRoom.updateSkill != None : strUpdateSkill = playerRoom.updateSkill.idSkill
				else : strUpdateSkill = "None"
				strUpdateObjects = "Mob:" + str(len(playerRoom.updateMobList)) + "  R-Item:" + str(len(playerRoom.updateItemList)) + "  P-Item:" + str(len(DATA_PLAYER.updateItemList))
				Utility.writeFast(strUpdateObjects, displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("Spell:" + strUpdateSkill, displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				displayLoc[1] += 12
				
			# Player Data #
			if True:
				Utility.writeFast("-Player Data-", displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("Status: " + str(DATA_PLAYER.currentAction), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				Utility.writeFast("Carry Weight: " + str(DATA_PLAYER.currentWeight) + "/" + str(DATA_PLAYER.maxWeight), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				
				# Bags Info #
				if True:
					for item in DATA_PLAYER.inventoryList:
						if item.type == "Container":
							strDisplayLine = item.defaultTitle + ": " + str(item.flags["Container Current Weight"]) + "/" + str(item.flags["Container Max Weight"])
							Utility.writeFast(strDisplayLine, displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN)
							displayLoc[1] += 12
								
			# Planet Time Data #
			if True:
				displayLoc = [400, 7]
				Utility.writeFast("-Planet Data-", displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
				for targetPlanetId in SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict:
					targetPlanet = SOLAR_SYSTEM_DICT[DATA_PLAYER.currentSolarSystem].planetDict[targetPlanetId]
					Utility.writeFast(str(targetPlanet.idPlanet)[0:3] + " " + str(targetPlanet.constantHoursInYear) + "/" + str(targetPlanet.totalHoursInYear), displayLoc, [200, 200, 200], Config.FONT_ROMAN_12, SCREEN) ; displayLoc[1] += 12
			
		Config.DISPLAY_RECT_LIST.append(self.rect)
		