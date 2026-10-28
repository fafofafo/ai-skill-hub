
const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',
    headless: 'new',
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-web-security','--allow-file-access-from-files','--mute-audio'],
  });
  const page = await browser.newPage();
  page.on('console', m => console.log('CONSOLE:', m.type(), m.text().slice(0,300)));
  page.on('pageerror', e => console.log('PAGEERROR:', String(e).slice(0,300)));
  page.on('requestfailed', r => console.log('REQFAIL:', r.url().slice(0,150), r.failure()?.errorText));
  await page.setViewport({width:880, height:1184, deviceScaleFactor:1});
  try {
    await page.goto('file:///tmp/mv_job/_viz_sketch.html', {waitUntil:'networkidle0', timeout:30000});
  } catch(e) { console.log('GOTO-ERR:', e.message.slice(0,200)); }
  await new Promise(r=>setTimeout(r,3000));
  const hasCanvas = await page.evaluate(() => !!document.querySelector('canvas'));
  const p5Ready = await page.evaluate(() => window._p5Ready || false);
  console.log('hasCanvas:', hasCanvas, 'p5Ready:', p5Ready);
  await browser.close();
})().catch(e => { console.log('FATAL:', e.message.slice(0,300)); process.exit(1); });
