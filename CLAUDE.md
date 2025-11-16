# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

MeTube 是一个基于 Web 的用户界面，用于 youtube-dl（使用 yt-dlp 分支）并支持播放列表功能。它允许用户从 YouTube 和其他几十个网站下载视频。

## 项目架构

这是一个前后端分离的应用程序：

### 后端 (Python)
- **主入口**: `app/main.py` - 基于 aiohttp 的 web 服务器
- **核心下载逻辑**: `app/ytdl.py` - 封装 yt-dlp 功能的下载队列管理
- **格式处理**: `app/dl_formats.py` - 处理不同下载格式的配置

### 前端 (Angular)
- **Angular 应用**: 位于 `ui/` 目录
- **主组件**: `ui/src/app/app.component.*` - 主要的 UI 组件
- **服务**: `ui/src/app/downloads.service.ts` - 处理与后端的通信
- **WebSocket**: 通过 socket.io 与后端实时通信

## 常用开发命令

### 本地开发和构建

1. **安装前端依赖并构建 UI**:
   ```bash
   cd metube/ui
   npm install
   node_modules/.bin/ng build
   ```

2. **安装 Python 依赖**:
   ```bash
   cd ..
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync
   ```

3. **运行开发服务器**:
   ```bash
   uv run python3 app/main.py
   ```

### Docker 构建
```bash
docker build -t metube .
```

### 前端开发命令
```bash
cd ui
npm start          # 启动开发服务器
npm run build      # 构建生产版本
npm test           # 运行测试
npm run lint       # 代码检查
```

## 核心配置

环境变量配置（主要在 `app/main.py` 中的 Config 类）：
- `DOWNLOAD_DIR`: 下载目录（默认: `/downloads`）
- `DOWNLOAD_MODE`: 下载模式（`sequential`, `concurrent`, `limited`）
- `MAX_CONCURRENT_DOWNLOADS`: 最大并发下载数（默认: 3）
- `OUTPUT_TEMPLATE`: 输出文件名模板
- `YTDL_OPTIONS`: yt-dlp 的额外配置选项

### 身份验证配置
- `ENABLE_HTTP_AUTH`: 启用 HTTP 基本身份验证（默认: `false`）
- `HTTP_AUTH_USERNAME`: 身份验证用户名
- `HTTP_AUTH_PASSWORD`: 身份验证密码
- `HTTP_AUTH_REALM`: 身份验证领域名称（默认: `MeTube Restricted Area`）

**重要**: 当启用身份验证时，所有 API 端点、WebSocket 连接和文件下载都会受到保护。

## 关键功能组件

### 下载管理
- `DownloadQueue` 管理下载队列
- `DownloadInfo` 存储下载项信息
- 支持播放列表下载和自定义下载目录

### 前端组件
- 使用 Angular 19 和 Bootstrap 5
- 实时更新下载进度（通过 WebSocket）
- 支持主题切换（亮色/暗色）

### API 接口
主要通过 REST API 和 socket.io 提供：
- `/add` - 添加下载任务
- `/queue` - 获取下载队列
- `/delete` - 删除下载项

## 部署注意事项

- 默认监听端口: 8081
- 支持 HTTPS 配置
- 支持 Docker 部署
- 支持 Nginx/Apache 反向代理配置

## 身份验证和安全

### HTTP 基本身份验证
MeTube 现已支持内置的 HTTP 基本身份验证功能：
- 全面的请求保护（API、WebSocket、文件下载）
- 安全的凭据验证和日志记录
- 与浏览器扩展和客户端工具兼容
- 支持 HTTPS 和反向代理环境

### 测试身份验证
使用提供的测试脚本验证功能：
```bash
python test_auth.py
```

详细配置说明请参考 `HTTP_AUTH_SETUP.md` 文档。

## 依赖要求

- Python 3.13+
- Node.js（用于构建前端）
- yt-dlp（核心下载引擎）