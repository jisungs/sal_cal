#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""급여명세서 자동생성기 - 메인 애플리케이션"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageDraw, ImageTk

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'payroll_generator'))

try:
    from payroll_generator.calculator import PayrollCalculator
    from payroll_generator.excel_handler import ExcelHandler
    from payroll_generator.dashboard import Dashboard
    from payroll_generator.pdf_generator import PDFGenerator
    from payroll_generator.settings import SettingsManager
    from payroll_generator.logger import setup_logger
    from payroll_generator.utils import resource_path
except ImportError:
    from calculator import PayrollCalculator
    from excel_handler import ExcelHandler
    from dashboard import Dashboard
    from pdf_generator import PDFGenerator
    from settings import SettingsManager
    from logger import setup_logger
    from utils import resource_path

logger = setup_logger()

# 모던 색상 팔레트
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

# 카드 색상
CARD_COLORS = {
    'employee_count': {
        'start': '#E3F2FD', 'end': '#BBDEFB', 'border': '#90CAF9',
        'text': '#1565C0', 'icon': '#1976D2'
    },
    'work_status': {
        'start': '#1976D2', 'end': '#1565C0', 'border': '#0D47A1',
        'text': '#FFFFFF', 'icon': '#E3F2FD'
    },
    'special_notes': {
        'start': '#FF6B35', 'end': '#FF8C65', 'border': '#E55A2B',
        'text': '#FFFFFF', 'icon': '#FFF3E0'
    }
}

# 타이포그래피
TYPOGRAPHY = {
    'h1': ('맑은 고딕', 24, 'bold'),
    'h2': ('맑은 고딕', 20, 'bold'),
    'h3': ('맑은 고딕', 18, 'bold'),
    'h4': ('맑은 고딕', 16, 'bold'),
    'h5': ('맑은 고딕', 14, 'bold'),
    'body_large': ('맑은 고딕', 14, 'normal'),
    'body': ('맑은 고딕', 12, 'normal'),
    'body_small': ('맑은 고딕', 11, 'normal'),
    'caption': ('맑은 고딕', 10, 'normal')
}

# 간격 시스템
SPACING = {
    'xs': 4, 'sm': 8, 'md': 16, 'lg': 24, 'xl': 32, '2xl': 48, '3xl': 64
}

# 카드 아이콘
CARD_ICONS = {
    'employee_count': '👥',
    'work_status': '📊',
    'special_notes': '⚠️'
}

# 그래프 색상
CHART_COLORS = {
    'regular_light': '#2196F3',
    'regular_medium': '#64B5F6',
    'contract_dark': '#FF6B35',
    'new_dark': '#4CAF50'
}

