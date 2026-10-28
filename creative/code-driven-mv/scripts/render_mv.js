#!/usr/bin/env node
/** p5.js 逐帧渲染: puppeteer-core + chromium, noLoop+redraw 精确逐帧
 * 用法: NODE_PATH=<p5js技能scripts>/node_modules node render_mv.js <sketch.html> \
 *         --frames N --width W --height H --chrome <playwright-chromium路径> --output <dir>
 * ⚠️ chrome 必须用 Playwright 的 chromium（snap 版被 AppArmor 挡 file:// 和 /tmp 写入）
 * ⚠️ 帧输出必须用 canvas.toDataURL()——canvas.screenshot() 会把 canvas 内容
 *    截窄留白边（880px 宽被截到 ~700px，右侧整列纯白），且 toDataURL 版更快
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
const settle = parseInt(opt('settle', '15'), 10);
const chrome = opt('chrome', '/usr/bin/chromium');

if (!input) { console.error('usage: node render_mv.js <sketch.html> --frames N --width W --height H'); process.exit(1); }
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
  catch (e) { console.log('timed fallback'); }

  const t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    await page.evaluate(() => { redraw(); });
    await new Promise(r => setTimeout(r, settle));
    const name = path.join(output, 'frame-' + String(i).padStart(4, '0') + '.png');
    const dataUrl = await page.evaluate(() => document.querySelector('canvas').toDataURL('image/png'));
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
