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

### 站点标题与图标

```id="site-branding-config"
site_config.yml
```

素材目录：

```id="site-branding-assets"
site_assets/
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
python3 scripts/publish.py
```

显示 notebook 代码：

```id="publish-show-code"
python3 scripts/publish.py --show-code
```

边发布边启动静态服务：

```id="publish-serve"
bash scripts/build_and_serve.sh
```

边发布边启动静态服务并显示代码：

```id="publish-serve-show-code"
PUBLISH_ARGS=--show-code bash scripts/build_and_serve.sh
```

长期静态服务：

```id="server-start"
bash scripts/start_server.sh
```

查看服务状态：

```id="server-status"
bash scripts/server_status.sh
```

停止服务：

```id="server-stop"
bash scripts/stop_server.sh
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

当前已具备最小可用发布链，长期 LAN 服务可直接指向：

```id="1ts11f"
_build/html/
```

---

## 9. 最终目标

```id="77bbt4"
放内容 → 一键发布 → 刷新网页
```
