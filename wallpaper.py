import requests
import platform
import os
import winreg, ctypes, win32con

FILL, FIT, STRETCH, TILE, CENTER, SPAN = 0, 1, 2, 3, 4, 5
MODES = (0, 10), (0, 6), (0, 2), (1, 0), (0, 0), (0, 22)
value1, value2 = MODES[STRETCH] 

url = "https://pic.re/images"

key = winreg.OpenKey(
	winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_WRITE
)
winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, str(value1))
winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, str(value2))
winreg.CloseKey(key)


def download_pic_of_day():
	r = requests.get(url, allow_redirects=True)
	if r.status_code != 200:
		print("error")
		return
	filename = "images.jpg"
	open(filename, "wb").write(r.content)
	print(f"saved the picture to {filename}!")

def download_again():
	repeat = input("Would you like to download another pic? Y or N? ")
	if repeat == "Y":
		download_pic_of_day()
		changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
		cmd = ctypes.windll.user32.SystemParametersInfoW(
		win32con.SPI_SETDESKWALLPAPER, 0, os.path.abspath("images.jpg"), changed
		)
		print(cmd)
		os.system("rundll32.exe user32.dll, UpdatePerUserSystemParameters")
		os.system("cls")
		download_again()
	elif repeat == "N":
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



