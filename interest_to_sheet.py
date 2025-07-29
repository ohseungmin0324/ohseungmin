from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import re

# ---------------------------
# 1. Selenium (ChromeDriver) 설정
# ---------------------------
options = Options()
options.add_argument("--headless")  # headless 모드
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
url = "https://smartstore.naver.com/hangugmall"
driver.get(url)

# 페이지 로딩 완료 대기
WebDriverWait(driver, 15).until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# ---------------------------
# 2. 관심고객수 추출 로직
# ---------------------------
interest_count = "데이터 없음"

try:
    # 관심고객수 div가 로딩될 때까지 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#header div"))
    )

    all_divs = driver.find_elements(By.CSS_SELECTOR, "#header div")
    for el in all_divs:
        text = el.text.strip()
        if "관심고객수" in text:
            match = re.search(r'\d[\d,]*', text)
            if match:
                interest_count = match.group(0).replace(",", "")
            break

    # Fallback: 모든 페이지 소스에서 "관심고객수" 검색
    if interest_count == "데이터 없음":
        page_text = driver.page_source
        match = re.search(r'관심고객수[^0-9]*([\d,]+)', page_text)
        if match:
            interest_count = match.group(1).replace(",", "")

except Exception as e:
    print("크롤링 실패:", e)

driver.quit()

# ---------------------------
# 3. Google Sheet 저장
# ---------------------------
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("14Su0OGiAwZsD5jRCPMf5ar0NrDnB0WZmAPcK23thuvw")
worksheet = spreadsheet.sheet1
worksheet.append_row([today, interest_count])

print(f"{today} : {interest_count} 저장 완료!")
