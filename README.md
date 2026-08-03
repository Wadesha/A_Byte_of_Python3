👉 在线演示（GitHub Pages）：https://wadesha.github.io/A_Byte_of_Python3/

# A Byte of Python3 · 中文版示例代码库

> 《A Byte of Python》（中文版《简明 Python 教程》，作者 Swaroop C H）的**配套可运行示例代码**整理仓库。
> 原始教材 PDF 见原项目；本仓库聚焦于**每一章的源码 + 可交互 Notebook + 一个综合示例程序**，并附带在线展示页。

---

## 📌 项目简介

| 项 | 内容 |
|---|---|
| 教程原名 | A Byte of Python |
| 中文名 | 简明 Python 教程 |
| 作者 | Swaroop C H |
| 许可 | CC BY-SA 4.0（详见 [LICENSE](LICENSE)） |
| 示例代码 | 59 个 `.py` / `.pyw` |
| 交互笔记本 | 11 个 `.ipynb` |
| 综合示例 | 1 个（通讯录程序） |
| 在线展示 | [GitHub Pages](https://wadesha.github.io/A_Byte_of_Python3/) |

> ⚠️ **第一行链接说明**：GitHub Pages 地址中的用户名 `wadesha` 是根据推送所用账号推测的占位值，**仓库创建并开启 Pages 后需核对实际用户名**。

---

## 🗂️ 项目架构

```
A_Byte_of_Python3/
├── README.md            # 本文件
├── index.html           # GitHub Pages 展示页（使用模拟数据）
├── LICENSE              # CC BY-SA 4.0
├── .gitignore           # 忽略 __pycache__ / *.data / 检查点等
├── chapters/            # 各章源码（已重命名为清晰 slug）
│   ├── ch01-07-basics/      # 第1–7章：基础
│   │   ├── *.py / *.pyw
│   │   └── ch01-07-basics.ipynb
│   ├── ch08-functions/      # 第8章：函数
│   ├── ch09-modules/        # 第9章：模块
│   ├── ch10-data-structures/# 第10章：数据结构
│   ├── ch11-problem-solving/# 第11章：解决问题
│   ├── ch12-oop/            # 第12章：面向对象编程
│   ├── ch13-io/             # 第13章：输入输出
│   ├── ch14-exceptions/     # 第14章：异常
│   ├── ch15-stdlib/         # 第15章：标准库
│   └── ch16-more/           # 第16章：更多内容
├── examples/
│   └── address-book/        # 综合示例：通讯录程序（pickle）
│       ├── contacts.py
│       └── address-book.ipynb
└── tools/
    └── merge_to_ipynb.py    # 把各章 .py 重新合并为 .ipynb 的构建脚本
```

### 重命名映射表（原中文名 → 仓库 slug）

| 原目录名 | 仓库 slug | 内容 |
|---|---|---|
| 第01--07章 | `ch01-07-basics` | 安装 / Hello World / 变量 / 运算符 / 控制流 / 字符串格式化 / 文件读写入门 |
| 第08章--函数 | `ch08-functions` | 形参实参 / 默认参数 / 关键字参数 / 可变参数 / 局部·全局·nonlocal / 返回值 |
| 第09章--模块 | `ch09-modules` | 自定义模块 / import 机制 / `__name__` / sys |
| 第10章--数据结构 | `ch10-data-structures` | 列表 / 元组 / 字典 / 字符串方法 / 序列 |
| 第11章--解决问题 | `ch11-problem-solving` | 备份脚本四个演进版本 / 设计思路 |
| 第12章--面向对象编程 | `ch12-oop` | 类与对象 / 方法 / 继承 / 实例变量 |
| 第13章--输入输出 | `ch13-io` | 文件读写 / pickle 序列化 / 用户输入 |
| 第14章--异常 | `ch14-exceptions` | try/except / raise / finally / with |
| 第15章--标准库 | `ch15-stdlib` | logging / 版本检查 / Yahoo 搜索（API 可能失效） |
| 第16章--更多内容 | `ch16-more` | lambda 表达式 / 列表推导式 |
| 地址薄程序 | `examples/address-book` | 基于 pickle 的完整联系人管理小程序（增删改查） |

---

## 🛠️ 操作方法

### 1. 直接运行示例代码
```bash
# 进入某一章目录
cd chapters/ch08-functions
python func_default.py
# 输出: Hello
#       WorldWorldWorldWorldWorld
```

### 2. 使用 Jupyter Notebook 交互阅读
```bash
# 安装并启动 Jupyter
pip install notebook
jupyter notebook chapters/ch08-functions/ch08-functions.ipynb
```
> 注意：含 `while True:` 或 `input()` 的示例已在 Notebook 中标注**运行警告**，建议仅阅读、勿直接运行。

### 3. 由源码重新生成 Notebook（可选）
```bash
# 依赖 chapters/ 与 examples/ 下的 .py 源码，重新生成各章 .ipynb
python tools/merge_to_ipynb.py
```
> 该脚本已**移除原版硬编码的本地路径**，默认基于仓库根目录运行，可在任意机器上使用。

### 4. 运行综合示例（通讯录）
```bash
cd examples/address-book
python contacts.py
# 菜单: 1:add 2:delete 3:search 4:modify 5:display 0:quit
```
> 该程序会把数据用 `pickle` 写入本地 `contactsfile.data`（已被 `.gitignore` 忽略，不会上传）。

---

## 🌐 在线展示页（index.html）

`index.html` 是部署在 **GitHub Pages** 的项目展示页，包含：
- 项目概览与统计
- 章节卡片导航
- **真实代码片段浏览**（仅嵌入部分代表性示例，性能优先）
- **模拟运行演示**：用 JavaScript 仿真的"通讯录"交互，**仅用模拟数据**，不执行 Python、不读写真实文件

> 展示页刻意只展示**部分数据**，以保证加载性能与隐私安全；完整代码请克隆仓库查看。

---

## 🔒 安全与隐私说明

- **不改动原始数据**：本仓库由本地 OneDrive 原始资料**复制整理**而来，原始文件保持不动。
- **不含隐私 / 原始采集数据**：仓库内仅有教程示例代码，无任何个人隐私、业务或采集数据。
- **本地路径已清除**：原 `merge_to_ipynb.py` 中的硬编码本地绝对路径已移除，改为相对路径。
- **展示页用模拟数据**：`index.html` 中的"运行结果"为前端仿真，不依赖也不暴露任何真实数据。
- **运行时产物不上传**：`*.data`、`contactsfile.data`、`__pycache__` 等已被 `.gitignore` 排除。

---

## 📄 许可与致谢

- 教程与示例代码版权归 **Swaroop C H** 所有，基于 [CC BY-SA 4.0](LICENSE) 发布。
- 本仓库的结构、重命名、README 与展示页 © 2026 Wade，同样以 CC BY-SA 4.0 发布。
- 致谢 Swaroop C H 创作了这本优秀的免费 Python 入门教程。
