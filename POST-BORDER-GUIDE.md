# 主页文章边框和背景样式指南

## 功能概述

为博客主页的每篇文章添加了圆角虚线黑色边框和淡蓝色背景，提供更好的视觉区分和美观效果。

## 样式详情

### 边框样式
```css
.post-preview {
    border: 2px dashed #000000;  /* 2px黑色虚线边框 */
    border-radius: 12px;         /* 12px圆角 */
    padding: 25px;              /* 内边距 */
    margin-bottom: 30px;        /* 文章间距 */
    background-color: rgba(227, 242, 253, 0.7);  /* 30%透明度的淡蓝色背景 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
```

### 内容层次样式
```css
.post-title {
    color: #1565c0;              /* 深蓝色标题 */
    font-weight: 700;
}

.post-subtitle {
    color: #1976d2;              /* 蓝色副标题 */
    font-weight: 500;
}

.post-content-preview {
    color: #333333;              /* 深灰色内容 */
    background-color: rgba(255, 255, 255, 0.5);  /* 白色半透明内衬 */
    border-left: 3px solid #1976d2;
}

.post-meta {
    color: #666666;              /* 中灰色元数据 */
    border-top: 1px dashed rgba(0, 0, 0, 0.2);
}
```

## 颜色方案

- **边框**: 黑色 (#000000) 虚线
- **背景**: 淡蓝色 (#e3f2fd) - 与Sidebar保持一致
- **标题**: 深蓝色 (#1565c0)
- **副标题**: 蓝色 (#1976d2)
- **内容**: 深灰色 (#333333)
- **元数据**: 中灰色 (#666666)

## 交互效果

### 悬停动画
- **轻微上浮**: transform: translateY(-2px)
- **阴影增强**: box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15)
- **边框加深**: border-color: #333333
- **标题变色**: color: #0d47a1

### 过渡效果
- 所有变化都有0.3秒的平滑过渡
- 使用CSS3硬件加速优化性能

## 响应式设计

### 桌面端 (≥768px)
- 边框宽度: 2px
- 内边距: 25px
- 圆角: 12px

### 移动端 (<768px)
- 边框宽度: 1px
- 内边距: 20px
- 圆角: 8px
- 内容内衬内边距: 12px

## 自定义修改

### 修改边框颜色
```css
.post-preview {
    border-color: #1976d2;  /* 改为蓝色虚线 */
}
```

### 修改背景颜色
```css
.post-preview {
    background-color: #f5f5f5;  /* 改为浅灰色 */
}
```

### 调整边框样式
```css
.post-preview {
    border-style: solid;  /* 改为实线 */
    border-width: 1px;      /* 改为1px */
    border-radius: 8px;     /* 改为8px圆角 */
}
```

### 修改悬停效果
```css
.post-preview:hover {
    transform: none;        /* 移除上浮效果 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  /* 减小阴影 */
}
```

## 浏览器兼容性

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+
- ✅ 移动端浏览器

## 性能优化

- 使用CSS3硬件加速
- 优化的阴影效果
- 最小化的重绘和重排
- 响应式断点优化

## 使用说明

### 自动应用
样式会自动应用到所有主页文章，无需额外配置。

### 验证效果
- 访问主页查看文章边框和背景效果
- 使用浏览器开发者工具检查元素
- 在不同设备上测试响应式效果

### 故障排除

#### 边框不显示
1. 检查CSS选择器是否正确
2. 确认样式没有被其他CSS覆盖
3. 清除浏览器缓存

#### 颜色不一致
1. 检查颜色值是否与Sidebar一致
2. 确认CSS优先级设置
3. 检查是否有内联样式冲突

#### 响应式问题
1. 检查媒体查询断点设置
2. 确认viewport meta标签
3. 测试不同屏幕尺寸

## 相关文件

- `_includes/head.html` - 包含所有样式定义
- `index.html` - 主页模板
- `test-post-borders.html` - 测试页面