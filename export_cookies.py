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


# setup chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# set path to chromedriver as per your configuration
chromedriver_autoinstaller.install()

print('v1')
# set the target URL
url = 'https://www.leagueofgraphs.com/champions/tier-list/samira'

# set up the webdriver
driver = webdriver.Chrome(options=chrome_options)
# cookies=driver.get_cookies()
# for cookie in cookies:
#     print(cookie['name'], cookie['value'])
driver.get(url)

print("driver.title",driver.title)
# print(driver.get_cookies())
print(driver.get_cookies())

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
driver.quit()

