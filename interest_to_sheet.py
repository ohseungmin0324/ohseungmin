from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
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
time.sleep(3)  # JS 로딩 대기 (필요 시 5초로 늘려도 됨)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# 2. 관심고객수 추출
interest_count = "데이터 없음"
try:
    element = soup.select_one("#header div._1Y0GXNu6q8 div")  # 셀렉터 확인 필요
    if element:
        interest_count = element.text.strip()
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
