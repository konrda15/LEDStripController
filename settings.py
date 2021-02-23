class Settings:
	def __init__(self, variation, tick_length, color1, color2, color3, mode, brightness):
		self.variation = variation #some integer
		self.tick_length = tick_length 
		self.color1 = color1 #index of dict
		self.color2 = color2
		self.color3 = color3
		self.mode = mode #some integer
		self.brightness = brightness #[0,1]
		
	def reset(self):
		self.variation = 1
		self.tick_length = 0.001 
		self.color1 = 0
		self.color2 = 0
		self.color3 = 0
		self.mode = 0
		self.brightness = 1
