import Utility, DataAttack

class LoadSkillTree:

	def __init__(self, ID_SKILL_TREE):
	
		self.idSkillTree = ID_SKILL_TREE
		self.skillDict = {}
		
		self.initData()
		
	def initData(self):
		
		if self.idSkillTree == "Basic Combat":
			self.skillDict["Unarmed"] = loadPrefab(self.idSkillTree, "Unarmed", 50.0)
			self.skillDict["Swords"] = loadPrefab(self.idSkillTree, "Swords", 50.0)
			self.skillDict["Lances"] = loadPrefab(self.idSkillTree, "Lances", 50.0)
			self.skillDict["Bludgeons"] = loadPrefab(self.idSkillTree, "Bludgeons", 50.0)
			self.skillDict["Shields"] = loadPrefab(self.idSkillTree, "Shields", 50.0)
			self.skillDict["Ranged"] = loadPrefab(self.idSkillTree, "Ranged", 50.0)
			
			self.skillDict["Parry"] = loadPrefab(self.idSkillTree, "Parry", 50.0)
			self.skillDict["Dodge"] = loadPrefab(self.idSkillTree, "Dodge", 50.0)
	
		elif self.idSkillTree == "Advanced Combat":
			self.skillDict["Dual Wield"] = loadPrefab(self.idSkillTree, "Dual Wield", 50.0)
			self.skillDict["Counter Attack"] = loadPrefab(self.idSkillTree, "Counter Attack", 50.0)
			
			self.skillDict["Debug Power"] = loadPrefab(self.idSkillTree, "Debug Power", 50.0)
			self.skillDict["Debug AttackAll"] = loadPrefab(self.idSkillTree, "Debug AttackAll", 50.0)
			self.skillDict["Debug RangedAll"] = loadPrefab(self.idSkillTree, "Debug RangedAll", 50.0)
			self.skillDict["Debug PowerGun"] = loadPrefab(self.idSkillTree, "Debug PowerGun", 50.0)
			self.skillDict["Debug PowerSword"] = loadPrefab(self.idSkillTree, "Debug PowerSword", 50.0)
			self.skillDict["Debug PowerFist"] = loadPrefab(self.idSkillTree, "Debug PowerFist", 50.0)
			self.skillDict["DualAttack"] = loadPrefab(self.idSkillTree, "DualAttack", 50.0)
			self.skillDict["DualBlade"] = loadPrefab(self.idSkillTree, "DualBlade", 50.0)
			self.skillDict["DualGun"] = loadPrefab(self.idSkillTree, "DualGun", 50.0)
			
		elif self.idSkillTree == "Basic Magic":
			self.skillDict["Fire A"] = loadPrefab(self.idSkillTree, "Fire A", 50.0)
			self.skillDict["Fire B"] = loadPrefab(self.idSkillTree, "Fire B", 50.0)
			self.skillDict["Ice A"] = loadPrefab(self.idSkillTree, "Ice A", 50.0)
			self.skillDict["Ice B"] = loadPrefab(self.idSkillTree, "Ice B", 50.0)
			self.skillDict["Lit A"] = loadPrefab(self.idSkillTree, "Lit A", 50.0)
			self.skillDict["Lit B"] = loadPrefab(self.idSkillTree, "Lit B", 50.0)
			self.skillDict["Heal A"] = loadPrefab(self.idSkillTree, "Heal A", 50.0)
			self.skillDict["Heal B"] = loadPrefab(self.idSkillTree, "Heal B", 50.0)
			self.skillDict["Heal C"] = loadPrefab(self.idSkillTree, "Heal C", 50.0)
			self.skillDict["Heal D"] = loadPrefab(self.idSkillTree, "Heal D", 50.0)
			self.skillDict["Heal E"] = loadPrefab(self.idSkillTree, "Heal E", 50.0)
			self.skillDict["Heal F"] = loadPrefab(self.idSkillTree, "Heal F", 50.0)
			self.skillDict["Room A"] = loadPrefab(self.idSkillTree, "Room A", 50.0)
			self.skillDict["Room B"] = loadPrefab(self.idSkillTree, "Room B", 50.0)
			self.skillDict["Room Heal A"] = loadPrefab(self.idSkillTree, "Room Heal A", 50.0)
			self.skillDict["Room Heal B"] = loadPrefab(self.idSkillTree, "Room Heal B", 50.0)
		
		elif self.idSkillTree == "Advanced Magic":
			self.skillDict["Cast All"] = loadPrefab(self.idSkillTree, "Cast All", 50.0)
			
		elif self.idSkillTree == "General Skills":
			self.skillDict["Debug Dig"] = loadPrefab(self.idSkillTree, "Debug Dig", 50.0)
			self.skillDict["Debug Repair"] = loadPrefab(self.idSkillTree, "Debug Repair", 50.0)
			self.skillDict["Tame"] = loadPrefab(self.idSkillTree, "Tame", 90.0)

