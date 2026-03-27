# PUBLISHING.md

# Publishing Guide

本文件说明如何使用本仓库进行 notebook 发布。

---

## 1. 核心原则

```id="7a4k35"
内容放进去 → 执行发布命令 → 网页更新
```

---

## 2. 内容位置

### Weekly

```id="57v4rm"
weekly_discussion/YYYY-MM-DD/
```

### Project

```id="nqog0a"
projects/<project_name>/
```

---

## 3. 新增内容

### Weekly

```id="a7m53l"
python scripts/scaffold_entry.py weekly 2026-03-27
```

### Project

```id="0m2l58"
python scripts/scaffold_entry.py project MyProject
```

---

## 4. 发布

```id="mhjlwm"
bash scripts/build_and_serve.sh
```

---

## 5. 输出目录

```id="lx0xsr"
_build/html/
```

---

## 6. 推荐流程

```id="brc08p"
新增 notebook
→ 放入目录
→ 执行发布命令
→ 浏览器查看
```

---

## 7. 常见问题

* notebook 路径是否正确
* myst.yml 是否被破坏
* jupyter book build 是否能成功

---

## 8. 当前未完成部分

需要补充：

```id="1ts11f"
长期静态服务（LAN访问）
```

---

## 9. 最终目标

```id="77bbt4"
放内容 → 一键发布 → 刷新网页
```
