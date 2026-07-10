# Git 提交中误添加 Co-Authored-By 行并批量移除

## 问题来源

前端 — Git 提交历史

## 现象

所有 commit message 底部都包含了 Claude 的 co-author 信息：

```
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

这些行不属于正常的代码贡献者信息，会让提交历史显得混乱，且在 GitHub 上会显示虚假的协作者。

## 根因

在每次 `git commit -m` 时，commit message 末尾拼接了 `Co-Authored-By` 行。

## 解决方案

使用 `git filter-branch` 批量移除所有提交中的该行：

```bash
# 1. 确保工作区干净
git status

# 2. 使用 msg-filter 过滤掉 Co-Authored-By 行
FILTER_BRANCH_SQUELCH_WARNING=1 \
  git filter-branch -f \
  --msg-filter 'sed "/^Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>$/d"' \
  -- --all

# 3. 验证是否清理干净
git log --grep="Co-Authored-By" --oneline
# 应无输出

# 4. 强制推送到远程
git push --force origin main
```

## 关键知识点

- `git filter-branch --msg-filter` 可以批量修改所有 commit 的 message
- `sed "/^pattern$/d"` 删除匹配的整行
- 重写 Git 历史后，必须 `git push --force` 才能同步到远程
- **force push 是危险操作**，会覆盖远程历史，团队协作时需提前通知所有成员
- 如果仓库有多个分支，`-- --all` 会处理所有分支

## 日期

2026-07-10
