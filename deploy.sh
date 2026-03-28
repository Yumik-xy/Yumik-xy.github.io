#!/bin/bash
# 自动提交并推送博客到 GitHub

cd "$(dirname "$0")" || exit 1

if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "没有需要提交的变更"
  exit 0
fi

git add -A
git commit -m "post: $(date '+%Y-%m-%d') update"
git push origin main
