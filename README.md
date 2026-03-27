# ReportPublish

**中文**：一个用于便捷渲染和发布 Jupyter Notebook 为网页的轻量仓库，方便在内部局域网中进行研究结果的交流、共享与查阅。
**English**: A lightweight repository for rendering and publishing Jupyter Notebooks as web pages, designed for internal LAN-based sharing, browsing, and communication of research outputs.

---

## Quick Start

```id="9ix0c2"
# 新增 weekly discussion
python scripts/scaffold_entry.py weekly 2026-03-27

# 或新增 project
python scripts/scaffold_entry.py project MyProject

# 发布静态站点
python3 scripts/publish.py

# 第一次启动长期静态服务
bash scripts/start_server.sh
```

---

## 1. 项目定位 | Project Purpose

### 中文

ReportPublish 的目标是将分散的研究型 notebook 整理成一个可持续维护的静态网页站点，降低“把 notebook 分享给别人看”的成本。
这个仓库不是用来做研究本身，而是用来做研究结果的发布层。

适用场景：

* 每周组会 notebook 沉淀
* 项目研究 notebook 沉淀
* 内部量化研究共享
* 局域网网页查阅 notebook
* 长期研究档案

### English

ReportPublish turns scattered research notebooks into a maintainable static website for easy sharing.
It is not for running research, but for publishing research outputs.

---

## 2. 当前工作流 | Workflow

核心流程：

把 notebook 放进约定目录
→ 执行发布命令
→ `_build/html` 更新
→ 网页刷新即可查看

发布命令：

```id="k13rc9"
python3 scripts/publish.py
```

长期服务命令：

```id="readme-server-start"
bash scripts/start_server.sh
```

---

## 3. 仓库结构 | Structure

```id="x6w20j"
.
├── index.md
├── myst.yml
├── projects
│   ├── MultiFeatureDL
│   │   └── index.md
│   └── overview.md
├── PUBLISHING.md
├── README.md
├── site_assets
│   └── README.md
├── site_config.yml
├── scripts
│   ├── build_and_serve.sh
│   ├── publish.py
│   ├── scaffold_entry.py
│   ├── server_status.sh
│   ├── start_server.sh
│   ├── stop_server.sh
│   └── update_toc.py
└── weekly_discussion
    ├── 2026-03-26
    │   ├── 2026-03-26_level2_dl_backtest.ipynb
    │   └── index.md
    └── overview.md
```

---

## 4. 内容组织规则 | Content Rules

Weekly Discussion：

```id="dnhqj5"
weekly_discussion/YYYY-MM-DD/
```

Projects：

```id="52is3h"
projects/<project_name>/
```

站点标题与图标：

```id="readme-site-config"
site_config.yml
site_assets/
```

---

## 5. 日常使用 | Usage

```id="l99n8n"
# 新增 weekly
python scripts/scaffold_entry.py weekly 2026-03-27

# 新增 project
python scripts/scaffold_entry.py project MyProject

# 发布
python3 scripts/publish.py

# 如需显示 notebook 代码
python3 scripts/publish.py --show-code

# 第一次启动长期服务
bash scripts/start_server.sh
```

---

## 6. 脚本说明 | Scripts

* build_and_serve.sh：一次性 build 并立即启动临时静态服务
* publish.py：统一发布入口，负责扫描内容、补最小入口页、更新导航并 build
* update_toc.py：扫描 `weekly_discussion/` 和 `projects/`，自动更新 `myst.yml`
* scaffold_entry.py：创建新的 weekly/project 目录和最小 `index.md`
* start_server.sh：长期托管 `_build/html`
* stop_server.sh：停止长期静态服务
* server_status.sh：查看长期静态服务状态

---

## 7. 构建产物

```id="mjlwmq"
_build/html/
```

这是最终网页目录。

---

## 8. 当前状态

已完成：

* 基础站点结构
* 一键发布流程
* 自动目录扫描与导航生成
* 最小入口页自动补齐
* notebook 页面接入站点导航
* 持久静态服务（局域网长期访问）
* 站点标题与图标自定义入口

---

## 9. 最终目标

```id="x1h1r7"
放内容 → 一键发布 → 刷新网页
```
