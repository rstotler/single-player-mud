class LoadModule:

	def __init__(self):
	
		self.idModule = None
		
def loadModule(ID_MODULE):

	module = LoadModule()
	module.idModule = ID_MODULE
	
	return module
	