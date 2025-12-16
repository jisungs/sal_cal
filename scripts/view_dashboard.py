#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""대시보드 GUI 뷰어 - 모던 디자인 적용"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageDraw, ImageTk
import math

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from excel_handler import ExcelHandler
from dashboard import Dashboard
from utils import mask_resident_number

# 모던 색상 팔레트 (Phase 1)
MODERN_COLORS = {
    'primary': {
        '50': '#E3F2FD', '100': '#BBDEFB', '200': '#90CAF9',
        '300': '#64B5F6', '400': '#42A5F5', '500': '#2196F3',
        '600': '#1E88E5', '700': '#1976D2', '800': '#1565C0', '900': '#0D47A1'
    },
    'accent': {
        'orange': '#FF6B35', 'orange_light': '#FF8C65', 'orange_dark': '#E55A2B',
        'green': '#4CAF50', 'red': '#F44336', 'amber': '#FFC107'
    },
    'neutral': {
        'white': '#FFFFFF', 'gray_50': '#FAFAFA', 'gray_100': '#F5F5F5',
        'gray_200': '#EEEEEE', 'gray_300': '#E0E0E0', 'gray_400': '#BDBDBD',
        'gray_500': '#9E9E9E', 'gray_600': '#757575', 'gray_700': '#616161',
        'gray_800': '#424242', 'gray_900': '#212121', 'black': '#000000'
    }
}

# 개선된 카드 색상 (그라데이션 적용)
CARD_COLORS = {
    'employee_count': {
        'start': '#E3F2FD',  # 연한 파란색
        'end': '#BBDEFB',    # 더 연한 파란색
        'border': '#90CAF9',
        'text': '#1565C0',
        'icon': '#1976D2'
    },
    'work_status': {
        'start': '#1976D2',  # 진한 파란색
        'end': '#1565C0',    # 더 진한 파란색
        'border': '#0D47A1',
        'text': '#FFFFFF',
        'icon': '#E3F2FD'
    },
    'special_notes': {
        'start': '#FF6B35',  # 모던한 주황색
        'end': '#FF8C65',    # 밝은 주황색
        'border': '#E55A2B',
        'text': '#FFFFFF',
        'icon': '#FFF3E0'
    }
}

# 타이포그래피 시스템 (Tkinter는 semibold를 지원하지 않으므로 bold 사용)
TYPOGRAPHY = {
    'h1': ('맑은 고딕', 24, 'bold'),
    'h2': ('맑은 고딕', 20, 'bold'),
    'h3': ('맑은 고딕', 18, 'bold'),
    'h4': ('맑은 고딕', 16, 'bold'),  # semibold -> bold
    'h5': ('맑은 고딕', 14, 'bold'),  # semibold -> bold
    'body_large': ('맑은 고딕', 14, 'normal'),
    'body': ('맑은 고딕', 12, 'normal'),
    'body_small': ('맑은 고딕', 11, 'normal'),
    'caption': ('맑은 고딕', 10, 'normal')
}

# 간격 시스템 (8px 기준)
SPACING = {
    'xs': 4, 'sm': 8, 'md': 16, 'lg': 24, 'xl': 32, '2xl': 48, '3xl': 64
}

# 카드 아이콘
CARD_ICONS = {
    'employee_count': '👥',
    'work_status': '📊',
    'special_notes': '⚠️'
}

# 그래프 색상 (개선)
CHART_COLORS = {
    'regular_light': '#2196F3',    # 파란색
    'regular_medium': '#64B5F6',   # 중간 파란색
    'contract_dark': '#FF6B35',    # 주황색
    'new_dark': '#4CAF50'          # 초록색
}

class DashboardViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("급여명세서 자동생성기 - 대시보드")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)  # 최소 크기 설정
        self.root.configure(bg=MODERN_COLORS['neutral']['gray_50'])
        
        # 창 크기 조절 가능하도록 설정
        self.root.resizable(True, True)
        
        self.handler = ExcelHandler()
        self.dashboard = Dashboard()
        self.df = None
        self.dashboard_data = None
        
        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'AppleGothic'  # macOS
        plt.rcParams['axes.unicode_minus'] = False
        
        # 그라데이션 이미지 캐시
        self.gradient_cache = {}
        
        self.create_widgets()
        self.load_default_file()
    
    def create_gradient_image(self, width, height, start_color, end_color):
        """그라데이션 이미지 생성"""
        cache_key = f"{width}x{height}_{start_color}_{end_color}"
        if cache_key in self.gradient_cache:
            return self.gradient_cache[cache_key]
        
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # RGB 색상 변환
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        # 그라데이션 생성 (135도 대각선)
        for y in range(height):
            for x in range(width):
                # 대각선 그라데이션 계산
                ratio = (x + y) / (width + height)
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.point((x, y), (r, g, b))
        
        photo = ImageTk.PhotoImage(image)
        self.gradient_cache[cache_key] = photo
        return photo
    
    def create_card(self, parent, card_type, title, min_height=200):
        """모던 카드 위젯 생성 (그라데이션, 그림자 효과)"""
        card_colors = CARD_COLORS[card_type]
        
        # 그림자 효과를 위한 외부 프레임
        shadow_frame = tk.Frame(parent, bg=MODERN_COLORS['neutral']['gray_300'])
        shadow_frame.pack(side=tk.LEFT, padx=SPACING['md'], pady=SPACING['md'], fill=tk.BOTH, expand=True)
        
        # 카드 프레임
        card_frame = tk.Frame(shadow_frame, bg=card_colors['start'], relief=tk.FLAT, borderwidth=0)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)  # 그림자 효과를 위한 패딩
        
        # 최소 높이 설정
        card_frame.config(height=min_height)
        card_frame.pack_propagate(False)
        
        # 그라데이션 배경 적용을 위한 Canvas
        canvas = tk.Canvas(
            card_frame,
            highlightthickness=0,
            borderwidth=0
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # 그라데이션 이미지 생성 및 적용
        def update_gradient(event=None):
            width = card_frame.winfo_width()
            height = card_frame.winfo_height()
            if width > 1 and height > 1:
                gradient_img = self.create_gradient_image(
                    width, height,
                    card_colors['start'],
                    card_colors['end']
                )
                canvas.delete("gradient")
                canvas.create_image(0, 0, anchor=tk.NW, image=gradient_img, tags="gradient")
                canvas.config(width=width, height=height)
        
        card_frame.bind('<Configure>', update_gradient)
        
        # 내용 컨테이너
        content_container = tk.Frame(canvas, bg=card_colors['start'])
        canvas_window = canvas.create_window(0, 0, window=content_container, anchor=tk.NW)
        
        def update_canvas_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Canvas 크기에 맞춰 내용 컨테이너 크기 조정
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        content_container.bind('<Configure>', update_canvas_scroll_region)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        # 헤더 영역 (아이콘 + 제목)
        header_frame = tk.Frame(content_container, bg=card_colors['start'])
        header_frame.pack(fill=tk.X, padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['md']))
        
        # 아이콘
        icon_label = tk.Label(
            header_frame,
            text=CARD_ICONS[card_type],
            font=('맑은 고딕', 20),
            bg=card_colors['start'],
            fg=card_colors['text']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, SPACING['sm']))
        
        # 제목
        title_label = tk.Label(
            header_frame,
            text=title,
            font=TYPOGRAPHY['h5'],
            bg=card_colors['start'],
            fg=card_colors['text']
        )
        title_label.pack(side=tk.LEFT)
        
        # 내용 프레임
        content_frame = tk.Frame(content_container, bg=card_colors['start'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        return card_frame, content_frame, canvas
    
    def create_widgets(self):
        """위젯 생성"""
        # 상단 프레임
        top_frame = tk.Frame(
            self.root,
            bg=MODERN_COLORS['neutral']['gray_50'],
            pady=SPACING['lg']
        )
        top_frame.pack(fill=tk.X, padx=SPACING['lg'])
        
        # 제목
        title_label = tk.Label(
            top_frame, 
            text="📊 급여 대시보드", 
            font=TYPOGRAPHY['h1'],
            bg=MODERN_COLORS['neutral']['gray_50'],
            fg=MODERN_COLORS['neutral']['gray_900']
        )
        title_label.pack(side=tk.LEFT)
        
        # 파일 선택 버튼 (모던 스타일)
        file_btn = tk.Button(
            top_frame,
            text="📁 파일 선택",
            command=self.select_file,
            bg=MODERN_COLORS['primary']['600'],
            fg='white',
            font=TYPOGRAPHY['body'],
            padx=SPACING['lg'],
            pady=SPACING['sm'],
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            activebackground=MODERN_COLORS['primary']['700'],
            activeforeground='white'
        )
        file_btn.pack(side=tk.RIGHT)
        
        # 상단 카드 영역 (3개 카드)
        cards_frame = tk.Frame(
            self.root,
            bg=MODERN_COLORS['neutral']['gray_50']
        )
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=SPACING['md'])
        
        # 카드 1: 총 직원 수
        card1, self.card1_content, self.card1_canvas = self.create_card(
            cards_frame,
            'employee_count',
            "총 직원 수",
            min_height=200
        )
        self.card1_labels = {}
        
        # 카드 2: 근무현황
        card2, self.card2_content, self.card2_canvas = self.create_card(
            cards_frame,
            'work_status',
            "근무현황",
            min_height=200
        )
        self.card2_labels = {}
        
        # 카드 3: 특이사항
        card3, self.card3_content, self.card3_canvas = self.create_card(
            cards_frame,
            'special_notes',
            "특이사항",
            min_height=200
        )
        self.notes_text = None
        
        # 하단 차트 영역 (2개 차트) - 반응형 높이
        charts_frame = tk.Frame(
            self.root,
            bg=MODERN_COLORS['neutral']['gray_50']
        )
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=SPACING['md'])
        # 높이 제한 제거하여 반응형으로 동작
        
        # 차트 1: 월별 급여 지출 현황 (막대 그래프)
        chart1_frame = tk.LabelFrame(
            charts_frame,
            text="월별 급여 지출 현황",
            font=TYPOGRAPHY['h5'],
            bg=MODERN_COLORS['neutral']['white'],
            fg=MODERN_COLORS['neutral']['gray_900'],
            padx=SPACING['md'],
            pady=SPACING['md'],
            relief=tk.FLAT,
            borderwidth=1,
            highlightbackground=MODERN_COLORS['neutral']['gray_300']
        )
        chart1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=SPACING['sm'])
        self.salary_chart_frame = chart1_frame
        self.salary_chart_container = tk.Frame(
            chart1_frame,
            bg=MODERN_COLORS['neutral']['white']
        )
        self.salary_chart_container.pack(fill=tk.BOTH, expand=True)
        self.salary_canvas = None
        
        # 차트 2: 근무자 구성 (도넛 차트)
        chart2_frame = tk.LabelFrame(
            charts_frame,
            text="근무자 구성",
            font=TYPOGRAPHY['h5'],
            bg=MODERN_COLORS['neutral']['white'],
            fg=MODERN_COLORS['neutral']['gray_900'],
            padx=SPACING['md'],
            pady=SPACING['md'],
            relief=tk.FLAT,
            borderwidth=1,
            highlightbackground=MODERN_COLORS['neutral']['gray_300']
        )
        chart2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=SPACING['sm'])
        self.workforce_chart_frame = chart2_frame
        self.workforce_chart_container = tk.Frame(
            chart2_frame,
            bg=MODERN_COLORS['neutral']['white']
        )
        self.workforce_chart_container.pack(fill=tk.BOTH, expand=True)
        self.workforce_canvas = None
    
    def load_default_file(self):
        """기본 파일 로드"""
        default_path = 'payroll_generator/templates/employee_template.xlsx'
        if os.path.exists(default_path):
            self.load_file(default_path)
    
    def select_file(self):
        """파일 선택"""
        file_path = filedialog.askopenfilename(
            title="직원 정보 엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """파일 로드 및 대시보드 업데이트"""
        try:
            # 엑셀 파일 읽기
            self.df = self.handler.read_employee_data(file_path)
            
            # 대시보드 데이터 분석
            self.dashboard_data = self.dashboard.analyze_employee_data(self.df)
            
            # UI 업데이트
            self.update_cards()
            self.update_charts()
            
            messagebox.showinfo("성공", f"{len(self.df)}명의 직원 정보를 불러왔습니다.")
            
        except Exception as e:
            messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다:\n{str(e)}")
    
    def update_cards(self):
        """카드 내용 업데이트"""
        if not self.dashboard_data:
            return
        
        data = self.dashboard_data
        work_status = data.get('work_status', {})
        
        # 카드 1: 총 직원 수 (기존 내용 제거 후 재생성)
        for widget in self.card1_content.winfo_children():
            widget.destroy()
        
        # 총 직원 수
        self.add_card_item(
            self.card1_content,
            "총 직원 수:",
            f"{data['total_employees']}명",
            'employee_count'
        )
        
        # 총급여 (만원 단위로 표시)
        total_payment_manwon = data['total_payment'] / 10000
        self.add_card_item(
            self.card1_content,
            "총급여:",
            f"{total_payment_manwon:.0f}만원",
            'employee_count'
        )
        
        # 총공제 (만원 단위로 표시)
        total_deduction_manwon = data['total_deduction'] / 10000
        self.add_card_item(
            self.card1_content,
            "총공제:",
            f"{total_deduction_manwon:.0f}만원",
            'employee_count'
        )
        
        # 카드 2: 근무현황 (기존 내용 제거 후 재생성)
        for widget in self.card2_content.winfo_children():
            widget.destroy()
        
        self.add_card_item(
            self.card2_content,
            "정규직:",
            f"{work_status.get('regular', 0)}명",
            'work_status'
        )
        
        self.add_card_item(
            self.card2_content,
            "계약직:",
            f"{work_status.get('contract', 0)}명",
            'work_status'
        )
        
        self.add_card_item(
            self.card2_content,
            "신입:",
            f"{work_status.get('new', 0)}명",
            'work_status'
        )
        
        # 카드 3: 특이사항 (기존 내용 제거 후 재생성)
        for widget in self.card3_content.winfo_children():
            widget.destroy()
        
        notes = data.get('special_notes', [])
        card_colors = CARD_COLORS['special_notes']
        if notes:
            notes_text = tk.Text(
                self.card3_content,
                font=TYPOGRAPHY['body_small'],
                bg=card_colors['start'],
                fg=card_colors['text'],
                wrap=tk.WORD,
                relief=tk.FLAT,
                borderwidth=0,
                height=6
            )
            notes_text.pack(fill=tk.BOTH, expand=True, padx=0, pady=SPACING['xs'])
            for note in notes:
                notes_text.insert(tk.END, f"• {note}\n")
            notes_text.config(state=tk.DISABLED)
        else:
            empty_label = tk.Label(
                self.card3_content,
                text="특이사항 없음",
                font=TYPOGRAPHY['body'],
                bg=card_colors['start'],
                fg=card_colors['text']
            )
            empty_label.pack(fill=tk.BOTH, expand=True, pady=SPACING['xl'])
    
    def add_card_item(self, parent, label, value, card_type):
        """카드에 항목 추가 (모던 스타일)"""
        card_colors = CARD_COLORS[card_type]
        bg_color = card_colors['start']
        text_color = card_colors['text']
        
        row = tk.Frame(parent, bg=bg_color)
        row.pack(fill=tk.X, pady=SPACING['xs'], padx=0)
        
        label_widget = tk.Label(
            row,
            text=label,
            font=TYPOGRAPHY['body'],
            bg=bg_color,
            fg=text_color,
            anchor='w'
        )
        label_widget.pack(side=tk.LEFT)
        
        # bold 폰트 생성
        bold_font = (TYPOGRAPHY['body_large'][0], TYPOGRAPHY['body_large'][1], 'bold')
        value_widget = tk.Label(
            row,
            text=value,
            font=bold_font,
            bg=bg_color,
            fg=text_color,
            anchor='e'
        )
        value_widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def update_charts(self):
        """그래프 업데이트"""
        if not self.dashboard_data:
            return
        
        # 막대 그래프 업데이트
        self.update_salary_chart()
        
        # 도넛 차트 업데이트
        self.update_workforce_chart()
    
    def update_salary_chart(self):
        """월별 급여 지출 현황 그래프 업데이트 (클러스터 막대 그래프)"""
        # 기존 캔버스 제거
        if self.salary_canvas:
            self.salary_canvas.get_tk_widget().destroy()
        
        # 월별 데이터 가져오기
        monthly_data = self.dashboard_data.get('monthly_data')
        if not monthly_data:
            # 월별 데이터가 없으면 빈 그래프 표시
            fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
            ax.text(0.5, 0.5, '월별 데이터 없음', 
                   ha='center', va='center', fontsize=10)
            ax.set_title('월별 급여 지출 현황', fontsize=11, fontweight='bold')
            plt.tight_layout()
        else:
            # 월별 클러스터 막대 그래프 생성
            fig = self.dashboard.create_monthly_workforce_chart(monthly_data)
        
        # 캔버스에 추가
        canvas = FigureCanvasTkAgg(fig, master=self.salary_chart_container)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.salary_canvas = canvas
        
        # 창 크기 변경 시 그래프 재조정
        def on_resize(event):
            if self.salary_canvas and event.width > 1 and event.height > 1:
                # 프레임 크기에 맞게 그래프 크기 조정
                width_inch = event.width / 100  # DPI 100 기준
                height_inch = event.height / 100
                fig = self.salary_canvas.figure
                fig.set_size_inches(width_inch, height_inch)
                fig.tight_layout(pad=1.0)
                self.salary_canvas.draw()
        
        canvas_widget.bind('<Configure>', on_resize)
        
        # 초기 크기 설정
        self.salary_chart_container.update_idletasks()
        if self.salary_chart_container.winfo_width() > 1:
            width_inch = self.salary_chart_container.winfo_width() / 100
            height_inch = self.salary_chart_container.winfo_height() / 100
            fig.set_size_inches(width_inch, height_inch)
            fig.tight_layout(pad=1.0)
            canvas.draw()
    
    def update_workforce_chart(self):
        """근무자구성 그래프 업데이트 (도넛 차트)"""
        # 기존 캔버스 제거
        if self.workforce_canvas:
            self.workforce_canvas.get_tk_widget().destroy()
        
        # 도넛 차트 생성
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        
        work_status = self.dashboard_data['work_status']
        
        labels = []
        sizes = []
        colors_list = []
        
        if work_status.get('regular', 0) > 0:
            labels.append('정규')
            sizes.append(work_status['regular'])
            colors_list.append(CHART_COLORS['regular_light'])
        
        if work_status.get('contract', 0) > 0:
            labels.append('계약')
            sizes.append(work_status['contract'])
            colors_list.append(CHART_COLORS['contract_dark'])
        
        if work_status.get('new', 0) > 0:
            labels.append('신입')
            sizes.append(work_status['new'])
            colors_list.append(CHART_COLORS['new_dark'])
        
        if not sizes:
            ax.text(0.5, 0.5, '데이터 없음', 
                   ha='center', va='center', fontsize=10)
            ax.set_title('근무자구성', fontsize=11, fontweight='bold')
            plt.tight_layout()
        else:
            # 도넛 그래프 생성
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                autopct='%1.1f%%',
                startangle=90,
                colors=colors_list,
                wedgeprops=dict(width=0.5),  # 도넛 모양
                textprops={'fontsize': 9}
            )
            
            ax.set_title('근무자구성', fontsize=11, fontweight='bold', pad=15)
            plt.tight_layout()
        
        # 캔버스에 추가
        canvas = FigureCanvasTkAgg(fig, master=self.workforce_chart_container)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.workforce_canvas = canvas
        
        # 창 크기 변경 시 그래프 재조정
        def on_resize(event):
            if self.workforce_canvas and event.width > 1 and event.height > 1:
                # 프레임 크기에 맞게 그래프 크기 조정
                width_inch = event.width / 100  # DPI 100 기준
                height_inch = event.height / 100
                fig = self.workforce_canvas.figure
                fig.set_size_inches(width_inch, height_inch)
                fig.tight_layout(pad=1.0)
                self.workforce_canvas.draw()
        
        canvas_widget.bind('<Configure>', on_resize)
        
        # 초기 크기 설정
        self.workforce_chart_container.update_idletasks()
        if self.workforce_chart_container.winfo_width() > 1:
            width_inch = self.workforce_chart_container.winfo_width() / 100
            height_inch = self.workforce_chart_container.winfo_height() / 100
            fig.set_size_inches(width_inch, height_inch)
            fig.tight_layout(pad=1.0)
            canvas.draw()

def main():
    """메인 함수"""
    root = tk.Tk()
    app = DashboardViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
