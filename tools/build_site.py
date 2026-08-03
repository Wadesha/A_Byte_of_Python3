# -*- coding: utf-8 -*-
"""
build_site.py — 生成本项目的多层级 GitHub Pages 静态站点。

结构:
    index.html                  首页（导航 / 统计 / 章节卡片 / 精选代码 / 仿真演示）
    chapters/<slug>.html        每章独立页（展示该章全部 .py 源码 + 下载 .ipynb）
    examples/address-book.html  综合示例页（contacts.py 源码 + 可交互仿真）
    assets/style.css, app.js    共享样式与脚本

用法:
    python tools/build_site.py
"""
import os, html, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(ROOT, "chapters")
EXAMPLES_DIR = os.path.join(ROOT, "examples")
ASSETS_DIR = os.path.join(ROOT, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

REPO_URL = "https://github.com/Wadesha/A_Byte_of_Python3"
PAGES_URL = "https://wadesha.github.io/A_Byte_of_Python3/"

CHAPTERS = [
    ("ch01-07-basics", "第 1–7 章 基础", "Basics",
     "安装 / Hello World / 变量 / 运算符 / 控制流（if·while·break·continue）/ 字符串格式化 / 文件读写入门。"),
    ("ch08-functions", "第 8 章 函数", "Functions",
     "形参与实参 / 默认参数 / 关键字参数 / 可变参数 / 局部·全局·nonlocal / 返回值。"),
    ("ch09-modules", "第 9 章 模块", "Modules",
     "自定义模块 / import 机制 / __name__ / sys 模块。"),
    ("ch10-data-structures", "第 10 章 数据结构", "Data Structures",
     "列表 / 元组 / 字典 / 字符串方法 / 序列。"),
    ("ch11-problem-solving", "第 11 章 解决问题", "Problem Solving",
     "备份脚本的四个演进版本，以及自顶向下的设计思路。"),
    ("ch12-oop", "第 12 章 面向对象编程", "OOP",
     "类与对象 / 方法 / 继承 / 实例变量。"),
    ("ch13-io", "第 13 章 输入输出", "I/O",
     "文件读写 / pickle 序列化 / 用户输入。"),
    ("ch14-exceptions", "第 14 章 异常", "Exceptions",
     "try/except / raise / finally / with 语句。"),
    ("ch15-stdlib", "第 15 章 标准库", "Standard Library",
     "logging / 版本检查 / Yahoo 搜索（旧 API，可能已失效，仅供学习）。"),
    ("ch16-more", "第 16 章 更多内容", "More",
     "lambda 表达式 / 列表推导式。"),
]
EXAMPLE = ("examples/address-book", "综合示例：通讯录程序", "Address Book",
           "基于 pickle 的完整联系人管理小程序，支持增、删、改、查。对应源码 examples/address-book/contacts.py。")


def read_file(path):
    for enc in ("utf-8", "gbk"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    with open(path, "rb") as f:
        return f.read().decode("utf-8", "replace")


def count_py():
    n = 0
    for base in (CHAPTERS_DIR, EXAMPLES_DIR):
        n += len(glob.glob(os.path.join(base, "**", "*.py"), recursive=True))
        n += len(glob.glob(os.path.join(base, "**", "*.pyw"), recursive=True))
    return n


def count_nb():
    n = 0
    for base in (CHAPTERS_DIR, EXAMPLES_DIR):
        n += len(glob.glob(os.path.join(base, "**", "*.ipynb"), recursive=True))
    return n


def code_block(filename, code):
    esc = html.escape(code)
    return (
        '<div class="code-card">'
        '<div class="code-head"><span class="fname">' + html.escape(filename) + '</span>'
        '<button class="copy" onclick="copyCode(this)">复制</button></div>'
        '<pre><code class="language-python">' + esc + '</code></pre></div>'
    )


def page(rel, title, body):
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · A Byte of Python3</title>
<link rel="stylesheet" href="{rel}assets/style.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js"></script>
</head>
<body>
<header class="nav"><div class="wrap nav-inner">
  <a class="brand" href="{rel}index.html">A Byte of <span>Python3</span></a>
  <nav>
    <a href="{rel}index.html">首页</a>
    <a href="{rel}chapters/ch01-07-basics.html">章节</a>
    <a href="{rel}examples/address-book.html">示例</a>
    <a href="{repo}">仓库</a>
    <button class="ghost" onclick="toggleTheme()" title="切换主题">🌓</button>
  </nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">
  <p>示例代码改编自 《A Byte of Python》© Swaroop C H · 本仓库整理 © 2026 Wade · CC BY-SA 4.0</p>
  <p class="muted">展示页仅使用模拟数据，不含任何个人隐私或原始采集数据。</p>
</div></footer>
<script src="{rel}assets/app.js"></script>
</body></html>'''.format(title=title, rel=rel, body=body, repo=REPO_URL)


def sim_html():
    return '''
<div class="sim">
  <div class="note">📇 通讯录仿真：完全用 JavaScript 模拟，仅使用<b>模拟数据</b>，不执行 Python、不读写任何真实文件（对应源码见 examples/address-book/contacts.py）。</div>
  <div class="row">
    <input id="cName" placeholder="联系人姓名（如 张三）" />
    <input id="cPhone" placeholder="电话号码（如 13800000000）" />
    <button onclick="simAdd()">添加</button>
    <button class="alt" onclick="simSearch()">查找</button>
    <button class="alt" onclick="simDel()">删除</button>
    <button class="alt" onclick="simDisplay()">显示全部</button>
  </div>
  <div class="out" id="simOut">> 已预置 3 条模拟数据，点击「显示全部」开始。\\n> 对应源码：examples/address-book/contacts.py</div>
</div>'''


def build_index():
    total_py = count_py()
    total_nb = count_nb()
    cards = []
    for slug, zh, en, desc in CHAPTERS:
        card = (
            '<div class="card"><div class="slug">{slug}</div>'
            '<h3><a href="chapters/{slug}.html">{zh}</a></h3>'
            '<p>{desc}</p>'
            '<div class="cnt"><a href="chapters/{slug}.html">查看全部源码 →</a></div></div>'
        ).format(slug=slug, zh=zh, desc=desc)
        cards.append(card)
    card = (
        '<div class="card"><div class="slug">examples/address-book</div>'
        '<h3><a href="examples/address-book.html">{zt}</a></h3>'
        '<p>{zd}</p>'
        '<div class="cnt"><a href="examples/address-book.html">查看示例与仿真 →</a></div></div>'
    ).format(zt=EXAMPLE[1], zd=EXAMPLE[3])
    cards.append(card)

    # 精选代码
    feat = []
    for slug, fn in [
        ("ch01-07-basics", "helloworld.py"),
        ("ch08-functions", "func_default.py"),
        ("ch10-data-structures", "using_list.py"),
        ("ch16-more", "list_comprehension.py"),
    ]:
        fp = os.path.join(CHAPTERS_DIR, slug, fn)
        if os.path.exists(fp):
            feat.append(code_block(fn, read_file(fp)))

    body = '''
<div class="hero"><div class="wrap">
  <h1>《简明 Python 教程》中文版 · 示例代码库</h1>
  <p>整理自 Swaroop C H 的《A Byte of Python》。这里汇集每一章的可运行示例、交互式 Notebook，以及一个综合通讯录小程序。本站为<b>多层级静态站点</b>，可逐级深入查看每一章的完整源码。</p>
  <div class="badges">
    <span class="badge"><b>{py}</b> 个示例代码</span>
    <span class="badge"><b>{nb}</b> 个 Notebook</span>
    <span class="badge"><b>10</b> 章 + <b>1</b> 综合示例</span>
    <span class="badge">许可 <b>CC BY-SA 4.0</b></span>
  </div>
  <div>
    <a class="btn" href="{repo}">查看 GitHub 仓库</a>
    <a class="btn ghost" href="examples/address-book.html">▶ 看仿真演示</a>
  </div>
</div></div>

<section><div class="wrap">
  <h2>章节 <span class="em">导航</span></h2>
  <p class="sub">点击任意卡片进入该章独立页面，查看全部源码。</p>
  <div class="grid">{cards}</div>
</div></section>

<section><div class="wrap">
  <h2>精选 <span class="em">代码片段</span></h2>
  <p class="sub">以下为代表性示例；<b>完整代码请进入对应章节页</b>。含 <code>while True:</code> 或 <code>input()</code> 的示例建议仅阅读、勿在 Notebook 中直接运行。</p>
  <div class="feat">{feat}</div>
</div></section>

<section><div class="wrap">
  <h2>快速 <span class="em">体验仿真</span></h2>
  <p class="sub">通讯录程序的纯前端仿真（模拟数据）。完整可运行源码见 <a href="examples/address-book.html">示例页</a>。</p>
  {sim}
</div></section>
'''.format(py=total_py, nb=total_nb, repo=REPO_URL, cards="".join(cards),
           feat="".join(feat), sim=sim_html())

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("", "首页", body))
    print("已生成 index.html")


def build_chapters():
    for slug, zh, en, desc in CHAPTERS:
        d = os.path.join(CHAPTERS_DIR, slug)
        files = sorted(glob.glob(os.path.join(d, "*.py")) +
                      glob.glob(os.path.join(d, "*.pyw")))
        blocks = []
        for fp in files:
            name = os.path.basename(fp)
            blocks.append(code_block(name, read_file(fp)))
        ipynb = os.path.join(d, slug + ".ipynb")
        nb_link = ""
        if os.path.exists(ipynb):
            nb_link = '<p class="muted" style="margin-top:10px"><a href="{s}.ipynb">⬇ 下载本章 Jupyter 笔记本（{s}.ipynb）</a></p>'.format(s=slug)
        body = '''
<div class="breadcrumb"><a href="../index.html">首页</a> / <span>{zh}</span></div>
<div class="chapter-head"><h1>{zh}</h1><span class="slug">{slug}</span></div>
<p class="lead">{desc}</p>
<p class="muted">本页共 <b>{n}</b> 个示例文件（完整源码如下）。</p>
<div class="filelist">{blocks}</div>
{nb}
'''.format(zh=zh, slug=slug, desc=desc, n=len(files),
           blocks="".join(blocks), nb=nb_link)
        out = os.path.join(CHAPTERS_DIR, slug + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(page("../", zh, body))
        print("已生成", out)


def build_example():
    d = os.path.join(EXAMPLES_DIR, "address-book")
    src = os.path.join(d, "contacts.py")
    code = read_file(src) if os.path.exists(src) else ""
    body = '''
<div class="breadcrumb"><a href="../index.html">首页</a> / <span>综合示例：通讯录</span></div>
<h1>综合示例：通讯录程序</h1>
<p class="lead">{desc}</p>
<p class="muted">源码文件：<code>examples/address-book/contacts.py</code>（基于 <code>pickle</code> 持久化，运行时产生 <code>contactsfile.data</code>，已被 .gitignore 排除）。</p>

<h2 style="margin-top:24px">源码</h2>
{code}

<h2 style="margin-top:24px">可交互仿真</h2>
<p class="sub">下方为前端仿真，完全使用模拟数据，不执行 Python。</p>
{sim}
'''.format(desc=EXAMPLE[3], code=code_block("contacts.py", code), sim=sim_html())
    out = os.path.join(d, "address-book.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page("../", "通讯录示例", body))
    print("已生成", out)


if __name__ == "__main__":
    build_index()
    build_chapters()
    build_example()
    print("站点生成完成。根目录：", ROOT)
