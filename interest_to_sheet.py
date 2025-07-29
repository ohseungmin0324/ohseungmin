from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Selenium으로 페이지 로드
url = "https://smartstore.naver.com/hangugmall"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(url)

interest_count = "데이터 없음"
try:
    # 관심고객수 텍스트가 포함된 div가 로드될 때까지 대기
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_3kDC7jvaa-"))
    )
    if element:
        # 요소의 텍스트를 직접 가져옴
        raw_text = element.text.strip()
        interest_count = raw_text.replace("관심고객수", "").strip()
except Exception as e:
    print("크롤링 실패:", e)

driver.quit()

# 3. Google Sheets에 기록
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("14Su0OGiAwZsD5jRCPMf5ar0NrDnB0WZmAPcK23thuvw")
worksheet = spreadsheet.sheet1
worksheet.append_row([today, interest_count])

print(f"{today} : {interest_count} 저장 완료!")
