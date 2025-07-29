import requests
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# API URL
url = "https://smartstore.naver.com/i/v2/channels/2sWDvfVZ7JcpctEbCV9yS/individual-info"

# Headers 설정 (User-Agent만 있어도 정상 호출 가능)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://smartstore.naver.com/hangugmall"
}

response = requests.get(url, headers=headers)
interest_count = "데이터 없음"

if response.status_code == 200:
    data = response.json()
    print("API 응답:", data)  # 전체 데이터 확인
    # followerCount 값 추출
    if "followerCount" in data:
        interest_count = data["followerCount"]
    else:
        print("followerCount 키가 없음:", data.keys())
else:
    print("API 요청 실패:", response.status_code)

# 한국 시간
today = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")

# Google Sheet 기록
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key("14Su0OGiAwZsD5jRCPMf5ar0NrDnB0WZmAPcK23thuvw")
worksheet = spreadsheet.sheet1
worksheet.append_row([today, interest_count])

print(f"{today} : {interest_count} 저장 완료!")
