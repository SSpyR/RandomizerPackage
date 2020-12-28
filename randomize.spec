# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['randomize.py'],
             pathex=['C:\\Users\\Angel LaVoie\\Downloads\\BL3\\StandaloneHotfixInjection\\RandomizerPackage'],
             binaries=[],
             datas=[('C:\\Users\\Angel LaVoie\\Downloads\\BL3\\StandaloneHotfixInjection\\RandomizerPackage\\utils\\', 'utils')],
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
          name='randomize',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
