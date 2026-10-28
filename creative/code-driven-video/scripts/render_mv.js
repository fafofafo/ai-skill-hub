#!/usr/bin/env node
/**
 * p5.js 代码直出视频: puppeteer-core + Playwright chromium 逐帧渲染
 * 要求 sketch: noLoop() + window._p5Ready = true (脚本 redraw() 逐帧推进)
 *
 * 用法: node render_mv.js <sketch.html> [--frames N] [--output dir]
 *       [--width W] [--height H] [--settle ms] [--chrome PATH]
 * 默认: 450 帧 / 720x1280 / settle 15ms / chromium 自动探测
 *
 * chromium 自动探测顺序: --chrome 参数 > ms-playwright 缓存 > /usr/bin/chromium
 * 注意: snap 版 chromium 被 AppArmor 挡 file:// 与 /tmp 写入, 不可用
 */
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');
const os = require('os');

const args = process.argv.slice(2);
function opt(k, d) { const i = args.indexOf('--' + k); return i >= 0 ? args[i+1] : d; }

const input = opt('input', null) || args[0];
const output = opt('output', './frames');
const width = parseInt(opt('width', '720'), 10);
const height = parseInt(opt('height', '1280'), 10);
const frames = parseInt(opt('frames', '450'), 10);
const settle = parseInt(opt('settle', '15'), 10);

function findChrome() {
  const explicit = opt('chrome', null);
  if (explicit && fs.existsSync(explicit)) return explicit;
  const cache = path.join(os.homedir(), '.cache', 'ms-playwright');
  if (fs.existsSync(cache)) {
    const dirs = fs.readdirSync(cache).filter(d => d.startsWith('chromium')).sort();
    for (const d of dirs.reverse()) {
      const cand = path.join(cache, d, 'chrome-linux64', 'chrome');
      if (fs.existsSync(cand)) return cand;
    }
  }
  for (const c of ['/usr/bin/chromium', '/usr/bin/google-chrome']) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

const chrome = findChrome();
if (!input) { console.error('usage: node render_mv.js <sketch.html> --frames N --width W --height H'); process.exit(1); }
if (!chrome) { console.error('no chromium found; pass --chrome <path>'); process.exit(1); }
const inputPath = path.resolve(input);
fs.mkdirSync(output, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    executablePath: chrome,
    headless: 'new',
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-web-security','--allow-file-access-from-files','--mute-audio'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto('file://' + inputPath, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('canvas', { timeout: 10000 });
  try { await page.waitForFunction('window._p5Ready === true', { timeout: 5000 }); }
  catch (e) { console.log('timed fallback (sketch missing noLoop/_p5Ready — frames may drift)'); }

  const t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    await page.evaluate(() => { redraw(); });
    await new Promise(r => setTimeout(r, settle));
    const name = path.join(output, 'frame-' + String(i).padStart(4, '0') + '.png');
    const canvas = await page.$('canvas');
    await canvas.screenshot({ path: name, type: 'png' });
    if (i % 50 === 0 || i === frames - 1) {
      const pct = ((i+1)/frames*100).toFixed(1);
      const el = ((Date.now()-t0)/1000).toFixed(0);
      process.stdout.write(`\r  Frame ${i+1}/${frames} (${pct}%) ${el}s`);
    }
  }
  console.log('\nDone. ' + frames + ' frames in ' + ((Date.now()-t0)/1000).toFixed(0) + 's');
  await browser.close();
})().catch(e => { console.error('Error:', e.message); process.exit(1); });
