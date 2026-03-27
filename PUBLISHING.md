# PUBLISHING.md

本文件用于说明 `ReportPublish` 仓库的实际发布流程。  
This document describes the practical publishing workflow for the `ReportPublish` repository.

---

# 1. 核心原则 | Core Principle

本仓库的发布流程遵循一个简单原则：

> **内容放进去，发布命令跑一次，网页更新即可查看。**

The publishing workflow follows one simple principle:

> **Put content in the right folder, run the publish command once, and the website updates.**

---

# 2. 内容应该放在哪里 | Where Content Should Go

## 2.1 Weekly Discussion

每周讨论内容应放在：

```text
weekly_discussion/YYYY-MM-DD/

例如：

weekly_discussion/2026-03-27/

推荐内容：

.ipynb notebook
index.md（可极简）

推荐结构：

weekly_discussion/2026-03-27/
├── my_notebook.ipynb
└── index.md
2.2 Projects

项目类内容应放在：

projects/<project_name>/

例如：

projects/MyProject/

推荐内容：

.ipynb notebook
index.md（可极简）

推荐结构：

projects/MyProject/
├── analysis.ipynb
└── index.md
3. 如何新增内容 | How to Add New Content
3.1 新增 weekly discussion
方式 A：手动
mkdir -p weekly_discussion/2026-03-27

然后把 notebook 放进去。

方式 B：使用脚手架（推荐）
python scripts/scaffold_entry.py weekly 2026-03-27
3.2 新增 project
方式 A：手动
mkdir -p projects/MyProject

然后把 notebook 放进去。

方式 B：使用脚手架（推荐）
python scripts/scaffold_entry.py project MyProject
4. 如何发布 | How to Publish

当前统一发布命令：

bash scripts/build_and_serve.sh

这个命令通常负责：

扫描内容目录
更新 myst.yml 导航
构建 Jupyter Book 站点
生成最新的静态网页
5. 发布后结果在哪里 | Where the Output Goes

构建完成后的静态网页通常位于：

_build/html/

这就是最终网页内容所在目录。

6. 当前推荐工作流 | Recommended Workflow
最常见流程
新增或更新 notebook
-> 放到 weekly_discussion/ 或 projects/ 对应目录
-> 执行 bash scripts/build_and_serve.sh
-> 查看生成结果
7. 失败时先检查什么 | What to Check If Publishing Fails

如果发布失败，优先检查：

7.1 notebook 路径是否正确

确认 notebook 是否放在正确目录：

weekly_discussion/YYYY-MM-DD/
projects/<project_name>/
7.2 notebook 文件名或内容是否异常

例如：

文件损坏
notebook metadata 异常
内容为空或格式有问题
7.3 myst.yml 是否被手工改坏

如果站点 build 报错，优先检查：

myst.yml
scripts/update_toc.py
最近新增目录是否结构异常
7.4 Jupyter Book 是否能正常 build

可单独测试：

jupyter book build .

如果这一步都失败，说明问题不在服务，而在站点构建本身。

8. 当前尚未完全闭环的部分 | Current Missing Piece

目前仓库已经接近“一键发布”，但还有最后一个待补环节：

长期静态服务（LAN persistent serving）

理想状态应为：

内容更新
-> 一键发布
-> 网页端刷新即可看到新内容

当前 _build/html/ 已经是静态网页输出目录，后续只需要为它增加一个长期运行的静态服务即可完全闭环。

9. 最终目标 | Final Goal

本仓库最终目标不是“做一个复杂系统”，而是：

把 notebook 发布这件事压缩成一个低成本、低心智负担的日常动作。

也就是说，未来你应该尽量只做两件事：

把内容放对位置
执行一次发布命令