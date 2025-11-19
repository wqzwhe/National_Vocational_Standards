# 国家职业标准检索与下载（前后端分离）

本项目实现“国家职业标准”关键词检索与 PDF 下载，采用前后端分离架构：
- 前端：Vue 2.7 + Element‑UI，现代卡片式界面，移动端友好
- 后端：Flask（Python 3），代理官方接口并拼接 PDF 直链
- 安全：搜索需通过图片验证码校验，有效期 120 秒

---

## 快速开始

- 后端启动
  ```bash
  cd /Users/wuzihao/PycharmProjects/pythonProject/国家职业标准
  pip install -r requirements.txt
  python app.py  # 开发模式，监听 0.0.0.0:5050
  # 生产推荐
  pip install gunicorn
  gunicorn -w 2 -b 0.0.0.0:5050 app:app
  ```

- 前端开发
  ```bash
  cd frontend-spa
  npm install
  npm run dev  # 开发调试
  npm run build  # 生成 dist 静态资源
  ```

---

## 目录结构

```
国家职业标准/
├── app.py                # 后端入口（Flask API）
├── requirements.txt      # 后端依赖（Flask、requests、Pillow）
└── frontend-spa/         # 前端工程（Vite + Vue2 + Element‑UI）
    ├── src/App.vue
    ├── src/components/SearchList.vue
    ├── index.html
    └── dist/             # 构建输出（用于部署）
```

---

## 后端 API 文档

- 健康检查
  - `GET /` → `{ "msg": "backend_ok" }`

- 获取图片验证码
  - `GET /api/captcha/new`
  - 响应：
    ```json
    { "code": 200, "msg": "OK", "body": { "id": "<captcha_id>", "image": "data:image/png;base64,..." } }
    ```
  - 说明：验证码由 5 位字母数字组成，大小写不敏感，有效期 120 秒。

- 搜索职业标准
  - `GET /api/search`
  - 请求参数：
    - `q`：关键词（必填）
    - `pageNum`：页码（默认 1）
    - `pageSize`：每页数量（默认 10）
    - `captchaId`：验证码 ID（必填）
    - `captchaAnswer`：验证码答案（必填）
  - 响应：
    ```json
    {
      "code": 200,
      "msg": "OK",
      "body": {
        "list": [ { "name": "...", "code": "...", "issueTime": "YYYY-MM-DD ...", "standardInfoName": "...", "downloadUrl": "http://osta.mohrss..." } ],
        "total": 123,
        "pageNum": 1,
        "pages": 13
      }
    }
    ```
  - 特性：当返回项包含 `standardInfo` 时，服务端自动拼接成可下载直链 `downloadUrl`。

- 关键代码位置
  - 验证码生成：`/Users/wuzihao/PycharmProjects/pythonProject/国家职业标准/app.py:58`
  - 搜索接口验证码校验：`/Users/wuzihao/PycharmProjects/pythonProject/国家职业标准/app.py:72`
  - 直链拼接：`/Users/wuzihao/PycharmProjects/pythonProject/国家职业标准/app.py:99`
  - CORS 处理：`/Users/wuzihao/PycharmProjects/pythonProject/国家职业标准/app.py:108`

---

## 前端使用说明

- 首屏点击“开始搜索”进入搜索界面
- 输入关键词后点击“搜索”，弹出图片验证码
  - 支持“看不清，换一张”，自动聚焦输入框
- 验证通过后显示卡片列表，宽屏自动多列
- 下载按钮固定在卡片左下角

- 关键代码位置
  - 打开验证码弹窗：`frontend-spa/src/components/SearchList.vue:9,15,82`
  - 验证码弹窗模板：`frontend-spa/src/components/SearchList.vue:51`
  - 刷新验证码：`frontend-spa/src/components/SearchList.vue:100`
  - 搜索与错误处理：`frontend-spa/src/components/SearchList.vue:120`

---

## 1Panel/Nginx 部署参考

- 前端（静态站点，监听 8080）：
  - 将 `frontend-spa/dist` 上传至站点根目录（例如 `/www/sites/gbxz.wzhcn.cn/index`）
  - Nginx 站点配置示例：
    ```nginx
    server {
      listen 8080;
      server_name www.wzhcn.cn ip;
      root /www/sites/gbxz.wzhcn.cn/index;
      index index.html;

      location / { try_files $uri $uri/ /index.html; }

      location /api/ {
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_pass http://127.0.0.1:5050;
      }
    }
    ```

- 后端（容器方式）
  - 挂载后端目录（含 `app.py` 与 `requirements.txt`）到容器 `/app`
  - 启动命令：
    ```bash
    pip install -r requirements.txt && gunicorn -w 2 -b 0.0.0.0:5050 app:app
    ```
  - 发布端口 `5050:5050`，并确保 Nginx 反代到 `127.0.0.1:5050`

---

## 常见问题与排查

- 502 Bad Gateway
  - 检查后端是否在 `0.0.0.0:5050` 监听并对外发布
  - 确认 Nginx `location /api/ { proxy_pass http://127.0.0.1:5050; }`
  - URL 末尾不要包含中文标点（如 `pageSize=10。`）

- 前端路由 404
  - 加入 `try_files $uri $uri/ /index.html;` 以支持 SPA 回退

- 验证码无法输入
  - 弹窗使用 `append-to-body` 并自动聚焦输入框；保持页面未处于 loading 状态

- 验证码错误或过期
  - 服务端返回 `400` 与 `captcha_invalid`；前端自动刷新验证码并提示重试

---

## 安全提示

- 验证码仅用于基础防刷，请避免在高并发场景直接暴露后端接口
- 如需更强对抗（扭曲文字、更多噪点、滑块/行为验证、签名令牌），可在此基础上扩展

---

## 许可与贡献

- 仅用于学习与演示；如需商用或公开部署，请遵循相关法规与目标网站的使用条款
- 欢迎提交优化建议（UI 细节、性能、验证码增强、部署脚本）

---

## 附：示例请求

- 获取验证码
  ```bash
  curl -i http://127.0.0.1:5050/api/captcha/new
  ```

- 搜索（需替换 `<id>` 与 `<ans>`）
  ```bash
  curl -i "http://127.0.0.1:5050/api/search?q=计算机&pageNum=1&pageSize=10&captchaId=<id>&captchaAnswer=<ans>"
  ```
