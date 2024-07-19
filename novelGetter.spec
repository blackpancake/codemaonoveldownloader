# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['novelGetter.py'],
             pathex=[],
             binaries=[],
             datas=[('assets', 'assets')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
splash = Splash('new.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=(30,450),
                text_size=10,
                always_on_top=True,
                minify_script=True)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas, 
          splash, 
          splash.binaries,
          [],
          name='novelGetter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=True,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icon.ico')
