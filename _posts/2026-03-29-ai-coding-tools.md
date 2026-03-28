---
title: AI 编码工具合集
date: 2026-03-29
categories:
  - AI
tags:
  - AI
  - 工具
  - Claude Code
---

> 本文完全由 AI 生成，持续更新中。记录我在 AI 辅助编码过程中觉得好用的工具和框架。

## 工具总览

| 工具                    | 类型    | 介绍                         |
| --------------------- | ----- | -------------------------- |
| [OpenSpec](#openspec) | 规格管理  | 写代码前先签"合同"，Markdown 规格驱动开发 |
| [GSD](#gsd)           | 工作流框架 | 子代理架构，从规划到执行到验证全包          |

---

## OpenSpec

[GitHub](https://github.com/Fission-AI/OpenSpec) \| 规格驱动开发框架，支持 Claude Code、Cursor、Copilot 等 21+ AI 工具

用 Markdown 写需求规格，AI 按文档干活，你按文档验收。流程三步：`Propose → Apply → Archive`。用 Delta 标记（`ADDED` / `MODIFIED` / `REMOVED`）追踪变更。

**推荐命令**

| 命令 | 用途 |
|------|------|
| `openspec init` | 初始化项目 |
| `/opsx:new <name>` | 创建新的变更提案 |
| `/opsx:ff` | 一键生成所有规划文档 |
| `/opsx:apply` | 按规格执行实现 |
| `/opsx:archive` | 归档完成的变更，合并到主规格 |

- **优点**：纯 Markdown 不锁定工具、不需要 API Key 完全本地、Delta 标记对改已有代码友好
- **缺点**：只管规格不管执行、生态较新社区资源少
- **适合**：多工具混用、团队协作统一规格、在已有代码库上迭代

---

## GSD

[GitHub](https://github.com/gsd-build/get-shit-done) \| Claude Code 工作流框架 \| 35k+ stars

把大项目拆成小任务，每个任务派全新子代理执行，解决长对话的"上下文腐烂"问题。核心流程：`new-project → plan-phase → execute-phase`。

**推荐命令**

| 命令 | 用途 |
|------|------|
| `/gsd:new-project` | 初始化项目，生成规格和路线图 |
| `/gsd:plan-phase N` | 规划第 N 阶段 |
| `/gsd:execute-phase N` | 执行第 N 阶段 |
| `/gsd:autonomous` | 全自动端到端，全部阶段一口气跑完 |
| `/gsd:fast` | 小任务快速执行，跳过规划开销 |
| `/gsd:debug` | 系统化调试，状态跨会话持久 |
| `/gsd:resume-work` | 恢复上次中断的工作 |
| `/gsd:do` | 说人话，自动匹配对应命令 |

- **优点**：规划/执行/验证全包、每任务独立上下文不会质量退化、原子 git commit 可回滚、可配模型组合平衡成本
- **缺点**：重度绑定 Claude Code、60+ 命令上手成本高、中间文件多
- **适合**：个人开发主力 Claude Code、大型多阶段项目、需要自动化规划验证
