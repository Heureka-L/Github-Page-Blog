#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
博客管理工具 - PyQt版
基于文章发布指南的自动化管理脚本
"""

import sys
import os
import yaml
import re
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QComboBox, QDateEdit, QTabWidget,
                             QTableWidget, QTableWidgetItem, QMessageBox,
                             QFileDialog, QGroupBox, QFormLayout, QSplitter,
                             QCheckBox, QSpinBox)
from PyQt5.QtCore import Qt, QDate, QTimer
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
        
        # 快捷填充组
        quick_group = QGroupBox("快捷填充")
        quick_layout = QVBoxLayout()
        
        # 自动编号
        auto_layout = QHBoxLayout()
        self.auto_number = QCheckBox("自动编号")
        self.auto_number.setChecked(True)
        self.auto_number.toggled.connect(self.toggle_auto_number)
        auto_layout.addWidget(self.auto_number)
        
        self.chapter_spin = QSpinBox()
        self.chapter_spin.setRange(1, 20)
        self.chapter_spin.setValue(1)
        self.chapter_spin.setPrefix("第")
        self.chapter_spin.setSuffix("章")
        self.chapter_spin.valueChanged.connect(self.auto_fill_chapter)
        auto_layout.addWidget(QLabel("章节:"))
        auto_layout.addWidget(self.chapter_spin)
        
        self.section_spin = QSpinBox()
        self.section_spin.setRange(1, 10)
        self.section_spin.setValue(1)
        self.section_spin.valueChanged.connect(self.auto_fill_section)
        auto_layout.addWidget(QLabel("小节:"))
        auto_layout.addWidget(self.section_spin)
        quick_layout.addLayout(auto_layout)
        
        # 快捷填充按钮
        fill_buttons = QHBoxLayout()
        fill_chapter_btn = QPushButton("填充章节")
        fill_chapter_btn.clicked.connect(lambda: self.auto_fill_chapter_text())
        fill_buttons.addWidget(fill_chapter_btn)
        
        fill_section_btn = QPushButton("填充小节")
        fill_section_btn.clicked.connect(lambda: self.auto_fill_section_text())
        fill_buttons.addWidget(fill_section_btn)
        
        quick_layout.addLayout(fill_buttons)
        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)
        
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
        
        # 预览区域
        preview_group = QGroupBox("预览")
        preview_layout = QVBoxLayout()
        self.preview_text = QTextEdit()
        self.preview_text.setMaximumHeight(150)
        preview_layout.addWidget(self.preview_text)
        preview_group.setLayout(preview_layout)
        
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
        layout.addWidget(preview_group)
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
        """保存文章 - 完美匹配现有格式"""
        article_data = self.get_article_data()
        if not article_data:
            return
            
        try:
            # 生成标准格式的小节名称
            chapter_num = self.extract_chapter_number(article_data['chapter'])
            section_num = 1  # 默认小节编号
            
            # 根据章节和小节生成标准格式
            formatted_section = f"{chapter_num}.{section_num} {article_data['title']}"
            
            # 更新书籍数据
            self.update_books_data_exact(article_data, formatted_section)
            
            # 创建文章文件
            self.create_article_file_exact(article_data, formatted_section)
            
            QMessageBox.information(self, "成功", 
                                  f"文章已创建并更新书籍数据！\n"
                                  f"书籍：{article_data['book']}\n"
                                  f"章节：{article_data['chapter']}\n"
                                  f"小节：{formatted_section}")
            self.clear_form()
            self.refresh_data()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
            
    def extract_chapter_number(self, chapter_name):
        """提取章节数字"""
        match = re.search(r'第(\d+)章', chapter_name)
        return int(match.group(1)) if match else 1
        
    def generate_slug(self, title):
        """生成URL友好的slug"""
        # 简单的拼音转换映射
        pinyin_map = {
            'STM32': 'STM32', 'GPIO': 'GPIO', 'ADC': 'ADC', 'UART': 'UART',
            '定时器': 'timer', '配置': 'configuration', '详解': 'detailed',
            '标准库': 'standard-library', '外设': 'peripheral',
            '中断': 'interrupt', '输入': 'input', '输出': 'output',
            '模式': 'mode', '流程': 'process', '原理': 'principle',
            '二进制': 'binary', '浮点数': 'floating-point', '表示': 'representation'
        }
        
        slug = title.lower()
        for chinese, pinyin in pinyin_map.items():
            slug = slug.replace(chinese.lower(), pinyin)
        
        # 处理剩余字符
        slug = re.sub(r'[^a-zA-Z0-9\-]', '-', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        return slug
        
    def update_books_data_exact(self, article_data, formatted_section):
        """精确更新books.yml - 严格匹配现有格式"""
        book_name = article_data['book']
        chapter_name = article_data['chapter']
        section_name = article_data['title']
        
        # 生成URL友好的slug
        slug = self.generate_slug(section_name)
        date_path = article_data['date'].strftime('%Y/%m/%d')
        url_path = f"/{date_path}/{slug}/"
        
        # 查找或创建书籍
        book_found = False
        for book in self.books_data['books']:
            if book['name'] == book_name:
                book_found = True
                
                # 查找或创建章节
                chapter_found = False
                for chapter in book.get('chapters', []):
                    if chapter['name'] == chapter_name:
                        chapter_found = True
                        
                        # 确保sections存在
                        if 'sections' not in chapter:
                            chapter['sections'] = []
                            
                        # 检查是否已存在相同小节
                        section_exists = False
                        for section in chapter['sections']:
                            if section['name'] == formatted_section:
                                section_exists = True
                                # 更新URL和slug
                                section['slug'] = slug
                                section['url'] = url_path
                                break
                        
                        if not section_exists:
                            # 添加新小节 - 完全匹配现有格式
                            section_data = {
                                'name': formatted_section,
                                'slug': slug,
                                'url': url_path
                            }
                            chapter['sections'].append(section_data)
                        break
                
                if not chapter_found:
                    # 创建新章节 - 完全匹配现有格式
                    new_chapter = {
                        'name': chapter_name,
                        'sections': [{
                            'name': formatted_section,
                            'slug': slug,
                            'url': url_path
                        }]
                    }
                    if 'chapters' not in book:
                        book['chapters'] = []
                    book['chapters'].append(new_chapter)
                break
        
        if not book_found:
            # 创建新书籍 - 完全匹配现有格式
            new_book = {
                'name': book_name,
                'chapters': [{
                    'name': chapter_name,
                    'sections': [{
                        'name': formatted_section,
                        'slug': slug,
                        'url': url_path
                    }]
                }]
            }
            if 'books' not in self.books_data:
                self.books_data['books'] = []
            self.books_data['books'].append(new_book)
            
        # 写回文件 - 保持YAML格式一致
        with open(self.books_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.books_data, f, allow_unicode=True, 
                     default_flow_style=False, sort_keys=False)
            
    def create_article_file_exact(self, article_data, formatted_section):
        """创建文章文件 - 完美匹配现有格式"""
        date_str = article_data['date'].strftime('%Y-%m-%d')
        title_slug = self.generate_slug(article_data['title'])
        filename = f"{date_str}-{title_slug}.md"
        filepath = os.path.join(self.posts_dir, filename)
        
        # 生成章节信息
        chapter_match = re.search(r'第(\d+)章', article_data['chapter'])
        chapter_num = chapter_match.group(1) if chapter_match else "1"
        
        # 生成标准YAML前置数据
        yaml_header = f"""---
