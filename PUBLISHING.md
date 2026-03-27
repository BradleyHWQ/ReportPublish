# Publishing Workflow

内容目录约定：

- `weekly_discussion/YYYY-MM-DD/`
- `projects/<project_name>/`

内容发现规则：

- 只扫描各目录下一层的 `.md` 与 `.ipynb`
- `index.md` 缺失时会自动补最小入口页
- 空目录不会进入导航

发布命令：

```bash
python3 scripts/publish.py
```

可选静态服务：

```bash
bash scripts/build_and_serve.sh
```

自动维护文件：

- `myst.yml`
- 缺失或仍为自动生成状态的 `index.md`
- 缺失或仍为自动生成状态的 `overview.md`

手工维护文件：

- notebook
- 你自己写的 markdown
- 任何你主动改成手工维护的 `index.md`
- 任何你主动改成手工维护的 `overview.md`
