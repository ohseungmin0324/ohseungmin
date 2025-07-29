const puppeteer = require('puppeteer-core');
const { GoogleSpreadsheet } = require('google-spreadsheet');
const { execSync } = require('child_process');

async function main() {
  // 시스템 chromium 경로 찾기
  const chromePath = execSync('which chromium-browser || which chromium || which google-chrome').toString().trim();

  const browser = await puppeteer.launch({
    executablePath: chromePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto('https://smartstore.naver.com/hangugmall', { waitUntil: 'networkidle2' });

  const count = await page.$eval('.3K0c7jvaa', el => el.innerText);
  console.log('관심고객수:', count);

  const creds = JSON.parse(process.env.GCP_CREDENTIALS);
  const doc = new GoogleSpreadsheet(process.env.SPREADSHEET_ID);

  await doc.useServiceAccountAuth(creds);
  await doc.loadInfo();

  const sheet = doc.sheetsByIndex[0];
  await sheet.addRow({ timestamp: new Date().toISOString(), customer_count: count });

  await browser.close();
}

main().catch(console.error);
