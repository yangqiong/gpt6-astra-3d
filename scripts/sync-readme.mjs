// Regenerates the creations table in README.md / README.zh-CN.md from
// data/creations.json (the single source of truth for both the site and docs).
// Tables live between <!-- creations:start --> and <!-- creations:end --> markers.

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(readFileSync(join(root, 'data/creations.json'), 'utf8'));

const MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const pad = (n) => String(n).padStart(2, '0');

function fmtLikes(n, locale) {
  if (locale === 'zh') {
    if (n >= 10000) {
      const v = n / 10000;
      return `${v >= 100 ? Math.round(v) : parseFloat(v.toFixed(1))}万`;
    }
    return String(n);
  }
  if (n >= 100000) return `${Math.round(n / 1000)}K`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

function fmtViews(n, locale) {
  if (locale === 'zh') {
    if (n >= 100000000) return `${parseFloat((n / 100000000).toFixed(1))}亿`;
    if (n >= 10000) {
      const v = n / 10000;
      return `${v >= 100 ? Math.round(v) : parseFloat(v.toFixed(1))}万`;
    }
    return String(n);
  }
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 100000) return `${Math.round(n / 1000)}K`;
  if (n >= 1000) return `${(n / 1000).toFixed(1)}K`;
  return String(n);
}

function fmtDate(iso, locale) {
  const d = new Date(iso);
  const hm = `${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}`;
  return locale === 'zh'
    ? `${d.getUTCMonth() + 1}月${d.getUTCDate()}日 ${hm}`
    : `${MONTHS_EN[d.getUTCMonth()]} ${d.getUTCDate()}, ${hm}`;
}

function demoCell(item, locale) {
  if (!item.demos || item.demos.length === 0) return '—';
  return item.demos
    .map((d) =>
      d.kind === 'play'
        ? `[🎮 ${locale === 'zh' ? '在线体验' : 'Play'}](${d.url})`
        : `[${locale === 'zh' ? '源码' : 'Source'}](${d.url})`
    )
    .join(' · ');
}

function buildTable(locale) {
  const header =
    locale === 'zh'
      ? '| # | 作者 | 总结标题 | 总结描述 | 热度 | 技术栈 | 时间 (UTC) | 体验地址 |\n|---|------|---------|---------|------|--------|-----------|---------|'
      : '| # | Author | Title | Description | Engagement | Tech | Time (UTC) | Demo |\n|---|--------|-------|-------------|------------|------|-----------|------|';

  const sorted = [...data.creations].sort((a, b) => b.likes - a.likes || b.views - a.views);
  const rows = sorted.map(
    (item, i) =>
      `| ${i + 1} | [@${item.author}](${item.url}) | ${item.title[locale]} | ${item.description[locale]} | ❤ ${fmtLikes(item.likes, locale)} / 👁 ${fmtViews(item.views, locale)} | ${item.tech[locale]} | ${fmtDate(item.postedAt, locale)} | ${demoCell(item, locale)} |`
  );
  return [header, ...rows].join('\n');
}

function sync(file, locale) {
  const path = join(root, file);
  const source = readFileSync(path, 'utf8');
  const re = /(<!-- creations:start -->)[\s\S]*?(<!-- creations:end -->)/;
  if (!re.test(source)) {
    throw new Error(`${file}: markers <!-- creations:start/end --> not found`);
  }
  const next = source.replace(re, `$1\n\n${buildTable(locale)}\n\n$2`);
  writeFileSync(path, next);
  console.log(`synced ${file}`);
}

sync('README.md', 'en');
sync('README.zh-CN.md', 'zh');