class LoadSkill:

	def __init__(self, ID_SKILL_TREE, ID_SKILL, FLAGS={}):
	
		self.idSkillTree = ID_SKILL_TREE
		self.idSkill = ID_SKILL
		self.keyList = Utility.createKeyList(ID_SKILL)
		
		self.useTarget = None   # Entity, Item, Room 
		self.learnPercent = 0.0
		
		if "Use Target" in FLAGS:
			self.useTarget = FLAGS["Use Target"]
		
def loadPrefab(ID_SKILL_TREE, ID_SKILL, STARTING_PERCENT=0.0):

	targetSkill = None

	if ID_SKILL_TREE == "Basic Combat":
		if ID_SKILL in ["Unarmed", "Swords", "Lances", "Bludgeons", "Shields", "Ranged", "Parry", "Dodge"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL)
			
	elif ID_SKILL_TREE == "Advanced Combat":
		
		if ID_SKILL in ["Dual Wield", "Counter Attack"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL)
		
		elif ID_SKILL in ["Debug Power", "Debug AttackAll", "Debug RangedAll", "Debug PowerGun", "Debug PowerSword", "Debug PowerFist", "DualAttack", "DualBlade", "DualGun"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL, {"Use Target":"Entity"})
			
	elif ID_SKILL_TREE == "Basic Magic":
		if ID_SKILL in ["Fire A", "Fire B", "Ice A", "Ice B", "Lit A", "Lit B", "Heal A", "Heal B", "Heal C", "Heal D", "Heal E", "Heal F", "Room A", "Room B", "Room Heal A", "Room Heal B"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL)
			
	elif ID_SKILL_TREE == "Advanced Magic":
		if ID_SKILL in ["Cast All"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL)
			
	elif ID_SKILL_TREE == "General Skills":
		if ID_SKILL in ["Debug Dig"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL, {"Use Target":"General"})
			
		elif ID_SKILL in ["Debug Repair"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL, {"Use Target":"Item"})
			
		elif ID_SKILL in ["Tame"]:
			targetSkill = LoadSkill(ID_SKILL_TREE, ID_SKILL, {"Use Target":"Entity (Passive)"})
		
	# Starting Learn Percent #
	if targetSkill != None : targetSkill.learnPercent = STARTING_PERCENT
	
	return targetSkill
	
def getMasterSkillTreeList():

	return ["Basic Combat", "Advanced Combat", "Basic Magic", "Advanced Magic", "General Skills"]
	
def getMasterSkillKeyList():

	keyList = []
	
	for skillId in ["Debug Power", "Debug AttackAll", "Debug RangedAll", "Debug PowerGun", "Debug PowerSword", "Debug PowerFist", "DualAttack", "DualBlade", "DualGun", "Debug Dig", "Debug Repair"]:
		
		if skillId.lower() not in keyList:
			keyList.append(skillId.lower())
		
		if len(skillId.split()) > 2:
			for iNum in range(len(skillId.split())-2):
				if ' '.join(skillId.split()[0:iNum+2]).lower() not in keyList:
					keyList.append(' '.join(skillId.split()[0:iNum+2]).lower())
			
		if len(skillId.split()) > 1:
			for skillKeyword in skillId.split():
				if skillKeyword.lower() not in keyList:
					keyList.append(skillKeyword.lower())
	
	return keyList
	
def getTargetWeaponSkillTree(TARGET_WEAPON_TYPE):

	return "Basic Combat"
	
def getTargetWeaponSkillID(TARGET_WEAPON_TYPE):

	if TARGET_WEAPON_TYPE == None:
		targetWeaponSkillID = "Unarmed"
	elif TARGET_WEAPON_TYPE == "Sword":
		targetWeaponSkillID = "Swords"
	elif TARGET_WEAPON_TYPE == "Lance":
		targetWeaponSkillID = "Lances"
	elif TARGET_WEAPON_TYPE == "Bludgeon":
		targetWeaponSkillID = "Bludgeons"
	elif TARGET_WEAPON_TYPE == "Shield":
		targetWeaponSkillID = "Shields"
	else:
		targetWeaponSkillID = TARGET_WEAPON_TYPE
		
	return targetWeaponSkillID
	