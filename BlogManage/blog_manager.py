#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客管理工具 - PyQt版
基于文章发布指南的自动化管理脚本
"""

import sys
import os
import yaml
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QComboBox, QDateEdit, QTabWidget,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QFileDialog, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class BlogManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.books_file = os.path.join(self.project_root, '_data', 'books.yml')
        self.posts_dir = os.path.join(self.project_root, '_posts')
        
        self.init_ui()
        self.load_books_data()
        
    def init_ui(self):
        self.setWindowTitle('博客文章管理器')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建标签页
        self.tabs = QTabWidget()
        self.create_overview_tab()
        self.create_add_article_tab()
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        main_widget.setLayout(layout)
        
    def create_overview_tab(self):
        """创建概览标签页"""
        overview_widget = QWidget()
        layout = QHBoxLayout()
        
        # 左侧书籍列表
        left_group = QGroupBox("书籍列表")
        left_layout = QVBoxLayout()
        
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(3)
        self.books_table.setHorizontalHeaderLabels(['书籍名称', '章节数', '文章总数'])
        self.books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.books_table.itemClicked.connect(self.show_book_details)
        
        left_layout.addWidget(self.books_table)
        left_group.setLayout(left_layout)
        
        # 右侧详情
        right_group = QGroupBox("详细信息")
        right_layout = QVBoxLayout()
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        right_layout.addWidget(self.details_text)
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新数据")
        refresh_btn.clicked.connect(self.refresh_data)
        right_layout.addWidget(refresh_btn)
        
        right_group.setLayout(right_layout)
        
        layout.addWidget(left_group, 1)
        layout.addWidget(right_group, 2)
        overview_widget.setLayout(layout)
        
        self.tabs.addTab(overview_widget, "文章概览")
        
    def create_add_article_tab(self):
        """创建添加文章标签页"""
        add_widget = QWidget()
        layout = QVBoxLayout()
        
        # 文章信息表单
        form_group = QGroupBox("文章信息")
        form_layout = QFormLayout()
        
        self.book_combo = QComboBox()
        self.book_combo.setEditable(True)
        self.book_combo.setPlaceholderText("选择或输入书籍名称")
        
        self.chapter_input = QLineEdit()
        self.chapter_input.setPlaceholderText("例如：第1章")
        
        self.section_input = QLineEdit()
        self.section_input.setPlaceholderText("例如：1.1")
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("文章标题")
        
        self.subtitle_input = QLineEdit()
        self.subtitle_input.setPlaceholderText("副标题（可选）")
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("标签，用逗号分隔")
        
        self.content_text = QTextEdit()
        self.content_text.setPlaceholderText("文章内容（支持Markdown格式）")
        
        form_layout.addRow("书籍：", self.book_combo)
        form_layout.addRow("章节：", self.chapter_input)
        form_layout.addRow("小节：", self.section_input)
        form_layout.addRow("标题：", self.title_input)
        form_layout.addRow("副标题：", self.subtitle_input)
        form_layout.addRow("日期：", self.date_edit)
        form_layout.addRow("标签：", self.tags_input)
        form_layout.addRow("内容：", self.content_text)
        
        form_group.setLayout(form_layout)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        preview_btn = QPushButton("预览")
        preview_btn.clicked.connect(self.preview_article)
        
        save_btn = QPushButton("保存文章")
        save_btn.clicked.connect(self.save_article)
        
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_form)
        
        button_layout.addWidget(preview_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        
        layout.addWidget(form_group)
        layout.addLayout(button_layout)
        add_widget.setLayout(layout)
        
        self.tabs.addTab(add_widget, "添加文章")
        
    def load_books_data(self):
        """加载书籍数据"""
        try:
            with open(self.books_file, 'r', encoding='utf-8') as f:
                self.books_data = yaml.safe_load(f) or {'books': []}
            self.update_books_list()
        except Exception as e:
            QMessageBox.warning(self, "警告", f"加载书籍数据失败: {str(e)}")
            self.books_data = {'books': []}
            
    def update_books_list(self):
        """更新书籍下拉列表"""
        self.book_combo.clear()
        book_names = [book['name'] for book in self.books_data['books']]
        self.book_combo.addItems(book_names)
        
    def refresh_data(self):
        """刷新数据"""
        self.load_books_data()
        self.display_books_overview()
        
    def display_books_overview(self):
        """显示书籍概览"""
        self.books_table.setRowCount(0)
        
        for book in self.books_data['books']:
            row = self.books_table.rowCount()
            self.books_table.insertRow(row)
            
            # 计算章节数和文章数
            chapter_count = len(book.get('chapters', []))
            article_count = sum(len(chapter.get('sections', [])) 
                              for chapter in book.get('chapters', []))
            
            self.books_table.setItem(row, 0, QTableWidgetItem(book['name']))
            self.books_table.setItem(row, 1, QTableWidgetItem(str(chapter_count)))
            self.books_table.setItem(row, 2, QTableWidgetItem(str(article_count)))
            
    def show_book_details(self, item):
        """显示书籍详情"""
        row = item.row()
        book_name = self.books_table.item(row, 0).text()
        
        for book in self.books_data['books']:
            if book['name'] == book_name:
                details = f"书籍名称: {book['name']}\n"
                details += f"章节数量: {len(book.get('chapters', []))}\n"
                details += f"文章总数: {sum(len(chapter.get('sections', [])) for chapter in book.get('chapters', []))}\n\n"
                
                details += "章节详情:\n"
                for i, chapter in enumerate(book.get('chapters', []), 1):
                    details += f"  {chapter['name']} ({len(chapter.get('sections', []))}篇文章)\n"
                    for section in chapter.get('sections', []):
                        details += f"    - {section['name']}\n"
                        
                self.details_text.setPlainText(details)
                break
                
    def preview_article(self):
        """预览文章"""
        article_data = self.get_article_data()
        if not article_data:
            return
            
        preview_text = f"""---
