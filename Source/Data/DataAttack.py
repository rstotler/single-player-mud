import Utility

class LoadAttack:

	def __init__(self):
	
		self.idSkill = None
		self.idNum = None
		self.keyList = []
		self.flags = {}                  # Required Weapon Type List, Excluded Weapon Type List, Ammo Required, Dual Wield Required
		
		# Attack Data #
		self.basePower = 1
		self.mpCost = 0
		
		self.targetSkillTree = None      # Basic Combat, Advanced Combat, Basic Magic, Advanced Magic
		self.damageType = "Physical"     # Physical, Magic, Both
		self.effectType = "Damage"       # Damage, Heal
		self.rangeType = "Short"         # Short, Long
		self.weaponDamage = False
		self.attackSpeed = 50            # 1 - 100 (Except For Super Fast Attacks)
		
		# Attack Target Data #
		self.targetType = "Entity"       # Entity, Room
		self.targetSize = "Single Only"  # Single Only, All Only, Single Or All, None (Room)
		self.currentCount = 1            # 1, All, Self, None (Room)
		self.targetRoomData = None
		
		# Timer Data #
		self.attackTimer = 3
		self.cooldownTimer = 1.5
		
def loadPrefab(ID_SKILL):

	# Load Default Data #
	if True:
	
		# Create Upper Case Target Attack String Key #
		tempString = ""
		for wNum, word in enumerate(ID_SKILL.split()):
			if len(word) == 1 : tempString = tempString + word.upper()
			else : tempString = tempString + word[0].upper() + word[1::]
			if wNum < len(ID_SKILL.split()) - 1 : tempString = tempString + " "
		ID_SKILL = tempString
		
		attack = LoadAttack()
		attack.idSkill = ID_SKILL
		attack.keyList = Utility.createKeyList(ID_SKILL)
		
	# Default Attack - Basic Attack #
	if attack.idNum == None and ID_SKILL == "Basic Attack":
		attack.idNum = -1
		attack.targetSkillTree = "Basic Combat"
		attack.weaponDamage = True

	# Spell Attacks #
	if attack.idNum == None:
		
		# Fire A #
		if attack.idNum == None and ID_SKILL == "Fire A":
			attack.idNum = 1
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.targetSize = "Single Or All"
			
		# Fire B #
		if attack.idNum == None and ID_SKILL == "Fire B":
			attack.idNum = 2
			attack.basePower = 15
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.rangeType = "Long"
			attack.targetSize = "Single Or All"
		
		# Ice A #
		if attack.idNum == None and ID_SKILL == "Ice A":
			attack.idNum = 3
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.targetSize = "All Only"
			
		# Ice B #
		if attack.idNum == None and ID_SKILL == "Ice B":
			attack.idNum = 4
			attack.basePower = 15
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.rangeType = "Long"
			attack.targetSize = "All Only"
			
		# Lit A #
		if attack.idNum == None and ID_SKILL == "Lit A":
			attack.idNum = 5
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			
		# Lit B #
		if attack.idNum == None and ID_SKILL == "Lit B":
			attack.idNum = 6
			attack.basePower = 15
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.rangeType = "Long"
		
		# Heal A #
		if attack.idNum == None and ID_SKILL == "Heal A":
			attack.idNum = 7
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			
		# Heal B #
		if attack.idNum == None and ID_SKILL == "Heal B":
			attack.idNum = 8
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.rangeType = "Long"
			
		# Heal C #
		if attack.idNum == None and ID_SKILL == "Heal C":
			attack.idNum = 9
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.targetSize = "All Only"
			
		# Heal D #
		if attack.idNum == None and ID_SKILL == "Heal D":
			attack.idNum = 10
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.rangeType = "Long"
			attack.targetSize = "All Only"
			
		# Heal E #
		if attack.idNum == None and ID_SKILL == "Heal E":
			attack.idNum = 11
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.targetSize = "Single Or All"
			
		# Heal F #
		if attack.idNum == None and ID_SKILL == "Heal F":
			attack.idNum = 12
			attack.basePower = 10
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.rangeType = "Long"
			attack.targetSize = "Single Or All"
			
		# Room A #
		if attack.idNum == None and ID_SKILL == "Room A":
			attack.idNum = 13
			attack.basePower = 1
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.targetType = "Room"
			attack.cooldownTimer = 3
			attack.flags["Room Ticks"] = 8
			
		# Room B #
		if attack.idNum == None and ID_SKILL == "Room B":
			attack.idNum = 14
			attack.basePower = 2
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.rangeType = "Long"
			attack.targetType = "Room"
			attack.cooldownTimer = 3
			
		# Room Heal A #
		if attack.idNum == None and ID_SKILL == "Room Heal A":
			attack.idNum = 15
			attack.basePower = 1
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.targetType = "Room"
			attack.cooldownTimer = 3
			attack.flags["Room Ticks"] = 8
			
		# Room Heal B #
		if attack.idNum == None and ID_SKILL == "Room Heal B":
			attack.idNum = 16
			attack.basePower = 2
			attack.mpCost = 1
			attack.targetSkillTree = "Basic Magic"
			attack.damageType = "Magic"
			attack.effectType = "Heal"
			attack.rangeType = "Long"
			attack.targetType = "Room"
			attack.cooldownTimer = 3
			
	# Skill Attacks #
	if True:
		
		# Debug Power #
		if attack.idNum == None and ID_SKILL == "Debug Power":
			attack.idNum = 17
			attack.basePower = 2000000
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.weaponDamage = True
			#attack.flags["Required Weapon Type List"] = ["Sword"]
		
		# Debug AttackAll #
		if attack.idNum == None and ID_SKILL == "Debug AttackAll":
			attack.idNum = 18
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.weaponDamage = True
			attack.targetSize = "All Only"
			#attack.flags["Required Weapon Type List"] = ["Sword"]
		
		# Debug RangedAll #
		if attack.idNum == None and ID_SKILL == "Debug RangedAll":
			attack.idNum = 19
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.rangeType = "Long"
			attack.weaponDamage = True
			attack.targetSize = "All Only"
			attack.flags["Required Weapon Type List"] = ["Ranged"]
			attack.flags["Ammo Required"] = True
			
		# Debug PowerGun #
		if attack.idNum == None and ID_SKILL == "Debug PowerGun":
			attack.idNum = 20
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.rangeType = "Long"
			attack.weaponDamage = True
			attack.targetSize = "Single Or All"
			attack.flags["Required Weapon Type List"] = ["Ranged"]
			
		# Debug PowerSword #
		if attack.idNum == None and ID_SKILL == "Debug PowerSword":
			attack.idNum = 21
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.weaponDamage = True
			attack.targetSize = "Single Or All"
			attack.flags["Required Weapon Type List"] = ["Sword"]
			
		# Debug PowerFist # (Requires Empty Hand)
		if attack.idNum == None and ID_SKILL == "Debug PowerFist":
			attack.idNum = 22
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.weaponDamage = True
			attack.flags["Required Weapon Type List"] = [None]
			
		# DualAttack #
		if attack.idNum == None and ID_SKILL == "DualAttack":
			attack.idNum = 23
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.weaponDamage = True
			attack.targetSize = "Single Or All"
			attack.flags["Dual Wield Only"] = True
		
		# DualBlade #
		if attack.idNum == None and ID_SKILL == "DualBlade":
			attack.idNum = 24
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.weaponDamage = True
			attack.targetSize = "Single Or All"
			attack.flags["Required Weapon Type List"] = ["Sword"]
			attack.flags["Dual Wield Only"] = True
		
		# DualGun #
		if attack.idNum == None and ID_SKILL == "DualGun":
			attack.idNum = 25
			attack.basePower = 20
			attack.mpCost = 1
			attack.targetSkillTree = "Advanced Combat"
			attack.rangeType = "Long"
			attack.weaponDamage = True
			attack.targetSize = "Single Or All"
			attack.flags["Required Weapon Type List"] = ["Ranged"]
			attack.flags["Ammo Required"] = True
			attack.flags["Dual Wield Only"] = True
			
	# Spell Variable Checks #
	if attack.targetSize == "All Only":
		attack.currentCount = "All"
	if attack.targetType == "Room":
		attack.targetSize = None
		attack.currentCount = None
	
	if attack.idNum != None : return attack
	else : return None
	
def getMasterSpellKeyList():

	keyList = []

	for spellId in ["Fire A", "Fire B", "Ice A", "Ice B", "Lit A", "Lit B", "Heal A", "Heal B", "Heal C", "Heal D", "Heal E", "Heal F", "Room A", "Room B", "Room Heal A", "Room Heal B"]:
		targetAttack = loadPrefab(spellId)
		if targetAttack != None:
			for targetAttackKey in targetAttack.keyList:
				if targetAttackKey not in keyList:
					keyList.append(targetAttackKey.lower())
		
	return keyList
	