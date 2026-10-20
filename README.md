# Git Commit Skills

用于按 `[标签] 简短摘要` 格式撰写和检查中文 Git 提交消息的 Codex 技能，
并在明确授权范围内完成本地提交和推送。

技能入口：[skills/git-commit/SKILL.md](skills/git-commit/SKILL.md)。
完整消息规则只在该文件维护；目标项目自身的 `AGENTS.md` 优先。

## 安装

选择一种安装方式即可。安装前检查是否已有名为 `git-commit` 的技能，
保留已有修改，避免重复安装或覆盖。

### 使用安装器

在 Codex 中输入：

```text
使用 $skill-installer 从 myzxcvn/git-commit-skills 仓库安装 skills/git-commit
```

### 手动安装

克隆仓库，并将技能链接到用户技能目录。以下命令适用于 Linux/macOS 的 Bash 环境，
要求已安装 Git，且克隆目录和目标技能路径均不存在：

```bash
git clone https://github.com/myzxcvn/git-commit-skills.git
cd git-commit-skills
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/git-commit" "$HOME/.agents/skills/git-commit"
```

保留克隆目录，符号链接需要通过它读取技能内容。

<details>
<summary>兼容使用 .codex/skills 的环境</summary>

如果当前 Codex 环境通过 `${CODEX_HOME:-$HOME/.codex}/skills` 管理用户技能，
在克隆仓库并进入目录后，用以下两行替代上面的目录创建和链接命令。
只选择一个安装位置：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/skills/git-commit" "${CODEX_HOME:-$HOME/.codex}/skills/git-commit"
```

</details>

若新技能没有出现，重启 Codex 后重试。
技能目录结构、符号链接支持及发现行为参见
[OpenAI 官方文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用

只生成消息，不修改 Git 状态：

```text
使用 $git-commit 为当前暂存区生成提交消息，不执行提交。
```

完成本地提交：

```text
使用 $git-commit 检查当前任务改动，完成必要验证并提交。
```

明确授权提交并推送：

```text
使用 $git-commit 提交当前任务改动，并推送到当前分支对应的 origin 分支。
```

## 更新与卸载

### 手动链接安装

更新时，进入安装时保留的仓库克隆目录，运行：

```bash
git pull --ff-only
```

符号链接会读取更新后的内容。如果存在本地修改或分支分歧，先检查并处理，
保留需要的修改。

卸载时，先检查安装路径：

```bash
ls -ld "$HOME/.agents/skills/git-commit"
```

确认它是指向本仓库的符号链接后，仅移除该链接：

```bash
test -L "$HOME/.agents/skills/git-commit" && unlink "$HOME/.agents/skills/git-commit"
```

这会保留仓库克隆目录。使用兼容路径安装时，将上述路径替换为实际安装位置。

### 安装器安装

安装器安装的是独立副本，更新其他克隆目录不会更新该副本。
以安装器输出的路径为准，先检查并保存本地修改，再将旧副本移出技能目录，
重新运行安装命令。备份应放在技能扫描目录之外。

卸载时，确认实际安装目录中的 `SKILL.md` 对应本技能，再移除该技能目录。
更新或卸载后若 Codex 仍显示旧内容，重启后重试。

## 开发与验证

修改文档或技能后，在本仓库根目录检查差异格式：

```bash
git diff --check
```

结构校验是面向维护者的可选步骤，使用技能时无需执行。
如果本机安装了 Codex 内置 `skill-creator`，且以下脚本路径存在，可运行：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/git-commit
```

该命令需要 Python 3 和 PyYAML；预期输出 `Skill is valid!`。
此检查验证技能结构和元数据，不代表已验证模型在真实仓库中的所有提交行为。
本项目不附带自动提交脚本或 Git hook，也未配置 GitHub Actions。

## 适用范围

本技能提供提交消息格式、任务范围判断、暂存核对和推送核验指引。
具体项目的分支约定、构建工具和验证要求以目标仓库的规则为准。

## 问题反馈

欢迎通过 [GitHub Issues](https://github.com/myzxcvn/git-commit-skills/issues)
反馈问题或提出改进建议。请说明使用场景、预期结果和实际结果，
并提供必要的脱敏示例。

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。
