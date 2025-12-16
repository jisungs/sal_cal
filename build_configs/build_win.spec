# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 빌드 설정 파일 (Windows용 - .exe 파일 생성)
급여명세서 자동생성기 v1.0
"""

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('payroll_generator/templates', 'templates'),
        ('payroll_generator/assets/NanumGothic.ttf', 'assets'),
    ],
    hiddenimports=[
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'pandas',
        'openpyxl',
        'reportlab',
        'reportlab.pdfbase',
        'reportlab.pdfbase.ttfonts',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageTk',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy.distutils',
        'scipy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='급여명세서생성기',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 모드
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='payroll_generator/assets/icon.ico',  # Windows 아이콘 파일 (선택사항)
)

