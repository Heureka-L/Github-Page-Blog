---
layout: null
---
// 这是一个模拟的评论API，用于GitHub Pages
// 实际使用时需要替换为真实的后端服务

const fs = require('fs');
const path = require('path');

// 评论数据文件路径
const commentsFile = path.join(__dirname, '..', 'comment', 'comments.json');

// 获取评论
function getComments(postId) {
    try {
        const data = JSON.parse(fs.readFileSync(commentsFile, 'utf8'));
        return data.comments[postId] || [];
    } catch (error) {
        return [];
    }
}

// 添加评论
function addComment(postId, comment) {
    try {
        let data = { comments: {} };
        if (fs.existsSync(commentsFile)) {
            data = JSON.parse(fs.readFileSync(commentsFile, 'utf8'));
        }
        
        if (!data.comments[postId]) {
            data.comments[postId] = [];
        }
        
        const newComment = {
            id: Date.now(),
            author: comment.author,
            content: comment.content,
            date: new Date().toISOString(),
            postId: postId
        };
        
        data.comments[postId].unshift(newComment);
        fs.writeFileSync(commentsFile, JSON.stringify(data, null, 2));
        
        return newComment;
    } catch (error) {
        throw error;
    }
}

// 导出函数（供Jekyll使用）
module.exports = {
    getComments,
    addComment
};