#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""페이지 라우트 Blueprint - About, Design, Contact 등 정적 페이지"""

from flask import Blueprint, render_template

# Blueprint 생성
pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/about')
def about():
    """About 페이지"""
    return render_template('pages/about.html')


@pages_bp.route('/design')
def design():
    """Design 페이지"""
    return render_template('pages/design.html')


@pages_bp.route('/contact')
def contact():
    """Contact 페이지"""
    return render_template('pages/contact.html')


@pages_bp.route('/main')
def main():
    """Main 페이지"""
    return render_template('pages/main.html')

