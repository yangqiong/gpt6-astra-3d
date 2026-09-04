# Deployment · 部署指南

网站是纯静态 Astro 站点，数据源为 [`data/creations.json`](data/creations.json)（站点与 README 表格共用）。

## 日常更新流程

```bash
# 1. 编辑 data/creations.json（新增/修改作品）

# 2. 重新生成两个 README 中的表格（必须，否则 README 与站点不同步）
npm run sync:readme

# 3. 本地预览确认
npm run dev          # http://localhost:4321

# 4. 构建并部署到 Cloudflare Pages
npm run deploy       # = astro build + wrangler pages deploy dist
```

## Cloudflare Pages 部署方式

### 方式 A：Wrangler 直传（当前使用）

```bash
npx wrangler login                                   # 仅首次；或使用 API Token
npx wrangler pages project create gpt6-astra-3d --production-branch main
npx wrangler pages deploy dist --project-name gpt6-astra-3d --branch main --commit-dirty=true
```

- 默认获得 `https://gpt6-astra-3d.pages.dev` 子域名
- API Token 替代登录：在 [API Tokens](https://dash.cloudflare.com/profile/api-tokens) 用
  *Edit Cloudflare Workers* 模板创建，然后 `export CLOUDFLARE_API_TOKEN=xxx`（勿提交到仓库）

### 方式 B：Git 集成（每次 push 自动构建）

1. 仓库推送到 GitHub
2. Cloudflare Dashboard → Workers & Pages → Create → Pages → **Connect to Git** 选择仓库
3. 构建配置：
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Build output directory: `dist`
4. 保存后每次 `git push` 自动构建部署（生产分支 `main`，其他分支生成 preview URL）

## 绑定自定义域名

1. 在 Cloudflare Registrar / Porkbun / Namecheap 注册域名（Cloudflare Registrar 为成本价）
2. Pages 项目 → **Custom domains** → Set up a custom domain → 输入域名
3. DNS 解析：
   - 域名 DNS 在 Cloudflare：自动添加 CNAME 记录，零配置
   - DNS 在其他注册商：添加 CNAME，`www`/根域名 → `<project>.pages.dev`（或按控制台提示改 NS 到 Cloudflare）
4. 等 HTTPS 证书签发完成（几分钟到几小时），即可通过 `https://你的域名` 访问
5. 绑定后把 `astro.config.mjs` 里的 `site` 改为自定义域名并重新部署（保证 canonical/OG 链接正确）

## 目录结构

```
data/creations.json      # 唯一数据源（中英双语）
scripts/sync-readme.mjs  # 由 JSON 重新生成 README 表格
src/pages/index.astro    # 英文页 /
src/pages/zh/index.astro # 中文页 /zh/
public/_headers          # Cloudflare Pages 缓存/安全头
```
