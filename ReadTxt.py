f = open('Dead Frontier Clan Hollow Prestige.txt')
FunDiction = {}
FoodBuy = {'driedtruffles_cooked': 0, 'driedtruffles': 0}
iCnt = 0
cMemName = ''
cName = ''
lineNum = ''
for line in f:
	iCnt += 1
	if 43 > iCnt: continue
	if 60 < iCnt: break
	line = line.strip()
	if cMemName == '':
		cName = line.split('\t')[0]
	else:
		cName = cMemName
	LastEl = line.split('\t')[-1].replace(",","")
	print('Line: %s LasteEl: %s cName: %s' % (iCnt,LastEl,cName))
	if LastEl.isdigit() == True:
		if cName == 'driedtruffles_cooked' and int(LastEl) < 16000:
			print('last El: %s' % (LastEl))
			FoodBuy['driedtruffles_cooked'] += 1
		if cName == 'driedtruffles' and int(LastEl) < 10000:
			print('last El: %s' % (LastEl))
			FoodBuy['driedtruffles'] += 1
		cMemName = ''
	else:
		cMemName = cName
	
print('FoodBuy:\n %s' % (str(FoodBuy)))




