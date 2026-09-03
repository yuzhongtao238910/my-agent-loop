---
name: commit
description: |
  根据当前的改动来生成通用规范的 commit message，但是不会执行 git 提交。
  只读取 git status / git diff / git log，产出 Conventional Commits 格式的完整提交说明，不执行 git add、git commit、git push。
  触发词：「commit message」「生成 commit」「写一下提交说明」「commit 文案」「提交信息」
  「帮我写 commit」「需要 commit message」「给我个 commit」。
  即使用户只说「帮我 commit 一下文案」「这条改动怎么写 commit」且没有要求真正提交，也应触发。
  用户明确要求执行 git commit / 提交代码时，不要用本 skill 代替提交；本 skill 只负责生成 message。
---

# 生成 Commit Message

根据当前工作区改动生成 **Conventional Commits** 格式的提交说明。只出文案，**不执行 git 提交**。

## 硬性约束

- **禁止**执行 `git add`、`git commit`、`git push`，以及任何会改写仓库状态的 git 命令（`commit --amend`、`reset`、`rebase` 等）。
- **禁止**修改 git config。
- 只允许只读命令：`git status`、`git diff`、`git diff --staged`、`git log`。
- 生成结束后把 message 交给用户，由用户自己决定是否提交。

## 工作流

并行读取（Windows 用 PowerShell 即可，不要用 bash HEREDOC）：

1. `git status` — 未跟踪 / 已暂存 / 未暂存
2. `git diff` 与 `git diff --staged` — 全部改动（不要只看 staged）
3. `git log -8 --oneline` — 对齐本仓库已有文案语言和 type 习惯

然后根据**全部相关改动**起草一条 message，在回复里原样给出，方便复制。

若没有任何改动（无 untracked、无 staged、无 unstaged），不要编造，直接说明工作区是干净的。

不要读取或把 `.env`、密钥、凭证写进 message。发现用户改了这类文件时，在 message 外单独提醒：这些文件不该进提交。

## Message 格式

```
<type>(<scope>): <subject>

<body>
```

- `type`：`feat` 新功能 · `fix` 修 bug · `refactor` 重构 · `perf` 性能 · `docs` 文档 · `style` 格式 · `test` 测试 · `chore` 构建/杂项
- `scope` 可选，短小：模块或目录名，如 `auth`、`memory`
- `subject`：一行，祈使句，聚焦 **why** 而不是文件清单；不加句号；约 50 字以内
- `body`：可选，1–2 句补充动机或影响；改动很小时可省略
- 语言跟 `git log`：仓库里中文就中文，英文就英文；log 看不出时默认中文 subject
- 不要把 `Made-with: Cursor` 或类似 trailer 写进 message，除非用户明确要求

选 type 时看改动本质：新能力用 `feat`，修缺陷用 `fix`，行为不变的整理用 `refactor`，不要一律 `chore`。

## 回复形态

先给可复制的 message 代码块，再必要时用一两句说明选这个 type 的原因。不要问「要不要我帮你提交」——本 skill 到此结束。

```
feat(memory): 在页面上展示单个 extra div 的内存构成

把原先只能在对话里看到的均摊结果写进实验页，避免必须打开画布才能理解 230B 与 0.8KB 的差别。
```