layout: book
title: "{article_data['title']}"""
        
        if article_data['subtitle']:
            yaml_header += f'\nsubtitle: "{article_data["subtitle"]}"'
            
        yaml_header += f"""
date: {article_data['date'].strftime('%Y-%m-%d %H:%M:%S')}
author: Heureka
book: "{article_data['book']}"
chapter: "第{chapter_num}章"
section: "{formatted_section}"
tags: 
{chr(10).join([f'    - {tag.strip()}' for tag in article_data['tags'].split(',')]) if article_data['tags'] != 'General' else '    - 未分类'}
---

## {article_data['title']}

### 1. 简介

### 2. 实现步骤

### 3. 代码示例

### 4. 注意事项

### 5. 扩展应用
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_header)
            
    def clear_form(self):
        """清空表单"""
        self.title_input.clear()
        self.subtitle_input.clear()
        self.chapter_input.clear()
        self.section_input.clear()
        self.tags_input.clear()
        self.content_text.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.preview_text.clear()
        
    def toggle_auto_number(self, checked):
        """切换自动编号状态"""
        self.chapter_spin.setEnabled(checked)
        self.section_spin.setEnabled(checked)
        
    def auto_fill_chapter(self, value):
        """自动填充章节"""
        if self.auto_number.isChecked():
            self.chapter_input.setText(f"第{value}章")
            
    def auto_fill_section(self, value):
        """自动填充小节"""
        if self.auto_number.isChecked():
            chapter_num = self.chapter_spin.value()
            self.section_input.setText(f"{chapter_num}.{value}")
            
    def auto_fill_chapter_text(self):
        """手动填充章节"""
        chapter_num = self.chapter_spin.value()
        self.chapter_input.setText(f"第{chapter_num}章")
        
    def auto_fill_section_text(self):
        """手动填充小节"""
        chapter_num = self.chapter_spin.value()
        section_num = self.section_spin.value()
        self.section_input.setText(f"{chapter_num}.{section_num}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 设置中文字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    
    manager = BlogManager()
    manager.show()
    sys.exit(app.exec_())