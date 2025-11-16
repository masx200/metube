# MeTube HTTP 基本身份验证设置指南

## 概述

MeTube 现已支持内置的 HTTP 基本身份验证功能，可通过环境变量进行配置。这个功能为 MeTube 提供了第一道安全防线，防止未经授权的访问。

## 环境变量配置

### 基本身份验证设置

| 环境变量 | 必需 | 默认值 | 说明 |
|----------|------|--------|------|
| `ENABLE_HTTP_AUTH` | 否 | `false` | 启用/禁用 HTTP 基本身份验证 (true/false) |
| `HTTP_AUTH_USERNAME` | 是* | - | 身份验证用户名 |
| `HTTP_AUTH_PASSWORD` | 是* | - | 身份验证密码 |
| `HTTP_AUTH_REALM` | 否 | `MeTube Restricted Area` | 身份验证领域名称 |

*当 `ENABLE_HTTP_AUTH=true` 时必需

### 启用身份验证的方法

#### 1. Docker 命令行方式

```bash
docker run -d -p 8081:8081 \
  -v /path/to/downloads:/downloads \
  -e ENABLE_HTTP_AUTH=true \
  -e HTTP_AUTH_USERNAME=myuser \
  -e HTTP_AUTH_PASSWORD=mypassword \
  ghcr.io/alexta69/metube
```

#### 2. Docker Compose 方式

```yaml
services:
  metube:
    image: ghcr.io/alexta69/metube
    container_name: metube
    restart: unless-stopped
    ports:
      - "8081:8081"
    volumes:
      - /path/to/downloads:/downloads
    environment:
      - ENABLE_HTTP_AUTH=true
      - HTTP_AUTH_USERNAME=myuser
      - HTTP_AUTH_PASSWORD=mypassword
      - HTTP_AUTH_REALM=My Private MeTube
```

#### 3. 本地开发方式

```bash
export ENABLE_HTTP_AUTH=true
export HTTP_AUTH_USERNAME=myuser
export HTTP_AUTH_PASSWORD=mypassword
uv run python3 app/main.py
```

## 安全特性

### 全面的请求保护

启用身份验证后，以下所有功能都将受到保护：

- ✅ **Web 界面访问** (`/`) - 主界面
- ✅ **API 端点** (`/add`, `/delete`, `/queue`, `/history` 等)
- ✅ **文件下载** (`/download/`, `/audio_download/`)
- ✅ **WebSocket 连接** (`/socket.io`)
- ✅ **配置信息** (`/version`, `/robots.txt`)

### 安全日志记录

- 成功的身份验证请求正常记录
- 失败的身份验证尝试会记录警告日志
- 身份验证错误会记录错误日志

## 客户端访问方式

### 1. Web 浏览器

浏览器会自动弹出身份验证对话框：
- 输入配置的用户名和密码即可访问
- 凭据通常会在浏览器会话中保持

### 2. cURL 命令行工具

```bash
# 基本请求
curl -u "myuser:mypassword" http://localhost:8081/

# API 调用示例
curl -u "myuser:mypassword" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","quality":"best"}' \
  http://localhost:8081/add
```

### 3. 浏览器扩展

对于浏览器扩展，需要更新发送请求的代码以包含身份验证头：

```javascript
const credentials = btoa('myuser:mypassword');
const headers = {
  'Authorization': `Basic ${credentials}`,
  'Content-Type': 'application/json'
};

fetch('http://localhost:8081/add', {
  method: 'POST',
  headers: headers,
  body: JSON.stringify({
    url: document.location.href,
    quality: 'best'
  })
});
```

## 最佳实践

### 1. 强密码策略

```bash
# 使用强密码（示例）
export HTTP_AUTH_USERNAME=metube_admin
export HTTP_AUTH_PASSWORD="MyStr0ng!P@ssw0rd#2024"
```

### 2. HTTPS 配置

建议在生产环境中同时启用 HTTPS：

```yaml
environment:
  - ENABLE_HTTP_AUTH=true
  - HTTP_AUTH_USERNAME=admin
  - HTTP_AUTH_PASSWORD=strongpassword
  - HTTPS=true
  - CERTFILE=/path/to/cert.pem
  - KEYFILE=/path/to/key.pem
```

### 3. 反向代理兼容性

此身份验证功能与反向代理兼容：

```nginx
# Nginx 配置示例
location /metube/ {
    proxy_pass http://metube:8081;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Authorization $http_authorization;
}
```

## 故障排除

### 常见问题

1. **身份验证失败循环**
   - 检查环境变量是否正确设置
   - 确认用户名和密码没有多余的空格

2. **浏览器扩展无法连接**
   - 更新扩展代码以包含 `Authorization` 头
   - 检查 CORS 设置

3. **WebSocket 连接失败**
   - 确保 WebSocket 客户端也发送身份验证信息
   - 检查查询参数中的授权信息

### 调试技巧

1. **检查日志**：
   ```bash
   docker logs metube | grep -i auth
   ```

2. **测试身份验证**：
   ```bash
   # 运行提供的测试脚本
   python test_auth.py
   ```

3. **验证环境变量**：
   ```bash
   docker exec metube env | grep HTTP_AUTH
   ```

## 安全注意事项

1. **密码安全**：避免在日志或版本控制中暴露密码
2. **网络安全**：考虑使用 VPN 或防火墙限制访问
3. **定期更换**：定期更换身份验证凭据
4. **监控日志**：监控失败的身份验证尝试

## 测试

使用提供的测试脚本验证身份验证功能：

```bash
# 启动带身份验证的 MeTube
ENABLE_HTTP_AUTH=true HTTP_AUTH_USERNAME=testuser HTTP_AUTH_PASSWORD=testpass uv run python3 app/main.py

# 在另一个终端运行测试
python test_auth.py
```

这个身份验证功能为 MeTube 提供了基本的安全保护，同时保持了简单易用的特性。