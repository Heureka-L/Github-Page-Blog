# 自定义评论系统使用指南

## 功能特点

- ✅ **无需登录**：用户无需注册或登录即可发表评论
- ✅ **用户名验证**：要求用户必须填写用户名
- ✅ **人机验证**：使用简单的数学计算题进行验证
- ✅ **本地存储**：评论数据存储在浏览器本地存储中
- ✅ **响应式设计**：适配各种设备屏幕

## 文件结构

```
comment/
├── comments.json          # 评论数据文件（模板）
css/
├── comments.css           # 评论系统样式
js/
├── comments.js            # 评论系统主逻辑
_includes/
├── comments.html          # 评论系统HTML模板
```

## 本地测试

1. **启动本地服务器**：
   ```bash
   bundle exec jekyll serve --port=4000
   ```

2. **访问测试**：
   打开浏览器访问 `http://localhost:4000`

3. **测试评论功能**：
   - 在任意文章底部找到评论区
   - 填写用户名（必填）
   - 填写评论内容（必填）
   - 完成数学计算题验证
   - 点击"发表评论"按钮

## 人机验证说明

- 系统会随机生成简单的数学计算题
- 支持加法、减法、乘法运算
- 用户可以点击"换一题"按钮刷新题目
- 验证通过后才能提交评论

## 数据存储

- **GitHub Issues**：评论数据存储在GitHub Issues中
- **标签系统**：每篇文章的评论使用标签 `comment:文章ID` 进行分类
- **持久化**：评论永久保存在GitHub上，不受浏览器影响
- **公开可见**：所有评论都可在GitHub Issues中查看

## 自定义配置

在 `js/github-issues-comments.js` 中可以修改以下配置：

```javascript
// 修改仓库信息
this.owner = 'Heureka-L';
this.repo = 'Heureka-L.github.io';

// 修改用户名长度限制
author.length > 50

// 修改评论长度限制
content.length > 1000
```

## 注意事项

1. **GitHub API限制**：匿名用户每小时只能创建60个Issues
2. **审核机制**：所有评论需要通过GitHub Issues审核后显示
3. **浏览器兼容性**：支持现代浏览器（Chrome, Firefox, Safari, Edge）
4. **网络要求**：需要网络连接才能加载和提交评论
5. **隐私保护**：用户名和评论内容会公开在GitHub Issues中

## GitHub Issues配置

在GitHub仓库设置中：
1. 启用Issues功能
2. 配置Issues模板（可选）
3. 设置标签自动分类

## 评论审核流程

1. 用户提交评论
2. 系统自动创建GitHub Issue
3. 博主在GitHub Issues中审核
4. 审核通过后评论显示在网站上

## 查看所有评论

访问：https://github.com/Heureka-L/Heureka-L.github.io/issues
标签筛选：comment:文章ID