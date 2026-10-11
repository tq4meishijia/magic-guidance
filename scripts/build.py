# -*- coding: utf-8 -*-
"""
build.py — 构建脚本：content/doc.md → index.html
用法： python scripts/build.py
依赖： pip install markdown
产物： 项目根目录 index.html（纯静态，双击即可打开）
"""
import markdown
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "doc.md"
OUT = ROOT / "index.html"


def cn_slugify(value: str, separator: str) -> str:
    """目录锚点：保留中文，删空白与标点，转小写。"""
    value = re.sub(r"\s+", "", value)
    value = re.sub(r"[^\w\u4e00-\u9fff]", "", value)
    return value.lower()


md_text = SRC.read_text(encoding="utf-8")
body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc", "sane_lists"],
    extension_configs={"toc": {"permalink": False, "slugify": cn_slugify}},
)

# 网页用侧栏目录替代 md 手写目录（连同其后的分隔线一并移除，避免残留空隙）
body = re.sub(r"<h2[^>]*>\s*目录\s*</h2>\s*<ol>.*?</ol>(\s*<hr\s*/?>)?", "", body, flags=re.S)

# 表格包入凹陷托盘（Neumorphism inset），防移动端溢出
body = re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap">\1</div>', body, flags=re.S)

# 安全合规说明引用块 → 警示强调样式
body = re.sub(
    r"<blockquote>(\s*<p><strong>安全合规说明（面向中国大陆用户）</strong>)",
    r'<blockquote class="notice-strong">\1',
    body,
)

# 文首主标题与引用块由 hero 卡片承载，从正文流中剥离
m = re.search(r"<h1[^>]*>.*?</h1>", body, flags=re.S)
body = body[m.end():] if m else body
body = re.sub(r"^\s*(<blockquote>.*?</blockquote>\s*)+", "", body, count=1, flags=re.S)
body = re.sub(r"^(?:\s|<p>\s*</p>|<hr\s*/?>)+", "", body)  # 清理剥离后残留的空元素
body = body.replace(
    "<p><em>本文基于各项目官方仓库与公开资料整理，所涉软件与协议的细节以官方文档为准。</em></p>",
    "",
)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="多平台代理软件使用文档（新手版）——Neumorphism 风格静态阅读页">
<title>多平台代理软件使用文档 · 新手版</title>
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/components.css">
</head>
<body>

<div id="progress" role="progressbar" aria-label="阅读进度"></div>

<!-- 顶栏 -->
<header class="topbar">
  <button id="menuBtn" aria-label="打开目录" aria-expanded="false">☰</button>
  <span class="brand">多平台代理软件使用文档</span>
  <span class="tag">新手版 · 2026.10</span>
</header>

<div class="layout">

  <!-- 侧栏目录（JS 自动生成） -->
  <nav class="sidebar" id="sidebar" aria-label="文档目录">
    <p class="cap">目 录</p>
    <div id="toc"></div>
  </nav>

  <!-- 主内容：hero 由模板承载，章节由 JS 切卡 -->
  <main id="main">
    <section class="hero">
      <h1>多平台代理软件使用文档</h1>
      <p>适用读者：第一次接触代理软件、手里刚拿到一条订阅链接、不知道从哪下手的用户。</p>
      <p>整理时间：2026 年 10 月 · 软件信息以官方发布页为准</p>
      <div class="note"><b>免责声明：</b>在中国大陆，个人未经批准自行连接国际互联网属于行政违法行为，依照《计算机信息网络国际联网管理暂行规定》可处警告或罚款。本文档仅用于技术交流目的，不构成任何使用建议；请读者了解并遵守所在地区的法律法规，使用后果由本人承担。在校学生请特别留意校园网环境的使用限制，详见第六章。</div>
      <div class="note"><b>写在前面：</b>这份文档只介绍开源工具软件的功能与用法。所有工具都不附带节点和订阅，请确保你的服务来源合法合规。</div>
    </section>
__BODY__
  </main>
</div>

<footer>本文基于各项目官方仓库与公开资料整理，所涉软件与协议的细节以官方文档为准。</footer>

<button id="backtop" aria-label="返回顶部">↑</button>

<script src="js/main.js"></script>
</body>
</html>
"""

page = TEMPLATE.replace("__BODY__", "\n" + body)
OUT.write_text(page, encoding="utf-8")
print(f"build OK -> {OUT}  ({OUT.stat().st_size} bytes)")
