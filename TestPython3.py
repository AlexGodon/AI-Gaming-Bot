import pyautogui, time, logging
import os, sys
import image
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')

pyautogui.displayMousePosition()