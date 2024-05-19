from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup;
import pandas as pd;
import time;

option = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
option.add_experimental_option("prefs",prefs)
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=option)

link = "https://www.facebook.com"

driver.get(link)

# targeting email dan username
username = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
password = driver.find_element(By.CSS_SELECTOR, "input[name='pass']")

# enter email and password
username.clear()
username.send_keys("email anda")
password.clear()
password.send_keys("password anda")

# login
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
time.sleep(5)

driver.get("https://www.facebook.com/groups/453998274965730" )
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']")))

y = 500
for timer in range(0,20):
    driver.execute_script("window.scrollTo(0, "+str(y)+")")
    y += 500  
    time.sleep(1)

data_group = []

# get HTML dari halaman grup
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

all_posts = soup.find_all("div", class_="x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z")

# log jumlah postingan yang ditemukan
print(f"Found {len(all_posts)} posts.")

for post in all_posts:
    name_account = post.find("a", class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f" )
    content_account = post.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
    
    if name_account and content_account :
        name = name_account.get_text()
        content = content_account.get_text()
        data_group.append({
            'nama' : name,
            'content' : content,
        }) 

driver.quit()

print(data_group)

df = pd.DataFrame(data_group)
with pd.ExcelWriter('facebook.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)