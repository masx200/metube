# MeTube

![构建状态](https://github.com/alexta69/metube/actions/workflows/main.yml/badge.svg)
![Docker 拉取次数](https://img.shields.io/docker/pulls/alexta69/metube.svg)

youtube-dl 的 Web 图形界面（使用 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 分支），支持播放列表功能。允许您从 YouTube 和[几十个其他网站](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)下载视频。

![截图1](https://github.com/alexta69/metube/raw/master/screenshot.gif)

## 🐳 使用 Docker 运行

```bash
docker run -d -p 8081:8081 -v /path/to/downloads:/downloads ghcr.io/alexta69/metube
```

## 🐳 使用 docker-compose 运行

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
```

## ⚙️ 通过环境变量配置

某些值可以通过环境变量设置，使用 docker 命令行的 `-e` 参数，或 docker-compose 中的 `environment:` 部分。

### ⬇️ 下载行为

* **__DOWNLOAD_MODE__**: 此标志控制下载任务的调度和执行方式。选项包括 `sequential`（顺序）、`concurrent`（并发）和 `limited`（限制）。默认为 `limited`：
    *   `sequential`: 一次处理一个下载。新的下载要等到前一个完成后才会开始。此模式有助于节省系统资源或确保下载按严格顺序进行。
    *   `concurrent`: 下载任务在添加后立即开始，对同时运行的下载数量没有内置限制。如果同时启动太多下载，此模式可能会使系统不堪重负。
    *   `limited`: 下载任务并发启动，但受到并发限制的限制。在此模式下，使用信号量，因此在任何给定时间最多运行固定数量的下载。
* **__MAX_CONCURRENT_DOWNLOADS__**: 此标志仅在 `DOWNLOAD_MODE` 设置为 `limited` 时使用。
    它指定允许的最大同时下载数。例如，如果设置为 `5`，则最多同时运行五个下载，任何额外的下载将等待其中一个活动下载完成。默认为 `3`。
* **__DELETE_FILE_ON_TRASHCAN__**: 如果为 `true`，当文件从 UI 的"已完成"部分中删除时，服务器上的下载文件也会被删除。默认为 `false`。
* **__DEFAULT_OPTION_PLAYLIST_STRICT_MODE__**: 如果为 `true`，"严格播放列表模式"开关将默认启用。在此模式下，只有当 URL 严格指向播放列表时才会下载播放列表。播放列表中视频的 URL 将被视为直接视频 URL。默认为 `false`。
* **__DEFAULT_OPTION_PLAYLIST_ITEM_LIMIT__**: 可下载的播放列表项目最大数量。默认为 `0`（无限制）。

### 📁 存储和目录

* **__DOWNLOAD_DIR__**: 下载文件保存的路径。在 Docker 镜像中默认为 `/downloads`，否则为 `.`。
* **__AUDIO_DOWNLOAD_DIR__**: 音频下载文件的保存路径（如果您希望将它们与视频下载分开）。默认为 `DOWNLOAD_DIR` 的值。
* **__CUSTOM_DIRS__**: 是否启用在 `__DOWNLOAD_DIR__`（或 `__AUDIO_DOWNLOAD_DIR__`）内将视频下载到自定义目录。启用后，添加按钮旁边会出现一个下拉菜单来指定下载目录。默认为 `true`。
* **__CREATE_CUSTOM_DIRS__**: 是否支持在 `__DOWNLOAD_DIR__`（或 `__AUDIO_DOWNLOAD_DIR__`）内自动创建目录（如果它们不存在）。启用后，下载目录选择器支持自由文本输入，指定的目录将被递归创建。默认为 `true`。
* **__CUSTOM_DIRS_EXCLUDE_REGEX__**: 用于从下拉菜单中排除某些自定义目录的正则表达式。空的正则表达式禁用排除。默认为 `(^|/)[.@].*$`，这意味着排除以 `.` 或 `@` 开头的目录。
* **__DOWNLOAD_DIRS_INDEXABLE__**: 如果为 `true`，下载目录（`__DOWNLOAD_DIR__` 和 `__AUDIO_DOWNLOAD_DIR__`）在 Web 服务器上可索引。默认为 `false`。
* **__STATE_DIR__**: 队列持久化文件保存的路径。在 Docker 镜像中默认为 `/downloads/.metube`，否则为 `.`。
* **__TEMP_DIR__**: 中间下载文件保存的路径。在 Docker 镜像中默认为 `/downloads`，否则为 `.`。
  * 将此设置为 SSD 或 RAM 文件系统（例如 `tmpfs`）以获得更好的性能。
  * **注意**: 使用 RAM 文件系统可能会阻止下载恢复。

### 📝 文件命名和 yt-dlp

* **__OUTPUT_TEMPLATE__**: 下载视频文件名的模板，根据[此规范](https://github.com/yt-dlp/yt-dlp/blob/master/README.md#output-template)格式化。默认为 `%(title)s.%(ext)s`。
* **__OUTPUT_TEMPLATE_CHAPTER__**: 当通过后处理器拆分为章节时，下载视频文件名的模板。默认为 `%(title)s - %(section_number)s %(section_title)s.%(ext)s`。
* **__OUTPUT_TEMPLATE_PLAYLIST__**: 当作为播放列表下载时，下载视频文件名的模板。默认为 `%(playlist_title)s/%(title)s.%(ext)s`。如果为空，则使用 `OUTPUT_TEMPLATE`。
* **__YTDL_OPTIONS__**: 以 JSON 格式传递给 yt-dlp 的附加选项。[在此处查看可用选项](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L222)。它们大致对应命令行选项，尽管一些在这里没有精确的等效项。例如，`--recode-video` 必须通过 `postprocessors` 指定。还要注意，破折号被替换为下划线。您可能会发现[此脚本](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py)对于将命令行选项转换为 `YTDL_OPTIONS` 有帮助。
* **__YTDL_OPTIONS_FILE__**: 将被加载并用于填充上述 `YTDL_OPTIONS` 的 JSON 文件路径。请注意，如果同时指定了 `YTDL_OPTIONS_FILE` 和 `YTDL_OPTIONS`，`YTDL_OPTIONS` 中的选项优先。该文件将被监控更改，并在检测到更改时自动重新加载。

### 🌐 Web 服务器和 URL

* **__URL_PREFIX__**: Web 服务器的基本路径（用于在反向代理后托管时）。默认为 `/`。
* **__PUBLIC_HOST_URL__**: UI 中显示的已完成文件下载链接的基本 URL。默认情况下，MeTube 在其自己的 URL 下提供它们。如果您的下载目录可在另一个 URL 上访问，并且您希望下载链接基于该 URL，请使用此变量进行设置。
* **__PUBLIC_HOST_AUDIO_URL__**: 与 PUBLIC_HOST_URL 相同，但用于音频下载。
* **__HTTPS__**: 使用 `https` 而不是 `http`（需要 `__CERTFILE__` 和 `__KEYFILE__`）。默认为 `false`。
* **__CERTFILE__**: HTTPS 证书文件路径。
* **__KEYFILE__**: HTTPS 密钥文件路径。
* **__ROBOTS_TXT__**: 容器中挂载的 `robots.txt` 文件的路径。

### 🔐 身份验证和安全

* **__ENABLE_HTTP_AUTH__**: 启用 HTTP 基本身份验证。默认为 `false`。
* **__HTTP_AUTH_USERNAME__**: 身份验证用户名（启用身份验证时必需）。
* **__HTTP_AUTH_PASSWORD__**: 身份验证密码（启用身份验证时必需）。
* **__HTTP_AUTH_REALM__**: 身份验证领域名称。默认为 `MeTube Restricted Area`。

**重要**: 当启用身份验证时，所有 API 端点、WebSocket 连接和文件下载都会受到保护。

### 🏠 基本设置

* **__UID__**: 运行 MeTube 的用户。默认为 `1000`。
* **__GID__**: 运行 MeTube 的组。默认为 `1000`。
* **__UMASK__**: MeTube 使用的 umask 值。默认为 `022`。
* **__DEFAULT_THEME__**: UI 使用的默认主题，可以设置为 `light`、`dark` 或 `auto`。默认为 `auto`。
* **__LOGLEVEL__**: 日志级别，可以设置为 `DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` 或 `NONE`。默认为 `INFO`。
* **__ENABLE_ACCESSLOG__**: 是否启用访问日志。默认为 `false`。

项目的 Wiki 包含了 MeTube 用户贡献的有用配置示例：
* [YTDL_OPTIONS 食谱](https://github.com/alexta69/metube/wiki/YTDL_OPTIONS-Cookbook)
* [OUTPUT_TEMPLATE 食谱](https://github.com/alexta69/metube/wiki/OUTPUT_TEMPLATE-Cookbook)

## 🍪 使用浏览器 Cookie

如果您需要将浏览器的 Cookie 与 MeTube 一起使用，例如下载受限或私人视频：

* 将以下内容添加到您的 docker-compose.yml：

```yaml
    volumes:
      - /path/to/cookies:/cookies
    environment:
      - YTDL_OPTIONS={"cookiefile":"/cookies/cookies.txt"}
```

* 在浏览器中安装提取 Cookie 的扩展程序：
  * [Firefox](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)
  * [Chrome](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
* 使用扩展程序提取您需要的 Cookie，并将文件重命名为 `cookies.txt`
* 将文件放在上面 docker-compose.yml 中配置的文件夹中
* 重启容器

## 🔌 浏览器扩展

浏览器扩展允许右键单击视频并将它们直接发送到 MeTube。请注意，如果您在 HTTPS 页面上，您的 MeTube 实例必须在 HTTPS 反向代理后面（见下文），扩展程序才能工作。

**Chrome**: 由 [Rpsl](https://github.com/rpsl) 贡献。您可以从 [Google Chrome Webstore](https://chrome.google.com/webstore/detail/metube-downloader/fbmkmdnlhacefjljljlbhkodfmfkijdh) 安装，或使用开发者模式从[源代码](https://github.com/Rpsl/metube-browser-extension)安装。

**Firefox**: 由 [nanocortex](https://github.com/nanocortex) 贡献。您可以从 [Firefox Addons](https://addons.mozilla.org/en-US/firefox/addon/metube-downloader) 安装，或从[这里](https://github.com/nanocortex/metube-firefox-addon)获取源代码。

## 📱 iOS 快捷方式

[rithask](https://github.com/rithask) 创建了一个 iOS 快捷方式，用于从 Safari 将 URL 发送到 MeTube。提示时输入 MeTube 实例地址，该地址将保存供以后使用。您可以从 Safari 的共享菜单运行该快捷方式。该快捷方式可以从 [此 iCloud 链接](https://www.icloud.com/shortcuts/66627a9f334c467baabdb2769763a1a6) 下载。

## 📱 iOS 兼容性

iOS 对视频文件有严格的要求，要求 MP4 容器中的 h264 或 h265 视频编解码器和 aac 音频编解码器。这有时可能低于可用的最佳质量。为了满足 iOS 要求，在下载 MP4 格式时，您可以选择"Best (iOS)"以获得尽可能与 iOS 要求兼容的最佳质量格式。

要强制将所有下载转换为 iOS 兼容的编解码器，请插入此环境变量：

```yaml
  environment:
    - 'YTDL_OPTIONS={"format": "best", "exec": "ffmpeg -i %(filepath)q -c:v libx264 -c:a aac %(filepath)q.h264.mp4"}'
```

## 🔖 书签小工具

[kushfest](https://github.com/kushfest) 创建了一个 Chrome 书签小工具，用于将当前打开的网页发送到 MeTube。请注意，如果您在 HTTPS 页面上，您的 MeTube 实例必须在环境中配置为 `HTTPS` 为 `true`，或在 HTTPS 反向代理后面（见下文），书签小工具才能工作。

GitHub 不允许将 JavaScript 嵌入为链接，因此必须通过将以下代码复制到您在书签栏上创建的新书签中来手动创建书签。将下面 URL 中的主机名更改为指向您的 MeTube 实例。

```javascript
javascript:!function(){xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.withCredentials=true;xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function(){if(xhr.status==200){alert("Sent to metube!")}else{alert("Send to metube failed. Check the javascript console for clues.")}}}();
```

[shoonya75](https://github.com/shoonya75) 贡献了 Firefox 版本：

```javascript
javascript:(function(){xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function(){if(xhr.status==200){alert("Sent to metube!")}else{alert("Send to metube failed. Check the javascript console for clues.")}}})();
```

上面的书签小工具使用 `alert()` 作为成功/失败通知。以下将显示提示消息：

Chrome:

```javascript
javascript:!function(){function notify(msg) {var sc = document.scrollingElement.scrollTop; var text = document.createElement('span');text.innerHTML=msg;var ts = text.style;ts.all = 'revert';ts.color = '#000';ts.fontFamily = 'Verdana, sans-serif';ts.fontSize = '15px';ts.backgroundColor = 'white';ts.padding = '15px';ts.border = '1px solid gainsboro';ts.boxShadow = '3px 3px 10px';ts.zIndex = '100';document.body.appendChild(text);ts.position = 'absolute'; ts.top = 50 + sc + 'px'; ts.left = (window.innerWidth / 2)-(text.offsetWidth / 2) + 'px'; setTimeout(function () { text.style.visibility = "hidden"; }, 1500);}xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function() { if(xhr.status==200){notify("Sent to metube!")}else {notify("Send to metube failed. Check the javascript console for clues.")}}}();
```

Firefox:

```javascript
javascript:(function(){function notify(msg) {var sc = document.scrollingElement.scrollTop; var text = document.createElement('span');text.innerHTML=msg;var ts = text.style;ts.all = 'revert';ts.color = '#000';ts.fontFamily = 'Verdana, sans-serif';ts.fontSize = '15px';ts.backgroundColor = 'white';ts.padding = '15px';ts.border = '1px solid gainsboro';ts.boxShadow = '3px 3px 10px';ts.zIndex = '100';document.body.appendChild(text);ts.position = 'absolute'; ts.top = 50 + sc + 'px'; ts.left = (window.innerWidth / 2)-(text.offsetWidth / 2) + 'px'; setTimeout(function () { text.style.visibility = "hidden"; }, 1500);}xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function() { if(xhr.status==200){notify("Sent to metube!")}else {notify("Send to metube failed. Check the javascript console for clues.")}}})();
```

## ⚡ Raycast 扩展

[dotvhs](https://github.com/dotvhs) 创建了一个 [Raycast 扩展](https://www.raycast.com/dot/metube)，允许直接从 Raycast 向 MeTube 添加视频。

## 🔒 HTTPS 支持和在反向代理后运行

可以将 MeTube 配置为以 HTTPS 模式监听。`docker-compose` 示例：

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
      - /path/to/ssl/crt:/ssl/crt.pem
      - /path/to/ssl/key:/ssl/key.pem
    environment:
      - HTTPS=true
      - CERTFILE=/ssl/crt.pem
      - KEYFILE=/ssl/key.pem
```

也可以在反向代理后面运行 MeTube 以支持身份验证。还可以通过这种方式添加 HTTPS 支持。

当在重新映射 URL 的反向代理后面运行时（即，MeTube 在子目录下而不是根目录下提供服务），不要忘记将 URL_PREFIX 环境变量设置为正确的值。

如果您使用 [linuxserver/swag](https://docs.linuxserver.io/general/swag) 镜像来满足您的反向代理需求（我衷心推荐），它已经在配置卷的 `nginx/proxy-confs` 目录下包含了用于在 [子文件夹](https://github.com/linuxserver/reverse-proxy-confs/blob/master/metube.subfolder.conf.sample) 和 [子域名](https://github.com/linuxserver/reverse-proxy-confs/blob/master/metube.subdomain.conf.sample) 模式下代理 MeTube 的现成代码片段。它还包括可用于身份验证的 Authelia。

### 🌐 NGINX

```nginx
location /metube/ {
        proxy_pass http://metube:8081;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
}
```

注意：额外的 `proxy_set_header` 指令是为了使 WebSocket 工作。

### 🌐 Apache

由 [PIE-yt](https://github.com/PIE-yt) 贡献。源代码在[这里](https://gist.github.com/PIE-yt/29e7116588379032427f5bd446b2cac4)。

```apache
# For putting in your Apache sites site.conf
# Serves MeTube under a /metube/ subdir (http://yourdomain.com/metube/)
<Location /metube/>
    ProxyPass http://localhost:8081/ retry=0 timeout=30
    ProxyPassReverse http://localhost:8081/
</Location>

<Location /metube/socket.io>
    RewriteEngine On
    RewriteCond %{QUERY_STRING} transport=websocket    [NC]
    RewriteRule /(.*) ws://localhost:8081/socket.io/$1 [P,L]
    ProxyPass http://localhost:8081/socket.io retry=0 timeout=30
    ProxyPassReverse http://localhost:8081/socket.io
</Location>
```

### 🌐 Caddy

以下示例 Caddyfile 在 [caddy](https://caddyserver.com) 后面设置反向代理。

```caddyfile
example.com {
  route /metube/* {
    uri strip_prefix metube
    reverse_proxy metube:8081
  }
}
```

## 🔄 更新 yt-dlp

为 MeTube 中实际视频下载提供动力的是 [yt-dlp](https://github.com/yt-dlp/yt-dlp)。由于视频网站经常更改其布局，需要频繁更新 yt-dlp 以跟上变化。

有一个自动的每日构建版本 MeTube，它会查找新版本的 yt-dlp，如果存在，构建会拉取它并发布更新的 docker 镜像。因此，为了跟上变化，建议您定期使用最新的镜像更新 MeTube 容器。

我建议为此目的安装和设置 [watchtower](https://github.com/containrrr/watchtower)。

## 🔧 故障排除和提交问题

在询问问题或为 MeTube 提交问题之前，请记住 MeTube 只是 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 的一个 UI。您可能遇到的任何关于视频网站身份验证、后处理、权限、其他似乎不起作用的 `YTDL_OPTIONS` 配置，或任何其他与底层 yt-dlp 库工作原理相关的问题，都不需要在 MeTube 项目上打开。为了调试和排除故障，建议先尝试直接使用 yt-dlp 二进制文件，绕过 UI，一旦它工作正常，将对您有效的选项导入到 `YTDL_OPTIONS` 中。

要直接使用 yt-dlp 命令进行测试，您可以下载它并在本地运行，或者为了更好地模拟其实际条件，您可以在 MeTube 容器本身中运行它。假设您的 MeTube 容器名为 `metube`，在您的 Docker 主机上运行以下命令以获取容器内的 shell：

```bash
docker exec -ti metube sh
cd /downloads
```

在那里，您可以自由使用 yt-dlp 命令。

## 💡 提交功能请求

MeTube 开发依赖于社区的代码贡献。该程序目前的版本适合我自己的用例，因此就我而言，功能已经完整。如果您的用例不同并且需要其他功能，请随时提交实现这些功能的 PR。建议首先创建一个问题来讨论计划的实现，因为为了减少臃肿，一些 PR 可能不会被接受。但是，请注意，当您不打算实现该功能时，打开功能请求很少会导致请求得到满足。

## 🛠️ 本地构建和运行

确保您已安装 Node.js 和 Python 3.13。

```bash
cd metube/ui
# 安装 Angular 并构建 UI
npm install
node_modules/.bin/ng build
# 安装 python 依赖
cd ..
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
# 运行
uv run python3 app/main.py
```

可以在本地构建 Docker 镜像（它也会构建 UI）：

```bash
docker build -t metube .
```

请注意，如果您在 VSCode 中运行服务器，您的下载将转到用户的 Downloads 文件夹（这是通过 `.vscode/launch.json` 中的环境配置的）。

## 🧪 测试身份验证功能

使用提供的测试脚本验证身份验证功能：

```bash
# 启动带身份验证的 MeTube
ENABLE_HTTP_AUTH=true HTTP_AUTH_USERNAME=testuser HTTP_AUTH_PASSWORD=testpass uv run python3 app/main.py

# 在另一个终端运行测试
python test_auth.py
```

详细配置说明请参考 `HTTP_AUTH_SETUP.md` 文档。

---

## 许可证

本项目遵循许可证文件中指定的许可证。