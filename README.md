<p align="center">
  <h1 align="center">🧠 AgentRecall</h1>
  <p align="center">
    <strong>轻量级 AI 编码代理持久化记忆引擎 CLI 工具</strong><br/>
    <em>Lightweight AI Coding Agent Persistent Memory Engine CLI</em>
  </p>
  <p align="center">
    <a href="#简体中文">简体中文</a> ·
    <a href="#繁體中文">繁體中文</a> ·
    <a href="#english">English</a>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/version-v1.0.0-blue" alt="Version"/>
    <img src="https://img.shields.io/badge/python-3.8+-green" alt="Python"/>
    <img src="https://img.shields.io/badge/license-MIT-orange" alt="License"/>
    <img src="https://img.shields.io/badge/dependencies-zero-red" alt="Zero Dependencies"/>
  </p>
</p>

---

## 📑 目录导航 | Table of Contents

- **[简体中文](#简体中文)**
- **[繁體中文](#繁體中文)**
- **[English](#english)**

---

<a id="简体中文"></a>

# 🇨🇳 简体中文

## 🎉 项目介绍

**AgentRecall** 是一款专为 AI 编码代理设计的**轻量级持久化记忆引擎**。它为 Claude Code、Cursor、GitHub Copilot 等 AI 编码助手提供了**长期记忆能力**，让 AI 在跨会话、跨项目中保持对关键决策、架构选择和编码经验的记忆。

### 为什么需要 AgentRecall？

AI 编码代理虽然强大，但每次新会话都从"零记忆"开始。开发者需要反复向 AI 解释项目背景、技术选型原因和之前的 bug 修复方案。**AgentRecall** 解决了这个问题：

- 🧠 **持久化记忆** — AI 的决策和经验不再随会话消失
- 🔍 **智能检索** — 四种搜索模式快速找到历史记忆
- 🤖 **多代理支持** — 一个记忆库服务多个 AI 编码代理
- 📦 **零外部依赖** — 纯 Python 标准库实现，即装即用

### 技术栈

| 技术 | 说明 |
|------|------|
| **Python 3.8+** | 核心运行环境 |
| **SQLite** | 嵌入式数据库，无需额外安装 |
| **TF-IDF** | 基于词频-逆文档频率的智能搜索 |
| **ANSI TUI** | 彩色终端用户界面 |

---

## ✨ 核心特性

### 1. 💾 持久化记忆存储
基于 **SQLite** 后端的可靠存储方案，支持多 Agent 数据隔离。所有记忆按 Agent ID 分区存储，互不干扰。

### 2. 🔍 智能混合搜索
提供 **四种搜索模式**，满足不同场景需求：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `hybrid` | **混合搜索**（默认） | 综合效果最佳 |
| `fulltext` | 全文搜索 | 精确短语匹配 |
| `keyword` | 关键词搜索 | 标签/标题快速定位 |
| `tfidf` | TF-IDF 语义搜索 | 语义相似内容查找 |

### 3. 🗜️ 智能记忆压缩
自动压缩冗余内容，**保留代码块和关键信息**，去除重复表述。支持手动触发和保存时自动压缩。

### 4. 🔄 会话管理
追踪编码会话的完整生命周期：开始 → 进行中 → 结束。将记忆关联到具体会话，方便回溯。

### 5. 📋 上下文注入
自动为 Agent 生成结构化上下文，支持 **Token 预算控制**，确保注入的上下文不超过 Agent 的上下文窗口限制。

### 6. 🤖 多 Agent 支持
原生支持 **Claude Code**、**Cursor**、**GitHub Copilot** 等主流 AI 编码代理，每个 Agent 拥有独立的记忆空间。

### 7. 📊 TUI 仪表盘
精美的**彩色终端界面**，提供记忆浏览、搜索结果展示和统计概览功能。

### 8. 📤 导入导出
支持 **JSON** 和 **Markdown** 两种格式导出，方便跨设备迁移和知识分享。

### 9. 🏷️ 关键词提取
基于 **TF（词频）算法**自动从记忆内容中提取关键词，增强搜索能力。

### 10. 💡 相关记忆推荐
基于语义相似度的智能推荐，帮助发现历史记忆中的关联知识。

---

## 🚀 快速开始

### 环境要求

- **Python 3.8** 或更高版本
- **pip** 包管理器
- 无需任何外部依赖！

### 安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/gitstq/AgentRecall.git
```

> 💡 **提示**：如果网络较慢，可以尝试使用国内镜像：
> ```bash
> pip install git+https://github.com/gitstq/AgentRecall.git -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 验证安装

```bash
recall --version
# 输出: AgentRecall v1.0.0
```

### 基本使用（5 分钟上手）

**第一步：保存一条记忆**

```bash
recall save \
  --title "使用 JWT 进行 API 认证" \
  --content "项目决定使用 JWT Token 进行 API 认证，Access Token 有效期 2 小时，Refresh Token 有效期 7 天。Token 存储在 httpOnly Cookie 中。" \
  --category decision \
  --tags auth,jwt,security \
  --importance 0.9
```

**第二步：搜索记忆**

```bash
recall search "JWT 认证" --mode hybrid --limit 10
```

**第三步：查看记忆详情**

```bash
recall show 1
```

**第四步：查看仪表盘**

```bash
recall dashboard
```

**第五步：生成 Agent 上下文**

```bash
recall context --agent claude-code --max-tokens 4000
```

---

## 📖 详细使用指南

### 记忆分类体系

AgentRecall 内置 **9 种记忆分类**，覆盖编码工作的方方面面：

| 分类 | 说明 | 示例 |
|------|------|------|
| `decision` | 🎯 技术决策 | "选择 PostgreSQL 作为主数据库" |
| `bug` | 🐛 Bug 记录 | "N+1 查询导致接口超时" |
| `feature` | ✨ 功能设计 | "用户权限系统采用 RBAC 模型" |
| `context` | 📝 项目上下文 | "项目使用 monorepo 架构管理" |
| `architecture` | 🏗️ 架构设计 | "微服务间使用 gRPC 通信" |
| `lesson` | 📚 经验教训 | "不要在循环中执行数据库查询" |
| `config` | ⚙️ 配置记录 | "Redis 连接池大小设为 20" |
| `workflow` | 🔧 工作流 | "PR 合并前必须通过 CI 检查" |
| `general` | 📌 通用记忆 | "团队每周三进行代码评审" |

### 完整命令参考

#### 💾 `recall save` — 保存记忆

```bash
# 基本用法
recall save --title "标题" --content "内容"

# 完整参数
recall save \
  --title "标题" \
  --content "记忆内容" \
  --category decision \
  --tags tag1,tag2,tag3 \
  --importance 0.8 \
  --agent claude-code \
  --session sess_001
```

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--title` | `-t` | 记忆标题（**必填**） | — |
| `--content` | `-c` | 记忆内容（**必填**） | — |
| `--category` | `-k` | 记忆分类 | `general` |
| `--tags` | — | 逗号分隔的标签 | — |
| `--importance` | `-i` | 重要度评分 (0.0-1.0) | `0.5` |
| `--agent` | `-a` | Agent ID | `default` |
| `--session` | `-s` | 关联会话 ID | — |

#### 🔍 `recall search` — 搜索记忆

```bash
# 混合搜索（默认）
recall search "认证方案" --mode hybrid --limit 20

# 全文搜索
recall search "JWT Token" --mode fulltext

# 关键词搜索
recall search "数据库" --mode keyword

# TF-IDF 语义搜索
recall search "性能优化" --mode tfidf

# 带过滤条件
recall search "bug" --category bug --min-importance 0.5 --agent cursor

# JSON 输出（方便脚本处理）
recall search "API" --json
```

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `query` | — | 搜索关键词（**必填**） | — |
| `--mode` | `-m` | 搜索模式 | `hybrid` |
| `--category` | `-k` | 按分类过滤 | — |
| `--limit` | `-l` | 最大结果数 | `20` |
| `--agent` | `-a` | Agent ID | `default` |
| `--min-importance` | — | 最低重要度 | `0.0` |
| `--json` | — | JSON 格式输出 | `false` |

#### 👁️ `recall show` — 查看详情

```bash
recall show 42
```

#### 📋 `recall list` — 列出记忆

```bash
# 列出最近记忆
recall list --limit 20

# 按分类过滤
recall list --category decision --limit 10

# 指定 Agent
recall list --agent claude-code

# JSON 输出
recall list --json
```

#### 🗑️ `recall delete` — 删除记忆

```bash
# 交互式确认删除
recall delete 42

# 强制删除（跳过确认）
recall delete 42 --force
```

#### ✏️ `recall update` — 更新记忆

```bash
# 更新标题和内容
recall update 42 --title "新标题" --content "新内容"

# 更新分类和重要度
recall update 42 --category architecture --importance 0.9

# 更新标签
recall update 42 --tags new-tag1,new-tag2
```

#### 📊 `recall dashboard` — TUI 仪表盘

```bash
# 默认 Agent 仪表盘
recall dashboard

# 指定 Agent
recall dashboard --agent cursor
```

#### 📋 `recall context` — 生成上下文

```bash
# 生成上下文（默认 4000 tokens）
recall context --agent claude-code

# 自定义 Token 预算
recall context --agent cursor --max-tokens 2000

# 指定分类
recall context --agent copilot --categories decision,architecture

# 输出到文件
recall context --agent claude-code --output context.md
```

#### 🔄 `recall session` — 会话管理

```bash
# 开始新会话
recall session start --agent claude-code --description "重构认证模块"

# 结束当前会话
recall session end --summary "完成 JWT 认证重构，新增 Refresh Token 机制"

# 查看会话历史
recall session history --agent claude-code --limit 10
```

#### 📤 `recall export` — 导出记忆

```bash
# 导出为 JSON
recall export --format json --output memories.json

# 导出为 Markdown
recall export --format markdown --output memories.md

# 导出指定 Agent 的记忆
recall export --agent cursor --format json --output cursor-memories.json
```

#### 📥 `recall import` — 导入记忆

```bash
recall import memories.json --agent claude-code
```

#### 📈 `recall stats` — 统计信息

```bash
# 查看统计
recall stats

# 指定 Agent
recall stats --agent claude-code

# JSON 输出
recall stats --json
```

#### 🤖 `recall agents` — 列出 Agent

```bash
recall agents
```

#### 📂 `recall categories` — 列出分类

```bash
recall categories --agent claude-code
```

#### 🧹 `recall cleanup` — 清理记忆

```bash
# 清理 90 天前的低重要度记忆
recall cleanup --max-age-days 90 --min-importance 0.3

# 预览模式（不实际删除）
recall cleanup --max-age-days 90 --min-importance 0.3 --dry-run

# 指定 Agent
recall cleanup --agent cursor --max-age-days 60
```

#### 🗜️ `recall compress` — 压缩记忆

```bash
# 预览压缩效果
recall compress 42

# 应用压缩
recall compress 42 --apply
```

#### 💡 `recall suggest` — 相关记忆推荐

```bash
# 推荐相关记忆（默认 5 条）
recall suggest 42

# 自定义推荐数量
recall suggest 42 --limit 10
```

### 典型使用场景

#### 场景一：项目技术决策记录

```bash
# 记录数据库选型决策
recall save \
  -t "数据库选型：PostgreSQL vs MySQL" \
  -c "经过团队讨论，最终选择 PostgreSQL。原因：1) 对 JSON 数据类型支持更好；2) 扩展性更强；3) 团队更熟悉。" \
  -k decision \
  --tags database,postgresql,architecture \
  -i 0.9 \
  -a claude-code

# 记录缓存方案
recall save \
  -t "缓存方案：Redis + 本地缓存" \
  -c "采用两级缓存策略：L1 使用 Python functools.lru_cache 做本地缓存，TTL 5分钟；L2 使用 Redis 做分布式缓存，TTL 30分钟。缓存击穿时使用互斥锁防止雪崩。" \
  -k architecture \
  --tags cache,redis,performance \
  -i 0.85
```

#### 场景二：Bug 修复经验沉淀

```bash
# 记录 Bug 及修复方案
recall save \
  -t "N+1 查询导致列表接口超时" \
  -c "问题：用户列表接口在数据量超过 1000 时响应时间超过 5 秒。原因：循环中执行了 N 次数据库查询获取关联数据。修复：使用 SQLAlchemy 的 joinedload 预加载关联数据，响应时间降至 200ms。" \
  -k bug \
  --tags performance,sqlalchemy,optimization \
  -i 0.8

# 记录经验教训
recall save \
  -t "避免在循环中执行数据库查询" \
  -c "经验教训：在处理列表数据时，务必使用批量查询或预加载（eager loading）来获取关联数据。可以使用 Django 的 select_related/prefetch_related 或 SQLAlchemy 的 joinedload/subqueryload。" \
  -k lesson \
  --tags best-practice,performance,database \
  -i 0.95
```

#### 场景三：为 AI Agent 注入上下文

```bash
# 开始新的编码会话
recall session start --agent claude-code -d "开发用户权限模块"

# 保存编码过程中的关键决策
recall save -t "RBAC 权限模型设计" -c "采用基于角色的访问控制（RBAC）模型。用户 -> 角色 -> 权限，支持多角色绑定。权限粒度到 API 端点级别。" -k architecture -a claude-code

# 为新会话生成上下文
recall context --agent claude-code --max-tokens 4000 --output .claude-context.md

# 结束会话
recall session end -s "完成 RBAC 权限模块开发，包含用户、角色、权限 CRUD 接口"
```

#### 场景四：跨设备迁移记忆

```bash
# 在设备 A 上导出
recall export --format json --output my-memories.json

# 在设备 B 上导入
recall import my-memories.json --agent claude-code
```

---

## 💡 设计思路与迭代规划

### 设计哲学

1. **轻量优先** — 零外部依赖，纯 Python 标准库实现，安装即用
2. **CLI 原生** — 命令行界面，方便与各种 AI Agent 工作流集成
3. **存储可靠** — SQLite 后端，数据安全有保障
4. **搜索智能** — 多模式混合搜索，兼顾精确性和语义理解
5. **Agent 无关** — 不绑定特定 AI Agent，支持所有主流编码代理

### 架构概览

```
┌─────────────────────────────────────────────────┐
│                   CLI 层 (cli.py)                │
│  save / search / show / list / delete / update   │
├─────────────────────────────────────────────────┤
│              业务逻辑层                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ 搜索引擎  │ │ 压缩引擎  │ │  会话管理器      │ │
│  │(search)  │ │(compress) │ │  (session)       │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
├─────────────────────────────────────────────────┤
│              存储层 (store.py)                    │
│  ┌────────────────────────────────────────────┐  │
│  │              SQLite 数据库                  │  │
│  │  memories | memory_fts | sessions | agents │  │
│  └────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────┤
│              展示层 (tui.py)                      │
│  ANSI 彩色输出 | 仪表盘 | 搜索结果高亮          │
└─────────────────────────────────────────────────┘
```

### 迭代规划

#### v1.x — 稳定化（当前阶段）
- [x] 核心记忆 CRUD 操作
- [x] 四种搜索模式
- [x] 记忆压缩
- [x] 会话管理
- [x] TUI 仪表盘
- [x] 导入导出
- [x] 多 Agent 支持

#### v2.0 — 智能化（规划中）
- [ ] **向量搜索** — 集成 sentence-transformers 实现语义向量搜索
- [ ] **自动记忆提取** — 从 Git Commit 和代码变更中自动提取记忆
- [ ] **Web UI** — 提供浏览器端管理界面
- [ ] **插件系统** — 支持自定义搜索和压缩策略
- [ ] **云端同步** — 支持多设备记忆同步

#### v3.0 — 生态化（远期愿景）
- [ ] **Agent Marketplace** — 分享记忆模板和最佳实践
- [ ] **团队协作** — 多人共享记忆库
- [ ] **IDE 插件** — VS Code / JetBrains 原生集成
- [ ] **API 服务** — 提供 REST/GraphQL 接口

---

## 📦 打包与部署指南

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# 安装（开发模式）
pip install -e .

# 或直接安装
pip install .
```

### 构建发布包

```bash
# 安装构建工具
pip install build

# 构建 sdist 和 wheel
python -m build

# 构建产物位于 dist/ 目录
ls dist/
# agentrecall-1.0.0.tar.gz
# agentrecall-1.0.0-py3-none-any.whl
```

### 安装构建产物

```bash
# 从 wheel 安装
pip install dist/agentrecall-1.0.0-py3-none-any.whl

# 从 sdist 安装
pip install dist/agentrecall-1.0.0.tar.gz
```

### 数据存储位置

AgentRecall 默认将数据存储在用户主目录下：

```
~/.agentrecall/
└── memories.db    # SQLite 数据库文件
```

可通过环境变量自定义存储路径（规划中）。

### 卸载

```bash
pip uninstall agentrecall

# 如需删除数据
rm -rf ~/.agentrecall/
```

---

## 🤝 贡献指南

我们欢迎并感谢所有形式的贡献！无论是提交 Bug 报告、改进文档还是提交代码。

### 贡献流程

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m 'feat: add your feature'`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 **Pull Request**

### 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式检查
# （项目遵循 PEP 8 规范）
```

### 提交规范

请遵循 **Conventional Commits** 规范：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `refactor` | 代码重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具链更新 |

示例：
```bash
git commit -m "feat: add vector search support"
git commit -m "fix: resolve FTS5 fallback on older SQLite"
git commit -m "docs: update README with new commands"
```

### 报告 Bug

请在 [GitHub Issues](https://github.com/gitstq/AgentRecall/issues) 提交 Bug 报告，包含以下信息：

- **环境信息**：操作系统、Python 版本
- **复现步骤**：详细的操作步骤
- **期望行为**：你期望发生什么
- **实际行为**：实际发生了什么
- **错误日志**：完整的错误输出

---

## 📄 开源协议

本项目基于 **[MIT License](https://opensource.org/licenses/MIT)** 开源。

```
MIT License

Copyright (c) 2024 AgentRecall Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <a href="#简体中文">⬆️ 返回顶部</a> ·
  <a href="#繁體中文">繁體中文</a> ·
  <a href="#english">English</a>
</p>

---

<a id="繁體中文"></a>

# 🇹🇼 繁體中文

## 🎉 專案介紹

**AgentRecall** 是一款專為 AI 編碼代理設計的**輕量級持久化記憶引擎**。它為 Claude Code、Cursor、GitHub Copilot 等 AI 編碼助手提供了**長期記憶能力**，讓 AI 在跨會話、跨專案中保持對關鍵決策、架構選擇和編碼經驗的記憶。

### 為什麼需要 AgentRecall？

AI 編碼代理雖然強大，但每次新會話都從「零記憶」開始。開發者需要反覆向 AI 解釋專案背景、技術選型原因和之前的 Bug 修復方案。**AgentRecall** 解決了這個問題：

- 🧠 **持久化記憶** — AI 的決策和經驗不再隨會話消失
- 🔍 **智慧檢索** — 四種搜尋模式快速找到歷史記憶
- 🤖 **多代理支援** — 一個記憶庫服務多個 AI 編碼代理
- 📦 **零外部依賴** — 純 Python 標準函式庫實作，即裝即用

### 技術棧

| 技術 | 說明 |
|------|------|
| **Python 3.8+** | 核心執行環境 |
| **SQLite** | 嵌入式資料庫，無需額外安裝 |
| **TF-IDF** | 基於詞頻-逆文件頻率的智慧搜尋 |
| **ANSI TUI** | 彩色終端使用者介面 |

---

## ✨ 核心特性

### 1. 💾 持久化記憶儲存
基於 **SQLite** 後端的可靠儲存方案，支援多 Agent 資料隔離。所有記憶按 Agent ID 分區儲存，互不干擾。

### 2. 🔍 智慧混合搜尋
提供 **四種搜尋模式**，滿足不同場景需求：

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| `hybrid` | **混合搜尋**（預設） | 綜合效果最佳 |
| `fulltext` | 全文搜尋 | 精確片語匹配 |
| `keyword` | 關鍵字搜尋 | 標籤/標題快速定位 |
| `tfidf` | TF-IDF 語義搜尋 | 語義相似內容查找 |

### 3. 🗜️ 智慧記憶壓縮
自動壓縮冗餘內容，**保留程式碼區塊和關鍵資訊**，去除重複表述。支援手動觸發和儲存時自動壓縮。

### 4. 🔄 會話管理
追蹤編碼會話的完整生命週期：開始 → 進行中 → 結束。將記憶關聯到具體會話，方便回溯。

### 5. 📋 上下文注入
自動為 Agent 生成結構化上下文，支援 **Token 預算控制**，確保注入的上下文不超過 Agent 的上下文視窗限制。

### 6. 🤖 多 Agent 支援
原生支援 **Claude Code**、**Cursor**、**GitHub Copilot** 等主流 AI 編碼代理，每個 Agent 擁有獨立的記憶空間。

### 7. 📊 TUI 儀表板
精美的**彩色終端介面**，提供記憶瀏覽、搜尋結果展示和統計概覽功能。

### 8. 📤 匯入匯出
支援 **JSON** 和 **Markdown** 兩種格式匯出，方便跨裝置遷移和知識分享。

### 9. 🏷️ 關鍵字提取
基於 **TF（詞頻）演算法**自動從記憶內容中提取關鍵字，增強搜尋能力。

### 10. 💡 相關記憶推薦
基於語義相似度的智慧推薦，幫助發現歷史記憶中的關聯知識。

---

## 🚀 快速開始

### 環境需求

- **Python 3.8** 或更高版本
- **pip** 套件管理器
- 無需任何外部依賴！

### 安裝

```bash
# 從 GitHub 安裝
pip install git+https://github.com/gitstq/AgentRecall.git
```

> 💡 **提示**：如果網路較慢，可以嘗試使用鏡像源：
> ```bash
> pip install git+https://github.com/gitstq/AgentRecall.git -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 驗證安裝

```bash
recall --version
# 輸出: AgentRecall v1.0.0
```

### 基本使用（5 分鐘上手）

**第一步：儲存一條記憶**

```bash
recall save \
  --title "使用 JWT 進行 API 認證" \
  --content "專案決定使用 JWT Token 進行 API 認證，Access Token 有效期 2 小時，Refresh Token 有效期 7 天。Token 儲存在 httpOnly Cookie 中。" \
  --category decision \
  --tags auth,jwt,security \
  --importance 0.9
```

**第二步：搜尋記憶**

```bash
recall search "JWT 認證" --mode hybrid --limit 10
```

**第三步：查看記憶詳情**

```bash
recall show 1
```

**第四步：查看儀表板**

```bash
recall dashboard
```

**第五步：生成 Agent 上下文**

```bash
recall context --agent claude-code --max-tokens 4000
```

---

## 📖 詳細使用指南

### 記憶分類體系

AgentRecall 內建 **9 種記憶分類**，涵蓋編碼工作的各個方面：

| 分類 | 說明 | 範例 |
|------|------|------|
| `decision` | 🎯 技術決策 | "選擇 PostgreSQL 作為主資料庫" |
| `bug` | 🐛 Bug 記錄 | "N+1 查詢導致介面逾時" |
| `feature` | ✨ 功能設計 | "使用者權限系統採用 RBAC 模型" |
| `context` | 📝 專案上下文 | "專案使用 monorepo 架構管理" |
| `architecture` | 🏗️ 架構設計 | "微服務間使用 gRPC 通訊" |
| `lesson` | 📚 經驗教訓 | "不要在迴圈中執行資料庫查詢" |
| `config` | ⚙️ 設定記錄 | "Redis 連線池大小設為 20" |
| `workflow` | 🔧 工作流 | "PR 合併前必須通過 CI 檢查" |
| `general` | 📌 通用記憶 | "團隊每週三進行程式碼評審" |

### 完整指令參考

#### 💾 `recall save` — 儲存記憶

```bash
# 基本用法
recall save --title "標題" --content "內容"

# 完整參數
recall save \
  --title "標題" \
  --content "記憶內容" \
  --category decision \
  --tags tag1,tag2,tag3 \
  --importance 0.8 \
  --agent claude-code \
  --session sess_001
```

| 參數 | 縮寫 | 說明 | 預設值 |
|------|------|------|--------|
| `--title` | `-t` | 記憶標題（**必填**） | — |
| `--content` | `-c` | 記憶內容（**必填**） | — |
| `--category` | `-k` | 記憶分類 | `general` |
| `--tags` | — | 逗號分隔的標籤 | — |
| `--importance` | `-i` | 重要度評分 (0.0-1.0) | `0.5` |
| `--agent` | `-a` | Agent ID | `default` |
| `--session` | `-s` | 關聯會話 ID | — |

#### 🔍 `recall search` — 搜尋記憶

```bash
# 混合搜尋（預設）
recall search "認證方案" --mode hybrid --limit 20

# 全文搜尋
recall search "JWT Token" --mode fulltext

# 關鍵字搜尋
recall search "資料庫" --mode keyword

# TF-IDF 語義搜尋
recall search "效能最佳化" --mode tfidf

# 帶過濾條件
recall search "bug" --category bug --min-importance 0.5 --agent cursor

# JSON 輸出（方便腳本處理）
recall search "API" --json
```

| 參數 | 縮寫 | 說明 | 預設值 |
|------|------|------|--------|
| `query` | — | 搜尋關鍵字（**必填**） | — |
| `--mode` | `-m` | 搜尋模式 | `hybrid` |
| `--category` | `-k` | 按分類過濾 | — |
| `--limit` | `-l` | 最大結果數 | `20` |
| `--agent` | `-a` | Agent ID | `default` |
| `--min-importance` | — | 最低重要度 | `0.0` |
| `--json` | — | JSON 格式輸出 | `false` |

#### 👁️ `recall show` — 查看詳情

```bash
recall show 42
```

#### 📋 `recall list` — 列出記憶

```bash
# 列出最近記憶
recall list --limit 20

# 按分類過濾
recall list --category decision --limit 10

# 指定 Agent
recall list --agent claude-code

# JSON 輸出
recall list --json
```

#### 🗑️ `recall delete` — 刪除記憶

```bash
# 互動式確認刪除
recall delete 42

# 強制刪除（跳過確認）
recall delete 42 --force
```

#### ✏️ `recall update` — 更新記憶

```bash
# 更新標題和內容
recall update 42 --title "新標題" --content "新內容"

# 更新分類和重要度
recall update 42 --category architecture --importance 0.9

# 更新標籤
recall update 42 --tags new-tag1,new-tag2
```

#### 📊 `recall dashboard` — TUI 儀表板

```bash
# 預設 Agent 儀表板
recall dashboard

# 指定 Agent
recall dashboard --agent cursor
```

#### 📋 `recall context` — 生成上下文

```bash
# 生成上下文（預設 4000 tokens）
recall context --agent claude-code

# 自訂 Token 預算
recall context --agent cursor --max-tokens 2000

# 指定分類
recall context --agent copilot --categories decision,architecture

# 輸出到檔案
recall context --agent claude-code --output context.md
```

#### 🔄 `recall session` — 會話管理

```bash
# 開始新會話
recall session start --agent claude-code --description "重構認證模組"

# 結束當前會話
recall session end --summary "完成 JWT 認證重構，新增 Refresh Token 機制"

# 查看會話歷史
recall session history --agent claude-code --limit 10
```

#### 📤 `recall export` — 匯出記憶

```bash
# 匯出為 JSON
recall export --format json --output memories.json

# 匯出為 Markdown
recall export --format markdown --output memories.md

# 匯出指定 Agent 的記憶
recall export --agent cursor --format json --output cursor-memories.json
```

#### 📥 `recall import` — 匯入記憶

```bash
recall import memories.json --agent claude-code
```

#### 📈 `recall stats` — 統計資訊

```bash
# 查看統計
recall stats

# 指定 Agent
recall stats --agent claude-code

# JSON 輸出
recall stats --json
```

#### 🤖 `recall agents` — 列出 Agent

```bash
recall agents
```

#### 📂 `recall categories` — 列出分類

```bash
recall categories --agent claude-code
```

#### 🧹 `recall cleanup` — 清理記憶

```bash
# 清理 90 天前的低重要度記憶
recall cleanup --max-age-days 90 --min-importance 0.3

# 預覽模式（不實際刪除）
recall cleanup --max-age-days 90 --min-importance 0.3 --dry-run

# 指定 Agent
recall cleanup --agent cursor --max-age-days 60
```

#### 🗜️ `recall compress` — 壓縮記憶

```bash
# 預覽壓縮效果
recall compress 42

# 套用壓縮
recall compress 42 --apply
```

#### 💡 `recall suggest` — 相關記憶推薦

```bash
# 推薦相關記憶（預設 5 條）
recall suggest 42

# 自訂推薦數量
recall suggest 42 --limit 10
```

### 典型使用場景

#### 場景一：專案技術決策記錄

```bash
# 記錄資料庫選型決策
recall save \
  -t "資料庫選型：PostgreSQL vs MySQL" \
  -c "經過團隊討論，最終選擇 PostgreSQL。原因：1) 對 JSON 資料型別支援更好；2) 擴充性更強；3) 團隊更熟悉。" \
  -k decision \
  --tags database,postgresql,architecture \
  -i 0.9 \
  -a claude-code

# 記錄快取方案
recall save \
  -t "快取方案：Redis + 本地快取" \
  -c "採用兩級快取策略：L1 使用 Python functools.lru_cache 做本地快取，TTL 5 分鐘；L2 使用 Redis 做分散式快取，TTL 30 分鐘。快取擊穿時使用互斥鎖防止雪崩。" \
  -k architecture \
  --tags cache,redis,performance \
  -i 0.85
```

#### 場景二：Bug 修復經驗沉澱

```bash
# 記錄 Bug 及修復方案
recall save \
  -t "N+1 查詢導致列表介面逾時" \
  -c "問題：使用者列表介面在資料量超過 1000 時回應時間超過 5 秒。原因：迴圈中執行了 N 次資料庫查詢取得關聯資料。修復：使用 SQLAlchemy 的 joinedload 預載入關聯資料，回應時間降至 200ms。" \
  -k bug \
  --tags performance,sqlalchemy,optimization \
  -i 0.8

# 記錄經驗教訓
recall save \
  -t "避免在迴圈中執行資料庫查詢" \
  -c "經驗教訓：在處理列表資料時，務必使用批次查詢或預載入（eager loading）來取得關聯資料。可以使用 Django 的 select_related/prefetch_related 或 SQLAlchemy 的 joinedload/subqueryload。" \
  -k lesson \
  --tags best-practice,performance,database \
  -i 0.95
```

#### 場景三：為 AI Agent 注入上下文

```bash
# 開始新的編碼會話
recall session start --agent claude-code -d "開發使用者權限模組"

# 儲存編碼過程中的關鍵決策
recall save -t "RBAC 權限模型設計" -c "採用基於角色的存取控制（RBAC）模型。使用者 -> 角色 -> 權限，支援多角色綁定。權限粒度到 API 端點級別。" -k architecture -a claude-code

# 為新會話生成上下文
recall context --agent claude-code --max-tokens 4000 --output .claude-context.md

# 結束會話
recall session end -s "完成 RBAC 權限模組開發，包含使用者、角色、權限 CRUD 介面"
```

#### 場景四：跨裝置遷移記憶

```bash
# 在裝置 A 上匯出
recall export --format json --output my-memories.json

# 在裝置 B 上匯入
recall import my-memories.json --agent claude-code
```

---

## 💡 設計思路與迭代規劃

### 設計哲學

1. **輕量優先** — 零外部依賴，純 Python 標準函式庫實作，安裝即用
2. **CLI 原生** — 命令列介面，方便與各種 AI Agent 工作流整合
3. **儲存可靠** — SQLite 後端，資料安全有保障
4. **搜尋智慧** — 多模式混合搜尋，兼顧精確性和語義理解
5. **Agent 無關** — 不綁定特定 AI Agent，支援所有主流編碼代理

### 架構概覽

```
┌─────────────────────────────────────────────────┐
│                   CLI 層 (cli.py)                │
│  save / search / show / list / delete / update   │
├─────────────────────────────────────────────────┤
│              業務邏輯層                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ 搜尋引擎  │ │ 壓縮引擎  │ │  會話管理器      │ │
│  │(search)  │ │(compress) │ │  (session)       │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
├─────────────────────────────────────────────────┤
│              儲存層 (store.py)                    │
│  ┌────────────────────────────────────────────┐  │
│  │              SQLite 資料庫                  │  │
│  │  memories | memory_fts | sessions | agents │  │
│  └────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────┤
│              展示層 (tui.py)                      │
│  ANSI 彩色輸出 | 儀表板 | 搜尋結果高亮          │
└─────────────────────────────────────────────────┘
```

### 迭代規劃

#### v1.x — 穩定化（當前階段）
- [x] 核心記憶 CRUD 操作
- [x] 四種搜尋模式
- [x] 記憶壓縮
- [x] 會話管理
- [x] TUI 儀表板
- [x] 匯入匯出
- [x] 多 Agent 支援

#### v2.0 — 智慧化（規劃中）
- [ ] **向量搜尋** — 整合 sentence-transformers 實作語義向量搜尋
- [ ] **自動記憶提取** — 從 Git Commit 和程式碼變更中自動提取記憶
- [ ] **Web UI** — 提供瀏覽器端管理介面
- [ ] **外掛系統** — 支援自訂搜尋和壓縮策略
- [ ] **雲端同步** — 支援多裝置記憶同步

#### v3.0 — 生態化（遠期願景）
- [ ] **Agent Marketplace** — 分享記憶範本和最佳實踐
- [ ] **團隊協作** — 多人共享記憶庫
- [ ] **IDE 外掛** — VS Code / JetBrains 原生整合
- [ ] **API 服務** — 提供 REST/GraphQL 介面

---

## 📦 打包與部署指南

### 從原始碼安裝

```bash
# 複製倉庫
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# 安裝（開發模式）
pip install -e .

# 或直接安裝
pip install .
```

### 建構發布包

```bash
# 安裝建構工具
pip install build

# 建構 sdist 和 wheel
python -m build

# 建構產物位於 dist/ 目錄
ls dist/
# agentrecall-1.0.0.tar.gz
# agentrecall-1.0.0-py3-none-any.whl
```

### 安裝建構產物

```bash
# 從 wheel 安裝
pip install dist/agentrecall-1.0.0-py3-none-any.whl

# 從 sdist 安裝
pip install dist/agentrecall-1.0.0.tar.gz
```

### 資料儲存位置

AgentRecall 預設將資料儲存在使用者主目錄下：

```
~/.agentrecall/
└── memories.db    # SQLite 資料庫檔案
```

可透過環境變數自訂儲存路徑（規劃中）。

### 解除安裝

```bash
pip uninstall agentrecall

# 如需刪除資料
rm -rf ~/.agentrecall/
```

---

## 🤝 貢獻指南

我們歡迎並感謝所有形式的貢獻！無論是提交 Bug 報告、改進文件還是提交程式碼。

### 貢獻流程

1. **Fork** 本倉庫
2. 建立特性分支：`git checkout -b feature/your-feature-name`
3. 提交變更：`git commit -m 'feat: add your feature'`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 **Pull Request**

### 開發環境設定

```bash
# 複製倉庫
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
pytest tests/

# 程式碼格式檢查
# （專案遵循 PEP 8 規範）
```

### 提交規範

請遵循 **Conventional Commits** 規範：

| 類型 | 說明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修復 |
| `docs` | 文件更新 |
| `refactor` | 程式碼重構 |
| `test` | 測試相關 |
| `chore` | 建構/工具鏈更新 |

範例：
```bash
git commit -m "feat: add vector search support"
git commit -m "fix: resolve FTS5 fallback on older SQLite"
git commit -m "docs: update README with new commands"
```

### 回報 Bug

請在 [GitHub Issues](https://github.com/gitstq/AgentRecall/issues) 提交 Bug 報告，包含以下資訊：

- **環境資訊**：作業系統、Python 版本
- **重現步驟**：詳細的操作步驟
- **期望行為**：你期望發生什麼
- **實際行為**：實際發生了什麼
- **錯誤日誌**：完整的錯誤輸出

---

## 📄 開源協議

本專案基於 **[MIT License](https://opensource.org/licenses/MIT)** 開源。

```
MIT License

Copyright (c) 2024 AgentRecall Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <a href="#繁體中文">⬆️ 返回頂部</a> ·
  <a href="#简体中文">简体中文</a> ·
  <a href="#english">English</a>
</p>

---

<a id="english"></a>

# 🇬🇧 English

## 🎉 Introduction

**AgentRecall** is a **lightweight persistent memory engine** designed for AI coding agents. It provides **long-term memory capabilities** for AI coding assistants like Claude Code, Cursor, and GitHub Copilot, enabling AI to retain key decisions, architecture choices, and coding experiences across sessions and projects.

### Why AgentRecall?

AI coding agents are powerful, but every new session starts from a "zero-memory" state. Developers need to repeatedly explain project background, technology choices, and previous bug fixes to the AI. **AgentRecall** solves this problem:

- 🧠 **Persistent Memory** — AI decisions and experiences survive across sessions
- 🔍 **Intelligent Search** — Four search modes to quickly find historical memories
- 🤖 **Multi-Agent Support** — One memory store serves multiple AI coding agents
- 📦 **Zero External Dependencies** — Pure Python standard library, install and go

### Tech Stack

| Technology | Description |
|------------|-------------|
| **Python 3.8+** | Core runtime environment |
| **SQLite** | Embedded database, no additional installation required |
| **TF-IDF** | Term Frequency-Inverse Document Frequency based intelligent search |
| **ANSI TUI** | Colored terminal user interface |

---

## ✨ Core Features

### 1. 💾 Persistent Memory Storage
Reliable storage backed by **SQLite** with multi-Agent data isolation. All memories are partitioned by Agent ID for complete separation.

### 2. 🔍 Intelligent Hybrid Search
Four **search modes** for different use cases:

| Mode | Description | Best For |
|------|-------------|----------|
| `hybrid` | **Hybrid search** (default) | Best overall results |
| `fulltext` | Full-text search | Exact phrase matching |
| `keyword` | Keyword search | Tag/title quick lookup |
| `tfidf` | TF-IDF semantic search | Semantically similar content |

### 3. 🗜️ Smart Memory Compression
Automatically compresses redundant content while **preserving code blocks and key information**. Supports manual triggering and auto-compression on save.

### 4. 🔄 Session Management
Track the full lifecycle of coding sessions: start → in progress → end. Associate memories with specific sessions for easy retrospective.

### 5. 📋 Context Injection
Automatically generate structured context for Agents with **Token budget control**, ensuring injected context stays within the Agent's context window limits.

### 6. 🤖 Multi-Agent Support
Native support for **Claude Code**, **Cursor**, **GitHub Copilot**, and other mainstream AI coding agents. Each Agent has its own isolated memory space.

### 7. 📊 TUI Dashboard
Beautiful **colored terminal interface** with memory browsing, search result display, and statistical overview.

### 8. 📤 Import & Export
Supports **JSON** and **Markdown** export formats for cross-device migration and knowledge sharing.

### 9. 🏷️ Keyword Extraction
Automatically extracts keywords from memory content using **TF (Term Frequency)** algorithm to enhance search capabilities.

### 10. 💡 Related Memory Suggestions
Intelligent recommendations based on semantic similarity, helping discover related knowledge in historical memories.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8** or higher
- **pip** package manager
- No external dependencies required!

### Installation

```bash
# Install from GitHub
pip install git+https://github.com/gitstq/AgentRecall.git
```

### Verify Installation

```bash
recall --version
# Output: AgentRecall v1.0.0
```

### Basic Usage (5-Minute Guide)

**Step 1: Save a Memory**

```bash
recall save \
  --title "Use JWT for API Authentication" \
  --content "The project decided to use JWT Token for API authentication. Access Token validity: 2 hours, Refresh Token validity: 7 days. Tokens are stored in httpOnly cookies." \
  --category decision \
  --tags auth,jwt,security \
  --importance 0.9
```

**Step 2: Search Memories**

```bash
recall search "JWT authentication" --mode hybrid --limit 10
```

**Step 3: View Memory Details**

```bash
recall show 1
```

**Step 4: View Dashboard**

```bash
recall dashboard
```

**Step 5: Generate Agent Context**

```bash
recall context --agent claude-code --max-tokens 4000
```

---

## 📖 Detailed Usage Guide

### Memory Categories

AgentRecall includes **9 built-in memory categories** covering all aspects of coding work:

| Category | Description | Example |
|----------|-------------|---------|
| `decision` | 🎯 Technical decisions | "Choose PostgreSQL as primary database" |
| `bug` | 🐛 Bug records | "N+1 query causing API timeout" |
| `feature` | ✨ Feature design | "User permission system using RBAC model" |
| `context` | 📝 Project context | "Project uses monorepo architecture" |
| `architecture` | 🏗️ Architecture design | "Microservices communicate via gRPC" |
| `lesson` | 📚 Lessons learned | "Never execute DB queries inside loops" |
| `config` | ⚙️ Configuration records | "Redis connection pool size set to 20" |
| `workflow` | 🔧 Workflow | "PR must pass CI checks before merge" |
| `general` | 📌 General memories | "Team does code review every Wednesday" |

### Complete Command Reference

#### 💾 `recall save` — Save a Memory

```bash
# Basic usage
recall save --title "Title" --content "Content"

# Full parameters
recall save \
  --title "Title" \
  --content "Memory content" \
  --category decision \
  --tags tag1,tag2,tag3 \
  --importance 0.8 \
  --agent claude-code \
  --session sess_001
```

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--title` | `-t` | Memory title (**required**) | — |
| `--content` | `-c` | Memory content (**required**) | — |
| `--category` | `-k` | Memory category | `general` |
| `--tags` | — | Comma-separated tags | — |
| `--importance` | `-i` | Importance score (0.0-1.0) | `0.5` |
| `--agent` | `-a` | Agent ID | `default` |
| `--session` | `-s` | Associated session ID | — |

#### 🔍 `recall search` — Search Memories

```bash
# Hybrid search (default)
recall search "auth solution" --mode hybrid --limit 20

# Full-text search
recall search "JWT Token" --mode fulltext

# Keyword search
recall search "database" --mode keyword

# TF-IDF semantic search
recall search "performance optimization" --mode tfidf

# With filters
recall search "bug" --category bug --min-importance 0.5 --agent cursor

# JSON output (for scripting)
recall search "API" --json
```

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `query` | — | Search query (**required**) | — |
| `--mode` | `-m` | Search mode | `hybrid` |
| `--category` | `-k` | Filter by category | — |
| `--limit` | `-l` | Maximum results | `20` |
| `--agent` | `-a` | Agent ID | `default` |
| `--min-importance` | — | Minimum importance threshold | `0.0` |
| `--json` | — | JSON format output | `false` |

#### 👁️ `recall show` — View Memory Details

```bash
recall show 42
```

#### 📋 `recall list` — List Memories

```bash
# List recent memories
recall list --limit 20

# Filter by category
recall list --category decision --limit 10

# Specify Agent
recall list --agent claude-code

# JSON output
recall list --json
```

#### 🗑️ `recall delete` — Delete a Memory

```bash
# Interactive confirmation
recall delete 42

# Force delete (skip confirmation)
recall delete 42 --force
```

#### ✏️ `recall update` — Update a Memory

```bash
# Update title and content
recall update 42 --title "New Title" --content "New Content"

# Update category and importance
recall update 42 --category architecture --importance 0.9

# Update tags
recall update 42 --tags new-tag1,new-tag2
```

#### 📊 `recall dashboard` — TUI Dashboard

```bash
# Default Agent dashboard
recall dashboard

# Specify Agent
recall dashboard --agent cursor
```

#### 📋 `recall context` — Generate Context

```bash
# Generate context (default 4000 tokens)
recall context --agent claude-code

# Custom token budget
recall context --agent cursor --max-tokens 2000

# Specify categories
recall context --agent copilot --categories decision,architecture

# Output to file
recall context --agent claude-code --output context.md
```

#### 🔄 `recall session` — Session Management

```bash
# Start a new session
recall session start --agent claude-code --description "Refactoring auth module"

# End current session
recall session end --summary "Completed JWT auth refactor, added Refresh Token mechanism"

# View session history
recall session history --agent claude-code --limit 10
```

#### 📤 `recall export` — Export Memories

```bash
# Export as JSON
recall export --format json --output memories.json

# Export as Markdown
recall export --format markdown --output memories.md

# Export specific Agent's memories
recall export --agent cursor --format json --output cursor-memories.json
```

#### 📥 `recall import` — Import Memories

```bash
recall import memories.json --agent claude-code
```

#### 📈 `recall stats` — Statistics

```bash
# View statistics
recall stats

# Specify Agent
recall stats --agent claude-code

# JSON output
recall stats --json
```

#### 🤖 `recall agents` — List Agents

```bash
recall agents
```

#### 📂 `recall categories` — List Categories

```bash
recall categories --agent claude-code
```

#### 🧹 `recall cleanup` — Cleanup Memories

```bash
# Clean up memories older than 90 days with low importance
recall cleanup --max-age-days 90 --min-importance 0.3

# Dry run mode (preview only)
recall cleanup --max-age-days 90 --min-importance 0.3 --dry-run

# Specify Agent
recall cleanup --agent cursor --max-age-days 60
```

#### 🗜️ `recall compress` — Compress a Memory

```bash
# Preview compression result
recall compress 42

# Apply compression
recall compress 42 --apply
```

#### 💡 `recall suggest` — Suggest Related Memories

```bash
# Suggest related memories (default 5)
recall suggest 42

# Custom suggestion count
recall suggest 42 --limit 10
```

### Typical Use Cases

#### Use Case 1: Recording Technical Decisions

```bash
# Record database selection decision
recall save \
  -t "Database Selection: PostgreSQL vs MySQL" \
  -c "After team discussion, we chose PostgreSQL. Reasons: 1) Better JSON data type support; 2) More scalable; 3) Team is more familiar with it." \
  -k decision \
  --tags database,postgresql,architecture \
  -i 0.9 \
  -a claude-code

# Record caching strategy
recall save \
  -t "Caching Strategy: Redis + Local Cache" \
  -c "Two-level caching: L1 uses Python functools.lru_cache for local caching (TTL: 5 min); L2 uses Redis for distributed caching (TTL: 30 min). Mutex locks prevent cache stampede." \
  -k architecture \
  --tags cache,redis,performance \
  -i 0.85
```

#### Use Case 2: Bug Fix Knowledge Base

```bash
# Record bug and fix
recall save \
  -t "N+1 Query Causing List API Timeout" \
  -c "Problem: User list API response exceeds 5s with 1000+ records. Cause: N database queries executed in a loop for related data. Fix: Used SQLAlchemy joinedload for eager loading. Response time dropped to 200ms." \
  -k bug \
  --tags performance,sqlalchemy,optimization \
  -i 0.8

# Record lesson learned
recall save \
  -t "Avoid Database Queries Inside Loops" \
  -c "Lesson: When processing list data, always use batch queries or eager loading for related data. Use Django's select_related/prefetch_related or SQLAlchemy's joinedload/subqueryload." \
  -k lesson \
  --tags best-practice,performance,database \
  -i 0.95
```

#### Use Case 3: Injecting Context for AI Agents

```bash
# Start a new coding session
recall session start --agent claude-code -d "Developing user permission module"

# Save key decisions during coding
recall save -t "RBAC Permission Model Design" -c "Using Role-Based Access Control (RBAC). User -> Role -> Permission, supports multi-role binding. Permission granularity at API endpoint level." -k architecture -a claude-code

# Generate context for new session
recall context --agent claude-code --max-tokens 4000 --output .claude-context.md

# End session
recall session end -s "Completed RBAC permission module with User, Role, Permission CRUD APIs"
```

#### Use Case 4: Cross-Device Memory Migration

```bash
# Export on Device A
recall export --format json --output my-memories.json

# Import on Device B
recall import my-memories.json --agent claude-code
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Lightweight First** — Zero external dependencies, pure Python standard library, install and use immediately
2. **CLI Native** — Command-line interface for seamless integration with AI Agent workflows
3. **Reliable Storage** — SQLite backend ensures data safety and durability
4. **Smart Search** — Multi-mode hybrid search balancing precision and semantic understanding
5. **Agent Agnostic** — Not tied to any specific AI Agent, supports all mainstream coding agents

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   CLI Layer (cli.py)             │
│  save / search / show / list / delete / update   │
├─────────────────────────────────────────────────┤
│              Business Logic Layer                │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Search   │ │ Compress  │ │ Session Manager  │ │
│  │  Engine   │ │  Engine   │ │   (session)      │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
├─────────────────────────────────────────────────┤
│              Storage Layer (store.py)            │
│  ┌────────────────────────────────────────────┐  │
│  │              SQLite Database               │  │
│  │  memories | memory_fts | sessions | agents │  │
│  └────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────┤
│              Presentation Layer (tui.py)         │
│  ANSI Colored Output | Dashboard | Highlights   │
└─────────────────────────────────────────────────┘
```

### Roadmap

#### v1.x — Stabilization (Current)
- [x] Core memory CRUD operations
- [x] Four search modes
- [x] Memory compression
- [x] Session management
- [x] TUI dashboard
- [x] Import & export
- [x] Multi-Agent support

#### v2.0 — Intelligence (Planned)
- [ ] **Vector Search** — Integrate sentence-transformers for semantic vector search
- [ ] **Auto Memory Extraction** — Automatically extract memories from Git commits and code changes
- [ ] **Web UI** — Browser-based management interface
- [ ] **Plugin System** — Support custom search and compression strategies
- [ ] **Cloud Sync** — Multi-device memory synchronization

#### v3.0 — Ecosystem (Long-term Vision)
- [ ] **Agent Marketplace** — Share memory templates and best practices
- [ ] **Team Collaboration** — Shared memory repositories for teams
- [ ] **IDE Plugins** — Native integration with VS Code / JetBrains
- [ ] **API Service** — REST/GraphQL interface

---

## 📦 Packaging & Deployment Guide

### Install from Source

```bash
# Clone the repository
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

### Build Release Packages

```bash
# Install build tools
pip install build

# Build sdist and wheel
python -m build

# Build artifacts are in the dist/ directory
ls dist/
# agentrecall-1.0.0.tar.gz
# agentrecall-1.0.0-py3-none-any.whl
```

### Install Build Artifacts

```bash
# Install from wheel
pip install dist/agentrecall-1.0.0-py3-none-any.whl

# Install from sdist
pip install dist/agentrecall-1.0.0.tar.gz
```

### Data Storage Location

AgentRecall stores data in the user's home directory by default:

```
~/.agentrecall/
└── memories.db    # SQLite database file
```

Custom storage path via environment variable (planned).

### Uninstall

```bash
pip uninstall agentrecall

# To remove data as well
rm -rf ~/.agentrecall/
```

---

## 🤝 Contributing Guide

We welcome and appreciate all forms of contribution! Whether it's submitting bug reports, improving documentation, or submitting code.

### Contribution Workflow

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push the branch: `git push origin feature/your-feature-name`
5. Submit a **Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/AgentRecall.git
cd AgentRecall

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Code format check
# (Project follows PEP 8 conventions)
```

### Commit Convention

Please follow the **Conventional Commits** specification:

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation update |
| `refactor` | Code refactoring |
| `test` | Test related |
| `chore` | Build/toolchain update |

Examples:
```bash
git commit -m "feat: add vector search support"
git commit -m "fix: resolve FTS5 fallback on older SQLite"
git commit -m "docs: update README with new commands"
```

### Reporting Bugs

Please submit bug reports on [GitHub Issues](https://github.com/gitstq/AgentRecall/issues) with the following information:

- **Environment**: Operating system, Python version
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Error Logs**: Complete error output

---

## 📄 License

This project is licensed under the **[MIT License](https://opensource.org/licenses/MIT)**.

```
MIT License

Copyright (c) 2024 AgentRecall Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<p align="center">
  <a href="#english">⬆️ Back to Top</a> ·
  <a href="#简体中文">简体中文</a> ·
  <a href="#繁體中文">繁體中文</a>
</p>
