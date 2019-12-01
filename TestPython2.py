import pyautogui, time
time.sleep(3)
pyautogui.PAUSE = 2.5
distance = 200
while distance > 0:
		pyautogui.dragRel(distance, 0, 2)   # move right
		distance -= 5
		pyautogui.dragRel(0, distance, 2)   # move down
		pyautogui.dragRel(-distance, 0, 2)  # move left
		distance -= 5
		pyautogui.dragRel(0, -distance, 2)  # move up