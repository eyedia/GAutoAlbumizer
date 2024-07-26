# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=["D:\\Work\\Google\\Photos\\GAutoAlbumizer"],
    binaries=[],
    datas=[
         
        ('sample/MyPhotoDump/Abstracts/pexels-pixabay-50570.jpg', 'sample/MyPhotoDump/Abstracts'),
        ('sample/MyPhotoDump/Abstracts/pexels-steve-1266808.jpg', 'sample/MyPhotoDump/Abstracts'),
        ('sample/MyPhotoDump/Abstracts/pexels-skyler-ewing-266953-6747239.jpg', 'sample/MyPhotoDump/Abstracts'),
        ('sample/MyPhotoDump/Abstracts/pexels-pixabay-50570.jpg', 'sample/MyPhotoDump/Abstracts'),

        ('sample/MyPhotoDump/Mountains/pexels-david-besh-884788.jpg', 'sample/MyPhotoDump/Mountains'),
        ('sample/MyPhotoDump/Mountains/pexels-8moments-1323550.jpg', 'sample/MyPhotoDump/Mountains'),

        ('sample/MyPhotoDump/Mountains/More Mountains/pexels-sebastian-palomino-933481-1955134.jpg', 'sample/MyPhotoDump/Mountains/More Mountains'),
        ('sample/MyPhotoDump/Mountains/More Mountains/pexels-eberhardgross-1468555.jpg', 'sample/MyPhotoDump/Mountains/More Mountains'),

        ('sample/MyPhotoDump/My Photography/pexels-thatguycraig000-1563356.jpg', 'sample/MyPhotoDump/My Photography'),
        ('sample/MyPhotoDump/My Photography/pexels-jill-wellington-1638660-39853.jpg', 'sample/MyPhotoDump/My Photography'),

        ('sample/MyPhotoDump/Skies/pexels-therato-1933239.jpg', 'sample/MyPhotoDump/Skies'),
        ('sample/MyPhotoDump/Skies/pexels-egos68-1906658.jpg', 'sample/MyPhotoDump/Skies'),
        ('sample/MyPhotoDump/Skies/pexels-cliford-mervil-988071-2469122.jpg', 'sample/MyPhotoDump/Skies'),


        ('client_secrets.json', '.'),
        ('config.ini', '.'),

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
    hiddenimports=[],
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
    name='GAutoAlbumizer',
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
    icon='graphics/logo.ico'
)
