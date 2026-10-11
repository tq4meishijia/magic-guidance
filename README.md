# magic-guidance

一套新拟物派（Neumorphism / Soft UI）风格的多平台代理软件使用文档阅读站。纯静态、零运行时依赖、离线可用——克隆后直接打开 `index.html` 即可阅读。

> **免责声明**：本项目仅收录技术交流性质的软件使用文档，不提供任何节点或订阅服务。文档内容包含完整的合规提示：在中国大陆，个人未经批准自行连接国际互联网属于行政违法行为；在校学生应特别留意校园网环境的使用限制。请遵守所在地区法律法规。

## 功能

- **全量文档呈现**：六章内容（通用上手流程 / 分平台软件推荐与配置 / 基础概念 / 协议介绍 / 常见问题 / 合规提示），含 8 张对照表格
- **侧栏目录**：由章节标题自动生成，滚动时 IntersectionObserver 高亮当前章节
- **章节折叠**：点击章标题收起 / 展开该章内容
- **移动端适配**：<960px 时侧栏转为汉堡按钮唤出的抽屉，表格容器横向滚动
- **阅读辅助**：顶部阅读进度条、返回顶部按钮、顶栏滚动阴影
- **合规强调样式**：免责声明、校园网风险提示、安全合规说明以独立警示样式呈现

## 快速开始

无构建必需步骤——`index.html` 已预构建。

```bash
# 方式一：直接用浏览器打开
start index.html        # Windows
open index.html         # macOS

# 方式二：本地静态服务（推荐，路径行为与线上一致）
npm run serve           # 等价于 npx serve .
# 或
python -m http.server 8080
```

## 重新构建

修改 `content/doc.md` 后重新生成 `index.html`：

```bash
pip install markdown
python scripts/build.py
```

## 技术栈

| 层 | 选型 | 说明 |
|---|---|---|
| 结构 | 原生 HTML5 | 语义化标签，无框架 |
| 样式 | 原生 CSS3 | 三层拆分：令牌 / 布局 / 组件 |
| 交互 | 原生 JavaScript (ES5 兼容写法) | 无第三方库 |
| 构建 | Python 3.8+ | 仅 `markdown` 一个依赖 |

## 目录结构

```
magic-guidance/
├── index.html            # 预构建产物，直接打开即可阅读
├── css/
│   ├── tokens.css        # 设计令牌：颜色 / 双光源阴影 / 圆角 / 动效（含暗色阴影响应式与 reduced-motion）
│   ├── layout.css        # 布局：顶栏 / 侧栏 / 主区 / 抽屉 / 返回顶部
│   └── components.css    # 组件：hero / 章节卡片 / 表格 / 引用块 / 警示样式
├── js/
│   └── main.js           # 章节切分折叠 / 目录生成与滚动高亮 / 抽屉 / 进度条
├── content/
│   └── doc.md            # 文档 Markdown 源
├── scripts/
│   └── build.py          # 构建脚本：doc.md → index.html
├── docs/
│   └── handoff-*.md      # 交接文档
└── package.json          # npm run serve 本地预览
```

## 设计规范（Neumorphism / Soft UI）

本项目严格遵循以下风格约束，改动样式前请先阅读 `css/tokens.css` 内的注释：

- 背景 `#e0e5ec` 单色系，元素与背景同色；禁止纯黑 / 纯白背景、渐变、`border-2` 及以上边框
- 双光源阴影：亮阴影 `-X/-Y`（白），暗阴影 `+X/+Y`（`#b8bcc2`），方向全局锁死
- 交互三态：hover 阴影**缩小**（手指靠近遮光），active 外凸转**内凹**（Extrude to Intrude），全程无 `translate` 位移
- 圆角 12–24px；过渡 `0.3s ease-in-out`；`prefers-reduced-motion` 时全部动效关闭
- 文本对比度满足 WCAG AA（正文 `#333` ≈ 9.7:1，次要文字 `#5b6472` ≈ 5.2:1）

## License

文档内容基于各项目官方仓库与公开资料整理，仅供学习交流。