class PayrollApp:
    def __init__(self, root):
        self.root = root
        self.root.title("급여명세서 자동생성기 v1.0")
        self.root.geometry("1700x1050")
        self.root.minsize(900, 600)
        
        # 모듈 초기화
        self.calculator = PayrollCalculator()
        self.excel_handler = ExcelHandler()
        self.dashboard = Dashboard()
        self.pdf_generator = PDFGenerator()
        self.settings_manager = SettingsManager()
        
        # 변수 초기화 (설정에서 로드)
        self.employee_file_path = tk.StringVar()
        self.output_folder_path = tk.StringVar(value=self.settings_manager.get_last_output_folder())
        self.period = tk.StringVar(value=self.settings_manager.get_last_period())
        self.output_format = tk.StringVar(value=self.settings_manager.get_last_output_format())
        self.design_name = tk.StringVar(value=self.settings_manager.get_last_design_name())
        self.generated_files = []
        self.current_df = None  # 현재 로드된 직원 데이터
        self.dashboard_data = None  # 대시보드 데이터
        
        # 대시보드 관련 변수
        self.card1_content = None
        self.card2_content = None
        self.card3_content = None
        self.salary_canvas = None
        self.workforce_canvas = None
        self.gradient_cache = {}
        
        # 한글 폰트 설정 (플랫폼별)
        self.setup_matplotlib_font()
        
        self.create_widgets()
        logger.info("애플리케이션 시작")
    
    def create_widgets(self):
        """위젯 생성"""
        # 메뉴바 생성
        self.create_menu_bar()
        
        # 탭 노트북 생성
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 탭 전환 이벤트 바인딩
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # 탭 1: 대시보드
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="📊 대시보드")
        self.create_dashboard_tab()
        
        # 탭 2: 급여명세서 생성
        self.payroll_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.payroll_frame, text="📄 급여명세서 생성")
        self.create_payroll_tab()
        
        # 기본 탭을 대시보드로 설정
        self.notebook.select(0)
    
    def create_dashboard_tab(self):
        """대시보드 탭 UI 생성"""
        # 배경색 설정
        self.dashboard_frame.configure(style='Dashboard.TFrame')
        
        # 상단 프레임
        top_frame = tk.Frame(
            self.dashboard_frame,
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
        
        # 파일 선택 버튼
        file_btn = tk.Button(
            top_frame,
            text="📁 파일 선택",
            command=self.load_file_for_dashboard,
            bg=MODERN_COLORS['primary']['600'],
            fg='black',
            font=TYPOGRAPHY['body'],
            padx=SPACING['lg'],
            pady=SPACING['sm'],
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            activebackground=MODERN_COLORS['primary']['700'],
            activeforeground='black'
        )
        # 특이사항 박스와 오른쪽 여백을 맞추기 위해 (cards_frame의 padx + 카드의 padx)
        file_btn.pack(side=tk.RIGHT, padx=(0, SPACING['md']))
        
        # 상단 카드 영역 (3개 카드)
        cards_frame = tk.Frame(
            self.dashboard_frame,
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
        
        # 카드 2: 근무현황
        card2, self.card2_content, self.card2_canvas = self.create_card(
            cards_frame,
            'work_status',
            "근무현황",
            min_height=200
        )
        
        # 카드 3: 특이사항
        card3, self.card3_content, self.card3_canvas = self.create_card(
            cards_frame,
            'special_notes',
            "특이사항",
            min_height=200
        )
        
        # 하단 차트 영역 (2개 차트)
        charts_frame = tk.Frame(
            self.dashboard_frame,
            bg=MODERN_COLORS['neutral']['gray_50']
        )
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=SPACING['md'])
        
        # 차트 1: 월별 급여 지출 현황
        chart1_frame = tk.LabelFrame(
            charts_frame,
            text="",  # 제목 숨김
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
        self.salary_chart_container = tk.Frame(
            chart1_frame,
            bg=MODERN_COLORS['neutral']['white']
        )
        self.salary_chart_container.pack(fill=tk.BOTH, expand=True)
        
        # 차트 2: 근무자 구성
        chart2_frame = tk.LabelFrame(
            charts_frame,
            text="",  # 제목 숨김
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
        self.workforce_chart_container = tk.Frame(
            chart2_frame,
            bg=MODERN_COLORS['neutral']['white']
        )
        self.workforce_chart_container.pack(fill=tk.BOTH, expand=True)
        
        # 기본 파일 로드
        self.load_default_dashboard_file()
    
    def create_payroll_tab(self):
        """급여명세서 생성 탭 UI 생성"""
        # 파일 선택 프레임
        file_frame = ttk.LabelFrame(self.payroll_frame, text="입력 파일", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        entry_frame = ttk.Frame(file_frame)
        entry_frame.pack(fill=tk.X)
        
        ttk.Entry(entry_frame, textvariable=self.employee_file_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_frame, text="찾아보기", command=self.select_employee_file).pack(side=tk.LEFT)
        
        # 인라인 오류 메시지 라벨
        self.error_label = ttk.Label(file_frame, text="", foreground="red", font=("맑은 고딕", 9))
        self.error_label.pack(pady=(5, 0))
        
        # 미리보기 프레임
        preview_frame = ttk.LabelFrame(self.payroll_frame, text="파일 미리보기", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 선택 버튼 프레임 (트리뷰 위에 배치)
        selection_btn_frame = ttk.Frame(preview_frame)
        selection_btn_frame.pack(pady=(0, 5), fill=tk.X)
        
        ttk.Button(
            selection_btn_frame,
            text="전체 선택",
            command=self.select_all_employees,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            selection_btn_frame,
            text="전체 해제",
            command=self.deselect_all_employees,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # 선택 상태 표시 라벨
        self.selection_status_label = ttk.Label(
            selection_btn_frame,
            text="전체 직원 처리",
            font=("맑은 고딕", 9),
            foreground="gray"
        )
        self.selection_status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 체크박스 아이콘 상수
        self.CHECKBOX_UNCHECKED = '☐'  # 체크 안됨
        self.CHECKBOX_CHECKED = '☒'    # 체크됨
        
        # 미리보기 트리뷰 (다중 선택 가능)
        columns = ('체크', '이름', '주민번호', '입사일', '기본급')
        self.preview_tree = ttk.Treeview(
            preview_frame, 
            columns=columns, 
            show='headings', 
            height=5,
            selectmode='extended'  # 다중 선택 가능
        )
        
        # 체크박스 컬럼 설정
        self.preview_tree.heading('체크', text='')
        self.preview_tree.column('체크', width=30, anchor='center')
        
        # 나머지 컬럼 설정
        for col in ('이름', '주민번호', '입사일', '기본급'):
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=120)
        self.preview_tree.pack(fill=tk.BOTH, expand=True)
        
        # 선택 변경 이벤트 바인딩
        self.preview_tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # 체크박스 클릭 이벤트 바인딩
        self.preview_tree.bind('<Button-1>', self.on_treeview_click)
        
        # 설정 프레임
        settings_frame = ttk.LabelFrame(self.payroll_frame, text="설정", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(settings_frame, text="생성 기간:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(settings_frame, textvariable=self.period, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(settings_frame, text="출력 형식:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(settings_frame, text="엑셀", variable=self.output_format, value="excel").grid(row=1, column=1, padx=5)
        ttk.Radiobutton(settings_frame, text="PDF", variable=self.output_format, value="pdf").grid(row=1, column=2, padx=5)
        ttk.Radiobutton(settings_frame, text="둘 다", variable=self.output_format, value="both").grid(row=1, column=3, padx=5)
        
        ttk.Label(settings_frame, text="디자인 선택:").grid(row=2, column=0, sticky=tk.W, pady=5)
        design_combo = ttk.Combobox(settings_frame, textvariable=self.design_name, width=20, state="readonly")
        design_combo['values'] = ('default', 'template_sample1', 'template_sample2')
        design_combo.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=5)
        # 디자인 이름을 사용자 친화적인 레이블로 표시하기 위한 변환 딕셔너리
        design_labels = {
            'default': '기본 디자인',
            'template_sample1': '템플릿 1: 급여명세서',
            'template_sample2': '템플릿 2: 임금명세서'
        }
        # Combobox 값 변경 시 레이블 표시 (선택사항, 현재는 값 그대로 사용)
        
        # 출력 폴더 프레임
        output_frame = ttk.LabelFrame(self.payroll_frame, text="출력 폴더", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_folder_path, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_frame, text="찾아보기", command=self.select_output_folder).pack(side=tk.LEFT)
        
        # 버튼 프레임
        button_frame = ttk.Frame(self.payroll_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="생성하기", command=self.start_generation, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="초기화", command=self.reset_fields, width=15).pack(side=tk.LEFT, padx=5)
        
        # 진행 상태 프레임
        progress_frame = ttk.LabelFrame(self.payroll_frame, text="진행 상태", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="대기 중...")
        self.status_label.pack(pady=5)
        
        # 완료 후 액션 프레임
        self.action_frame = ttk.Frame(self.payroll_frame)
        self.action_frame.pack(pady=10)
        
        self.open_folder_btn = ttk.Button(
            self.action_frame, 
            text="📁 출력 폴더 열기", 
            command=self.open_output_folder,
            state=tk.DISABLED
        )
        self.open_folder_btn.pack(side=tk.LEFT, padx=5)
    
    def create_gradient_image(self, width, height, start_color, end_color):
        """그라데이션 이미지 생성"""
        cache_key = f"{width}x{height}_{start_color}_{end_color}"
        if cache_key in self.gradient_cache:
            return self.gradient_cache[cache_key]
        
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        for y in range(height):
            for x in range(width):
                ratio = (x + y) / (width + height)
                r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
                g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
                b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
                draw.point((x, y), (r, g, b))
        
        photo = ImageTk.PhotoImage(image)
        self.gradient_cache[cache_key] = photo
        return photo
    
    def create_card(self, parent, card_type, title, min_height=200):
        """모던 카드 위젯 생성"""
        card_colors = CARD_COLORS[card_type]
        
        # 특이사항 카드는 그림자 효과 제거
        if card_type == 'special_notes':
            # 그림자 효과 없이 직접 카드 프레임 생성
            card_frame = tk.Frame(
                parent, 
                bg=card_colors['start'], 
                relief=tk.FLAT, 
                borderwidth=0,
                highlightthickness=0
            )
            card_frame.pack(side=tk.LEFT, padx=SPACING['md'], pady=SPACING['md'], fill=tk.BOTH, expand=True)
        else:
            # 다른 카드는 그림자 효과 유지
            shadow_frame = tk.Frame(parent, bg=MODERN_COLORS['neutral']['gray_300'])
            shadow_frame.pack(side=tk.LEFT, padx=SPACING['md'], pady=SPACING['md'], fill=tk.BOTH, expand=True)
            
            card_frame = tk.Frame(
                shadow_frame, 
                bg=card_colors['start'], 
                relief=tk.FLAT, 
                borderwidth=0,
                highlightthickness=0
            )
            card_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        card_frame.config(height=min_height)
        card_frame.pack_propagate(False)
        
        canvas = tk.Canvas(
            card_frame, 
            highlightthickness=0, 
            borderwidth=0,
            highlightbackground=card_colors['start']
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        
        def update_gradient(event=None):
            width = card_frame.winfo_width()
            height = card_frame.winfo_height()
            if width > 1 and height > 1:
                gradient_img = self.create_gradient_image(
                    width, height, card_colors['start'], card_colors['end']
                )
                canvas.delete("gradient")
                canvas.create_image(0, 0, anchor=tk.NW, image=gradient_img, tags="gradient")
                canvas.config(width=width, height=height)
        
        card_frame.bind('<Configure>', update_gradient)
        
        content_container = tk.Frame(
            canvas, 
            bg=card_colors['start'],
            highlightthickness=0,
            borderwidth=0
        )
        canvas_window = canvas.create_window(0, 0, window=content_container, anchor=tk.NW)
        
        def update_canvas_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        content_container.bind('<Configure>', update_canvas_scroll_region)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        header_frame = tk.Frame(
            content_container, 
            bg=card_colors['start'],
            highlightthickness=0,
            borderwidth=0
        )
        header_frame.pack(fill=tk.X, padx=SPACING['lg'], pady=(SPACING['lg'], SPACING['md']))
        
        icon_label = tk.Label(
            header_frame,
            text=CARD_ICONS[card_type],
            font=('맑은 고딕', 20),
            bg=card_colors['start'],
            fg=card_colors['text']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, SPACING['sm']))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=TYPOGRAPHY['h5'],
            bg=card_colors['start'],
            fg=card_colors['text']
        )
        title_label.pack(side=tk.LEFT)
        
        content_frame = tk.Frame(
            content_container, 
            bg=card_colors['start'],
            highlightthickness=0,
            borderwidth=0
        )
        content_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['lg'], pady=(0, SPACING['lg']))
        
        return card_frame, content_frame, canvas
    
    def load_default_dashboard_file(self):
        """기본 파일 로드 (저장된 경로 또는 파일 선택)"""
        # 첫 실행 확인
        if self.settings_manager.is_first_run():
            # 첫 실행이면 대시보드를 먼저 초기화 (0으로)
            self.reset_dashboard()
            
            # 알림창으로 파일 입력 유도
            response = messagebox.showinfo(
                "환영합니다! 👋",
                "급여명세서 자동생성기에 오신 것을 환영합니다!\n\n"
                "직원 정보 엑셀 파일을 선택해주세요.\n"
                "파일을 선택하면 대시보드에 데이터가 표시됩니다.",
                type=messagebox.OK
            )
            
            # 알림창 확인 후 파일 선택 다이얼로그 표시
            filename = filedialog.askopenfilename(
                title="직원 정보 엑셀 파일 선택",
                filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
            )
            if filename:
                # 파일 경로 저장
                self.settings_manager.set_last_employee_file(filename)
                self.settings_manager.set_first_run_complete()
                # 파일 로드
                self.load_dashboard_file(filename, show_message=True)
            else:
                # 파일을 선택하지 않으면 기본 템플릿 로드
                # PyInstaller 환경과 개발 환경 모두 지원
                default_paths = [
                    resource_path('templates/employee_template.xlsx'),  # PyInstaller 환경
                    'payroll_generator/templates/employee_template.xlsx',  # 개발 환경
                ]
                default_path = None
                for path in default_paths:
                    if os.path.exists(path):
                        default_path = path
                        break
                if default_path:
                    self.load_dashboard_file(default_path, show_message=False)
        else:
            # 저장된 파일 경로 확인
            last_file = self.settings_manager.get_last_employee_file()
            if last_file and os.path.exists(last_file):
                # 저장된 파일이 있으면 자동 로드
                self.load_dashboard_file(last_file, show_message=False)
            else:
                # 저장된 파일이 없거나 삭제된 경우 대시보드 초기화 후 알림
                self.reset_dashboard()
                response = messagebox.showinfo(
                    "파일 선택 필요",
                    "저장된 직원 정보 파일을 찾을 수 없습니다.\n\n"
                    "직원 정보 엑셀 파일을 선택해주세요.",
                    type=messagebox.OK
                )
                # 알림창 확인 후 파일 선택 다이얼로그 표시
                filename = filedialog.askopenfilename(
                    title="직원 정보 엑셀 파일 선택",
                    filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
                )
                if filename:
                    self.settings_manager.set_last_employee_file(filename)
                    self.load_dashboard_file(filename, show_message=True)
                else:
                    # 파일을 선택하지 않으면 기본 템플릿 로드
                    # PyInstaller 환경과 개발 환경 모두 지원
                    default_paths = [
                        resource_path('templates/employee_template.xlsx'),  # PyInstaller 환경
                        'payroll_generator/templates/employee_template.xlsx',  # 개발 환경
                    ]
                    default_path = None
                    for path in default_paths:
                        if os.path.exists(path):
                            default_path = path
                            break
                    if default_path:
                        self.load_dashboard_file(default_path, show_message=False)
    
    def load_file_for_dashboard(self):
        """대시보드용 파일 선택"""
        filename = filedialog.askopenfilename(
            title="직원 정보 엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            # 파일 경로 저장
            self.settings_manager.set_last_employee_file(filename)
            self.settings_manager.set_first_run_complete()
            # 파일 로드
            self.load_dashboard_file(filename, show_message=True)
    
    def load_dashboard_file(self, file_path, show_message=True):
        """파일 로드 및 대시보드 업데이트"""
        try:
            # 엑셀 파일 읽기
            self.df = self.excel_handler.read_employee_data(file_path)
            self.dashboard_data = self.dashboard.analyze_employee_data(self.df)
            
            # 급여명세서 탭에서도 사용할 수 있도록 동기화
            self.employee_file_path.set(file_path)  # 파일 경로 동기화
            self.current_df = self.df  # 데이터 동기화
            
            # 대시보드 업데이트
            self.update_cards()
            self.update_charts()
            
            if show_message:
                messagebox.showinfo("성공", f"{len(self.df)}명의 직원 정보를 불러왔습니다.")
            logger.info(f"대시보드 데이터 로드 완료: {len(self.df)}명")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다:\n{str(e)}")
            logger.exception(f"대시보드 파일 로드 오류: {str(e)}")
    
    def update_cards(self):
        """카드 내용 업데이트"""
        if not self.dashboard_data:
            return
        
        data = self.dashboard_data
        work_status = data.get('work_status', {})
        
        # 카드 1: 총 직원 수
        for widget in self.card1_content.winfo_children():
            widget.destroy()
        
        self.add_card_item(self.card1_content, "총 직원 수:", f"{data['total_employees']}명", 'employee_count')
        total_payment_manwon = data['total_payment'] / 10000
        self.add_card_item(self.card1_content, "총급여:", f"{total_payment_manwon:.0f}만원", 'employee_count')
        total_deduction_manwon = data['total_deduction'] / 10000
        self.add_card_item(self.card1_content, "총공제:", f"{total_deduction_manwon:.0f}만원", 'employee_count')
        
        # 카드 2: 근무현황
        for widget in self.card2_content.winfo_children():
            widget.destroy()
        
        self.add_card_item(self.card2_content, "정규직:", f"{work_status.get('regular', 0)}명", 'work_status')
        self.add_card_item(self.card2_content, "계약직:", f"{work_status.get('contract', 0)}명", 'work_status')
        self.add_card_item(self.card2_content, "신입:", f"{work_status.get('new', 0)}명", 'work_status')
        
        # 카드 3: 특이사항
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
                highlightthickness=0,
                highlightbackground=card_colors['start'],
                highlightcolor=card_colors['start'],
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
        """카드에 항목 추가"""
        card_colors = CARD_COLORS[card_type]
        bg_color = card_colors['start']
        text_color = card_colors['text']
        
        row = tk.Frame(
            parent, 
            bg=bg_color,
            highlightthickness=0,
            borderwidth=0
        )
        row.pack(fill=tk.X, pady=SPACING['xs'], padx=0)
        
        label_widget = tk.Label(row, text=label, font=TYPOGRAPHY['body'], bg=bg_color, fg=text_color, anchor='w')
        label_widget.pack(side=tk.LEFT)
        
        bold_font = (TYPOGRAPHY['body_large'][0], TYPOGRAPHY['body_large'][1], 'bold')
        value_widget = tk.Label(row, text=value, font=bold_font, bg=bg_color, fg=text_color, anchor='e')
        value_widget.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def update_charts(self):
        """그래프 업데이트"""
        if not self.dashboard_data:
            return
        
        self.update_salary_chart()
        self.update_workforce_chart()
    
    def update_salary_chart(self):
        """월별 급여 지출 현황 그래프 업데이트"""
        if self.salary_canvas:
            self.salary_canvas.get_tk_widget().destroy()
        
        monthly_data = self.dashboard_data.get('monthly_data')
        if not monthly_data:
            fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
            ax.text(0.5, 0.5, '월별 데이터 없음', ha='center', va='center', fontsize=10)
            ax.set_title('월별 급여 지출 현황', fontsize=11, fontweight='bold')
            plt.tight_layout()
        else:
            fig = self.dashboard.create_monthly_workforce_chart(monthly_data)
        
        canvas = FigureCanvasTkAgg(fig, master=self.salary_chart_container)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.salary_canvas = canvas
    
    def update_workforce_chart(self):
        """근무자구성 그래프 업데이트"""
        if self.workforce_canvas:
            self.workforce_canvas.get_tk_widget().destroy()
        
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
            ax.text(0.5, 0.5, '데이터 없음', ha='center', va='center', fontsize=10)
            ax.set_title('근무자구성', fontsize=11, fontweight='bold')
            plt.tight_layout()
        else:
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct='%1.1f%%',
                startangle=90, colors=colors_list,
                wedgeprops=dict(width=0.5), textprops={'fontsize': 9}
            )
            ax.set_title('근무자구성', fontsize=11, fontweight='bold', pad=15)
            plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.workforce_chart_container)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        self.workforce_canvas = canvas
    
    def select_employee_file(self):
        """직원 정보 파일 선택"""
        filename = filedialog.askopenfilename(
            title="직원 정보 엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.employee_file_path.set(filename)
            # 파일 경로 저장
            self.settings_manager.set_last_employee_file(filename)
            self.error_label.config(text="")
            self.load_preview(filename)
    
    def load_preview(self, file_path):
        """엑셀 파일 미리보기 로드"""
        try:
            # 파일 존재 확인
            if not os.path.exists(file_path):
                error_msg = "파일을 찾을 수 없어요! 😊 파일 경로를 확인해주세요."
                self.error_label.config(text=error_msg)
                logger.error(f"파일 없음: {file_path}")
                return
            
            # 파일 권한 확인
            if not os.access(file_path, os.R_OK):
                error_msg = "파일을 읽을 권한이 없어요! 😊 파일 권한을 확인해주세요."
                self.error_label.config(text=error_msg)
                logger.error(f"파일 읽기 권한 없음: {file_path}")
                return
            
            # 기존 미리보기 데이터 삭제
            for item in self.preview_tree.get_children():
                self.preview_tree.delete(item)
            
            # 전체 파일 데이터 로드 (미리보기는 전체 데이터 표시)
            df = self.excel_handler.read_employee_data(file_path)
            preview_data = df.to_dict('records')
            
            # 주민번호 마스킹을 위한 utils import
            from payroll_generator.utils import mask_resident_number
            
            for row in preview_data:
                values = (
                    self.CHECKBOX_UNCHECKED,  # 체크박스 아이콘 (초기값: 체크 안됨)
                    str(row.get('이름', '')),
                    mask_resident_number(str(row.get('주민번호', ''))),
                    str(row.get('입사일', '')),
                    f"{row.get('기본급', 0):,}"
                )
                self.preview_tree.insert('', tk.END, values=values)
            
            # 미리보기 로드 후 선택 상태 초기화
            self.on_selection_change()
            
            logger.info(f"미리보기 로드 완료: {len(preview_data)}행")
        except FileNotFoundError as e:
            error_msg = "파일을 찾을 수 없어요! 😊 파일 경로를 확인해주세요."
            self.error_label.config(text=error_msg)
            logger.exception(f"파일 없음 오류: {str(e)}")
        except PermissionError as e:
            error_msg = "파일을 읽을 권한이 없어요! 😊 파일 권한을 확인해주세요."
            self.error_label.config(text=error_msg)
            logger.exception(f"권한 오류: {str(e)}")
        except ValueError as e:
            error_msg = "입력 형식에 문제가 있어요! 😊 파일을 확인해주세요."
            self.error_label.config(text=error_msg)
            logger.exception(f"데이터 형식 오류: {str(e)}")
        except MemoryError as e:
            error_msg = "메모리가 부족해요! 😊 파일 크기를 확인해주세요."
            self.error_label.config(text=error_msg)
            logger.exception(f"메모리 부족 오류: {str(e)}")
        except Exception as e:
            error_msg = "입력 형식에 문제가 있어요! 😊 파일을 확인해주세요."
            self.error_label.config(text=error_msg)
            logger.exception(f"미리보기 로드 오류: {str(e)}")
    
    def get_selected_employees(self):
        """선택된 직원 이름 목록 반환"""
        selected_items = self.preview_tree.selection()
        selected_names = []
        
        for item in selected_items:
            values = self.preview_tree.item(item, 'values')
            if values and len(values) > 1:
                name = values[1]  # 두 번째 컬럼이 이름 (첫 번째는 체크박스)
                selected_names.append(name)
        
        return selected_names
    
    def update_checkbox(self, item, checked):
        """체크박스 아이콘 업데이트"""
        values = list(self.preview_tree.item(item, 'values'))
        if len(values) > 0:
            values[0] = self.CHECKBOX_CHECKED if checked else self.CHECKBOX_UNCHECKED
            self.preview_tree.item(item, values=values)
    
    def update_all_checkboxes(self):
        """모든 체크박스 아이콘을 선택 상태에 맞게 업데이트"""
        selected_items = set(self.preview_tree.selection())
        all_items = self.preview_tree.get_children()
        
        for item in all_items:
            is_selected = item in selected_items
            self.update_checkbox(item, is_selected)
    
    def on_treeview_click(self, event):
        """Treeview 클릭 이벤트 처리 (체크박스 클릭 감지)"""
        region = self.preview_tree.identify_region(event.x, event.y)
        
        # 클릭한 영역이 셀인 경우
        if region == 'cell':
            column = self.preview_tree.identify_column(event.x)
            item = self.preview_tree.identify_row(event.y)
            
            # 체크박스 컬럼(첫 번째 컬럼)을 클릭한 경우
            if column == '#1' and item:
                # 현재 선택 상태 확인
                is_selected = item in self.preview_tree.selection()
                
                if is_selected:
                    # 선택 해제
                    self.preview_tree.selection_remove(item)
                else:
                    # 선택 추가
                    self.preview_tree.selection_add(item)
                
                # 선택 상태 변경 이벤트 발생 (체크박스 업데이트 포함)
                self.on_selection_change()
                
                # 이벤트 전파 방지 (기본 선택 동작 방지)
                return 'break'
    
    def on_selection_change(self, event=None):
        """선택 변경 시 호출 (개별 선택, 전체 선택, 전체 해제 모두에서 호출)"""
        # 체크박스 아이콘 업데이트
        self.update_all_checkboxes()
        
        selected_names = self.get_selected_employees()
        total_items = len(self.preview_tree.get_children())
        
        if selected_names:
            selected_count = len(selected_names)
            if selected_count == total_items and total_items > 0:
                # 전체 선택된 경우
                self.selection_status_label.config(
                    text=f"전체 선택됨 ({selected_count}명)",
                    foreground="green"
                )
            else:
                # 일부만 선택된 경우
                self.selection_status_label.config(
                    text=f"선택된 직원: {selected_count}명 / 전체: {total_items}명",
                    foreground="blue"
                )
        else:
            # 선택되지 않은 경우 (전체 처리 모드)
            self.selection_status_label.config(
                text="전체 직원 처리",
                foreground="gray"
            )
    
    def select_all_employees(self):
        """모든 직원 선택"""
        all_items = self.preview_tree.get_children()
        if not all_items:
            return
        
        # 모든 항목 선택
        for item in all_items:
            self.preview_tree.selection_add(item)
        
        # 선택 상태 업데이트
        self.on_selection_change()
        logger.info(f"전체 직원 선택: {len(all_items)}명")
    
    def deselect_all_employees(self):
        """모든 직원 선택 해제"""
        selected_items = self.preview_tree.selection()
        if not selected_items:
            return
        
        # 모든 선택 해제
        for item in selected_items:
            self.preview_tree.selection_remove(item)
        
        # 선택 상태 업데이트
        self.on_selection_change()
        logger.info("전체 선택 해제")
    
    def save_monthly_history(self, df, period):
        """월별 급여 이력 데이터 저장"""
        try:
            from payroll_generator.history_manager import HistoryManager
        except ImportError:
            from history_manager import HistoryManager
        
        history_manager = HistoryManager()
        
        # 정규직/계약직별 급여 합계 계산
        regular_payment = 0
        contract_payment = 0
        regular_count = 0
        contract_count = 0
        
        for idx, row in df.iterrows():
            payroll_data = self.calculator.calculate_deductions(row.to_dict())
            total_payment = payroll_data['총지급액']
            
            # 정규직/계약직 구분
            is_regular = self._is_regular_employee(row)
            
            if is_regular:
                regular_payment += total_payment
                regular_count += 1
            else:
                contract_payment += total_payment
                contract_count += 1
        
        # 이력 데이터 저장
        data = {
            'regular_payment': regular_payment,
            'contract_payment': contract_payment,
            'regular_count': regular_count,
            'contract_count': contract_count
        }
        
        history_manager.save_monthly_data(period, data)
        logger.info(f"월별 이력 데이터 저장 완료: {period}")
    
    def _is_regular_employee(self, row):
        """정규직 여부 판단"""
        from datetime import datetime
        
        join_date_str = row.get('입사일', '')
        if not join_date_str:
            return True  # 기본값: 정규직
        
        try:
            if isinstance(join_date_str, str):
                join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
            else:
                join_date = join_date_str
            # 1년 이상 근무하면 정규직으로 간주
            return (datetime.now() - join_date).days >= 365
        except:
            return True  # 기본값: 정규직
    
    def open_output_folder(self):
        """출력 폴더 열기"""
        folder_path = self.output_folder_path.get()
        if os.path.exists(folder_path):
            if platform.system() == 'Windows':
                os.startfile(folder_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', folder_path])
            else:  # Linux
                subprocess.Popen(['xdg-open', folder_path])
            logger.info(f"출력 폴더 열기: {folder_path}")
    
    def select_output_folder(self):
        """출력 폴더 선택"""
        folder = filedialog.askdirectory(title="출력 폴더 선택")
        if folder:
            self.output_folder_path.set(folder)
            # 출력 폴더 경로 저장
            self.settings_manager.set_last_output_folder(folder)
    
    def reset_fields(self):
        """필드 초기화"""
        self.employee_file_path.set("")
        self.output_folder_path.set("./payroll_generator/output")
        self.period.set("2025-01")
        self.output_format.set("both")
        self.design_name.set("default")
        self.progress_var.set(0)
        self.status_label.config(text="대기 중...")
        self.error_label.config(text="")
        self.open_folder_btn.config(state=tk.DISABLED)
        # 미리보기 트리뷰 초기화
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
    
    def start_generation(self):
        """급여명세서 생성 시작"""
        if not self.employee_file_path.get():
            self.error_label.config(text="직원 정보 파일을 선택해주세요! 😊")
            return
        
        # 설정 저장 (기간, 출력 형식, 디자인)
        self.settings_manager.set_last_period(self.period.get())
        self.settings_manager.set_last_output_format(self.output_format.get())
        self.settings_manager.set_last_design_name(self.design_name.get())
        
        # 오류 메시지 초기화
        self.error_label.config(text="")
        self.open_folder_btn.config(state=tk.DISABLED)
        self.generated_files = []
        
        # 별도 스레드에서 실행 (GUI 멈춤 방지)
        thread = threading.Thread(target=self.generate_payroll)
        thread.daemon = True
        thread.start()
    
    def generate_payroll(self):
        """급여명세서 생성 (백그라운드 스레드)"""
        try:
            # 진행 상태 업데이트
            self.status_label.config(text="직원 정보 읽는 중...")
            self.progress_var.set(10)
            
            # 파일 존재 확인
            file_path = self.employee_file_path.get()
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
            
            # 파일 읽기 권한 확인
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"파일을 읽을 권한이 없습니다: {file_path}")
            
            # 엑셀 파일 읽기
            df = self.excel_handler.read_employee_data(file_path)
            
            # 선택된 직원 확인
            selected_names = self.get_selected_employees()
            
            # 선택된 직원이 있으면 필터링
            if selected_names:
                # 선택된 이름이 실제 데이터에 있는지 확인
                available_names = df['이름'].tolist()
                valid_selected = [name for name in selected_names if name in available_names]
                
                if not valid_selected:
                    raise ValueError("선택된 직원이 파일에 없습니다.")
                
                # 선택된 직원만 필터링
                df = df[df['이름'].isin(valid_selected)]
                total_employees = len(df)
                
                logger.info(f"선택된 직원만 처리: {len(valid_selected)}명")
            else:
                # 선택된 직원이 없으면 전체 처리 (기존 동작)
                total_employees = len(df)
                logger.info(f"전체 직원 처리: {total_employees}명")
            
            if total_employees == 0:
                raise ValueError("처리할 직원 데이터가 없습니다.")
            
            # 출력 폴더 생성
            output_folder = self.output_folder_path.get()
            try:
                os.makedirs(output_folder, exist_ok=True)
            except PermissionError:
                raise PermissionError(f"출력 폴더를 생성할 권한이 없습니다: {output_folder}")
            
            # 출력 폴더 쓰기 권한 확인
            if not os.access(output_folder, os.W_OK):
                raise PermissionError(f"출력 폴더에 쓸 권한이 없습니다: {output_folder}")
            
            # 각 직원별 처리
            for idx, row in df.iterrows():
                employee_name = row.get('이름', f'직원{idx+1}')
                self.status_label.config(text=f"처리 중: {employee_name} ({idx+1}/{total_employees})")
                
                try:
                    # 급여 계산
                    payroll_data = self.calculator.calculate_deductions(row.to_dict())
                    
                    # 엑셀 출력
                    if self.output_format.get() in ['excel', 'both']:
                        try:
                            excel_path = os.path.join(output_folder, f"{employee_name}_급여명세서.xlsx")
                            design_name_value = self.design_name.get() if self.design_name.get() != 'default' else None
                            self.excel_handler.write_payroll(payroll_data, excel_path, row.to_dict(), self.period.get(), design_name=design_name_value)
                            self.generated_files.append(excel_path)
                        except Exception as excel_error:
                            logger.error(f"엑셀 생성 실패: {employee_name} - {str(excel_error)}")
                            # 계속 진행 (다음 직원 처리)
                    
                    # PDF 출력
                    if self.output_format.get() in ['pdf', 'both']:
                        try:
                            pdf_path = os.path.join(output_folder, f"{employee_name}_급여명세서.pdf")
                            design_name_value = self.design_name.get() if self.design_name.get() != 'default' else None
                            self.pdf_generator.generate_payslip(payroll_data, row.to_dict(), pdf_path, self.period.get(), design_name=design_name_value)
                            self.generated_files.append(pdf_path)
                        except Exception as pdf_error:
                            logger.warning(f"PDF 생성 실패 (엑셀은 생성됨): {employee_name} - {str(pdf_error)}")
                            # 계속 진행 (엑셀은 생성됨)
                    
                except Exception as emp_error:
                    logger.error(f"직원 처리 오류: {employee_name} - {str(emp_error)}")
                    # 계속 진행 (다음 직원 처리)
                
                # 진행률 업데이트
                progress = 10 + int((idx + 1) / total_employees * 90)
                self.progress_var.set(progress)
            
            self.status_label.config(text=f"✅ 완료! {total_employees}명 처리됨")
            self.open_folder_btn.config(state=tk.NORMAL)
            
            # 월별 이력 데이터 저장
            try:
                self.save_monthly_history(df, self.period.get())
            except Exception as history_error:
                logger.warning(f"월별 이력 데이터 저장 실패 (급여명세서는 생성됨): {history_error}")
                # 이력 저장 실패해도 급여명세서 생성은 완료된 것으로 처리
            
            # 완료 메시지
            if len(self.generated_files) > 0:
                messagebox.showinfo(
                    "완료", 
                    f"급여명세서 생성이 완료되었습니다! 😊\n\n"
                    f"처리된 직원: {total_employees}명\n"
                    f"생성된 파일: {len(self.generated_files)}개\n\n"
                    f"출력 폴더를 열어 확인해보세요!"
                )
                logger.info(f"급여명세서 생성 완료: {total_employees}명, {len(self.generated_files)}개 파일")
            else:
                error_msg = "생성된 파일이 없어요! 😊 로그 파일을 확인해주세요."
                self.error_label.config(text=error_msg)
                messagebox.showwarning(
                    "경고",
                    f"처리된 직원: {total_employees}명\n"
                    f"생성된 파일: 0개\n\n"
                    f"모든 파일 생성에 실패했습니다.\n"
                    f"로그 파일을 확인해주세요."
                )
                logger.warning(f"급여명세서 생성 실패: {total_employees}명 처리, 0개 파일 생성")
            
        except FileNotFoundError as e:
            error_msg = "파일을 찾을 수 없어요! 😊 파일 경로를 확인해주세요."
            self.error_label.config(text=error_msg)
            messagebox.showerror("오류", f"{error_msg}\n\n{str(e)}")
            self.status_label.config(text="❌ 오류 발생")
            logger.exception(f"파일 없음 오류: {str(e)}")
        except PermissionError as e:
            error_msg = "파일 권한이 없어요! 😊 파일 권한을 확인해주세요."
            self.error_label.config(text=error_msg)
            messagebox.showerror("오류", f"{error_msg}\n\n{str(e)}")
            self.status_label.config(text="❌ 오류 발생")
            logger.exception(f"권한 오류: {str(e)}")
        except ValueError as e:
            error_msg = "입력 형식에 문제가 있어요! 😊 파일을 확인해주세요."
            self.error_label.config(text=error_msg)
            messagebox.showerror("오류", f"{error_msg}\n\n{str(e)}")
            self.status_label.config(text="❌ 오류 발생")
            logger.exception(f"데이터 형식 오류: {str(e)}")
        except MemoryError as e:
            error_msg = "메모리가 부족해요! 😊 파일 크기를 확인해주세요."
            self.error_label.config(text=error_msg)
            messagebox.showerror("오류", f"{error_msg}\n\n{str(e)}")
            self.status_label.config(text="❌ 오류 발생")
            logger.exception(f"메모리 부족 오류: {str(e)}")
        except Exception as e:
            error_msg = "처리 중 문제가 발생했어요! 😊 로그 파일을 확인해주세요."
            self.error_label.config(text=error_msg)
            messagebox.showerror("오류", f"{error_msg}\n\n{str(e)}\n\n로그 파일을 확인해주세요.")
            self.status_label.config(text="❌ 오류 발생")
            logger.exception(f"급여명세서 생성 오류: {str(e)}")
    
    def create_menu_bar(self):
        """메뉴바 생성"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 파일 메뉴
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="직원 정보 파일 열기...", 
                             command=self.menu_open_employee_file,
                             accelerator="Ctrl+O")
        file_menu.add_command(label="출력 폴더 열기...",
                             command=self.menu_open_output_folder,
                             accelerator="Ctrl+Shift+O")
        file_menu.add_separator()
        file_menu.add_command(label="종료",
                             command=self.menu_quit,
                             accelerator="Ctrl+Q")
        
        # 설정 메뉴
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="설정", menu=settings_menu)
        settings_menu.add_command(label="설정 초기화...",
                                 command=self.menu_reset_settings)
        settings_menu.add_command(label="첫 실행 상태로 되돌리기...",
                                 command=self.menu_reset_first_run)
        settings_menu.add_separator()
        settings_menu.add_command(label="출력 폴더 설정...",
                                 command=self.select_output_folder)
        
        # 도움말 메뉴
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="사용자 매뉴얼",
                             command=self.menu_open_user_manual,
                             accelerator="F1")
        help_menu.add_command(label="샘플 파일 가이드",
                             command=self.menu_open_sample_guide)
        help_menu.add_separator()
        help_menu.add_command(label="정보...",
                             command=self.menu_show_about,
                             accelerator="Ctrl+I")
        
        # 키보드 단축키 바인딩
        self.bind_shortcuts()
    
    def menu_open_employee_file(self):
        """메뉴: 직원 정보 파일 열기"""
        # 대시보드 탭으로 전환
        self.notebook.select(0)
        # 파일 선택 다이얼로그 표시
        self.load_file_for_dashboard()
    
    def menu_open_output_folder(self):
        """메뉴: 출력 폴더 열기"""
        self.select_output_folder()
    
    def menu_quit(self):
        """메뉴: 종료"""
        if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
            self.root.quit()
    
    def menu_reset_settings(self):
        """메뉴: 설정 초기화"""
        if messagebox.askyesno("설정 초기화", 
                              "모든 설정을 초기화하시겠습니까?\n"
                              "저장된 파일 경로와 설정이 삭제됩니다.\n"
                              "대시보드의 모든 수치가 0으로 초기화됩니다."):
            # 설정 파일 삭제
            settings_file = self.settings_manager.settings_file
            if settings_file.exists():
                settings_file.unlink()
            # SettingsManager 재초기화
            self.settings_manager = SettingsManager()
            
            # 대시보드 초기화 (모든 수치를 0으로)
            self.reset_dashboard()
            
            messagebox.showinfo("완료", "설정이 초기화되었습니다.\n대시보드의 모든 수치가 0으로 초기화되었습니다.")
            logger.info("설정 초기화 완료")
    
    def reset_dashboard(self):
        """대시보드 초기화 (모든 수치를 0으로)"""
        # 빈 데이터프레임 생성
        import pandas as pd
        self.df = pd.DataFrame()
        
        # 대시보드 데이터를 0 값으로 초기화
        self.dashboard_data = {
            'total_employees': 0,
            'total_payment': 0,
            'total_deduction': 0,
            'total_net_pay': 0,
            'work_status': {
                'regular': 0,
                'contract': 0,
                'new': 0
            },
            'special_notes': [],
            'monthly_data': {
                'months': ['11월', '10월', '9월', '8월', '7월', '6월', '5월', '4월', '3월', '2월', '1월', '12월'],
                'regular': [0] * 12,
                'contract': [0] * 12
            }
        }
        
        # 대시보드 UI 업데이트
        self.update_cards()
        self.update_charts()
        
        logger.info("대시보드 초기화 완료 (모든 수치 0으로 설정)")
    
    def menu_reset_first_run(self):
        """메뉴: 첫 실행 상태로 되돌리기"""
        if messagebox.askyesno("첫 실행 상태로 되돌리기",
                              "다음 실행 시 파일 선택 다이얼로그가 표시됩니다."):
            self.settings_manager.settings['is_first_run'] = True
            self.settings_manager.save_settings()
            messagebox.showinfo("완료", "다음 실행 시 첫 실행 상태로 시작됩니다.")
            logger.info("첫 실행 상태로 되돌리기 완료")
    
    def menu_open_user_manual(self):
        """메뉴: 사용자 매뉴얼 열기"""
        manual_path = os.path.join(
            os.path.dirname(__file__),
            'payroll_generator', 'docs', '사용자_매뉴얼.md'
        )
        if os.path.exists(manual_path):
            self.open_file(manual_path)
        else:
            messagebox.showwarning("파일 없음", "사용자 매뉴얼 파일을 찾을 수 없습니다.")
            logger.warning(f"사용자 매뉴얼 파일을 찾을 수 없음: {manual_path}")
    
    def menu_open_sample_guide(self):
        """메뉴: 샘플 파일 가이드 열기"""
        guide_path = os.path.join(
            os.path.dirname(__file__),
            'payroll_generator', 'docs', '샘플_파일_가이드.md'
        )
        if os.path.exists(guide_path):
            self.open_file(guide_path)
        else:
            messagebox.showwarning("파일 없음", "샘플 파일 가이드 파일을 찾을 수 없습니다.")
            logger.warning(f"샘플 파일 가이드 파일을 찾을 수 없음: {guide_path}")
    
    def menu_show_about(self):
        """메뉴: 정보 표시"""
        about_text = """급여명세서 자동생성기 v1.0

급여명세서를 자동으로 생성하는 프로그램입니다.

주요 기능:
• 직원 정보 대시보드
• 급여명세서 자동 생성 (Excel/PDF)
• 4대보험 자동 계산
• 소득세/지방소득세 자동 계산

개발: 2025
라이선스: MIT"""
        messagebox.showinfo("정보", about_text)
    
    def open_file(self, file_path):
        """파일 열기 (시스템 기본 프로그램)"""
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', file_path])
            else:  # Linux
                subprocess.Popen(['xdg-open', file_path])
            logger.info(f"파일 열기: {file_path}")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{str(e)}")
            logger.exception(f"파일 열기 오류: {str(e)}")
    
    def bind_shortcuts(self):
        """키보드 단축키 바인딩"""
        # Ctrl+O: 직원 정보 파일 열기
        self.root.bind('<Control-o>', lambda e: self.menu_open_employee_file())
        self.root.bind('<Command-o>', lambda e: self.menu_open_employee_file())  # macOS
        
        # Ctrl+Shift+O: 출력 폴더 열기
        self.root.bind('<Control-Shift-O>', lambda e: self.menu_open_output_folder())
        self.root.bind('<Command-Shift-O>', lambda e: self.menu_open_output_folder())  # macOS
        
        # Ctrl+Q: 종료
        self.root.bind('<Control-q>', lambda e: self.menu_quit())
        self.root.bind('<Command-q>', lambda e: self.menu_quit())  # macOS
        
        # F1: 사용자 매뉴얼
        self.root.bind('<F1>', lambda e: self.menu_open_user_manual())
        
        # Ctrl+I: 정보
        self.root.bind('<Control-i>', lambda e: self.menu_show_about())
        self.root.bind('<Command-i>', lambda e: self.menu_show_about())  # macOS
        
        logger.info("키보드 단축키 바인딩 완료")
    
    def on_tab_changed(self, event):
        """탭 전환 이벤트 핸들러"""
        selected_tab = self.notebook.index(self.notebook.select())
        
        # 급여명세서 탭으로 전환 시
        if selected_tab == 1:  # 급여명세서 탭 인덱스 (0: 대시보드, 1: 급여명세서)
            # 파일 경로가 설정되어 있고 미리보기가 비어있으면 업데이트
            if self.employee_file_path.get():
                # 미리보기가 비어있거나, 대시보드에서 로드한 파일과 경로가 다를 때 업데이트
                preview_empty = not self.preview_tree.get_children()
                current_file = self.employee_file_path.get()
                
                # 미리보기가 비어있거나, 현재 파일 경로와 미리보기의 파일이 다를 때 업데이트
                if preview_empty or (self.current_df is not None and self.df is not None):
                    try:
                        self.load_preview(current_file)
                        logger.info(f"급여명세서 탭 미리보기 업데이트: {current_file}")
                    except Exception as e:
                        logger.exception(f"미리보기 업데이트 오류: {str(e)}")
    
    def setup_matplotlib_font(self):
        """플랫폼별 matplotlib 한글 폰트 설정"""
        system = platform.system()
        
        # 플랫폼별 폰트 우선순위 목록
        font_families = {
            'Darwin': ['AppleGothic', 'Arial Unicode MS', 'Helvetica'],  # macOS
            'Windows': ['Malgun Gothic', 'Gulim', 'Arial'],  # Windows
            'Linux': ['DejaVu Sans', 'Liberation Sans', 'Arial']  # Linux
        }
        
        fonts = font_families.get(system, ['DejaVu Sans'])
        # 첫 번째 폰트를 기본으로 설정 (GUI 초기화 전에는 테스트하지 않음)
        selected_font = fonts[0] if fonts else 'DejaVu Sans'
        plt.rcParams['font.family'] = selected_font
        
        # 음수 기호 깨짐 방지
        plt.rcParams['axes.unicode_minus'] = False
        
        logger.info(f"matplotlib 폰트 설정 완료: {selected_font} (플랫폼: {system})")

def main():
    """메인 함수"""
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

