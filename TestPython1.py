import pyautogui, time, logging
import os, sys
import image
import random
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
screenWidth, screenHeight = pyautogui.size()

# Food order constants (don't change these: the image filenames depend on these specific values)
ONIGIRI = 'onigiri'
GUNKAN_MAKI = 'gunkan_maki'
CALIFORNIA_ROLL = 'california_roll'
SALMON_ROLL = 'salmon_roll'
SHRIMP_SUSHI = 'shrimp_sushi'
UNAGI_ROLL = 'unagi_roll'
DRAGON_ROLL = 'dragon_roll'
COMBO = 'combo'
ALL_ORDER_TYPES = (ONIGIRI, GUNKAN_MAKI, CALIFORNIA_ROLL, SALMON_ROLL, SHRIMP_SUSHI, UNAGI_ROLL, DRAGON_ROLL, COMBO)
Accounts = []

GAME_REGION = () # (left, top, width, height) values coordinates of the entire game window

class Complex:
	def __init__(self, AtX, AtY,imagpart): #Constructeur
		self.pos = AtX, AtY
		self.i = imagpart

def SetAllAccounts():
	Accounts.append(Complex(1215,268,'AccTest1'))

def navigateStartGameMenu():
	"""Performs the clicks to navigate form the start screen (where the PLAY button is visible) to the beginning of the first level."""
	# Click on everything needed to get past the menus at the start of the game.

	# click on Play
	logging.info('Looking for Play button...')
	while True: # loop because it could be the blue or pink Play button displayed at the moment.
		pos = pyautogui.locateCenterOnScreen(imPath('play_button.png'), region=GAME_REGION)
		if pos is not None:
			break
	pyautogui.click(pos, duration=0.25)
	logging.info('Clicked on Play button.')

	time.sleep(1)
	# click on Continue
	pos = pyautogui.locateCenterOnScreen(imPath('continue_button.png'), region=GAME_REGION)
	pyautogui.click(pos, duration=0.25)
	logging.info('Clicked on Continue button.')

	time.sleep(1)
	# click on Skip
	logging.info('Looking for Skip button...')
	while True: # loop because it could be the yellow or red Skip button displayed at the moment.
		pos = pyautogui.locateCenterOnScreen(imPath('skip_button.png'), region=GAME_REGION)
		if pos is not None:
			break
	pyautogui.click(pos, duration=0.25)
	logging.info('Clicked on Skip button.')

	# click on Continue
	pos = pyautogui.locateCenterOnScreen(imPath('continue_button.png'), region=GAME_REGION)
	pyautogui.click(pos, duration=0.25)
	logging.info('Clicked on Continue button.')	
	
def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)	

def getOrders():
	"""Scans the screen for orders being made. Returns a dictionary with a (left, top, width, height) tuple of integers for keys and the order constant for a value.
	The order constants are ONIGIRI, GUNKAN_MAKI, CALIFORNIA_ROLL, SALMON_ROLL, SHRIMP_SUSHI, UNAGI_ROLL, DRAGON_ROLL, COMBO."""
	orders = {}
	allOrders = pyautogui.locateAllOnScreen(imPath('hungry_color_percent.png'), region=(1430, 120, 235, 460))
	for order in allOrders:
		orders[order] = 'Cars'
	return orders	
	
def getGameRegion():
	"""Obtains the region that the Sushi Go Round game is on the screen and assigns it to GAME_REGION. The game must be at the start screen (where the PLAY button is visible)."""
	global GAME_REGION
	
	# identify the top-left corner
	logging.info('Finding game region...')
	region = pyautogui.locateOnScreen(imPath('top_right_corner.png'))
	if region is None:
		raise Exception('Could not find game on screen. Is the game visible?')

	# calculate the region of the entire game
	logging.info('Left: %s' % region[0])
	logging.info('Top: %s' % region[1])
	logging.info('Width: %s' % region[2])
	logging.info('Hieght: %s' % region[3])
	logging.info('Region: %s' % (region,))
	topRightX = region[0] + region[2] # left + width
	topRightY = region[1] # top
	GAME_REGION = (topRightX - 640, topRightY, 640, 480) # the game screen is always 640 x 480
	logging.info('Game region found: %s' % (GAME_REGION,))
	
currentOrders = getOrders()
logging.info(list(currentOrders.values()))
logging.info(list(currentOrders.items()))

for k in currentOrders:
	logging.info(k)
	logging.info(currentOrders[k])

#SetAllAccounts()
#logging.info(Accounts[0].pos)





