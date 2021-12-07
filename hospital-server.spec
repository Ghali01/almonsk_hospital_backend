# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['hospital-server.py'],
             pathex=['E:\\projects\\hosiptal\\api'],
             binaries=[],
             datas=[],
              hiddenimports=['doctors.urls','doctors.apps','drugs.urls','drugs.apps'
             ,'surgeries.urls','surgeries.apps','patients.urls','patients.apps',
             'rest_framework.authentication','rest_framework.permissions','rest_framework.parsers','rest_framework.negotiation','rest_framework.negotiation',
             'rest_framework.metadata'],
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
          name='hospital-server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir='%TEMP%/hs-cache',
          console=True )
