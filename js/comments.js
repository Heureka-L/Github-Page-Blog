// 自定义评论系统
class CommentSystem {
    constructor() {
        this.commentsData = {};
        this.currentPostId = this.getPostId();
        this.captchaAnswer = 0;
        this.init();
    }

    init() {
        this.loadComments();
        this.bindEvents();
        this.generateCaptcha();
        this.renderComments();
    }

    getPostId() {
        const url = window.location.pathname;
        return url.replace(/\//g, '_').replace(/^_+|_+$/g, '') || 'home';
    }

    loadComments() {
        try {
            const localComments = localStorage.getItem('comments_' + this.currentPostId);
            if (localComments) {
                this.commentsData[this.currentPostId] = JSON.parse(localComments);
            } else {
                this.commentsData[this.currentPostId] = [];
            }
            this.renderComments();
        } catch (error) {
            console.error('加载评论失败:', error);
            this.commentsData[this.currentPostId] = [];
        }
    }

    saveComments() {
        try {
            localStorage.setItem('comments_' + this.currentPostId, 
                JSON.stringify(this.commentsData[this.currentPostId] || []));
            return true;
        } catch (error) {
            console.error('保存评论失败:', error);
            return false;
        }
    }

    generateCaptcha() {
        const operations = [
            { fn: (a, b) => a + b, symbol: '+' },
            { fn: (a, b) => a - b, symbol: '-' },
            { fn: (a, b) => a * b, symbol: '×' }
        ];
        
        const operation = operations[Math.floor(Math.random() * operations.length)];
        let a, b;
        
        if (operation.symbol === '×') {
            a = Math.floor(Math.random() * 10) + 1;
            b = Math.floor(Math.random() * 10) + 1;
        } else {
            a = Math.floor(Math.random() * 20) + 1;
            b = Math.floor(Math.random() * 20) + 1;
            
            // 确保减法结果为正
            if (operation.symbol === '-' && a < b) {
                [a, b] = [b, a];
            }
        }
        
        this.captchaAnswer = operation.fn(a, b);
        
        const questionSpan = document.getElementById('captcha-question');
        if (questionSpan) {
            questionSpan.textContent = `${a} ${operation.symbol} ${b} = ?`;
        }
        
        const answerInput = document.getElementById('captcha-answer');
        if (answerInput) {
            answerInput.value = '';
            answerInput.dataset.answer = this.captchaAnswer;
        }
    }

    bindEvents() {
        const form = document.getElementById('comment-form');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSubmit(e);
            });
        }

        const refreshBtn = document.getElementById('refresh-captcha');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.generateCaptcha();
            });
        }
    }

    handleSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('.submit-btn');
        const errorDiv = document.getElementById('comment-error');
        const successDiv = document.getElementById('comment-success');

        // 清除之前的消息
        if (errorDiv) {
            errorDiv.style.display = 'none';
            errorDiv.textContent = '';
        }
        if (successDiv) {
            successDiv.style.display = 'none';
            successDiv.textContent = '';
        }

        // 获取表单数据
        const author = form.querySelector('#comment-author').value.trim();
        const content = form.querySelector('#comment-content').value.trim();
        const captchaAnswer = parseInt(form.querySelector('#captcha-answer').value);

        // 验证输入
        if (!author) {
            this.showError('请输入用户名');
            return;
        }

        if (author.length > 50) {
            this.showError('用户名不能超过50个字符');
            return;
        }

        if (!content) {
            this.showError('请输入评论内容');
            return;
        }

        if (content.length > 1000) {
            this.showError('评论内容不能超过1000个字符');
            return;
        }

        if (isNaN(captchaAnswer) || captchaAnswer !== this.captchaAnswer) {
            this.showError('人机验证答案错误，请重新计算');
            this.generateCaptcha();
            return;
        }

        // 禁用提交按钮
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> 提交中...';

        // 创建新评论
        const newComment = {
            id: Date.now(),
            author: author,
            content: content,
            date: new Date().toISOString(),
            postId: this.currentPostId
        };

        // 保存评论
        if (!this.commentsData[this.currentPostId]) {
            this.commentsData[this.currentPostId] = [];
        }
        this.commentsData[this.currentPostId].unshift(newComment);

        const saved = this.saveComments();
        
        if (saved) {
            this.showSuccess('评论发表成功！');
            form.reset();
            this.generateCaptcha();
            this.renderComments();
        } else {
            this.showError('评论发表失败，请稍后重试');
        }

        // 恢复提交按钮
        submitBtn.disabled = false;
        submitBtn.textContent = '发表评论';
    }

    renderComments() {
        const container = document.getElementById('comment-list');
        if (!container) return;

        const comments = this.commentsData[this.currentPostId] || [];
        
        if (comments.length === 0) {
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
                <span class="comment-date">${formattedDate}</span>
            </div>
            <div class="comment-content">${this.escapeHtml(comment.content)}</div>
        `;

        return div;
    }

    showError(message) {
        const errorDiv = document.getElementById('comment-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    showSuccess(message) {
        const successDiv = document.getElementById('comment-success');
        if (successDiv) {
            successDiv.textContent = message;
            successDiv.style.display = 'block';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 初始化评论系统
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('comment-section')) {
        new CommentSystem();
    }
});

// 由于GitHub Pages限制，使用localStorage作为临时存储
function loadLocalComments() {
    const commentSystem = new CommentSystem();
    const localComments = localStorage.getItem('comments_' + commentSystem.currentPostId);
    if (localComments) {
        commentSystem.commentsData[commentSystem.currentPostId] = JSON.parse(localComments);
        commentSystem.renderComments();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', loadLocalComments);