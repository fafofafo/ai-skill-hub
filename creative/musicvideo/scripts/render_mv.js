#!/usr/bin/env node
/** p5.js 渲染: puppeteer-core + Playwright chromium, noLoop+redraw 逐帧精确渲染
 *  ⚠️ 铁律: 必须用 canvas.toDataURL() 序列化帧——canvas.screenshot() 会把 880px 宽内容截成 ~700px 留白边!
 *  用法:
 *    node render_mv.js <sketch.html> --frames N [--width W] [--height H] [--settle ms] [--chrome PATH]
 *    [--imgs a.png,b.png]  → 渲染前注入 window.__IMGS = [...] 并触发 reload(模板用它设置图片列表)
 *    [--json key=val,...]  → 注入任意 window.__CFG 键值
 */
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
function opt(k, d) { const i = args.indexOf('--' + k); return i >= 0 ? args[i+1] : d; }

const input = opt('input', null) || args[0];
const output = opt('output', './frames');
const width = parseInt(opt('width', '880'), 10);
const height = parseInt(opt('height', '1184'), 10);
const frames = parseInt(opt('frames', '450'), 10);
const start = parseInt(opt('start', '0'), 10);   // 断点续跑：跳过前 N 帧（快进不保存）
const settle = parseInt(opt('settle', '15'), 10);
const chrome = opt('chrome', '');
const imgsArg = opt('imgs', '');
const cfgArg = opt('json', '');
const fmt = opt('format', 'png');   // png | jpeg (jpeg 体积小~10x, 长视频必需)
const jpegQ = parseInt(opt('jpegq', '85'), 10);

if (!input) { console.error('usage: node render_mv.js <sketch.html> --frames N [--imgs a.png,b.png] [--json k=v,...]'); process.exit(1); }
const inputPath = path.resolve(input);
fs.mkdirSync(output, { recursive: true });

// 注入配置
const injectImgs = imgsArg ? imgsArg.split(',').map(s => s.trim()).filter(Boolean) : null;
const injectCfg = {};
if (cfgArg) {
  for (const kv of cfgArg.split(',')) {
    const [k, v] = kv.split('=');
    if (k && v !== undefined) injectCfg[k] = isNaN(Number(v)) ? v : Number(v);
  }
}

// 自动探测 chrome: Playwright 缓存 > snap chromium > 系统 chromium
function findChrome() {
  if (chrome) return chrome;
  const candidates = [
    '/home/ubuntu/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',
    '/home/ubuntu/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome',
    '/usr/bin/chromium-browser',
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  return '/usr/bin/chromium';
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: findChrome(),
    headless: 'new',
    args: ['--no-sandbox','--disable-setuid-sandbox','--disable-gpu','--disable-dev-shm-usage','--disable-web-security','--allow-file-access-from-files','--mute-audio'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: 1 });
  await page.goto('file://' + inputPath, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.waitForSelector('canvas', { timeout: 10000 });

  // 注入图片列表/配置后 reload（模板在 setup 里读 window.__IMGS）
  if (injectImgs || Object.keys(injectCfg).length) {
    await page.evaluate(({ imgs, cfg }) => {
      if (imgs) window.__IMGS = imgs;
      if (cfg) { window.__CFG = Object.assign(window.__CFG || {}, cfg); }
    }, { imgs: injectImgs, cfg: injectCfg });
    await page.reload({ waitUntil: 'networkidle0' });
    await page.waitForSelector('canvas', { timeout: 10000 });
  }
  try { await page.waitForFunction('window._p5Ready === true', { timeout: 5000 }); }
  catch (e) { console.log('timed fallback'); }

  const t0 = Date.now();
  // 断点续跑：快进到 start 帧（页面状态推进但不保存）
  if (start > 0) {
    for (let j = 0; j < start; j++) {
      await page.evaluate(() => { redraw(); });
      await new Promise(r => setTimeout(r, 2));
    }
    process.stdout.write(`Skip ${start} frames (warmup) ${((Date.now()-t0)/1000).toFixed(0)}s\n`);
  }
  for (let i = start; i < frames; i++) {
    await page.evaluate(() => { redraw(); });
    await new Promise(r => setTimeout(r, settle));
    const name = path.join(output, 'frame-' + String(i).padStart(4, '0') + '.' + fmt);
    const mime = fmt === 'jpeg' ? 'image/jpeg' : 'image/png';
    const dataUrl = await page.evaluate((m) => document.querySelector('canvas').toDataURL(m), mime);
    fs.writeFileSync(name, Buffer.from(dataUrl.split(',')[1], 'base64'));
    if (i % 50 === 0 || i === frames - 1) {
      const pct = ((i+1)/frames*100).toFixed(1);
      const el = ((Date.now()-t0)/1000).toFixed(0);
      process.stdout.write(`\r  Frame ${i+1}/${frames} (${pct}%) ${el}s`);
    }
  }
  console.log('\nDone. ' + frames + ' frames in ' + ((Date.now()-t0)/1000).toFixed(0) + 's');
  await browser.close();
})().catch(e => { console.error('Error:', e.message); process.exit(1); });
