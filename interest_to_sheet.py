from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=options)
url = "https://smartstore.naver.com/hangugmall"
driver.get(url)
WebDriverWait(driver, 15).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# 페이지 저장 (디버깅용)
with open("debug.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

interest_count = "데이터 없음"
try:
    all_divs = driver.find_elements(By.CSS_SELECTOR, "#header div")
    for el in all_divs:
        text = el.text.strip()
        if "관심고객수" in text:
            match = re.search(r'\d[\d,]*', text)
            if match:
                interest_count = match.group(0).replace(",", "")
            break
except Exception as e:
    print("크롤링 실패:", e)

driver.quit()

# 한국 시간
today = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("14Su0OGiAwZsD5jRCPMf5ar0NrDnB0WZmAPcK23thuvw")
worksheet = spreadsheet.sheet1
worksheet.append_row([today, interest_count])

print(f"{today} : {interest_count} 저장 완료!")
