# import undetected_chromedriver as uc

# options = uc.ChromeOptions()
# options.headless = True

# driver = uc.Chrome(options=options)
# driver.get('https://youtube.com')

# # (Éventuellement faire un login automatisé ici...)

# cookies = driver.get_cookies()

# with open('cookies.txt', 'w') as f:
#     for cookie in cookies:
#         f.write(cookie['name'], cookie['value'])

# driver.quit()


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

# #créer driver avec option 
# options = Options()
# options.headless = True

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# url = 'https://www.youtube.com/'
# driver.get(url)

# print(driver.get_cookies())



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import pickle
import json
import time

# from selnet_cookies import save_cookies_to_file
from netscape_cookies import to_netscape_string

from check_cookies_valid import validate_netscape_cookie_file


# setup chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# set path to chromedriver as per your configuration
chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=chrome_options)

print('v1')

# set the target URL
# url = "https://www.youtube.com/"

# # set up the webdriver

# # cookies=driver.get_cookies()
# # for cookie in cookies:
# #     print(cookie['name'], cookie['value'])
# driver.get(url)

# print("driver.title",driver.title)

# time.sleep(5)
# yt_click = driver.find_element(by=By.XPATH, value='//*[@id="video-title"]')
# print(yt_click)
# # yt_click[0].click()
# time.sleep(5)

# I searched "FFXIV", retrive links of the videos from that search
driver.get("https://www.youtube.com/results?search_query=asa")
# video_list = driver.find_elements("xpath", '//*[@id="video-title"]') 
video_list = driver.find_elements("id", "video-title")  
time.sleep(5)
print(video_list)

video_list[0].click()
time.sleep(5)
links = []
for video in video_list:
            links.append(video)



print(links)
# print(driver.get_cookies())
cookies = driver.get_cookies()


print('COOKIES---------------------------')
res=to_netscape_string(cookies)

with open("cookies.txt", "w") as f:
    f.write("# Netscape HTTP Cookie File\n")
    # f.write("# http://curl.haxx.se/rfc/cookie_spec.html\n")
    # f.write("# This is a generated file!  Do not edit.\n")
    f.write(str(res))
# print(len(driver.get_cookies()))

# Sauvegarde au format texte simple
# with open("cookies.txt", "w") as f:
#     for cookie in cookies:
#         f.write(f"{cookie['name']}={cookie['value']}; ")

# Sauvegarde au format JSON
with open("cookies.json", "w") as f_json:
    json.dump(cookies, f_json, indent=4)

validate_netscape_cookie_file('cookies.txt')


driver.quit()

