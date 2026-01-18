# GitHub 推送指南

本地 Git 提交已完成！现在需要将代码推送到 GitHub。

## 步骤 1: 在 GitHub 上创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `live-stream-scrolling-ad-tool` (或你喜欢的名称)
   - **Description**: `直播间滚动字幕广告工具 - 支持无缝循环滚动、透明背景、字体颜色自定义`
   - **Visibility**: 选择 Public (开源) 或 Private (私有)
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
3. 点击 "Create repository"

## 步骤 2: 添加远程仓库并推送

创建仓库后，GitHub 会显示推送命令。在项目目录下执行以下命令：

### 如果使用 HTTPS（推荐，简单）：

```bash
# 添加远程仓库（将 YOUR_USERNAME 替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/live-stream-scrolling-ad-tool.git

# 推送代码到 GitHub
git push -u origin main
```

### 如果使用 SSH（需要配置 SSH 密钥）：

```bash
# 添加远程仓库（将 YOUR_USERNAME 替换为你的 GitHub 用户名）
git remote add origin git@github.com:YOUR_USERNAME/live-stream-scrolling-ad-tool.git

# 推送代码到 GitHub
git push -u origin main
```

## 步骤 3: 验证推送

推送成功后，访问你的 GitHub 仓库页面，应该能看到所有文件已经上传。

## 常见问题

### Q: 提示需要身份验证？
A: 如果使用 HTTPS，GitHub 现在要求使用 Personal Access Token 而不是密码。
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 选择权限：至少勾选 `repo`
   - 生成后复制 token，在推送时使用 token 作为密码

### Q: 提示权限被拒绝？
A: 检查：
   - 远程仓库 URL 是否正确
   - 是否有推送权限
   - SSH 密钥是否正确配置（如果使用 SSH）

### Q: 想修改远程仓库地址？
A: 使用命令：
```bash
git remote set-url origin NEW_URL
```

## 后续更新

以后修改代码后，使用以下命令推送：

```bash
git add .
git commit -m "更新说明"
git push
```
