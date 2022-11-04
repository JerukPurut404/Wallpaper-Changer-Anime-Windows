import requests
import platform
import os
import winreg, ctypes, win32con
from PIL import Image
from time import sleep 
import random
FILL, FIT, STRETCH, TILE, CENTER, SPAN = 0, 1, 2, 3, 4, 5
MODES = (0, 10), (0, 6), (0, 2), (1, 0), (0, 0), (0, 22)

url = "https://wallhaven.cc/api/v1/search?categories=010&sorting=random&resolutions=1920x1080"
answer_yes = ["Y", "y", "yes"]
answer_no = ["N", "n", "no"]

def download_pic_of_day():
	data = requests.get(url).json()
	response = data['data'][int(random.randint(1,24))]['path']
	image_data = requests.get(response).content
	filename = "images.jpg"
	open(filename, "wb").write(image_data)
	with Image.open(os.path.abspath(filename)) as img:
		width, height = img.size
		print("The picture size is " + str(img.size))
	if img.size[0] > 1080:
		value1, value2 = MODES[FILL]
	else:
		value1, value2 = MODES[STRETCH]
	key = winreg.OpenKey(
	winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_WRITE
	)
	winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, str(value1))
	winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, str(value2))
	winreg.CloseKey(key)
	print(f"saved the picture to {filename}!")
	sleep(5)
		

def download_again():
	repeat = input("Would you like to download another pic? Y or N? ")
	if repeat in answer_yes:
		download_pic_of_day()
		changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
		cmd = ctypes.windll.user32.SystemParametersInfoW(
		win32con.SPI_SETDESKWALLPAPER, 0, os.path.abspath("images.jpg"), changed
		)
		print(cmd)
		os.system("rundll32.exe user32.dll, UpdatePerUserSystemParameters")
		os.system("cls")
		download_again()
	elif repeat in answer_no:
		quit()
	else:
		os.system("cls")
		download_again()

if __name__ == "__main__":
	download_pic_of_day()
	changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
	cmd = ctypes.windll.user32.SystemParametersInfoW(
		win32con.SPI_SETDESKWALLPAPER, 0, os.path.abspath("images.jpg"), changed
	)
	print(cmd)
	os.system("rundll32.exe user32.dll, UpdatePerUserSystemParameters")
	os.system("cls")
	download_again()
