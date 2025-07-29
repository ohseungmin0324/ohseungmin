const puppeteer = require('puppeteer');
const { GoogleSpreadsheet } = require('google-spreadsheet');

async function main() {
  // Puppeteer로 관심고객수 크롤링
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto('https://smartstore.naver.com/hangugmall', { waitUntil: 'networkidle2' });

  const count = await page.$eval('.3K0c7jvaa', el => el.innerText);
  console.log('관심고객수:', count);

  // Google Sheets API 연결
  const creds = JSON.parse(process.env.GCP_CREDENTIALS);
  const doc = new GoogleSpreadsheet(process.env.SPREADSHEET_ID);

  await doc.useServiceAccountAuth(creds);
  await doc.loadInfo();

  const sheet = doc.sheetsByIndex[0]; // 첫 번째 시트
  await sheet.addRow({ timestamp: new Date().toISOString(), customer_count: count });

  await browser.close();
}

main().catch(console.error);
