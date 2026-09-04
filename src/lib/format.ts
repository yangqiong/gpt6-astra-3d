import type { Locale } from '../i18n';

const MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function pad(n: number): string {
  return String(n).padStart(2, '0');
}

/** 23000 → "23.0K" (en) / "2.3万" (zh); 857 → "857" */
export function formatLikes(n: number, locale: Locale): string {
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

/** 6920000 → "6.9M" (en) / "692万" (zh); 40300 → "40.3K" / "4.0万" */
export function formatViews(n: number, locale: Locale): string {
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

/** "2026-09-03T19:33:00Z" → "Sep 3, 19:33" (en) / "9月3日 19:33" (zh), always UTC */
export function formatDate(iso: string, locale: Locale): string {
  const d = new Date(iso);
  const hm = `${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}`;
  if (locale === 'zh') return `${d.getUTCMonth() + 1}月${d.getUTCDate()}日 ${hm}`;
  return `${MONTHS_EN[d.getUTCMonth()]} ${d.getUTCDate()}, ${hm}`;
}
