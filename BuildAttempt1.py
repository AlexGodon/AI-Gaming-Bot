import pyautogui, time, logging, os, sys, random, copy, image #Modules
import ImportPSW # Other python files.
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
screenWidth, screenHeight = pyautogui.size()
#SCREEN_REGION = (1920,0,1680,1050) # sencond screen
pyautogui.PAUSE = 1 # This will increase the time btw each pyautogui func. 
#pyautogui.keyDown('capslock') # Turns capslock off.

# /////////////////////////////////////////////
# 			LIST OF THINGS TO DO
# 
# 	1. Give statistiques on which account eat the most food in the day, and how much food use, and at what price.
#	3. Prioritize whiskey and milk over truffles, currently it the truffles that go first... 
# 	4. 
# 	5. Always scan when in for the chef turn since Ninja is filling it up.
# 
# /////////////////////////////////////////////


# Take out any AutoHotKey scripts running
pyautogui.press('f6')

globalAccountCoord = () # This will be the account coordinates that will be used in all functions

# Market Food definied by HollowPrestige
TRUFFLE_COOKED = 'driedtruffles_cooked'
TRUFFLE_RAW = 'driedtruffles'


# Hunger levels that can be used
NOURISHED = 'nourished'
FINE = 'fine'
HUNGRY = 'hungry'
STARVING = 'starving'
ALL_NOURISH_TYPES = (FINE, HUNGRY, STARVING)

# All the different locations in DF
NT = 'nastya'
DS = 'dogg_stockade'
P13 = 'precinct_13'
FP = 'fort_pastor'
SB = 'secronom_bunker'
ALL_OUTPOSTS = (NT, DS, P13, FP, SB)

NEZ = 'north_end_zone'
SEZ = 'south_end_zone'
ALL_INNER_CITY = (NEZ, SEZ)

# All the different type of food that could be found in inventory
FRESH_MEAT = 'fresh_meat'
FRESH_VEG = 'fresh_vegitable'
FRESH_VEG1 = 'fresh_vegitable1'
RED_WINE = 'red_wine'
QUINOA = 'quinoa'
QUINOA1 = 'quinoa1'
TRUFFLE = 'truffle'
TRUFFLE1 = 'truffle1'
FRESH_MILK = 'fresh_milk'
WHISKY = 'whisky'
EMPTY_SLOT = 'empty_slot'

ALL_FOOD_TYPES_COLOR = {
FRESH_MEAT: {0: (93, 43, 29), 1: (163, 105, 97), 2: (161, 73, 62), 3: (14, 14, 14), 4: (177, 113, 96)},
FRESH_VEG: {0: (70, 37, 17), 1: (24, 18, 14), 2: (90, 102, 81), 3: (87, 79, 72), 4: (63, 59, 11)},
FRESH_VEG1: {0: (98,55,33), 1: (81,60,52), 2: (101,110,88), 3: (23,19,19), 4: (96,106,66)},
RED_WINE: {0: (55, 56, 51), 1: (209, 121, 128), 2: (22, 21, 17), 3: (175, 163, 144), 4: (23, 21, 17)},
QUINOA: {0: (98, 79, 36), 1: (90, 79, 57), 2: (83, 58, 23), 3: (51, 52, 43), 4: (21, 21, 17)},
QUINOA1: {0: (74,55,12), 1: (109,94,64), 2: (89,64,28), 3: (23,22,21), 4: (14,17,15)},
TRUFFLE: {0: (72, 60, 61), 1: (53, 51, 39), 2: (113, 78, 43), 3: (73, 65, 48), 4: (129, 128, 118)},
TRUFFLE1: {0: (19,13,18), 1: (98,98,85), 2: (99,62,31), 3: (24,22,20), 4: (114,113,104)},
FRESH_MILK: {0: (211, 194, 171), 1: (160, 125, 96), 2: (148, 120, 89), 3: (101, 85, 63), 4: (99, 91, 73)},
WHISKY: {0: (76, 47, 0), 1: (80, 80, 77), 2: (19, 20, 17), 3: (167, 111, 75), 4: (19, 19, 17)},
EMPTY_SLOT: {0: (21,19,17), 1: (17,14,13), 2: (19,20,17), 3: (18,16,15), 4: (19,19,17)}
}

ALL_FOOD_TYPES = (FRESH_MEAT, FRESH_VEG, FRESH_VEG1, RED_WINE, QUINOA, QUINOA1,
TRUFFLE, TRUFFLE1, FRESH_MILK, WHISKY, EMPTY_SLOT)

# We do not have and tables for 45+ food, cuz they are alone and in dividual per % range.
FOOD_LVL75_45PER = (QUINOA, TRUFFLE)
FOOD_LVL75_25PER = (FRESH_MILK, WHISKY)

# Proffession that they have
EXP = 'experience' #Exp class with +30% like entertainer.
FRM = 'farmer'
CHF = 'chef'
ENG = 'engineer'
DOC = 'doctor'

# Regiona Variable names
WIDTH = 'width'
HEIGHT = 'height'

# Region and pixel Vraiables
NOUTRISH_REGION = () # (left, top, width, height) values coordinates of the entire nourishment chart
NR_ZOOM = 150 # This can be either 200, or 150, this will change the Region location.
NR_CELL_SIZE = {WIDTH: {150: 75, 200: 105}, HEIGHT: {150: 65, 200: 90}} # gives you w/h of both 150 or 200 zoom

WEB_BROWSER_REGION = () # (left, top, width, height) values coordinates of the entire game window
WEB_BROWSER_SIZE = (840, 1010) # Width , Height, the web browser on a 1680x1050 window resolution, on half screen should have this size
WEB_B_ZOOM = 80 # all web pages, the login page, the innecr city, and the inventory page.

LOGIN_BOX_REGION = ()
LOGIN_BOX_SIZE = (585, 280)

GAME_REGION = ()
GAME_SIZE = (790, 560)

OUTGOING_OFFERS_REGION = ()
INCOMING_OFFERS_REGION = ()

INVENTORY_REGION = ()
STORAGE_REGION = ()
INVT_CELL_SIZE = (43,43) # Web browser zoom 80%
#INVENTORY_SIZE = (535, 75)

CHARACTER_REGION = ()
CHARACTER_SIZE = (575,455)

DF_TC_REGION = ()
DF_TC_SIZE = (193,139)

LAUNCH_IC_REGION = ()
LAUNCH_IC_SIZE = (300,63)

INVEN_BT = 'inventory'
THE_YARD = 'the_yard'
STORAGE_BT = 'storage'
MARKETPLACE = 'marketplace'
BANK = 'bank'
HISTORY_TOOLBAR = 'history_toolbar'

USERNAME_INPUT = 'username_input'
PSW_INPUT = 'password_input'
PRICE_INPUT = 'price_input'

LOGIN = 'login' # Shouldn't need this cuz 'Enter' can do it.

LOGOUT = 'logout'
BACK_TO_OUTPOST = 'back_to_outpost'
ACCEPT_MISSION = 'accept_mission' # NOT DOING THIS, This may not be needed. Cuz go drectly to inventroy, and in the inner city there are no missions.

DF_TOPCENTER = 'deadfrontier_top_center' # This will be add in ALL_BOUTONS_CORD only.This is the dead frontier log top center of the web page need to click, to take off and commercials.
PLAY_NOW = 'login_page_play_now' # This will be add in ALL_BOUTONS_CORD only.

INNER_CITY_PO = 'inner_city_personal_outpost' # This should be always to same cord, cuz will always be in 'Personal Outpost', if not then just log out.
LAUNCH_IN_INNERCITY = 'launch_in_browser'
START = 'start_ic'

CENTER_CHARACTER = 'center_of_character' # Needed to feed the alts.
BROWSER_ZOOM_100 = 'browser_zoom_100'

REMEBER_PSW = 'remembre_psw'
UPDATE_PSW = 'update_psw'
PSW_INCORRECT = 'password_incorrect'

DOWN_ARROW_INC_OFFER = 'down_arrow_incoming_offer'
DOWN_ARROW_OUT_OFFER = 'down_arrow_outgoing_offer'
DOWN_ARROW_MARKETPLACE = 'down_arrow_marketplace'
PRIVATE_TRADES = 'private_trades'


HOLLOW_MARKET_TAB = 'hollow_market_tab'
DEADFRONTIER_TAB = 'deadfrontier_tab'
SELECT_TRADEZONE = 'select_tradezone'
MARKETFILE_REP = 'marketfile_repertoire'
MARKETFILE_NAME = 'marketfile_name'
MARKETFILE_SAVE = 'marketfile_save'

ALL_LOGIN_BOX = {USERNAME_INPUT: (), PSW_INPUT: (), LOGIN: ()}
ALL_TOP_HEADER = {INVEN_BT: (), THE_YARD: (), STORAGE_BT: (), MARKETPLACE: (),BANK: (), HISTORY_TOOLBAR: (130,10)}
ALL_BOUTONS_CORD = {} # All other will be added dynamically.


# Default values every user accounts will need in there dictionary.
INVENTORY_DIC = 'inventory_dictionary'
STORAGE_DIC = 'storage_dictionary'
USEDFOOD_DIC = 'used_food_dictionary'

FOOD_SUPP = 'food_supplies'
FOOD_POS = 'food_postions'

PSW = 'password'
HUNGER_LVL = 'hunger_level'

LOCATION = 'location'

SKIPACC = 'skip_account' # This will skip the account that Has this true.
FIRST_TIME = 'first_time_logging_in' #This flag is use to calculate, and count how many truffles/food are in the inventory
STORAGE_SCANNED = 'storage_scanned'
INVENTORY_SCANNED = 'inventory_scanned'
OUTGOING_LIST_SCANNED = 'outgoing_list_scanned'
OUTGOING_LIST_COUNT = 'outgoing_list_count'
NO_FOOD_IN_STORAGE = 'no_food_in_storage'
SEND_FOOD_CHF = 'send_food_chef' # this is to know the chef account who will recieve the generated food.
FOOD_SELLING_LIST = 'food_in_selling_list'
LVL_ACC = 'level_of_account'
LOG_IN = 'logged_in_the_account'



ALL_FRM_ACCOUNTS = ((10,12),(31,12),(33,12),(2,12),(22,12))

ACCOUNTS_USERNAME = {
'1alex12': (1,1), '2alex12': (2,12), '3alex12': (2,5), '4alex12': (3,1), '5alex12': (1,4),
'6alex12': (1,3), '7alex12': (3,5), '8alex12': (3,2), '9alex12': (2,2), '10alex12': (10,12),
'22alex12': (22,12), '31alex12': (31,12), '33alex12': (33,12), 'Aizawa Shouta': (2,1), 'Chimney Train': (1,5),
'Detrimenta1': (1,2), 'Dirty Heads': (2,4), 'Django Unchained': (3,4), 'Ehhh Whats Up Doc': (2,3), 
'Zoro Roronoa': (3,3)
}

# Any other values every user may need. That will be unique for every account.
USERNAME = 'username'
USER_ID = 'user_id' # Account ID if ever needed
PROFF = 'proffession' # The profession of that character
OUTPOST = 'outpostlocation' # if its none, need to check it, and then set it. if logging in to it.

# Waiting timer default settings, all in seconds.
TIME_LOGIN_ACCOUNT = 15
TIME_WAIT_IC_LOAD = 40
TIME_TYPING_SPEED = 0.1

