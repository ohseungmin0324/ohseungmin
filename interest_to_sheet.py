from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Selenium으로 페이지 로드
url = "https://smartstore.naver.com/hangugmall"

options = Options()
options.add_argument("--headless")  # 화면 표시 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(url)

try:
    # 관심고객수 요소가 나타날 때까지 최대 10초 대기
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div._3kDC7jvaa-"))
    )
except Exception as e:
    print("관심고객수 요소를 찾지 못했습니다:", e)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# 2. 관심고객수 추출
interest_count = "데이터 없음"
try:
    element = soup.select_one("div._3kDC7jvaa-")
    if element:
        interest_count = element.get_text(strip=True).replace("관심고객수", "").strip()
except Exception as e:
    print("크롤링 실패:", e)

# 3. Google Sheets에 기록
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("14Su0OGiAwZsD5jRCPMf5ar0NrDnB0WZmAPcK23thuvw")
worksheet = spreadsheet.sheet1
worksheet.append_row([today, interest_count])

print(f"{today} : {interest_count} 저장 완료!")
