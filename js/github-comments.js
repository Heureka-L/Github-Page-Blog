// GitHub Issues评论系统
// 使用GitHub Issues作为评论存储后端
class GitHubComments {
    constructor() {
        this.owner = 'Heureka-L'; // 替换为你的GitHub用户名
        this.repo = 'Heureka-L.github.io'; // 替换为你的仓库名
        this.postId = this.getPostId();
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadComments();
    }

    getPostId() {
        const url = window.location.pathname;
        return url.replace(/\//g, '_').replace(/^_+|_+$/g, '') || 'home';
    }

    getIssueTitle() {
        const title = document.querySelector('h1.post-title')?.textContent || 
                     document.title || 
                     'Untitled Post';
        return `Comments for: ${title}`;
    }

    async createIssueIfNotExists() {
        try {
            // 检查是否已存在该文章的issue
            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues?state=open&labels=comment,${this.postId}`, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json'
                }
            });
            
            const issues = await response.json();
            
            if (issues.length > 0) {
                return issues[0].number;
            }
            
            // 创建新的issue
            const createResponse = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    title: this.getIssueTitle(),
                    body: `这是文章 "${this.getIssueTitle()}" 的评论线程。\n\n文章链接: ${window.location.href}`,
                    labels: ['comment', this.postId]
                })
            });
            
            const newIssue = await createResponse.json();
            return newIssue.number;
            
        } catch (error) {
            console.error('创建issue失败:', error);
            return null;
        }
    }

    async loadComments() {
        try {
            const issueNumber = await this.createIssueIfNotExists();
            if (!issueNumber) {
                this.showLocalComments();
                return;
            }

            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues/${issueNumber}/comments`, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json'
                }
            });
            
            const comments = await response.json();
            this.renderComments(comments);
            
        } catch (error) {
            console.error('加载评论失败:', error);
            this.showLocalComments();
        }
    }

    async submitComment(author, content) {
        try {
            const issueNumber = await this.createIssueIfNotExists();
            if (!issueNumber) {
                throw new Error('无法创建评论issue');
            }

            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues/${issueNumber}/comments`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    body: `**${author}** 说：\n\n${content}`
                })
            });
            
            if (response.ok) {
                this.loadComments(); // 重新加载评论
                return true;
            } else {
                throw new Error('提交评论失败');
            }
            
        } catch (error) {
            console.error('提交评论失败:', error);
            // 回退到本地存储
            this.saveLocalComment(author, content);
            return false;
        }
    }

    renderComments(comments) {
        const container = document.getElementById('comment-list');
        if (!container) return;

        if (!comments || comments.length === 0) {
            container.innerHTML = '<p>暂无评论，快来发表第一条评论吧！</p>';
            return;
        }

        container.innerHTML = '';
        comments.forEach(comment => {
            const commentEl = this.createCommentElement(comment);
            container.appendChild(commentEl);
        });
    }

    createCommentElement(comment) {
        const div = document.createElement('div');
        div.className = 'comment-item';
        
        const date = new Date(comment.created_at);
        const formattedDate = date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });

        // 解析GitHub评论格式
        const body = comment.body;
        const authorMatch = body.match(/^\*\*(.*?)\*\* 说：/);
        const author = authorMatch ? authorMatch[1] : comment.user.login;
        const content = body.replace(/^\*\*.*?\*\* 说：\n\n/, '');

        div.innerHTML = `
            <div class="comment-header">
                <span class="comment-author">${author}</span>
                <span class="comment-date">${formattedDate}</span>
            </div>
            <div class="comment-content">${this.escapeHtml(content)}</div>
        `;

        return div;
    }

    // 本地存储作为回退方案
    saveLocalComment(author, content) {
        const key = `local_comments_${this.postId}`;
        const localComments = JSON.parse(localStorage.getItem(key) || '[]');
        
        localComments.unshift({
            id: Date.now(),
            author: author,
            content: content,
            date: new Date().toISOString(),
            user: { login: 'local' }
        });
        
        localStorage.setItem(key, JSON.stringify(localComments));
        this.showLocalComments();
    }

    showLocalComments() {
        const key = `local_comments_${this.postId}`;
        const localComments = JSON.parse(localStorage.getItem(key) || '[]');
        
        const container = document.getElementById('comment-list');
        if (!container) return;

        if (localComments.length === 0) {
            container.innerHTML = '<p>暂无评论，快来发表第一条评论吧！</p>';
            return;
        }

        container.innerHTML = '';
        localComments.forEach(comment => {
            const commentEl = this.createLocalCommentElement(comment);
            container.appendChild(commentEl);
        });
    }

    createLocalCommentElement(comment) {
        const div = document.createElement('div');
        div.className = 'comment-item';
        
        const date = new Date(comment.date);
        const formattedDate = date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });

        div.innerHTML = `
            <div class="comment-header">
                <span class="comment-author">${this.escapeHtml(comment.author)}</span>
                <span class="comment-date">${formattedDate} (本地存储)</span>
            </div>
            <div class="comment-content">${this.escapeHtml(comment.content)}</div>
        `;

        return div;
    }

    bindEvents() {
        const form = document.getElementById('comment-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const author = form.querySelector('#comment-author').value.trim();
                const content = form.querySelector('#comment-content').value.trim();
                const recaptchaResponse = form.querySelector('#g-recaptcha-response')?.value;

                if (!author) {
                    alert('请输入用户名');
                    return;
                }

                if (!content) {
                    alert('请输入评论内容');
                    return;
                }

                if (!recaptchaResponse) {
                    alert('请完成人机验证');
                    return;
                }

                const submitBtn = form.querySelector('.submit-btn');
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loading"></span> 提交中...';

                const success = await this.submitComment(author, content);
                
                if (success) {
                    form.reset();
                    grecaptcha.reset();
                    alert('评论发表成功！');
                } else {
                    alert('评论发表失败，已保存到本地存储');
                }

                submitBtn.disabled = false;
                submitBtn.textContent = '发表评论';
            });
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初始化GitHub评论系统
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('comment-section')) {
        new GitHubComments();
    }
});