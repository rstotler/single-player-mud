import pygame, os, Utility
from Data import DataAttack, DataSkill
from pygame import *
pygame.init()

VERSION = "V0.02487"
SCREEN_SIZE = [1280, 720]
RESOLUTION_LIST = [[640, 480], [800, 600], [960, 720], [1024, 576], [1024, 768], [1152, 648], [1280, 720], [1280, 800], [1280, 960], [1360, 768], [1366, 768], [1400, 1050], [1440, 900], [1440, 1080], [1600, 900], [1600, 1200], [1680, 1050], [1856, 1392], [1920, 1080], [1920, 1200], [1920, 1440], [2048, 1536], [2560, 1440], [2560, 1600]]
RESOLUTION_INDEX = 6
FULLSCREEN_MODE = False
COLOR_DICT = Utility.loadColorDict()
ALPHABET_STRING = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DRAW_SCREEN_DICT = {"cnslMain":True, "frmMain":True, "Bottom Bar":True, "Room":["All"], "Target Stats":True, "Map":True, "Player Stats":True, "Player Utility":True, "Player Utility Bar":True}
DISPLAY_RECT_LIST = []
DISPLAY_LINE_DICT_LIST = []

# General Game Constants #
GAME_TICK_SPEED = 1
SYNCH_TICK_SPEED = 30
SPACESHIP_TIMER = {"Update":5, "Speed":125}
MOB_TIMER = {"Mobile Min":15, "Mobile Max":30, "Corpse Decay":500}
ITEM_TIMER = {"Wilt":500, "Decay":250}

# Planet Constants #
FREEZE_TEMP = {"Default":30, "Acid":40}
EVAPORATE_TEMP = {"Default":200, "Acid":600}
WET_TIMER = {"Rain Start":100, "Max Ground Liquid":750}

# Plant Constants #
PLANT_MAX_AGE_TIMER = {"Tree":8000, "Bush":5000, "Plant":5000, "Vine":5000, "Root":5000, "Flower":4000}
PLANT_MAX_LIQUID_TIMER = {"Tree":1000, "Bush":750, "Plant":500, "Vine":500, "Root":350, "Flower":400}
PLANT_STAGE_TIMER = {"Germinate":100, "Tree":100, "Bush":100, "Plant":100, "Vine":100, "Root":100, "Flower":100}
PLANT_TIMER = {"Blossom":100, "Unripe":100, "Fall Off Vine":100}

# Map & Movement Data #
WORLD_MAP_CELL_SIZE = [32, 32]
WORLD_MAP_SIZE = [128, 128]
MAP_RATIO_LIST = [1.0, .72, .50, .30, .18, .12]
PLAYER_UPDATE_RANGE = 4         # For SAFETY PURPOSES The Player & Mobs View Distance Should Not Exceed The Player Update Range
MOB_MOVE_CHECK_TARGET_RANGE = 5 # Determines How Many Rooms Away From A Target Mob To Check If It Is Out Of Other Mob's Views

# Key Lists #
SPACESHIP_COMMANDS_KEYLIST = ["launch", "launc", "laun", "lau", "land", "lan", "scan", "sca", "radar", "rada", "rad", "course", "cours", "cour", "cou", "throttle", "throttl", "thrott", "throt", "thro", "thr"]
SPELL_MASTER_KEY_LIST = DataAttack.getMasterSpellKeyList()
SKILL_MASTER_KEY_LIST = DataSkill.getMasterSkillKeyList()
COMBAT_ACTION_LIST = ["Attacking", "Parrying", "Dodging", "Attack Cooldown", "Stumbling", "Down"]

# Fonts #
FONT_ROMAN_20 = pygame.font.Font(os.path.dirname(os.getcwd())+"/Font/CodeNewRomanB.otf", 20)
FONT_ROMAN_19 = pygame.font.Font(os.path.dirname(os.getcwd())+"/Font/CodeNewRomanB.otf", 19)
FONT_ROMAN_18 = pygame.font.Font(os.path.dirname(os.getcwd())+"/Font/CodeNewRomanB.otf", 18)
FONT_ROMAN_16 = pygame.font.Font(os.path.dirname(os.getcwd())+"/Font/CodeNewRomanB.otf", 16)
FONT_ROMAN_12 = pygame.font.Font(os.path.dirname(os.getcwd())+"/Font/CodeNewRomanB.otf", 12)
FONT_ROMAN_11 = pygame.font.Font(os.path.dirname(os.getcwd())+"/Font/CodeNewRomanB.otf", 11)

# Emote Dict #
EMOTE_DICT = {"tap":{"Display Line":"You tap your foot impatiently..", "Color Code":"29w2y"},
			  "boggle":{"Display Line":"You boggle in complete incomprehension.", "Color Code":"38w1y"},
			  "gasp":{"Display Line":"You gasp!", "Color Code":"8w1y"},
			  "ahah":{"Display Line":"Comprehension dawns upon you.", "Color Code":"28w1y"},
			  "haha":{"Display Line":"You laugh out loud!", "Color Code":"18w1y"},
			  "lol":{"Display Line":"You laugh out loud!", "Color Code":"18w1y"},
			  "hmm":{"Display Line":"You scratch your chin and go, \"Hmm..\"", "Color Code":"28w3y3w3y"},
			  "hm":{"Display Line":"You scratch your chin and go, \"Hmm..\"", "Color Code":"28w3y3w3y"},
			  "cheer":{"Display Line":"And the peasants rejoiced.", "Color Code":"25w1y"},
			  "jump":{"Display Line":"You jump up and down.", "Color Code":"20w1y"},
			  "nod":{"Display Line":"You nod.", "Color Code":"7w1y"},
			  "nodnod":{"Display Line":"You nodnod.", "Color Code":"10w1y"},
			  "smile":{"Display Line":"You smile happily.", "Color Code":"17w1y"},
			  "swear":{"Display Line":"@*$#!", "Color Code":"4w1y"}}
