# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=["D:\\Work\\Google\\Photos\\GAutoAlbumizer"],
    binaries=[],
    datas=[
         ('common/__init__.py', 'common'),
         ('common/config.py', 'common'),
         ('common/fileHandler.py', 'common'),

         ('exif/__init__.py', 'exif'),
         ('exif/updateExif.py', 'exif'),

         ('meta/__init__.py', 'meta'),
         ('meta/metaFile.py', 'meta'),

         ('upload/__init__.py', 'upload'),
         ('upload/GooglePhotoUploader.py', 'upload'),
    ],
    hiddenimports=['pandas'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
