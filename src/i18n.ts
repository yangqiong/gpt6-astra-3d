export type Locale = 'en' | 'zh';

export const REPO_URL = 'https://github.com/yangqiong/gpt6-astra-3d';

export const ui: Record<Locale, {
  htmlLang: string;
  brand: string;
  navGithub: string;
  langToggle: { label: string; href: string };
  kicker: string;
  title: string;
  subtitle: string;
  statWorks: string;
  statLikes: string;
  statViews: string;
  filterAll: string;
  categories: Record<string, string>;
  playLabel: string;
  sourceLabel: string;
  utcNote: string;
  footerCollected: string;
  footerBuilt: string;
}> = {
  en: {
    htmlLang: 'en',
    brand: 'GPT-6 Astra · 3D',
    navGithub: 'GitHub',
    langToggle: { label: '中文', href: '/zh/' },
    kicker: 'Sep 3–5, 2026 · the first 48 hours after release',
    title: 'GPT-6 Astra 3D Creations',
    subtitle:
      'The standout 3D works built with OpenAI’s GPT-6 Astra in its first 48 hours — collected from X, sorted by engagement. Click an author handle to open the original post.',
    statWorks: 'works',
    statLikes: 'likes',
    statViews: 'views',
    filterAll: 'All',
    categories: {
      world: 'Worlds & Games',
      web3d: 'Web 3D',
      modeling: 'Modeling',
      video: '3D Video',
    },
    playLabel: 'Play',
    sourceLabel: 'Source',
    utcNote: 'UTC',
    footerCollected: 'Data collected Sep 5, 2026 · curated from X',
    footerBuilt: 'Built with Astro · Hosted on Cloudflare Pages',
  },
  zh: {
    htmlLang: 'zh-CN',
    brand: 'GPT-6 Astra · 3D',
    navGithub: 'GitHub',
    langToggle: { label: 'English', href: '/' },
    kicker: '2026 年 9 月 3–5 日 · 发布后 48 小时',
    title: 'GPT-6 Astra 3D 作品集',
    subtitle:
      'OpenAI GPT-6 Astra 发布后 48 小时内涌现的精彩 3D 作品——收集自 X，按热度排序。点击作者 @handle 可打开原帖。',
    statWorks: '作品',
    statLikes: '点赞',
    statViews: '浏览',
    filterAll: '全部',
    categories: {
      world: '世界与游戏',
      web3d: 'Web 3D',
      modeling: '建模',
      video: '3D 视频',
    },
    playLabel: '在线体验',
    sourceLabel: '源码',
    utcNote: 'UTC',
    footerCollected: '数据收集于 2026 年 9 月 5 日 · 来自 X',
    footerBuilt: '使用 Astro 构建 · 托管于 Cloudflare Pages',
  },
};