# This will be the account Dictionary that will give all the info needed on account corridnates
# This is relate the the webpage. DF Alt Nourishment Final.html or Image: ImageCorrAccounts.png
ACCOUNTS = {}
COLUMS = 3 # number of colmuns in the html file
ROWS = 5 # number of rows in the html file
def main(pLogFarmers=1,pSetInitial=1):
	iCntMin = 0
	# iCntHour = 0

	iMinuteLoop = 3
	"""Runs the entire program. The Sushi Go Round game must be visible on the screen and the PLAY button visible."""
	logging.info('Program Started. Press Ctrl-C to abort at any time.')
	logging.info('To interrupt mouse movement, move mouse to upper left corner.')

	SetAccValues()
	getQuickRegionBoutonsCoord()
	if pSetInitial == 1: initialSetup() #Sets the browsers, and goes on df.

	if pLogFarmers == 1: loggingAllFarmerAccounts()

	while True:
		mainLoop()
		iMinuteLoop = random.randint(1, 4)
		logging.info('Going to wait %smin before next scan...' % iMinuteLoop)
		for t in range(iMinuteLoop): # Num minutes total
			time.sleep(60) # 1 minute
			iCntMin += 1

		if iCntMin >= 30: # 30 minutes
			reportOnAccountNeedFood()
			iCntMin = 0
			# iCntHour += 1

		# if iCntHour >= 2: # 2*30min = 1hour
		# 	logging.info('1hour check for food from incoming selling list...')
		# 	getFoodFromIncomingOfferFromChef()
		# 	iCntHour = 0

def mainLoop():
	CurntAccntNeedFood = getAccountsNeedFood()
	# logging.info(CurntAccntNeedFood)
	for Cord,Hunger in CurntAccntNeedFood.items():
		logging.info('Account: %s Hunger: %s' % (ACCOUNTS[Cord][USERNAME],Hunger))
		globalAccountCoord = Cord
		loggingInAccnt(Cord,Hunger)
		feedTheAccounts(Cord,Hunger)
		loggingOutAccnt(Cord)

def reportOnAccountNeedFood():
	""" This is going to give a small report to say
	which was used, and is now out of food.

	"""
	bFlagFoundFood = 0
	iCntAccFound = 0 

	logging.info('30min report on empty inventory accounts:')

	for Coord, AccDic in ACCOUNTS.items():
		if AccDic[LOG_IN] == True:
			if Coord not in ALL_FRM_ACCOUNTS:
				if AccDic[SKIPACC] == True:
					for FoodType in ALL_FOOD_TYPES:
						if AccDic[INVENTORY_DIC][FOOD_SUPP][FoodType] != 0 and FoodType != EMPTY_SLOT:
							bFlagFoundFood = 1
							break
					if bFlagFoundFood == 0:
						logging.info('Account: %s is OUT OF FOOD!!!' % AccDic[USERNAME])
						iCntAccFound += 1
					bFlagFoundFood = 0

				logging.info('Account: %s - Used Food: %s' % (AccDic[USERNAME],AccDic[USEDFOOD_DIC][FOOD_SUPP]))

	# if iCntAccFound == 0:
	# 	logging.info('No accounts need food.')

def SetAccDefaultDictionary():

	global ACCOUNTS
	
	for Corr,AccDic in ACCOUNTS.items():
		# Set in the default values for all accounts.
		AccDic[INVENTORY_DIC] = {}
		AccDic[STORAGE_DIC] = {}
		AccDic[USEDFOOD_DIC] = {FOOD_SUPP: {}}		
		# Account Status
		AccDic[PSW] = ImportPSW.PSWACC_ALT
		AccDic[HUNGER_LVL] = HUNGRY
		AccDic[LVL_ACC] = 75
		# Flags needed
		AccDic[FIRST_TIME] = True
		AccDic[INVENTORY_SCANNED] = False
		AccDic[SKIPACC] = False
		AccDic[LOG_IN] = False
		AccDic[FOOD_SELLING_LIST] = True
		AccDic[STORAGE_SCANNED] = False
		AccDic[NO_FOOD_IN_STORAGE] = False
		AccDic[OUTGOING_LIST_SCANNED] = False
		AccDic[OUTGOING_LIST_COUNT] = 0

def SetAccValues():
	""" This is where all the DF accounts are setup. """

	# How to setup and use the ACCOUNTS variable:
	#SetAccValues()		
	#logging.info(ACCOUNTS[(1,1)])
	#logging.info(ACCOUNTS[(1,1)][USERNAME])

	global ACCOUNTS

	# Creates to coordinates in a dictionary based on global variable ROWS, COLUMS
	#for k in range(1,COLUMS+1):
	#	for j in range(1,ROWS+1):
	#		ACCOUNTS[(k, j)] = {}

	#for FrmCord in ALL_FRM_ACCOUNTS:
	#	ACCOUNTS[FrmCord] = {}

	for UserName, Coord in ACCOUNTS_USERNAME.items():
		ACCOUNTS[Coord] = {}
		ACCOUNTS[Coord][USERNAME] = UserName

	#ACCOUNTS[(10,12)] = {} # account 10alex12, to setup to boutons coordinates.

	# Set in the default values for all accounts.
	SetAccDefaultDictionary()
	
	for Corr,AccDic in ACCOUNTS.items():
		# Set in individule unique values per account.
		if AccDic[USERNAME] == '1alex12':
			# if Corr == (1,1):
			AccDic[USER_ID] = 4763057
			AccDic[PROFF] = EXP
			AccDic[OUTPOST] = None
			AccDic[PSW] = ImportPSW.PSWACC_MAIN
		elif AccDic[USERNAME] == 'Aizawa Shouta':	
			# elif Corr == (2,1):
			AccDic[USER_ID] = 12598203
			AccDic[PROFF] = DOC
			AccDic[OUTPOST] = SB
			AccDic[LVL_ACC] = 51
			AccDic[HUNGER_LVL] = STARVING
		elif AccDic[USERNAME] == '4alex12':	
			# elif Corr == (3,1):
			AccDic[USER_ID] = 8819066
			AccDic[PROFF] = ENG
			AccDic[OUTPOST] = SB
			AccDic[LVL_ACC] = 51
			AccDic[HUNGER_LVL] = HUNGRY
			# AccDic[SKIPACC] = True

		elif AccDic[USERNAME] == 'Detrimenta1':	
			# elif Corr == (1,2):
			AccDic[USER_ID] = 12251511
			AccDic[PROFF] = ENG
			AccDic[OUTPOST] = None
		elif AccDic[USERNAME] == '9alex12':	
			# elif Corr == (2,2):
			AccDic[USER_ID] = 9700265
			AccDic[PROFF] = DOC
			AccDic[OUTPOST] = NEZ
			AccDic[LVL_ACC] = 51
			AccDic[HUNGER_LVL] = HUNGRY
		elif AccDic[USERNAME] == '8alex12':
			# elif Corr == (3,2):
			AccDic[USER_ID] = 9657621
			AccDic[PROFF] = ENG
			AccDic[OUTPOST] = NEZ
			AccDic[LVL_ACC] = 51
			AccDic[HUNGER_LVL] = HUNGRY

		elif AccDic[USERNAME] == '6alex12':
			# elif Corr == (1,3):
			AccDic[USER_ID] = 9554926
			AccDic[PROFF] = CHF
			AccDic[OUTPOST] = None
			AccDic[PSW] = ImportPSW.PSWACC_OTH
			#AccDic[SKIPACC] = True
		elif AccDic[USERNAME] == 'Ehhh Whats Up Doc':
			# elif Corr == (2,3):
			AccDic[USER_ID] = 10703710
			AccDic[PROFF] = DOC
			AccDic[OUTPOST] = NEZ
		elif AccDic[USERNAME] == 'Zoro Roronoa':
			# elif Corr == (3,3):
			AccDic[USER_ID] = 9833806
			AccDic[PROFF] = ENG
			AccDic[OUTPOST] = NEZ
			#AccDic[SKIPACC] = True

		elif AccDic[USERNAME] == '5alex12':
			# elif Corr == (1,4):
			AccDic[USER_ID] = 8816971
			AccDic[PROFF] = CHF
			AccDic[OUTPOST] = SEZ
			#AccDic[SKIPACC] = True
		elif AccDic[USERNAME] == 'Dirty Heads':
			# elif Corr == (2,4):
			AccDic[USER_ID] = 10882756
			AccDic[PROFF] = DOC
			AccDic[OUTPOST] = SB
			#AccDic[SKIPACC] = 1
		elif AccDic[USERNAME] == 'Django Unchained':
			# elif Corr == (3,4):
			AccDic[USER_ID] = 11769177
			AccDic[PROFF] = ENG
			AccDic[OUTPOST] = SB
			#AccDic[SKIPACC] = 1

		elif AccDic[USERNAME] == 'Chimney Train':
			# elif Corr == (1,5):
			AccDic[USER_ID] = 9554926
			AccDic[PROFF] = CHF
			AccDic[OUTPOST] = FP
			AccDic[LVL_ACC] = 51
		elif AccDic[USERNAME] == '3alex12':
			# elif Corr == (2,5):
			AccDic[USER_ID] = 4765544
			AccDic[PROFF] = DOC
			AccDic[OUTPOST] = FP
			AccDic[LVL_ACC] = 51
		elif AccDic[USERNAME] == '7alex12':
			# elif Corr == (3,5):
			AccDic[USER_ID] = 9614619
			AccDic[PROFF] = ENG
			AccDic[OUTPOST] = FP
			AccDic[LVL_ACC] = 51

		# Farmers
		elif AccDic[USERNAME] == '10alex12':
			# elif Corr == (10,12):
			AccDic[USER_ID] = 9710128
			AccDic[PROFF] = FRM
			AccDic[LVL_ACC] = 51
			AccDic[OUTPOST] = SB
			AccDic[SKIPACC] = 1
			AccDic[SEND_FOOD_CHF] = '6alex12'
		elif AccDic[USERNAME] == '2alex12':
			# elif Corr == (2,12):
			AccDic[USER_ID] = 6881326
			AccDic[PROFF] = FRM
			AccDic[LVL_ACC] = 82
			AccDic[OUTPOST] = None
			AccDic[SKIPACC] = 0
			AccDic[SEND_FOOD_CHF] = '6alex12'
		elif AccDic[USERNAME] == '22alex12':
			# elif Corr == (22,12):
			AccDic[USER_ID] = 12632060
			AccDic[PROFF] = FRM
			AccDic[LVL_ACC] = 82
			AccDic[OUTPOST] = None
			AccDic[SKIPACC] = 0
			AccDic[SEND_FOOD_CHF] = '6alex12'
		elif AccDic[USERNAME] == '31alex12':
			# elif Corr == (31,12):
			AccDic[USER_ID] = 12633603
			AccDic[PROFF] = FRM
			AccDic[LVL_ACC] = 51
			AccDic[OUTPOST] = FP
			AccDic[SKIPACC] = 0
			AccDic[SEND_FOOD_CHF] = '6alex12'
		elif Corr == (33,12):
			#AccDic[USERNAME] = '33alex12'
			AccDic[USER_ID] = 12634662
			AccDic[PROFF] = FRM
			AccDic[LVL_ACC] = 51
			AccDic[OUTPOST] = FP
			AccDic[SKIPACC] = 0
			AccDic[SEND_FOOD_CHF] = '6alex12'


		else:
			logging.info('Account Corr: %s was not found' % str(Corr))

	logging.info('All Accounts are now set!')
	
