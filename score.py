
class Score:
	
	def __init__(self, auto=0, tote=0, container=0, litter=0, foul=0, coop=0):
		this.auto = auto
		this.tote = tote
		this.container = container
		this.litter = litter
		this.foul = foul
		this.coop = coop

	def total():
		return auto + tote + container + litter + coop - foul