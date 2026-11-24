# Agent Skills

三个可独立安装的 Codex / Agent Skills，无额外运行时依赖。

| Skill | 用途 |
| --- | --- |
| [git-commit](skills/git-commit/SKILL.md) | 自然简洁的 Git 提交消息、原子提交及安全推送 |
| [natural-writing](skills/natural-writing/SKILL.md) | 润色文字，保留事实、术语和原意 |
| [document-writing](skills/document-writing/SKILL.md) | 基于事实与源码编写、维护和评审工程文档 |

## 安装

任选一种方式。安装前检查目标位置，不覆盖已有技能或本地修改。

### Codex 安装器

在 Codex 中输入以下指令，按需选择技能：

```text
使用 $skill-installer 从 myzxcvn/git-commit-skills 安装 skills/git-commit
使用 $skill-installer 从 myzxcvn/git-commit-skills 安装 skills/natural-writing
使用 $skill-installer 从 myzxcvn/git-commit-skills 安装 skills/document-writing
```

### 手动安装（Linux / macOS）

在尚不存在同名克隆目录的位置执行：

```bash
git clone https://github.com/myzxcvn/git-commit-skills.git
cd git-commit-skills
mkdir -p "$HOME/.agents/skills"
for skill in git-commit natural-writing document-writing; do
    target="$HOME/.agents/skills/$skill"
    if [ -e "$target" ] || [ -L "$target" ]; then
        printf 'Skip existing: %s\n' "$target"
    else
        ln -s "$PWD/skills/$skill" "$target"
    fi
done
```

只需要某个技能时，将循环列表改为对应名称。保留克隆目录供符号链接读取。
兼容旧环境时，可将上述安装目录统一替换为 `${CODEX_HOME:-$HOME/.codex}/skills`，不要重复安装。
如果技能未出现，重启 Codex。技能发现规则参见 [OpenAI 文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用

```text
使用 $git-commit 为当前暂存区生成提交消息，不执行提交。
使用 $git-commit 检查本次改动，验证后完成本地提交。
使用 $git-commit 提交本次改动，并推送到 origin 对应分支。
使用 $natural-writing 润色这段技术说明，保留原意和术语。
使用 $document-writing 基于源码编写 docs/architecture.md，不修改程序代码。
```

Git 提交不默认推送；推送需明确授权并核对范围。写作任务不自动提交或推送。
具体项目的格式、分支、构建与验证规则优先，不能扩大用户授权。

## 更新与卸载

符号链接安装：在原克隆目录执行 `git pull --ff-only`。若存在本地修改或分歧，先保留并处理，不强制覆盖。
卸载时先用 `ls -ld` 核对对应技能路径确为指向本仓库的符号链接，再用 `unlink` 移除链接，保留克隆目录。
安装器安装的是独立副本；更新时先备份已有修改，将旧副本移出技能扫描目录，再重新安装。卸载前核对实际安装位置和技能身份。必要时重启 Codex。

## 开发与验证

维护规则见 [AGENTS.md](AGENTS.md)。在仓库根目录执行：

```bash
python3 scripts/validate-skills.py
git diff --check
```

静态验证要求 Python 3.10+，仅使用标准库，检查本仓库 Skill 元数据、Markdown 围栏、本地链接和评测定义。
[GitHub Actions 工作流](.github/workflows/validate.yml) 在 push 和 PR 时执行静态检查。
这些检查不代表实际 Agent 行为正确；行为评测见 [evals/README.md](evals/README.md)，需单独构建场景并运行模型。

## 参考资料

- git-commit：[提交示例](skills/git-commit/references/examples.md)、[Git 安全指南](skills/git-commit/references/git-safety.md)
- natural-writing：[文体指南](skills/natural-writing/references/style-guide.md)、[改写示例](skills/natural-writing/references/examples.md)
- document-writing：[文档类型](skills/document-writing/references/document-types.md)、[模板](skills/document-writing/references/templates.md)、[检查清单](skills/document-writing/references/review-checklist.md)

欢迎通过 [GitHub Issues](https://github.com/myzxcvn/git-commit-skills/issues) 提供脱敏的问题描述和复现示例。

许可证：[MIT](LICENSE)。
