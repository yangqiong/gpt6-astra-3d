# GPT-6 Astra 创建的 three.js 作品收集

> 收集时间：2026-09-05（覆盖 GPT-6 Astra 发布后最近两天：9 月 3 日 – 9 月 5 日）
> 数据来源：X（Twitter）原帖，经 fxtwitter API 逐条核实原文、作者、日期与外链；体验地址均已验证在线。

GPT-6 Astra 由 OpenAI 于 2026 年 9 月 3 日发布（[发布公告](https://x.com/OpenAI/status/2095595757072191802)），发布后 48 小时内 X 上出现了大量 three.js 相关演示，本仓库汇总其中已核实的关键帖子。

## 作品汇总表

| # | 原帖作者 | 原帖链接 | 总结标题 | 总结描述 | 体验地址 |
|---|---------|---------|---------|---------|---------|
| 1 | **Ethan Mollick**（@emollick，Wharton 教授）<br>9月4日 00:42 UTC | [x.com/emollick/status/2095673885605630429](https://x.com/emollick/status/2095673885605630429) | 深海生物群系模拟世界 Abyssal Living Deep | 以一个开源单文件「海面风暴生成器」为起点，让 GPT-6 Astra 补全整个海洋世界，包含程序化生成的深海动物行为模拟；支持切换珊瑚礁等场景、光照与随机种子。676 赞 / 7.2 万浏览 | [abyssal-living-deep.netlify.app](https://abyssal-living-deep.netlify.app/?site=reef&seed=713&light=day&surface=1)<br>源码：[github.com/emollick/abyssal-living-deep](https://github.com/emollick/abyssal-living-deep) |
| 2 | **Peter Gostev**（@petergostev，Arena.ai AI Capability Lead）<br>9月4日 07:31 UTC | [x.com/petergostev/status/2095776685807346105](https://x.com/petergostev/status/2095776685807346105) | 梵高小镇 Van Gogh Town | GPT-6-Astra (Max) 将 6 幅梵高画作（星月夜、在阿尔勒的卧室、夜晚露天咖啡座等）融合成一座可第一人称行走的 three.js 小镇，含约 3295 个可编辑物体；作者已托管供体验。1474 赞 / 10.8 万浏览 | [van-goghs-town.surge.sh](https://van-goghs-town.surge.sh/) |
| 3 | **leo 🐾**（@synthwavedd）<br>9月4日 11:44 UTC | [x.com/synthwavedd/status/2095840435319001278](https://x.com/synthwavedd/status/2095840435319001278) | 单回合生成的 Three.js 海战场景 | GPT-6 Astra (max) 仅用一轮对话（无示例、基础提示词）生成海战场景：舰船模型细节丰富、物体与水面有交互；约 5 万 token、12 分钟完成。741 赞 / 3.9 万浏览 | 无公开体验地址（原帖仅视频演示） |

## 相关汇总帖（索引性质）

| 作者 | 链接 | 说明 |
|------|------|------|
| TechHalla（@techhalla）· 9月4日 | [x.com/techhalla/status/2095778682648334421](https://x.com/techhalla/status/2095778682648334421) | 《GPT-6 Astra 发布仅 12 小时，8 个狂野案例》线程，其中包含梵高小镇（3295 个可编辑物体）等 three.js 案例 |

## 排除的边界案例（避免混淆）

| 案例 | 排除原因 |
|------|---------|
| [Tom Krcha 房屋 3D 重建](https://x.com/tomkrcha/status/2095598645190291775)（9月3日）、[蒸汽火车 3295 物体重建](https://x.com/tomkrcha/status/2095756085890310311)（9月4日） | 热度高但为 **Blender** 建模（可本地 60fps 运行），并非 three.js；多篇汇总文将其与 Gostev 的梵高小镇混淆 |
| [Matthew Berman 的 Fall Guys 克隆](https://x.com/MatthewBerman/status/2095595895584907501)（9月3日） | 视频演示，未注明 three.js，无体验链接 |
| [TimJayas 的 3D 飞船](https://x.com/TimJayas/status/2093702026601566272) | 发布于 8 月 29 日（发布前泄露），超出「最近两天」窗口 |
| CtrlAltDwayne 的 GTA 6 沼泽汽船游戏 | 发布于 8 月 28 日，且与 Astra 无关 |
| Mikko Ohtamaa 的赛车 / 3D 重建演示 | 使用上一代 GPT-5.6 Sol，非 Astra |

## 收集方法说明

- X 未登录无法直接搜索（登录墙），采用「多路 Web 搜索发现候选 + fxtwitter API 逐条验证原文与外链」的方式。
- 表中作者、日期、内容、互动数据均取自帖子原文（fxtwitter API 返回值），未采用二手转述。
- 体验地址 `van-goghs-town.surge.sh`、`abyssal-living-deep.netlify.app` 及 GitHub 源码仓库均已于 2026-09-05 验证返回 HTTP 200。