layout: book
title: "{article_data['title']}"
"""
        
        if article_data['subtitle']:
            preview_text += f"subtitle: {article_data['subtitle']}\n"
            
        preview_text += f"""date: {article_data['date'].strftime('%Y-%m-%d %H:%M:%S')}
author: Heureka
book: "{article_data['book']}"
chapter: "{article_data['chapter']}"
section: "{article_data['section']}"
tags: 
    - {article_data['tags']}
---

{article_data['content']}
"""
        
        QMessageBox.information(self, "文章预览", preview_text)
        
    def get_article_data(self):
        """获取文章数据"""
        book = self.book_combo.currentText().strip()
        chapter = self.chapter_input.text().strip()
        section = self.section_input.text().strip()
        title = self.title_input.text().strip()
        
        if not all([book, chapter, section, title]):
            QMessageBox.warning(self, "警告", "请填写所有必填字段")
            return None
            
        return {
            'book': book,
            'chapter': chapter,
            'section': section,
            'title': title,
            'subtitle': self.subtitle_input.text().strip(),
            'date': self.date_edit.date().toPyDate(),
            'tags': self.tags_input.text().strip() or 'General',
            'content': self.content_text.toPlainText().strip()
        }
        
    def save_article(self):
        """保存文章"""
        article_data = self.get_article_data()
        if not article_data:
            return
            
        try:
            # 更新书籍数据
            self.update_books_data(article_data)
            
            # 创建文章文件
            self.create_article_file(article_data)
            
            QMessageBox.information(self, "成功", "文章已创建并更新书籍数据！")
            self.clear_form()
            self.refresh_data()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
            
    def update_books_data(self, article_data):
        """更新书籍数据"""
        book_name = article_data['book']
        chapter_name = article_data['chapter']
        section_name = article_data['title']
        
        # 查找或创建书籍
        book = None
        for b in self.books_data['books']:
            if b['name'] == book_name:
                book = b
                break
                
        if not book:
            book = {'name': book_name, 'chapters': []}
            self.books_data['books'].append(book)
            
        # 查找或创建章节
        chapter = None
        for c in book['chapters']:
            if c['name'] == chapter_name:
                chapter = c
                break
                
        if not chapter:
            chapter = {'name': chapter_name, 'sections': []}
            book['chapters'].append(chapter)
            
        # 添加小节
        section_slug = section_name.lower().replace(' ', '-')
        section_url = f"/2025/{article_data['date'].strftime('%m/%d')}/{section_slug}/"
        
        # 检查是否已存在
        for s in chapter['sections']:
            if s['name'] == section_name:
                s['url'] = section_url
                break
        else:
            chapter['sections'].append({
                'name': section_name,
                'url': section_url
            })
            
        # 保存到文件
        with open(self.books_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.books_data, f, allow_unicode=True, default_flow_style=False)
            
    def create_article_file(self, article_data):
        """创建文章文件"""
        date_str = article_data['date'].strftime('%Y-%m-%d')
        title_slug = article_data['title'].lower().replace(' ', '-')
        filename = f"{date_str}-{title_slug}.md"
        filepath = os.path.join(self.posts_dir, filename)
        
        content = f"""---
layout: book
title: "{article_data['title']}"
"""
        
        if article_data['subtitle']:
            content += f"subtitle: {article_data['subtitle']}\n"
            
        content += f"""date: {article_data['date'].strftime('%Y-%m-%d %H:%M:%S')}
author: Heureka
book: "{article_data['book']}"
chapter: "{article_data['chapter']}"
section: "{article_data['section']}"
tags: 
    - {article_data['tags']}
---

{article_data['content']}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def clear_form(self):
        """清空表单"""
        self.title_input.clear()
        self.subtitle_input.clear()
        self.chapter_input.clear()
        self.section_input.clear()
        self.tags_input.clear()
        self.content_text.clear()
        self.date_edit.setDate(QDate.currentDate())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 设置中文字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    manager = BlogManager()
    manager.show()
    sys.exit(app.exec_())