# 背景图配置指南

## 整体背景图配置

### 全局背景图设置

在 `_config.yml` 中添加或修改 `bg-img` 配置：

```yaml
# 设置全局背景图
bg-img: img/bk3.jpg
```

### 文章级别背景图设置

在每篇文章的 Front Matter 中，可以单独设置背景图：

```yaml
---
layout: post
title: "文章标题"
bg-img: img/your-background.jpg
---
```

## 背景图文件位置

所有背景图文件都放在 `img/` 目录下，支持的图片格式：
- .jpg / .jpeg
- .png
- .gif

## 可用的背景图

当前项目中已有的背景图：
- `img/bk1.jpg`
- `img/bk2.png`
- `img/bk3.jpg`
- `img/home-bg.jpg`
- `img/post-bg-*.jpg` (各种主题背景)

## 使用示例

### 示例1：全局背景图
在 `_config.yml` 中设置：
```yaml
bg-img: img/home-bg.jpg
```

### 示例2：文章特定背景图
在文章头部设置：
```yaml
---
title: "我的技术文章"
bg-img: img/post-bg-tech.jpg
---
```

### 示例3：使用默认背景图
如果不设置 `bg-img`，则自动使用 `_config.yml` 中的全局背景图。

## 背景图样式

背景图采用以下样式：
- 固定背景（background-attachment: fixed）
- 居中显示（background-position: center）
- 覆盖整个页面（background-size: cover）
- 不重复（background-repeat: no-repeat）

## 注意事项

1. 建议使用高质量的图片作为背景图
2. 图片大小建议在 1920x1080 以上，确保在不同屏幕尺寸下都有良好效果
3. 避免使用过于复杂的图片，以免影响文字阅读
4. 可以调整图片的透明度或添加遮罩层来优化可读性

## 测试验证

可以在任意文章页面查看整体背景效果，背景图配置会自动生效。