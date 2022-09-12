import pygame, Config
from pygame import *
from Data import DataMain

# Initialize Variables #
fullscreenMode = Config.FULLSCREEN_MODE
if fullscreenMode : fullscreenMode = pygame.FULLSCREEN

windowMain = pygame.display.set_mode(Config.RESOLUTION_LIST[Config.RESOLUTION_INDEX], fullscreenMode, 32)
pygame.display.set_caption("TypeQuest " + Config.VERSION)
clock = pygame.time.Clock()
dataMain = DataMain.LoadDataMain(windowMain)

while True:

	lastTick = clock.tick(60) / 1000.0
	dataMain.updateMain(str(clock.get_fps())[:5], windowMain)
	