def initialSetup():
	""" This is the setup that will be used to setup both browser

	Drag and drop the length of the browser(Comodo) to the nessisary length (1059), and click on the 100%

	"""
	os.startfile("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
	time.sleep(5)
	pyautogui.hotkey('win','right')
	time.sleep(1)
	pyautogui.moveTo(843,50)
	pyautogui.dragTo((843-203),50,1.5) # Enlarge the web browser to the right size.
	time.sleep(3)
	pyautogui.press('f5')
	time.sleep(4)
	pyautogui.press('f5')
	time.sleep(4)	

	os.startfile("D:\Program Files (x86)\Comodo\IceDragon\icedragon.exe")
	time.sleep(5)
	pyautogui.hotkey('win','left')
	time.sleep(1)
	pyautogui.moveTo(835,50)
	pyautogui.dragTo(1059,50,1.5) # Enlarge the web browser to the right size.
	pyautogui.click(ALL_BOUTONS_CORD[BROWSER_ZOOM_100]) # Click for 100% Zoom
	pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT]) # Click for 100% Zoom


	time.sleep(3)
	pyautogui.keyDown('alt')
	pyautogui.press('tab')
	pyautogui.press('tab')
	pyautogui.keyUp('alt')
	
	pyautogui.keyDown('alt')
	pyautogui.press('tab')
	pyautogui.keyUp('alt')

	logging.info('Initial setup is set!')

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended.
	
	Make sure that the 'images' folder that contains all the images is in the same location 
	as the programe.
	
	Ex: C:\Temp\Test.py then the folder will be in C:\Temp\images"""
    return os.path.join('images', filename)

def getRegions():
	"""Obtains the region that Noutrition HTML is on the screen and assigns it to NOUTRISH_REGION. 
	The html must be in google chrome, under 150 or 200 zoom, change NR_ZOOM to decide.
	Also make sure, the account 1alex12 is on the cell 1,1, top left, or else it wont find it."""
	
	global NOUTRISH_REGION, WEB_BROWSER_REGION, GAME_REGION, INVENTORY_REGION, CHARACTER_REGION
	global ALL_TOP_HEADER, ALL_INGAME, ALL_BOUTONS_CORD

	# NOUTRISH_REGION
	# identify the top-left corner
	logging.info('Finding Nourishment chart region, using 1alex12 acc...')
	region = pyautogui.locateOnScreen(imPath('top_left_noutrition_chart_%s.png' % NR_ZOOM))
	if region is None:
		raise Exception('Could not find nourishment chart. Is the chart visible? Or.. is the zoom on the web page different then %s percent?' % NR_ZOOM)

	# The chart dimension is the CellWidthpx*# of colums, CellHeightpx*# of rows.
	NOUTRISH_REGION = (region[0], region[1], NR_CELL_SIZE[WIDTH][NR_ZOOM]*COLUMS, NR_CELL_SIZE[HEIGHT][NR_ZOOM]*ROWS) 
	logging.info('Chart region found: %s' % (NOUTRISH_REGION,))


	# WEB_BROWSER_REGION - THIS REGION IS NEVER FOUND NO MATTER THE IMAGE I PUT...
	logging.info('Finding Browser region, using top right "x" corner...')
	region = pyautogui.locateOnScreen(imPath('top_left_inactive_web_browser.png'),region=SCREEN_REGION)
	if region is None:
		logging.info('Could not find inactive web browser, looking for the active...')
		region = pyautogui.locateOnScreen(imPath('top_right_web_browser.png'))
		if region is None:
			raise Exception('Could not find the Web Browser. Is the Browser visible?')
	# calculate the region of the entire chart (left, top, width, height)/ ([0],[1],[2],[3])
	#topRightX = region[0] + region[2] # left + width
	topRightX = region[0] # left
	topRightY = region[1] # top
	#topRightX = topRightX - WEB_BROWSER_SIZE[0]
	if topRightX < 0: topRightX = 0
	if topRightY < 0: topRightY = 0
	WEB_BROWSER_REGION = (topRightX, topRightY, WEB_BROWSER_SIZE[0], WEB_BROWSER_SIZE[1]) 
	#WEB_BROWSER_REGION = (0, 0, WEB_BROWSER_SIZE[0], WEB_BROWSER_SIZE[1])
	logging.info('Web browser region found: %s' % (WEB_BROWSER_REGION,))
	logging.info('Also make sure all the web pages are at : %s zoom, login page, inner city, inventory, etc.' % WEB_B_ZOOM)

	
	# ALL_BOUTONS_CORD
	logging.info('Finding the boutons in the browser bookmarks toolbar...')
	for name in ALL_TOP_HEADER.keys():
		if name == HISTORY_TOOLBAR:
			ALL_TOP_HEADER[name] = (WEB_BROWSER_REGION[0]+ALL_TOP_HEADER[name][0], WEB_BROWSER_REGION[1]+ALL_TOP_HEADER[name][1])
		else:
			region = pyautogui.locateCenterOnScreen(imPath('bouton_%s.png' % name), region=(WEB_BROWSER_REGION[0],WEB_BROWSER_REGION[1],WEB_BROWSER_REGION[2],150))
			if region is None:
				raise Exception('Could not find %s bouton.' % name)
			else:
				ALL_TOP_HEADER[name] = (region)
		logging.info('Found bouton: %s in bookmark toolbar coordinates: %s' % (name, ALL_TOP_HEADER[name]))
	# Puts all the Boutons found in the Top header. bookmarks in the ALL_BOUTONS dictionary
	for key, val in ALL_TOP_HEADER.items():
		ALL_BOUTONS_CORD[key] = val

	pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT])
	logging.info('Finding the login box region, using creation account...')

	region = waitWhileTrue('top_left_login_box_creation_account', WEB_BROWSER_REGION)
	# LOGIN_BOX_REGION
	#if region is None:
	#	logging.info('Could not find Login Box, looking for DF top center...')
	##	getDF_TOPCENTnPLAY_NOWCoord()
	##	# Open the login box and try to set the coordinates again.
	#	pyautogui.moveTo(ALL_BOUTONS_CORD[PLAY_NOW])
	#	pyautogui.click()
	#	while True: # loop because waiting for the Start bouton in inner_city to show up
	#		pos = pyautogui.locateOnScreen(imPath('top_left_login_box_creation_account.png'), region=(WEB_BROWSER_REGION))
	#		if pos is not None:
	#			break
	#	region = pyautogui.locateOnScreen(imPath('top_left_login_box_creation_account.png'), region=(WEB_BROWSER_REGION))
	#	if region is None:
	#		raise Exception('Could not find Login Box, it didnt open after 5 second wait.')
	#	else:
	#		getLoginBoxBoutonsCoord(region)
	#else:
	#if region is None:
	#	('Login box is not found...')
	getLoginBoxBoutonsCoord(region)
	# Puts all the Boutons found in the Login Box in the ALL_BOUTONS dictionary
	for key, val in ALL_LOGIN_BOX.items():
		ALL_BOUTONS_CORD[key] = val

	# This will click to allow the programe to detect DF_TOPCENTER, and PLAY_NOW, if ever needed.
	pyautogui.click(region[0], region[1]-25) # Click outside of the Login box
	time.sleep(0.5)
	getDF_TOPCENTnPLAY_NOWCoord()

	# To open the Login box again, to be sure that its open after this process.
	pyautogui.click(ALL_BOUTONS_CORD[PLAY_NOW])
	
	region = waitWhileTrue('top_left_login_box_creation_account', WEB_BROWSER_REGION)

	# This will login to the account 10alex12.
	loggingInAccnt((10,12),5)
	pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
	time.sleep(0.5) # this is in case of a pop-up. No need to check for location cuz i know this account is at SB.

	# GAME_REGION
	logging.info('Finding the game region, using back to outpost...')
	region = pyautogui.locateOnScreen(imPath('top_left_back_to_outpost_bouton.png'), region=(WEB_BROWSER_REGION))
	if region is None:
		logging.info('Could not find game region, using "back to outpost" bouton.')
	else:
		GAME_REGION = (region[0], region[1], GAME_SIZE[0], GAME_SIZE[1])
		logging.info('Game region found: %s' % (GAME_REGION,))
		ALL_BOUTONS_CORD[BACK_TO_OUTPOST] = (region[0]+int(region[2]/2),region[1]+int(region[3]/2)+5)
		logging.info('Found bouton: %s in game region coordinates: %s' % (BACK_TO_OUTPOST, ALL_BOUTONS_CORD[BACK_TO_OUTPOST]))
		region = pyautogui.locateCenterOnScreen(imPath('bouton_%s.png' % LOGOUT), region=(GAME_REGION))
		if region is None:
			raise Exception('Could not find %s bouton.' % LOGOUT)
		else:
			ALL_BOUTONS_CORD[LOGOUT] = (region)
			logging.info('Found bouton: %s in game region coordinates: %s' % (LOGOUT, ALL_BOUTONS_CORD[LOGOUT]))

	# INVENTORY_REGION
	INVENTORY_REGION = (GAME_REGION[0]+206, GAME_REGION[1]+400, INVT_CELL_SIZE[0]*15, INVT_CELL_SIZE[1]*2)
	logging.info('Inventory region found: %s' % (INVENTORY_REGION,))

	# CHARACTER_REGION
	CHARACTER_REGION = (GAME_REGION[0]+185, GAME_REGION[1]+43, CHARACTER_SIZE[0], CHARACTER_SIZE[1])
	logging.info('Character region found: %s' % (CHARACTER_REGION,))

	ALL_BOUTONS_CORD[CENTER_CHARACTER] = (CHARACTER_REGION[0]+int(CHARACTER_REGION[2]/2),CHARACTER_REGION[1]+int(CHARACTER_REGION[3]/2)-88)
	logging.info('Center of character: %s' % ALL_BOUTONS_CORD[CENTER_CHARACTER])
	pyautogui.click(ALL_BOUTONS_CORD[LOGOUT])
	time.sleep(5)

	# Login to Zoro Roronoa. To get the inner_city boutons.
	loggingInAccnt((3,3),5)

	logging.info('Looking for "%s"...' % LAUNCH_IN_INNERCITY)
	region = waitWhileTrue('launch_in_browser', CHARACTER_REGION)
	CordX = region[0]+int(region[2]/2)
	CordY = region[1]+int(region[3]/2)
	ALL_BOUTONS_CORD[LAUNCH_IN_INNERCITY] = (CordX,CordY)
	logging.info('Found bouton: %s in game region coordinates: %s' % (LAUNCH_IN_INNERCITY, ALL_BOUTONS_CORD[LAUNCH_IN_INNERCITY]))
	ALL_BOUTONS_CORD[START] = (CordX,CordY+28)
	logging.info('Found bouton: %s in game region coordinates: %s' % (START, ALL_BOUTONS_CORD[START]))
	LAUNCH_IC_REGION = (region[0],region[1],LAUNCH_IC_SIZE[0],LAUNCH_IC_SIZE[1]+50)
	logging.info('Launch in browser region found: %s' % (LAUNCH_IC_REGION,))

	pyautogui.click(ALL_BOUTONS_CORD[LAUNCH_IN_INNERCITY])
	logging.info('Waiting for Start bouton to appear, %s seconds...' % TIME_WAIT_IC_LOAD)
	time.sleep(TIME_WAIT_IC_LOAD)
	logging.info('Going into personal outpost.')
	pyautogui.click(ALL_BOUTONS_CORD[START])
	pyautogui.press('o') # go into outpost
	time.sleep(10)
	pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
	time.sleep(0.5) # in case of pop-up.

	# You are now in personal outpost, so let set the innercity bouton coordinates.
	pos = pyautogui.locateCenterOnScreen(imPath('bouton_%s.png') % INNER_CITY_PO, region=(CHARACTER_REGION))
	if pos is None:
		raise Exception('Could not find bouton %s' % INNER_CITY_PO)
	else:
		ALL_BOUTONS_CORD[INNER_CITY_PO] = (pos)
		logging.info('Found bouton: %s in character region coordinates: %s' % (INNER_CITY_PO, ALL_BOUTONS_CORD[INNER_CITY_PO]))

	# this will loggout Zoro Roronoa
	innercityLogout((3,3))

def getQuickRegionBoutonsCoord():

	""" This will basically quickly set all the regions needed and the boutons to be able
	to test any other procedure without waiting 2min each time."""

	global NOUTRISH_REGION, WEB_BROWSER_REGION, LOGIN_BOX_REGION
	global DF_TC_REGION, GAME_REGION, INVENTORY_REGION, CHARACTER_REGION
	global LAUNCH_IC_REGION, STORAGE_REGION, OUTGOING_OFFERS_REGION, INCOMING_OFFERS_REGION
	global ALL_BOUTONS_CORD

	# REGIONS
	NOUTRISH_REGION = (1438,117,225,325)
	WEB_BROWSER_REGION = (0,0,1059,1010)
	LOGIN_BOX_REGION = (125,350,800,415)
	DF_TC_REGION = (350,95,345,305)
	GAME_REGION = (33,144,979,668)
	INVENTORY_REGION = (293,835,659,87) #inside on the first pixel, this is proven by tests. it official
	STORAGE_REGION = (368,512,513,278) #inside on the first pixel, this is proven by tests. it official
	CHARACTER_REGION = (262,200,718,572)
	LAUNCH_IC_REGION = (280,360,520,120)
	INCOMING_OFFERS_REGION = (285,485,678,150)
	OUTGOING_OFFERS_REGION = (285,650,678,144)

	# All boutons
	ALL_BOUTONS_CORD[MARKETPLACE] = (216,116)
	ALL_BOUTONS_CORD[BANK] = (291,116)
	ALL_BOUTONS_CORD[STORAGE_BT] = (352,116)
	ALL_BOUTONS_CORD[INVEN_BT] = (430,116)
	ALL_BOUTONS_CORD[THE_YARD] = (504,116)
	ALL_BOUTONS_CORD[HISTORY_TOOLBAR] = (130,10)
	ALL_BOUTONS_CORD[USERNAME_INPUT] = (710,493)
	ALL_BOUTONS_CORD[PSW_INPUT] = (710,524)
	ALL_BOUTONS_CORD[LOGIN] = (690,596)
	ALL_BOUTONS_CORD[DF_TOPCENTER] = (522,233)
	ALL_BOUTONS_CORD[PLAY_NOW] = (880,625)
	ALL_BOUTONS_CORD[BACK_TO_OUTPOST] = (173,370)
	ALL_BOUTONS_CORD[LOGOUT] = (890,370)
	ALL_BOUTONS_CORD[CENTER_CHARACTER] = (620,570)
	ALL_BOUTONS_CORD[LAUNCH_IN_INNERCITY] = (520,415)
	ALL_BOUTONS_CORD[START] = (535,465)
	ALL_BOUTONS_CORD[INNER_CITY_PO] = (835,705)
	ALL_BOUTONS_CORD[BROWSER_ZOOM_100] = (1010,115)
	ALL_BOUTONS_CORD[REMEBER_PSW] = (410,240)
	ALL_BOUTONS_CORD[UPDATE_PSW] = (310,240)
	ALL_BOUTONS_CORD[PSW_INCORRECT] = (635,485)
	ALL_BOUTONS_CORD[PRICE_INPUT] = (604,663)
	ALL_BOUTONS_CORD[SELECT_TRADEZONE] = (140,492)
	ALL_BOUTONS_CORD[MARKETFILE_REP] = (280,48)
	ALL_BOUTONS_CORD[MARKETFILE_NAME] = (380,422)
	ALL_BOUTONS_CORD[MARKETFILE_SAVE] = (680,493)
	ALL_BOUTONS_CORD[DOWN_ARROW_INC_OFFER] = (940,612)
	ALL_BOUTONS_CORD[DOWN_ARROW_OUT_OFFER] = (940,780)
	ALL_BOUTONS_CORD[DOWN_ARROW_MARKETPLACE] = (940,725)
	ALL_BOUTONS_CORD[PRIVATE_TRADES] = (714,462)


	#ALL_BOUTONS_CORD[HOLLOW_MARKET_TAB] = (330,48)
	#ALL_BOUTONS_CORD[DEADFRONTIER_TAB] = (115,48)

	logging.info('All quick coordinates are set!')

def getLoginBoxBoutonsCoord(pRegion):
	global ALL_LOGIN_BOX, LOGIN_BOX_REGION

	LOGIN_BOX_REGION = (pRegion[0], pRegion[1], LOGIN_BOX_SIZE[0], LOGIN_BOX_SIZE[1])
	logging.info('Login box region found: %s' % (LOGIN_BOX_REGION,))
	time.sleep(2)
	for name in ALL_LOGIN_BOX.keys():
		region = pyautogui.locateOnScreen(imPath('bouton_%s.png' % name), region=(LOGIN_BOX_REGION))
		if region is None:
			raise Exception('Could not find the bouton %s in the login box region, is the region opened?' % name)
		else:
			if name != LOGIN: # This will be either username or password input.
				ALL_LOGIN_BOX[name] = (region[0]+region[2]+10, region[1]+int(region[3]/2))
			else: # It is the login bouton that should not be needed. Becuase the 'Enter' keys does the same.
				ALL_LOGIN_BOX[name] = (region[0]+int(region[2]/2), region[1]+int(region[3]/2))
			logging.info('Found bouton: %s in login box coordinates: %s' % (name, ALL_LOGIN_BOX[name]))

def getDF_TOPCENTnPLAY_NOWCoord():
	global ALL_BOUTONS_CORD

	region = pyautogui.locateCenterOnScreen(imPath('login_page_dead_frontier_logo_center_position_415x210.png'), region=(WEB_BROWSER_REGION))
	if region is None:
		raise Exception('Could not find the DF top center logo.')
	else:
		ALL_BOUTONS_CORD[DF_TOPCENTER] = (region[0], region[1])
		DF_TC_REGION = (region[0], region[1], DF_TC_SIZE[0], DF_TC_SIZE[1])
		logging.info('DF_TopCenter region found: %s' % (DF_TC_REGION,))
		logging.info('Found bouton: %s in login page coordinates: %s' % (DF_TOPCENTER, ALL_BOUTONS_CORD[DF_TOPCENTER]))
		region = pyautogui.locateCenterOnScreen(imPath('%s.png' % PLAY_NOW), region=(WEB_BROWSER_REGION))
		if region is None:
			raise Exception('Could not find %s bouton.' % PLAY_NOW)
		else:
			ALL_BOUTONS_CORD[PLAY_NOW] = (region[0], region[1])
			logging.info('Found bouton: %s in login page coordinates: %s' % (PLAY_NOW, ALL_BOUTONS_CORD[PLAY_NOW]))

def getAccountsNeedFood():
	"""This will basically scan and give back any cooridnates of found "%" image 
	of a certaine hunger lvl.

	The Nourishment level are FINE, HUNGRY, STARVING """
	accnts = {}
	accntCord = ()
	for NourishLvl in ALL_NOURISH_TYPES:
		allAccnts = pyautogui.locateAllOnScreen(imPath('percent_%s_%s.png' % (NourishLvl,NR_ZOOM)), region=(NOUTRISH_REGION))
		for coord in allAccnts:
			# Check if account is skipped, or the hunger lvl is == or lower then its set lvl.
			accntCord = getChartCellFromXYCoordinates(coord[0], coord[1])
			if (ACCOUNTS[accntCord][SKIPACC] == 0) and (WeFeedTheAccnt(NourishLvl, accntCord) == True):
				accnts[accntCord] = NourishLvl
	return accnts

def getChartCellFromXYCoordinates(CordX, CordY):
	
	# coord[0] = X <-->, coord[1] = Y up n down.
	# X section
	Rng1 = NOUTRISH_REGION[0]
	for i in range(COLUMS):
		Rng2 = (Rng1+NR_CELL_SIZE[WIDTH][NR_ZOOM]) 
		if Rng1 < CordX < Rng2:
			CordX = (i+1)
			break
		Rng1 = Rng2

	# Y Section
	Rng1 = NOUTRISH_REGION[1]
	for i in range(ROWS):
		Rng2 = (Rng1+NR_CELL_SIZE[HEIGHT][NR_ZOOM]) 
		if Rng1 < CordY < Rng2:
			CordY = (i+1)
			break
		Rng1 = Rng2
	return (CordX, CordY)

def loggingInAccnt(Coord,HungerStatus=''):
	""" Always make sure when you logout you leave on the login box and make sure 
	When your done logging in you are always at the inventory screen.
	
	You need to only do tab, and try the browser account, psw, wait 6 sec, if you get "Password incorect" then try the default one.

	"""
	global ACCOUNTS

	# This will login to the account.

	logging.info('Looking for "creation account" in the login box...')
	region = pyautogui.locateOnScreen(imPath('top_left_login_box_creation_account.png'), region=(WEB_BROWSER_REGION))
	if region is None:
		pyautogui.click(ALL_BOUTONS_CORD[PLAY_NOW])
		region = pyautogui.locateOnScreen(imPath('top_left_login_box_creation_account.png'), region=(WEB_BROWSER_REGION))
		if region is None:
			raise Exception('The login box would not open and is not found.')
	logging.info('Logging in Account: %s, Hunger: %s' % (ACCOUNTS[Coord][USERNAME],HungerStatus))
	pyautogui.click(ALL_BOUTONS_CORD[USERNAME_INPUT])
	pyautogui.hotkey('ctrl', 'a')
	pyautogui.press('backspace')
	pyautogui.typewrite(ACCOUNTS[Coord][USERNAME], interval=TIME_TYPING_SPEED)
	time.sleep(1)
	pyautogui.press('tab')
	# use the browsers remebered psw if it doesnt work wait for the "password incorrect"
	#pyautogui.press('enter') # or could click on the login bt, ALL_BOUTONS_CORD[LOGIN]
	#time.sleep(7)
	#return
	#region = pyautogui.locateOnScreen(imPath('%s.png' % PSW_INCORRECT), region=(WEB_BROWSER_REGION))
	#if region != None: # if the remebered password is in correct, ex not defined, then try the default one.
		#logging.info('Found incorrect password from browser, will try default...')
		#pyautogui.press('enter')
		#time.sleep(3)
		#pyautogui.click(ALL_BOUTONS_CORD[PSW_INPUT])
	pyautogui.hotkey('ctrl', 'a')
	pyautogui.press('backspace')
	pyautogui.typewrite(ACCOUNTS[Coord][PSW], interval=TIME_TYPING_SPEED)
	pyautogui.press('enter')
	time.sleep(5)

	#region = pyautogui.locateOnScreen(imPath('%s.png' % PSW_INCORRECT), region=(WEB_BROWSER_REGION))
	#if region != None:
		#loging.info('Password could not be found, did not login the account: %s' % ACCOUNTS[Coord][USERNAME])
		#return
	#else:
		#pyautogui.click(ALL_BOUTONS_CORD[UPDATE_PSW])
		#pyautogui.click(ALL_BOUTONS_CORD[REMEBER_PSW])

	if ACCOUNTS[Coord][OUTPOST] == None:
		ACCOUNTS[Coord][OUTPOST] = getAccntLocation()

	if ACCOUNTS[Coord][OUTPOST] in ALL_OUTPOSTS:
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		time.sleep(2)
		pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT])
		time.sleep(5)
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		time.sleep(2)
	elif ACCOUNTS[Coord][OUTPOST] in ALL_INNER_CITY:
		pyautogui.click(ALL_BOUTONS_CORD[LAUNCH_IN_INNERCITY])
		logging.info('Waiting for Start bouton to appear, %s seconds...' % TIME_WAIT_IC_LOAD)
		time.sleep(TIME_WAIT_IC_LOAD)
		logging.info('Going into personal outpost.')
		pyautogui.click(ALL_BOUTONS_CORD[START])
		pyautogui.press('o') # go into outpost
		time.sleep(5)
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		time.sleep(2) # in case of pop-up.
		pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT])
		time.sleep(5)
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		time.sleep(2) # in case of pop-up.
	else:
		raise Exception('The account: %s in not in any locations defined.' % ACCOUNTS[Coord][USERNAME])

	ACCOUNTS[Coord][LOG_IN] = True # This will indicate you went into the account and used. or tried to use food.

def loggingOutAccnt(Coord):
	logging.info('Logging out of the account: %s' % ACCOUNTS[Coord][USERNAME])
	if ACCOUNTS[Coord][OUTPOST] in ALL_OUTPOSTS:
		pyautogui.click(ALL_BOUTONS_CORD[LOGOUT])
	elif ACCOUNTS[Coord][OUTPOST] in ALL_INNER_CITY:
		pyautogui.click(ALL_BOUTONS_CORD[BACK_TO_OUTPOST])
		time.sleep(2)
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		region = waitWhileTrue('bouton_%s' % INNER_CITY_PO, CHARACTER_REGION)
		pyautogui.click(ALL_BOUTONS_CORD[INNER_CITY_PO])
		time.sleep(2)
		pyautogui.click(ALL_BOUTONS_CORD[HISTORY_TOOLBAR])
		pyautogui.click(ALL_BOUTONS_CORD[HISTORY_TOOLBAR][0],ALL_BOUTONS_CORD[HISTORY_TOOLBAR][1]+50)
		pyautogui.press('enter')
		pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT]) #This will bring back the login box
		time.sleep(2)
	time.sleep(4)

def waitWhileTrue(ImgName, RegionName):
	while True: # loop because waiting for the Start bouton in inner_city to show up
		pos = pyautogui.locateOnScreen(imPath('%s.png' % ImgName), region=(RegionName))
		if pos is not None:
			break
	time.sleep(1)
	return pos

def getInventorySupplyNPositions(pCoord):
	"""This will basically scan and give back any cooridnates of and found food image.

	The food types are TRUFFLE, QUINOA, WHISKY, FRESH_MILK, RED_WINE, FRESH_VEG, FRESH_MEAT
	
	This will scan 5 pixel of every cell in the inventory, to determine every food type
	When i a food type has more then 3 out of 5 correct its food is determined 
	
	This is how to use this procedure:

	if ACCOUNTS[(10,12)][FIRST_TIME] == 1:
		ACCOUNTS[(10,12)][INVENTORY_DIC] = getInventorySupplyNPositions((10,12))
		if ACCOUNTS[(10,12)][INVENTORY_DIC][FOOD_SUPP][FRESH_MEAT] > 0:
			logging.info(ACCOUNTS[(10,12)][INVENTORY_DIC][FOOD_POS][FRESH_MEAT][ACCOUNTS[(10,12)][INVENTORY_DIC][FOOD_SUPP][FRESH_MEAT]])	"""
	pyautogui.PAUSE = 0
	logging.info('Scan character: %s INVENTORY for food...' % ACCOUNTS[pCoord][USERNAME])
	AccINVDict = {}
	AccINVDict[FOOD_SUPP] = {}
	AccINVDict[FOOD_POS] = {}
	for FoodType in ALL_FOOD_TYPES:
		AccINVDict[FOOD_SUPP][FoodType] = 0
		AccINVDict[FOOD_POS][FoodType] = {}

	# OffSet = (Center, Top, Right, Down, Left)
	All_FoodCnt = {}
	offSetPixelX = (21,21,32,21,7)
	offSetPixelY = (21,4,21,39,21)
	iMove = INVT_CELL_SIZE[0] # 43
	for j in range(15): #X coordinates
		for k in range (2): # Y cordinates
			#logging.info('STARTING COLUMN: %s Checking food: %s' % (j,k))
			Currnt_FoodTypeWin = {}
			for Ftype in ALL_FOOD_TYPES:
				Currnt_FoodTypeWin[Ftype] = 0

			for offSet in range(5): # This does all 5 dot locations defined above.
				xC = INVENTORY_REGION[0] + offSetPixelX[offSet] + (j*iMove) + j
				yC = INVENTORY_REGION[1] + offSetPixelY[offSet] + (k*iMove) + k
				#pyautogui.moveTo(xC,yC)
				#logging.info('X,Y: %s RGB: %s' % ((xC,yC),pyautogui.pixel(xC,yC)))
				for FoodType in ALL_FOOD_TYPES_COLOR.keys(): #This matches the defined color with the found colors
					if pyautogui.pixelMatchesColor(xC,yC,ALL_FOOD_TYPES_COLOR[FoodType][offSet],tolerance=15) == True:
						Currnt_FoodTypeWin[FoodType] += 1
						#logging.info('FoodType: %s, RGB Stored is: %s' % (FoodType,ALL_FOOD_TYPES_COLOR[FoodType][offSet]))
				#pyautogui.click(xC,yC)
			iCntWin = 0
			iSaveFood = ''
			for FoodType, Cnt in Currnt_FoodTypeWin.items(): # This will findout who is the biggest number of all found coulors
				if Cnt > iCntWin:
					iCntWin = Cnt
					iSaveFood = FoodType
			if iCntWin > 4: # This will make sure no junk, like anything but the food definied is found.
				#logging.info('For the Corodinates(center): %s , i found: %s with cnt: %s' % ((INVENTORY_REGION[0] + offSetPixelX[0] + (j*iMove)+j,	
				#INVENTORY_REGION[1] + offSetPixelY[0] + (k*iMove)+k), iSaveFood, iCntWin))
				# Supply Count
				iSaveFood = getReplaceFood(iSaveFood)
				AccINVDict[FOOD_SUPP][iSaveFood] += 1
				# Save Corrdinates of Supply Found. That macth the Supply Count Number.
				AccINVDict[FOOD_POS][iSaveFood][AccINVDict[FOOD_SUPP][iSaveFood]] = (INVENTORY_REGION[0] + offSetPixelX[0] + (j*iMove)+j,	
				INVENTORY_REGION[1] + offSetPixelY[0] + (k*iMove)+k)
	logging.info('INVENTORY food supply: %s' % AccINVDict[FOOD_SUPP])
	pyautogui.PAUSE = 1
	return AccINVDict

def getStorageSupplyNPositions(pCoord):
	""" This will scan and find any supply in the storage area, just like in the inventory."""
	pyautogui.PAUSE = 0
	logging.info('Scan character: %s STORAGE for food...' % ACCOUNTS[pCoord][USERNAME])

	AccSTODict = {}
	AccSTODict[FOOD_SUPP] = {}
	AccSTODict[FOOD_POS] = {}
	# for FoodType in ALL_FOOD_TYPES:
	# 	AccSTODict[FOOD_SUPP][FoodType] = 0
	# 	AccSTODict[FOOD_POS][FoodType] = {}

	# the five dots inside the box
	offSetPixelX = (21,21,32,21,7)
	offSetPixelY = (21,4,21,39,21)
	# Size of the box
	iMove = INVT_CELL_SIZE[0] # 43
	# Loop data in the coloums.
	xSeperator = (0,31,17,31,14,32,14) # Dont touche the right most row. Add "30" to the tuples if you last row.
	ySeperator = (0,17,12,17,17)
	# Loop counters since range is not being used.
	iCntX = 0
	iCntY = 0
	xSepSum = 0
	ySepSum = 0

	for xSep in xSeperator:
		xSepSum += xSep
		ySepSum = 0
		iCntY = 0
		for ySep in ySeperator:
			ySepSum += ySep
			#logging.info('STARTING COLUMN: %s Checking food: %s' % (iCntX,iCntY))
			Currnt_FoodTypeWin = {}
			for Ftype in ALL_FOOD_TYPES:
				Currnt_FoodTypeWin[Ftype] = 0

			for offSet in range(5):
				xC = STORAGE_REGION[0] + offSetPixelX[offSet] + (iCntX*iMove) + xSepSum
				yC = STORAGE_REGION[1] + offSetPixelY[offSet] + (iCntY*iMove) + ySepSum
				#logging.info('X,Y: %s RGB: %s' % ((xC,yC),pyautogui.pixel(xC,yC)))
				for FoodType in ALL_FOOD_TYPES_COLOR.keys():
					if pyautogui.pixelMatchesColor(xC,yC,ALL_FOOD_TYPES_COLOR[FoodType][offSet],tolerance=15) == True:
						Currnt_FoodTypeWin[FoodType] += 1
				#pyautogui.click(xC,yC)

			iCntWin = 0
			iSaveFood = ''
			for FoodType, Cnt in Currnt_FoodTypeWin.items():
				if Cnt > iCntWin:
					iCntWin = Cnt
					iSaveFood = FoodType
			if iCntWin > 3:
				# logging.info('For the Corodinates(center): %s , i found: %s with cnt: %s' % ((STORAGE_REGION[0] + offSetPixelX[0] + (iCntX*iMove) + xSep,	
				# STORAGE_REGION[1] + offSetPixelY[0] + (iCntY*iMove) + ySep), iSaveFood, iCntWin))
				# Supply Count
				iSaveFood = getReplaceFood(iSaveFood)
				if iSaveFood not in AccSTODict[FOOD_SUPP]:
					AccSTODict[FOOD_SUPP][iSaveFood] = 1
				else:
					AccSTODict[FOOD_SUPP][iSaveFood] += 1

				# Save Corrdinates of Supply Found. That macth the Supply Count Number.
				if iSaveFood not in AccSTODict[FOOD_POS]: AccSTODict[FOOD_POS][iSaveFood] = {}
				AccSTODict[FOOD_POS][iSaveFood][AccSTODict[FOOD_SUPP][iSaveFood]] = (STORAGE_REGION[0] + offSetPixelX[0] + (iCntX*iMove) + xSepSum,	
				STORAGE_REGION[1] + offSetPixelY[0] + (iCntY*iMove) + ySepSum)

			iCntY += 1
		iCntX += 1
	logging.info('STORAGE food supply: %s' % AccSTODict[FOOD_SUPP])
	pyautogui.PAUSE = 1
	return AccSTODict

def getLvlnPercentOfFood(FoodName):
	if FoodName == TRUFFLE or FoodName == QUINOA:
		return (75,45) # level, percentage feed.
	elif FoodName == WHISKY or FoodName == FRESH_MILK:
		return (75,25)
	elif FoodName == FRESH_VEG:
		return (51,45)
	elif FoodName == FRESH_MEAT:
		return (51,60)
	elif FoodName == RED_WINE:
		return (51,25)
	else:
		return None

def getCenterCoordWithRegion(pRegion,pOffSetX=0,pOffSetY=0):

	return (pRegion[0]+int(pRegion[2]/2)+pOffSetX,pRegion[1]+int(pRegion[3]/2)+pOffSetY)

def getAccntLocation():

	logging.info('Getting the account location')
	logging.info('Looking for "%s"...' % LAUNCH_IN_INNERCITY)
	region = pyautogui.locateOnScreen(imPath('launch_in_browser.png'), region=(LAUNCH_IC_REGION))
	if region is None:
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		time.sleep(1)
		logging.info('"launch in browser" was not found, looking for %s...' % DF_TOPCENTER)
		region = pyautogui.locateOnScreen(imPath('dead_frontier_logo_center_position1.png'), region=(WEB_BROWSER_REGION))
		if region is None:
			raise Exception('The account is not inner city, or outpost, end programme.')
		else: # in the outpost
			logging.info('Account location found: Outpost')
			return SB # Outpost
	else: # i am innercity
		logging.info('Account location found: InnerCity')
		return NEZ # InnerCity

def WeFeedTheAccnt(HungerFound, AccCord):
	""" This is going to eval if the hunger lvl found is low enough or set to the HungerLvl desired."""
	if (ACCOUNTS[AccCord][HUNGER_LVL] == FINE) and (HungerFound == FINE or HungerFound == HUNGRY or HungerFound == STARVING):
		return True
	elif (ACCOUNTS[AccCord][HUNGER_LVL] == HUNGRY) and (HungerFound == HUNGRY or HungerFound == STARVING):
		return True
	elif (ACCOUNTS[AccCord][HUNGER_LVL] == STARVING) and (HungerFound == STARVING):
		return True
	else:
		return False

def DONT_USE_THISsetScanInventory():
	""" This will scan 5 pixel of every cell in the inventory, to determine every food type
	When i a food type has more then 3 out of 5 correct its food is determined """

	# OffSet = (Center, Top, Right, Down, Left)
	pyautogui.PAUSE = 0
	All_FoodCnt = {}
	offSetPixelX = (21,21,32,21,7)
	offSetPixelY = (21,4,21,39,21)
	iMove = INVT_CELL_SIZE[0] # 43
	for j in range(15): #X coordinates
		for k in range (2): # Y cordinates
			logging.info('STARTING COLUMN: %s Checking food: %s' % (j,k))
			Currnt_FoodTypeWin = {}
			for Ftype in ALL_FOOD_TYPES:
				Currnt_FoodTypeWin[Ftype] = 0

			for offSet in range(5):
				xC = INVENTORY_REGION[0] + offSetPixelX[offSet] + (j*iMove) + j
				yC = INVENTORY_REGION[1] + offSetPixelY[offSet] + (k*iMove) + k
				#pyautogui.moveTo(xC,yC)
				logging.info('X,Y: %s RGB: %s' % ((xC,yC),pyautogui.pixel(xC,yC)))
				for FoodType in ALL_FOOD_TYPES_COLOR.keys():
					if pyautogui.pixelMatchesColor(xC,yC,ALL_FOOD_TYPES_COLOR[FoodType][offSet],tolerance=15) == True:
						Currnt_FoodTypeWin[FoodType] += 1
						#logging.info('FoodType: %s, RGB Stored is: %s' % (FoodType,ALL_FOOD_TYPES_COLOR[FoodType][offSet]))
				#pyautogui.click(xC,yC)
			iCntWin = 0
			iSaveFood = ''
			for FoodType, Cnt in Currnt_FoodTypeWin.items():
				if Cnt > iCntWin:
					iCntWin = Cnt
					iSaveFood = FoodType
			if iCntWin > 4:
				iSaveFood = getReplaceFood(iSaveFood)
				logging.info('For the Corodinates(center): %s , i found: %s with cnt: %s' % ((INVENTORY_REGION[0] + offSetPixelX[0] + (j*iMove)+j,	
				INVENTORY_REGION[1] + offSetPixelY[0] + (k*iMove)+k), iSaveFood, iCntWin))
			else: 
				logging.info('Didnt find anything for this coordinate.')
	pyautogui.PAUSE = 1

def feedTheAccounts(pCoordAcc, CurrentHunger):

	global ACCOUNTS

	if ACCOUNTS[pCoordAcc][INVENTORY_SCANNED] == False:
		ACCOUNTS[pCoordAcc][INVENTORY_DIC] = getInventorySupplyNPositions(pCoordAcc)
		ACCOUNTS[pCoordAcc][INVENTORY_SCANNED] = True # turn the flag off for the next times.

		if ACCOUNTS[pCoordAcc][USERNAME] == '6alex12': # So we do not get off set numbers.
			ACCOUNTS[pCoordAcc][INVENTORY_SCANNED] = False
	
	# if ACCOUNTS[pCoordAcc][FIRST_TIME] == True:
	# 	ACCOUNTS[pCoordAcc][FIRST_TIME] = False


	if ACCOUNTS[pCoordAcc][LVL_ACC] >= 75:
		if CurrentHunger == FINE:
			if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[0]] == 0:
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[1]] == 0:
					logging.info('Account: %s, Hunger was increased from FINE to HUNGRY' % ACCOUNTS[pCoordAcc][USERNAME])
					ACCOUNTS[pCoordAcc][HUNGER_LVL] = HUNGRY
				else:
					eatFood(FOOD_LVL75_25PER[1],pCoordAcc)
			else:
				eatFood(FOOD_LVL75_25PER[0],pCoordAcc)
		elif CurrentHunger == HUNGRY:
			if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[0]] == 0:
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[1]] == 0:
					for x in range(2):
						if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[0]] == 0:
							if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[1]] == 0:
								logging.info('Account: %s, Is out of all food type was made to be skipped' % ACCOUNTS[pCoordAcc][USERNAME])
								ACCOUNTS[pCoordAcc][SKIPACC] = 1
								break
							else:
								eatFood(FOOD_LVL75_25PER[1],pCoordAcc)
						else:
							eatFood(FOOD_LVL75_25PER[0],pCoordAcc)
				else:
					eatFood(FOOD_LVL75_45PER[1],pCoordAcc)
			else:
				eatFood(FOOD_LVL75_45PER[0],pCoordAcc)

		elif CurrentHunger == STARVING:
			Cnt20PerNeeded = 1
			No45Food = 0
			if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[0]] == 0:
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[1]] == 0:
					logging.info('Account: %s, Is starving and is out of 45 perc. types checking 25 perc...' % ACCOUNTS[pCoordAcc][USERNAME])
					No45Food = 1
					Cnt20PerNeeded += 2 # So we can eat 3 whiskeys/milk
				else:
					eatFood(FOOD_LVL75_45PER[1],pCoordAcc)
			else:
				eatFood(FOOD_LVL75_45PER[0],pCoordAcc)

			for x in range(Cnt20PerNeeded):
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[0]] == 0:
					if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[1]] == 0:
						if No45Food == 1:
							logging.info('Account: %s, Is out of all food type, it now has to be skipped' % ACCOUNTS[pCoordAcc][USERNAME])
							ACCOUNTS[pCoordAcc][SKIPACC] = 1
						break
					else:
						eatFood(FOOD_LVL75_25PER[1],pCoordAcc)
				else:
					eatFood(FOOD_LVL75_25PER[0],pCoordAcc)


	else: # 45+ accounts are here
		if CurrentHunger == FINE:
			if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][RED_WINE] == 0:
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[0]] == 0:
					if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[1]] == 0:
						logging.info('Account: %s, Hunger was increased from FINE to HUNGRY' % ACCOUNTS[pCoordAcc][USERNAME])
						ACCOUNTS[pCoordAcc][HUNGER_LVL] = HUNGRY
					else:
						eatFood(FOOD_LVL75_25PER[1],pCoordAcc)
				else:
					eatFood(FOOD_LVL75_25PER[0],pCoordAcc)
			else:
				eatFood(RED_WINE,pCoordAcc)
		elif CurrentHunger == HUNGRY:
			if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FRESH_VEG] == 0:
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[0]] == 0:
					if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[1]] == 0:
						logging.info('Account: %s, Is hungry and is out of 45 perc. types checking 25 perc...' % ACCOUNTS[pCoordAcc][USERNAME])

						for x in range(2):
							if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][RED_WINE] == 0:
								if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[0]] == 0:
									if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[1]] == 0:
										logging.info('Account: %s, Hunger was increased from HUNGRY to STARVING, for meat' % ACCOUNTS[pCoordAcc][USERNAME])
										ACCOUNTS[pCoordAcc][HUNGER_LVL] = STARVING
										break
									else:
										eatFood(FOOD_LVL75_25PER[1],pCoordAcc)
								else:
									eatFood(FOOD_LVL75_25PER[0],pCoordAcc)
							else:
								eatFood(RED_WINE,pCoordAcc)

					else:
						eatFood(FOOD_LVL75_45PER[1],pCoordAcc)
				else:
					eatFood(FOOD_LVL75_45PER[0],pCoordAcc)
			else:
				eatFood(FRESH_VEG,pCoordAcc)
		elif CurrentHunger == STARVING:
			Cnt20PerNeeded = 1
			No45Food = 0
			No25Food = 0
			if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FRESH_MEAT] == 0:
				if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FRESH_VEG] == 0:
					if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[0]] == 0:
						if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_45PER[1]] == 0:
							No45Food = 1
							Cnt20PerNeeded += 2 # So we can eat 3 redWine/whiskeys/milk
						else:
							eatFood(FOOD_LVL75_45PER[1],pCoordAcc)
					else:
						eatFood(FOOD_LVL75_45PER[0],pCoordAcc)
				else:
					eatFood(FRESH_VEG,pCoordAcc)

				for x in range(Cnt20PerNeeded):
					if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][RED_WINE] == 0:
						if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[0]] == 0:
							if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][FOOD_LVL75_25PER[1]] == 0:
								if No45Food == 1:
									logging.info('Account: %s, Is out of all food type, it now has to be skipped' % ACCOUNTS[pCoordAcc][USERNAME])
									ACCOUNTS[pCoordAcc][SKIPACC] = 1
								break
							else:
								eatFood(FOOD_LVL75_25PER[1],pCoordAcc)
						else:
							eatFood(FOOD_LVL75_25PER[0],pCoordAcc)
					else:
						eatFood(RED_WINE,pCoordAcc)
			else:
				eatFood(FRESH_MEAT,pCoordAcc)

	# if ACCOUNTS[pCoordAcc][OUTGOING_LIST_SCANNED] == False:
	# 	scanOutgoingOffers(pCoordAcc)
	# 	ACCOUNTS[pCoordAcc][OUTGOING_LIST_SCANNED] = True
	
	if ACCOUNTS[pCoordAcc][PROFF] != CHF:
		if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] > 9: 
			# getFoodFromIncomingOfferFromChef(pCoordAcc)
			getNstoreAllFoodOnAccount(pCoord)

	# Check for more food
	if ACCOUNTS[pCoordAcc][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] > 15:
		if ACCOUNTS[pCoordAcc][FOOD_SELLING_LIST] == True:
			getFoodFromSellingList(pCoordAcc)

		if ACCOUNTS[pCoordAcc][FOOD_SELLING_LIST] == False and ACCOUNTS[pCoordAcc][NO_FOOD_IN_STORAGE] == False:
			takeStorageFood(pCoordAcc)

def eatFood(FoodType,pCoord):

	global ACCOUNTS

	#logging.info('FoodType: %s, FoodSupply: %s' % (FoodType,ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType]))
	#logging.info(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType])

	pyautogui.moveTo(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType]])
	time.sleep(1)
	pyautogui.dragTo(ALL_BOUTONS_CORD[CENTER_CHARACTER][0],ALL_BOUTONS_CORD[CENTER_CHARACTER][1], 2)

	#Maybe also count the new empty slots, so you can get some back from storage.
	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] += 1
	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]] =	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType]]
	
	del ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType]]
	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType] -= 1

	if FoodType not in ACCOUNTS[pCoord][USEDFOOD_DIC][FOOD_SUPP]:
		ACCOUNTS[pCoord][USEDFOOD_DIC][FOOD_SUPP][FoodType] = 1
	else:
		ACCOUNTS[pCoord][USEDFOOD_DIC][FOOD_SUPP][FoodType] += 1

	logging.info('FoodType: %s, FoodSupply: %s' % (FoodType,ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType]))
	logging.info('Empty_Slots: %s' % (ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]))
	# logging.info(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]])
	# logging.info(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType])

def takeStorageFood(pCoord):

	global ACCOUNTS

	logging.info('Getting food from storage...')
	#logging.info(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType])
	pyautogui.click(ALL_BOUTONS_CORD[STORAGE_BT])
	time.sleep(4)
	canclePopup()

	bFlagFoundFood = 0
	numEmptySlots = ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]

	if numEmptySlots < 1: # Safety in case there are no empty slots
		return 0

	if ACCOUNTS[pCoord][STORAGE_SCANNED] == False:
		ACCOUNTS[pCoord][STORAGE_DIC] = getStorageSupplyNPositions(pCoord)
		ACCOUNTS[pCoord][STORAGE_SCANNED] = True

	tempoDiction = {}
	for key, val in ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP].items():
		if key == EMPTY_SLOT: continue
		tempoDiction[key] = val

	tempFoodAmount = 0
	tempFoodType = ''
	for FoodType, FoodAmount in tempoDiction.items():
		tempFoodType = FoodType
		tempFoodAmount = FoodAmount
		if tempFoodType == EMPTY_SLOT: continue # Saftey
		bFlagFoundFood = 1
		while numEmptySlots > 0:

			pyautogui.moveTo(ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][tempFoodType][tempFoodAmount])
			pyautogui.dragTo(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots][0],
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots][1], 1.3)
			# time.sleep(1)

			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][tempFoodType] += 1
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][tempFoodType][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][tempFoodType]] = ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots]

			del ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots]
			numEmptySlots -= 1
			# logging.info(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][tempFoodType])
			# logging.info(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots])

			if EMPTY_SLOT not in ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP]:
				ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][EMPTY_SLOT] = 1
				ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT] = {}
				ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT][1] = ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][tempFoodType][tempFoodAmount]
			else:
				ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][EMPTY_SLOT] += 1
				ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT][ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][EMPTY_SLOT]] = ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][tempFoodType][tempFoodAmount]

			del ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][tempFoodType][tempFoodAmount]
			tempFoodAmount -= 1

			
			if tempFoodAmount == 0:
				del ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][tempFoodType]
				del ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][tempFoodType]
				break			
		
		if tempFoodAmount != 0:
			ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][tempFoodType] = tempFoodAmount # Update the amount left of that food in storage.
		
	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] = numEmptySlots
	if bFlagFoundFood == 0: ACCOUNTS[pCoord][NO_FOOD_IN_STORAGE] = True

	# logging.info('tempFoodType: %s, FoodSupply: %s' % (FoodType,ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType]))
	logging.info('INVENTORY food supply: %s' % (ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP]))
	logging.info('STORAGE food supply: %s' % (ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP]))

	pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT])
	time.sleep(4)
	canclePopup()

def loggingAllFarmerAccounts():
	""" This will be the initial setup to log in all farmer accounts"""
	pyautogui.PAUSE = 0.60

	iCnt = 0
	for FrmCord in ALL_FRM_ACCOUNTS:
		iCnt += 1
		if ACCOUNTS[FrmCord][SKIPACC] == 1:
			continue
		loggingInAccnt(FrmCord)
		if iCnt == 1: #Put the browser zoom to 100% like it should be.
			pyautogui.click(ALL_BOUTONS_CORD[BROWSER_ZOOM_100]) # Click for 100% Zoom
		pyautogui.hotkey('alt','d')
		pyautogui.typewrite('http://fairview.deadfrontier.com/onlinezombiemmo/index.php?page=27&memto=%s' % ACCOUNTS[ACCOUNTS_USERNAME[ACCOUNTS[FrmCord][SEND_FOOD_CHF]]][USER_ID]) # trade 6alex12
		pyautogui.press('enter')
		time.sleep(4)
		pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
		time.sleep(2)
		for j in range(2): #X coordinates
			for k in range (2): # Y cordinates
				xC = INVENTORY_REGION[0] + 21 + (j*43) + j
				yC = INVENTORY_REGION[1] + 21 + (k*43) + k
				pyautogui.moveTo(xC,yC)
				pyautogui.dragTo(xC+100,(yC-160),1.2)
				pyautogui.click(ALL_BOUTONS_CORD[PRICE_INPUT])
				pyautogui.press('backspace')
				pyautogui.press('enter')
				pyautogui.press('enter')
		time.sleep(2)


		loggingOutAccnt(FrmCord)

	pyautogui.PAUSE = 1

def readTxtMarketFile():
	""" This is a procedure to read the txt file"""
	marketFile = open('Dead Frontier Clan Hollow Prestige.txt')
	FoodBuy = {} #{'driedtruffles_cooked': 0, 'driedtruffles': 0}
	iCnt = 0
	cMemName = ''
	cNameFood = ''
	for line in marketFile:
		iCnt += 1
		if iCnt < 43: continue
		#if 201 < iCnt: break
		#logging.info('Line: \n%s' % line.split())
		if cMemName == '':
			cNameFood = line.split('\t')[0]
		else:
			cNameFood = cMemName
		LineAmount = line.split('\t')[-1].replace(',','')
		logging.info('Line: %s LineAmount: %s cNameFood: %s' % (iCnt,LineAmount,cNameFood))
		if LineAmount.isdigit() == True:
			if int(LineAmount) == 1:
				cMemName = cNameFood
				continue
			elif LineAmount == cNameFood.replace(',',''):
				cNameFood = cMemName

			if cNameFood == TRUFFLE_RAW and int(LineAmount) < 8000:
				if cNameFood in FoodBuy:
					FoodBuy[cNameFood] += 1
				else:
					FoodBuy[cNameFood] = 1
			elif cNameFood == TRUFFLE_COOKED and int(LineAmount) < 15000:
				if cNameFood in FoodBuy:
					FoodBuy[cNameFood] += 1
				else:
					FoodBuy[cNameFood] = 1
			cMemName = ''
		else:
			cMemName = cNameFood
	return FoodBuy
	
def getTxtMarketFile(pItemSearch='',bCredits=0):
	""" Going of hollowpresitge market place and generate txt file"""

	pyautogui.hotkey('ctrl','tab')
	pyautogui.click(ALL_BOUTONS_CORD[SELECT_TRADEZONE])
	pyautogui.typewrite('sec')
	pyautogui.press('tab')
	if bCredits != 0:
		pyautogui.typewrite('cred')
		pyautogui.press('tab')
	else:
		pyautogui.press('tab')
		if pItemSearch != '':
			pyautogui.typewrite(pItemSearch)
	pyautogui.press('enter')
	time.sleep(8)
	pyautogui.click(button='right')
	pyautogui.moveRel(52,52)
	pyautogui.click()
	time.sleep(7)
	pyautogui.click(ALL_BOUTONS_CORD[MARKETFILE_REP])
	pyautogui.typewrite('C:\\Users\\Alex\\Desktop\\PythonScripts')
	pyautogui.press('enter')
	pyautogui.click(ALL_BOUTONS_CORD[MARKETFILE_NAME])
	pyautogui.typewrite('Dead Frontier Clan Hollow Prestige.txt')
	pyautogui.click(ALL_BOUTONS_CORD[MARKETFILE_SAVE])
	time.sleep(3)
	pyautogui.press('tab')
	pyautogui.press('enter')
	pyautogui.hotkey('ctrl','shift','tab')
	logging.info('The MarketFile is saved!')

def getReplaceFood(pFood):
	if pFood == TRUFFLE1: pFood = TRUFFLE
	if pFood == FRESH_VEG1: pFood = FRESH_VEG
	if pFood == QUINOA1: pFood = QUINOA
	return pFood

def canclePopup():
	pyautogui.click(ALL_BOUTONS_CORD[DF_TOPCENTER])
	time.sleep(2) # in case of pop-up.

def getFoodFromSellingList(pCoord):

	global ACCOUNTS

	eGotFood = 0
	logging.info('Getting food from Selling List...')
	time.sleep(2)
	canclePopup()
	# logging.info('Click TOPCENTER')
	pyautogui.hotkey('alt','d')
	pyautogui.typewrite('http://fairview.deadfrontier.com/onlinezombiemmo/index.php?page=27&memto=%s' % ACCOUNTS[ACCOUNTS_USERNAME['22alex12']][USER_ID]) # trade 6alex12
	pyautogui.press('enter')
	time.sleep(4)
	canclePopup()

	rangCnt = (ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]-eGotFood)
	for cnt in range(rangCnt):
		region = pyautogui.locateOnScreen(imPath('cancle_sales_outgoing_offers.png'), region=(OUTGOING_OFFERS_REGION))
		if region is None:
			logging.info('Not Found Image: %s' % 'cancle_sales_outgoing_offers.png')
			break
		else:
			pyautogui.click(getCenterCoordWithRegion(region))
			pyautogui.press('enter')
			pyautogui.moveRel(0,-120)
			time.sleep(1)
			eGotFood += 1

	rangCnt = (ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]-eGotFood)
	for cnt in range(rangCnt):
		region = pyautogui.locateOnScreen(imPath('cancle_sales_outgoing_offers.png'), region=(OUTGOING_OFFERS_REGION))
		if region is None:
			logging.info('Not Found Image 2nd try: %s' % 'cancle_sales_outgoing_offers.png')
			ACCOUNTS[pCoord][FOOD_SELLING_LIST] = False
			ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] = 0
			break
		else:
			pyautogui.click(getCenterCoordWithRegion(region))
			pyautogui.press('enter')
			pyautogui.moveRel(0,-120)
			time.sleep(1)
			eGotFood += 1

	if eGotFood != 0: 
		ACCOUNTS[pCoord][INVENTORY_DIC] = getInventorySupplyNPositions(pCoord)
		ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] -= eGotFood

	pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT])
	time.sleep(4)
	canclePopup()

def buyingIncomingOffers(pCoord,pNumEmptySlots):

	global ACCOUNTS

	bGotFood = 0

	pyautogui.PAUSE = 0

	freePic = 'free_trade.png'
	downPic = 'down_arrow.png'

	logging.info('Getting food from Trading Incoming Offers...')

	pyautogui.click(ALL_BOUTONS_CORD[MARKETPLACE])
	time.sleep(4)
	canclePopup()
	time.sleep(1)
	pyautogui.click(ALL_BOUTONS_CORD[PRIVATE_TRADES])
	time.sleep(2)

	while True:
		while True:
			region = pyautogui.locateOnScreen(imPath(freePic), region=(INCOMING_OFFERS_REGION))
			if region is None:
				# logging.info('Not Found Image: %s' % freePic)
				break
			else:
				# logging.info('Found Image: %s' % freePic)
				pyautogui.click(getCenterCoordWithRegion(region,94))
				time.sleep(1)
				pyautogui.press('enter')
				pyautogui.moveRel(0,-120)
				time.sleep(2)
				bGotFood += 1
				pNumEmptySlots -= 1

			if pNumEmptySlots <= 0: break
		
		if pNumEmptySlots <= 0: break

		region = pyautogui.locateOnScreen(imPath(downPic), region=(INCOMING_OFFERS_REGION))
		if region is None:
			# logging.info('Not Found Image: %s' % downPic)
			break
		else:
			# logging.info('Found Image: %s' % downPic)
			pyautogui.click(ALL_BOUTONS_CORD[DOWN_ARROW_INC_OFFER])
			pyautogui.moveRel(0,-120)
			time.sleep(1)

	if bGotFood != 0 and pNumEmptySlots >= 0: 
		ACCOUNTS[pCoord][INVENTORY_DIC] = getInventorySupplyNPositions(pCoord)
		ACCOUNTS[pCoord][INVENTORY_SCANNED] = True
		ACCOUNTS[pCoord][SKIPACC] = 0

	# pyautogui.click(ALL_BOUTONS_CORD[INVEN_BT])
	# time.sleep(4)
	# canclePopup()

	if bGotFood > 0:
		logging.info('Account: %s EMPTY_SLOTS: %s' % (ACCOUNTS[pCoord][USERNAME],ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]))
	else:
		logging.info('NO food was bought, next time...')

	pyautogui.PAUSE = 1

	return bGotFood

def getFoodFromIncomingOfferFromChef(pCoord,pLoginAcc=0):

	global ACCOUNTS

	boughtFood = 0
	# iCntGreaterThan = 12
	# for Coord, AccDic in ACCOUNTS.items():
	# 	if AccDic[LOG_IN] == 1 and Coord not in ALL_FRM_ACCOUNTS and AccDic[INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] > iCntGreaterThan:
	if pLoginAcc == 1:
		logging.info('Account: %s has %s EMPTY_SLOTS, its > %s' % (ACCOUNTS[pCoord][USERNAME],ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT],iCntGreaterThan))

		loggingInAccnt(pCoord)
		
		boughtFood = buyingIncomingOffers(pCoord,ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT])

		loggingOutAccnt(pCoord)
	else:
		logging.info('Account: %s EMPTY_SLOTS: %s' % (ACCOUNTS[pCoord][USERNAME],ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]))
		boughtFood = buyingIncomingOffers(pCoord,ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT])

def scanOutgoingOffers(pCoord):

	global ACCOUNTS

	logging.info('Counting the food in outgoing list...')


	pyautogui.PAUSE = 0
	downPic = 'down_arrow_outgoing.png'
	iCnt = 5 # Start off with 5 if empty it will be corrected by cancle sells.
	while True:
		region = pyautogui.locateOnScreen(imPath(downPic), region=(OUTGOING_OFFERS_REGION))
		if region is None:
			# logging.info('Not Found Image: %s' % downPic)
			break
		else:
			# logging.info('Found Image: %s' % downPic)
			pyautogui.click(ALL_BOUTONS_CORD[DOWN_ARROW_OUT_OFFER])
			pyautogui.moveRel(0,-120)
			time.sleep(1)
			iCnt += 1

	ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] = iCnt
	logging.info('Outgoing List Count: %s' % iCnt)
	pyautogui.PAUSE = 1

def getNstoreAllFoodOnAccount(pCoord):

	boughtFood = 0
	bAccFullFood = False

	while True:
		boughtFood = buyingIncomingOffers(pCoord,ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT])
		if boughtFood == 0: break
		else:
			if ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] == 0:
				bAccFullFood = storeFoodOnAccount(pCoord)
				if bAccFullFood == True: break
			else: break

def storeFoodOnAccount(pCoord):

	global ACCOUNTS

	bFlagFull = False # The account is NOT full.

	bChangeWebPage = True
	if ACCOUNTS[pCoord][OUTGOING_LIST_SCANNED] == False:
		# time.sleep(2)
		canclePopup()

		pyautogui.hotkey('alt','d')
		pyautogui.typewrite('http://fairview.deadfrontier.com/onlinezombiemmo/index.php?page=27&memto=%s' % ACCOUNTS[ACCOUNTS_USERNAME['22alex12']][USER_ID]) # trade 22alex12
		pyautogui.press('enter')
		time.sleep(4)
		canclePopup()
		scanOutgoingOffers(pCoord)
		bChangeWebPage = False # this will save 10sec on loading another page.
		ACCOUNTS[pCoord][OUTGOING_LIST_SCANNED] = True

	if ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] < 29:
		putFoodInOutgoingList(pCoord,bChangeWebPage)

	if ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] >= 29:
		if ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] < 10: # The inventory is still more then half full.
			bChangeWebPage = True
			if ACCOUNTS[pCoord][STORAGE_SCANNED] == False:
				pyautogui.click(ALL_BOUTONS_CORD[STORAGE_BT])
				time.sleep(4)
				canclePopup()

				ACCOUNTS[pCoord][STORAGE_DIC] = getStorageSupplyNPositions(pCoord)
				# logging.info('STORAGE food supply: %s' % ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP])
				logging.info('STORAGE food position: %s' % ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS])
				bChangeWebPage = False # this will save 10sec on loading another page.
				ACCOUNTS[pCoord][STORAGE_SCANNED] = True

			if EMPTY_SLOT in ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP]:
				if ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][EMPTY_SLOT] > 0:
					putFoodInStorage(pCoord,bChangeWebPage)
			else:
				bFlagFull = True

	return bFlagFull

def putFoodInOutgoingList(pCoord, pChangeWebPage=True):
	global ACCOUNTS

	logging.info('Putting food in outgoing list...')

	bFirstInteragtion = True

	eStartOutgoingCnt = ACCOUNTS[pCoord][OUTGOING_LIST_COUNT]

	if pChangeWebPage == True:
		canclePopup()
		pyautogui.hotkey('alt','d')
		pyautogui.typewrite('http://fairview.deadfrontier.com/onlinezombiemmo/index.php?page=27&memto=%s' % ACCOUNTS[ACCOUNTS_USERNAME['22alex12']][USER_ID]) # trade 22alex12
		pyautogui.press('enter')
		time.sleep(4)
		canclePopup()

	for FoodType, FoodAmount in copy.copy(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP]).items():
		if FoodAmount <= 1: continue
		if FoodType == EMPTY_SLOT: continue
		while FoodAmount > 1: # remeber to keep at least one foodtype, so that the accounts isnt skiped by mistake
			
			pyautogui.moveTo(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount])
			time.sleep(1)
			pyautogui.dragTo(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount][0],
			(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount][1]-160),1.2)
			if bFirstInteragtion == True:
				bFirstInteragtion = False
				pyautogui.click(ALL_BOUTONS_CORD[PRICE_INPUT])
				pyautogui.press('backspace',pause=0)
			pyautogui.press('del',pause=0)
			pyautogui.press('enter',pause=0)
			pyautogui.press('enter',pause=0)
			
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] += 1
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]] =	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount]

			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType] -= 1
			del ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount]
			
			ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] += 1

			FoodAmount -= 1

			if ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] >= 29: break

		if ACCOUNTS[pCoord][OUTGOING_LIST_COUNT] >= 29: break

	time.sleep(1) # Waiting for last foodtype to load in selling list.

	if eStartOutgoingCnt == 5: scanOutgoingOffers(pCoord) #This is to be accurate cuz of the default 5 count in the outgoing list, this will correct 

	ACCOUNTS[pCoord][FOOD_SELLING_LIST] = True

	logging.info('Outgoing List Count: %s' % ACCOUNTS[pCoord][OUTGOING_LIST_COUNT])

	logging.info('DONE, putting food in outgoing list')

def putFoodInStorage(pCoord, pChangeWebPage=True):
	global ACCOUNTS
 
	logging.info('Putting food in STORAGE...')

	if pChangeWebPage == True:
		pyautogui.click(ALL_BOUTONS_CORD[STORAGE_BT])
		time.sleep(4)
		canclePopup()

	numEmptySlots = ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][EMPTY_SLOT]

	logging.info('STORAGE food position: %s' % ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS])

	if numEmptySlots <= 0: return # safty

	for FoodType, FoodAmount in copy.copy(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP]).items():
		if FoodAmount <= 1: continue
		if FoodType == EMPTY_SLOT: continue
		while FoodAmount > 1: # remeber to keep at least one foodtype, so that the accounts isnt skiped by mistake
			pyautogui.moveTo(ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount])
			pyautogui.dragTo(ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots][0],
			ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots][1],1.4)
			
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT] += 1
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][EMPTY_SLOT][ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][EMPTY_SLOT]] =	ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount]

			del ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_POS][FoodType][FoodAmount]
			ACCOUNTS[pCoord][INVENTORY_DIC][FOOD_SUPP][FoodType] -= 1

			if FoodType not in ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP]: ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][FoodType] = 1
			else: ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][FoodType] += 1

			if FoodType not in ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS]: ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][FoodType] = {}
			ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][FoodType][ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][FoodType]] = ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots]

			del ACCOUNTS[pCoord][STORAGE_DIC][FOOD_POS][EMPTY_SLOT][numEmptySlots]
			numEmptySlots -= 1
			
			FoodAmount -= 1

			if numEmptySlots <= 0: break

		if numEmptySlots <= 0: break

	ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP][EMPTY_SLOT] = numEmptySlots

	ACCOUNTS[pCoord][NO_FOOD_IN_STORAGE] = False

	logging.info('STORAGE food supply: %s' % ACCOUNTS[pCoord][STORAGE_DIC][FOOD_SUPP])

	logging.info('DONE, putting food in STORAGE')


# SetAccValues()
# getQuickRegionBoutonsCoord()

# main()
# main(0,0) # LogginFamers=0, SetInitial Setup=0
# main(1,0) # LogginFamers=0, SetInitial Setup=0



ROLLING_COMPLETE = time.time() + 10.5 # give the mat enough time (1.5 seconds) to finish rolling before being used again

logging.info('Loop Start:')
while time.time() < ROLLING_COMPLETE:
	time.sleep(1)
	logging.info(time.time())
	logging.info(ROLLING_COMPLETE)

logging.info('Out of loops')



#initialSetup()
# imagepic = 'buy_incoming_offers1.png'
# region = pyautogui.locateOnScreen(imPath(imagepic), region=(INCOMING_OFFERS_REGION))
# if region is None:
# 	logging.info('Not Found Image: %s' % imagepic)
# 	# break
# else:
# 	logging.info('Found Image: %s' % imagepic)
# 	# pyautogui.click(getCenterCoordWithRegion(region,45))
# 	# pyautogui.press('enter')
# 	# pyautogui.moveRel(0,-120)
# 	time.sleep(1)
# 	# bGotFood += 1

# getFoodFromIncomingOfferFromChef((3,2))

# while True:

# 	while True:
# 		freePic = 'free_trade.png'
# 		region = pyautogui.locateOnScreen(imPath(freePic), region=(INCOMING_OFFERS_REGION))
# 		if region is None:
# 			logging.info('Not Found Image: %s' % freePic)
# 			break
# 		else:
# 			pyautogui.click(getCenterCoordWithRegion(region,94))
# 			logging.info('Found Image: %s' % freePic)
# 			pyautogui.press('enter')
# 			pyautogui.moveRel(0,-120)

# 	downPic = 'down_arrow.png'
# 	region = pyautogui.locateOnScreen(imPath(downPic), region=(INCOMING_OFFERS_REGION))
# 	if region is None:
# 		logging.info('Not Found Image: %s' % downPic)
# 		break
# 	else:
# 		logging.info('Found Image: %s' % downPic)
# 		# for x in range(5):
# 		# 	pyautogui.click(ALL_BOUTONS_CORD[DOWN_ARROW_INC_OFFER])
# 		pyautogui.click(ALL_BOUTONS_CORD[DOWN_ARROW_INC_OFFER])
# 		pyautogui.moveRel(0,-120)

#pyautogui.displayMousePosition()