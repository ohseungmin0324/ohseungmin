import requests
from bs4 import BeautifulSoup
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. 스마트스토어 페이지 요청
url = "https://smartstore.naver.com/hangugmall"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2. 관심고객수 추출
interest_count = "데이터 없음"
try:
    # 관심고객수 포함 요소 검색
    element = soup.select_one("#header div._1Y0GXNu6q8 div")
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
