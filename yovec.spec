# -*- mode: python ; coding: utf-8 -*-

from os import getcwd
from os.path import join
from site import USER_SITE

block_cipher = None


a = Analysis(['yovec.py'],
             pathex=[getcwd()],
             binaries=[],
             datas=[(join(USER_SITE, 'lark'), 'lark')],
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
          [],
          name='yovec',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
