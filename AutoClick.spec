# -*- mode: python ; coding: utf-8 -*-

from kivy.deps import sdl2, glew
block_cipher = None

added_files = [
         ( 'Icon.ico', '.' ),
         ( 'config.json', '.' ),
         ( 'AutoClick.kv', '.' ),
         ( 'img/*.jpg', 'img' )]


a = Analysis(['main.py'],
             pathex=['D:\\code\\myCode\\python\\autoclick\\epic87\\AutomationTower'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='epic7TowerBot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='Icon.ico')
