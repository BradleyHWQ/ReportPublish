# ReportPublish

**中文**：一个用于便捷渲染和发布 Jupyter Notebook 为网页的轻量仓库，方便在内部局域网中进行研究结果的交流、共享与查阅。  
**English**: A lightweight repository for rendering and publishing Jupyter Notebooks as web pages, designed for internal LAN-based sharing, browsing, and communication of research outputs.

---

## Quick Start

```bash
# 新增 weekly discussion
python scripts/scaffold_entry.py weekly 2026-03-27

# 或新增 project
python scripts/scaffold_entry.py project MyProject

# 一键发布
bash scripts/build_and_serve.sh
```

1. 项目定位 | Project Purpose
中文

ReportPublish 的目标是将分散的研究型 notebook（如 weekly discussion、项目分析、阶段性研究结论）整理成一个可持续维护的静态网页站点，降低“把 notebook 分享给别人看”的成本。

这个仓库不是用来做研究本身，而是用来做研究结果的发布层（publishing layer）。

它适合以下场景：

每周组会 notebook 沉淀
项目研究 notebook 沉淀
量化研究内部共享
局域网内网页化查阅 notebook 内容
作为长期研究档案 / 报告库
English

ReportPublish is designed to turn scattered research notebooks (e.g. weekly discussions, project analyses, intermediate research outputs) into a maintainable static website, making it much easier to share notebooks with others.

This repository is not for research execution itself.
It is the publishing layer for research outputs.

Typical use cases include:

Weekly discussion notebook archiving
Project research notebook publishing
Internal quant research sharing
LAN-based web browsing of notebook content
Long-term research archive / report library
2. 当前工作流 | Current Workflow
中文

当前工作流的核心目标是：

把 notebook 放进约定目录 → 一键发布为网页

当前的一键发布命令为：

bash scripts/build_and_serve.sh

它负责完成站点构建相关流程（包括更新站点内容和构建静态网页）。

English

The current workflow is designed around the following principle:

Put notebooks into the agreed folder structure → publish with one command

Current one-command publishing entry:

bash scripts/build_and_serve.sh

This handles the site build workflow (including updating site content and building the static website).

3. 仓库结构 | Repository Structure
.
├── index.md
├── myst.yml
├── projects
│   ├── MultiFeatureDL
│   │   └── index.md
│   └── overview.md
├── PUBLISHING.md
├── README.md
├── scripts
│   ├── build_and_serve.sh
│   ├── publish.py
│   ├── scaffold_entry.py
│   └── update_toc.py
└── weekly_discussion
    ├── 2026-03-26
    │   ├── 2026-03-26_level2_dl_backtest.ipynb
    │   └── index.md
    └── overview.md
4. 内容组织规则 | Content Organization Rules
4.1 Weekly Discussion
中文

每周组会 / 阶段性讨论内容放在：

weekly_discussion/YYYY-MM-DD/

例如：

weekly_discussion/2026-03-26/

该目录下通常包含：

一个或多个 notebook
一个极简 index.md

推荐示例：

weekly_discussion/2026-03-26/
├── 2026-03-26_level2_dl_backtest.ipynb
└── index.md
English

Weekly discussions / periodic discussion materials should be placed under:

weekly_discussion/YYYY-MM-DD/

Example:

weekly_discussion/2026-03-26/

Typical contents:

one or more notebooks
a minimal index.md

Recommended example:

weekly_discussion/2026-03-26/
├── 2026-03-26_level2_dl_backtest.ipynb
└── index.md
4.2 Projects
中文

长期项目相关 notebook 放在：

projects/<project_name>/

例如：

projects/MultiFeatureDL/

该目录下通常包含：

项目相关 notebook
一个极简 index.md

推荐示例：

projects/MultiFeatureDL/
└── index.md
English

Long-term project notebooks should be placed under:

projects/<project_name>/

Example:

projects/MultiFeatureDL/

Typical contents:

project-related notebooks
a minimal index.md

Recommended example:

projects/MultiFeatureDL/
└── index.md
5. 日常使用方式 | Daily Usage
5.1 新增一个 weekly discussion
方式 A：手动创建目录
mkdir -p weekly_discussion/2026-03-27

然后将 notebook 放进去，例如：

weekly_discussion/2026-03-27/my_notebook.ipynb
方式 B：使用脚手架脚本（推荐）
python scripts/scaffold_entry.py weekly 2026-03-27
5.2 新增一个 project
方式 A：手动创建目录
mkdir -p projects/MyProject
方式 B：使用脚手架脚本（推荐）
python scripts/scaffold_entry.py project MyProject
5.3 发布更新后的站点
bash scripts/build_and_serve.sh

执行后，站点会重新构建，最新内容将被写入静态网页输出目录。

5.4 日常推荐流程
创建或整理 notebook
-> 放入 weekly_discussion/ 或 projects/ 对应目录
-> 执行 bash scripts/build_and_serve.sh
-> 网页端查看更新后的结果
6. 自动化脚本说明 | Script Responsibilities
中文
scripts/build_and_serve.sh

统一发布入口。
负责执行构建相关流程，是当前主要的一键发布命令。

scripts/publish.py

站点发布主逻辑脚本。
通常负责串联：

内容扫描
导航更新
构建流程
scripts/update_toc.py

自动更新站点导航（myst.yml 中的 toc 结构）。

scripts/scaffold_entry.py

用于快速创建新的：

weekly discussion 目录
project 目录

并生成最小模板文件。

English
scripts/build_and_serve.sh

Unified publishing entry.
This is the current main one-command publishing script.

scripts/publish.py

Main publishing workflow script.
Typically responsible for:

content discovery
navigation updates
build workflow
scripts/update_toc.py

Automatically updates the site navigation (toc inside myst.yml).

scripts/scaffold_entry.py

Used to quickly scaffold:

new weekly discussion entries
new project entries

with minimal template files.

7. 哪些文件应该手改，哪些文件尽量别手改 | What to Edit vs. What to Avoid Editing
建议手工维护的文件
notebook 本体
各目录下的 index.md
顶层 index.md
projects/overview.md
weekly_discussion/overview.md
尽量不要频繁手工维护的文件
myst.yml
脚本目录下自动化逻辑相关文件

原因：
这些内容已经逐步被自动化脚本接管，未来应尽量减少手工修改。

8. 构建产物 | Build Output

Jupyter Book 构建后的静态网页通常输出到：

_build/html/

这是未来局域网长期静态服务应直接托管的目录。

9. 当前状态 | Current Status
已完成 | Implemented
基础 Jupyter Book 仓库结构
Weekly discussion / project 双区块内容组织
一键发布主链初步完成
自动化脚手架与 toc 更新脚本已接入
待补充 | TODO
持久化静态服务（LAN 内长期可访问）
刷新式访问工作流完全闭环
可选的首页 / 样式优化
可选的自动化部署增强
10. 未来目标 | Future Goal

理想状态下，本仓库的最终工作流应收敛为：

把 notebook 放进约定目录
-> 执行一次发布命令
-> 浏览器刷新即可看到更新后的网页内容

也就是说，研究 notebook 的网页化发布应成为一个低摩擦、低心智负担的过程。

11. 补充说明 | Notes

如果你未来想进一步扩展这个仓库，建议优先沿着下面方向演进：

持久化静态服务（局域网常驻）
自动发现新 notebook 并自动纳入导航
更统一的首页展示
更轻量的内部共享体验