// GitHub Issues 评论系统
class GitHubIssuesComments {
    constructor() {
        this.owner = 'Heureka-L';
        this.repo = 'Heureka-L.github.io';
        this.currentPostId = this.getPostId();
        this.captchaAnswer = 0;
        this.init();
    }

    init() {
        this.generateCaptcha();
        this.bindEvents();
        this.loadComments();
    }

    getPostId() {
        const url = window.location.pathname;
        return url.replace(/\//g, '_').replace(/^_+|_+$/g, '') || 'home';
    }

    async loadComments() {
        try {
            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues?state=open&labels=comment:${this.currentPostId}`);
            if (!response.ok) throw new Error('加载评论失败');
            
            const issues = await response.json();
            const commentsContainer = document.getElementById('comments-list');
            
            if (commentsContainer) {
                commentsContainer.innerHTML = '';
                
                // 更新评论数量
                const countElement = document.getElementById('comments-count');
                if (countElement) {
                    countElement.textContent = issues.length;
                }

                for (const issue of issues) {
                    await this.renderComment(issue);
                }
            }
        } catch (error) {
            console.error('加载评论失败:', error);
            this.showError('加载评论失败，请稍后重试');
        }
    }

    async renderComment(issue) {
        try {
            // 获取评论内容
            const commentsResponse = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues/${issue.number}/comments`);
            const comments = await commentsResponse.json();
            
            const commentsContainer = document.getElementById('comments-list');
            if (!commentsContainer) return;

            // 创建评论项
            const commentItem = document.createElement('div');
            commentItem.className = 'comment-item';
            
            const author = issue.title.replace('Comment by ', '').split(' - ')[0];
            const content = issue.body;
            const date = new Date(issue.created_at).toLocaleString('zh-CN');

            commentItem.innerHTML = `
                <div class="comment-header">
                    <strong class="comment-author">${author}</strong>
                    <span class="comment-date">${date}</span>
                </div>
                <div class="comment-content">${this.escapeHtml(content)}</div>
            `;

            commentsContainer.appendChild(commentItem);

            // 渲染回复评论
            for (const reply of comments) {
                const replyItem = document.createElement('div');
                replyItem.className = 'comment-reply';
                replyItem.innerHTML = `
                    <div class="comment-header">
                        <strong class="comment-author">${reply.user.login}</strong>
                        <span class="comment-date">${new Date(reply.created_at).toLocaleString('zh-CN')}</span>
                    </div>
                    <div class="comment-content">${this.escapeHtml(reply.body)}</div>
                `;
                commentsContainer.appendChild(replyItem);
            }
        } catch (error) {
            console.error('渲染评论失败:', error);
        }
    }

    generateCaptcha() {
        const num1 = Math.floor(Math.random() * 9) + 1;
        const num2 = Math.floor(Math.random() * 9) + 1;
        this.captchaAnswer = num1 + num2;
        
        const questionSpan = document.getElementById('captcha-question');
        if (questionSpan) {
            questionSpan.textContent = `${num1} + ${num2} = ?`;
        }
        
        const answerInput = document.getElementById('captcha-answer');
        if (answerInput) {
            answerInput.value = '';
            answerInput.focus();
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

    async handleSubmit(event) {
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

        try {
            // 创建GitHub Issue
            const issueData = {
                title: `Comment by ${author} - ${this.currentPostId}`,
                body: content,
                labels: [`comment:${this.currentPostId}`, 'blog-comment']
            };

            const response = await fetch(`https://api.github.com/repos/${this.owner}/${this.repo}/issues`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(issueData)
            });

            if (response.ok) {
                this.showSuccess('评论发表成功！审核后显示');
                form.reset();
                this.generateCaptcha();
                setTimeout(() => this.loadComments(), 1000);
            } else {
                const error = await response.json();
                if (error.message.includes('rate limit')) {
                    this.showError('评论过于频繁，请稍后再试');
                } else {
                    this.showError('评论发表失败，请稍后重试');
                }
            }
        } catch (error) {
            console.error('发表评论失败:', error);
            this.showError('网络错误，请检查网络连接');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = '发表评论';
        }
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
    new GitHubIssuesComments();
});