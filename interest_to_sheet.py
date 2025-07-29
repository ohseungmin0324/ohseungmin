from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import re

# ---------------------------
# 1. Selenium (ChromeDriver) 설정
# ---------------------------
chrome_driver_path = r"C:\chromedriver\chromedriver.exe"
options = Options()
# options.add_argument("--headless")  # 테스트 중에는 창을 띄워 확인
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# ---------------------------
# 2. 스마트스토어 페이지 접근
# ---------------------------
url = "https://smartstore.naver.com/hangugmall"
driver.get(url)
time.sleep(5)  # 페이지 로딩 대기

# ---------------------------
# 3. 관심고객수 추출 로직
# ---------------------------
interest_count = "데이터 없음"
all_divs = driver.find_elements(By.CSS_SELECTOR, "#header div")

for el in all_divs:
    text = el.text.strip()
    if "관심고객수" in text:
        # "관심고객수 64,688" 형태에서 숫자만 추출
        match = re.search(r'\d[\d,]*', text)
        if match:
            interest_count = match.group(0).replace(",", "")
        break

driver.quit()

# ---------------------------
# 4. Google Sheet 저장
# ---------------------------
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("14Su0OGiAwZsD5jRCPMf5ar0NrDnB0WZmAPcK23thuvw")
worksheet = spreadsheet.sheet1
worksheet.append_row([today, interest_count])

print(f"{today} : {interest_count} 저장 완료!")
