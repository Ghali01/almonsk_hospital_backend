# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['..\db-management.py'],
             pathex=['E:\\projects\\hosiptal\\api'],
             binaries=[],
             datas=[],
             hiddenimports=['doctors.urls','doctors.apps','doctors.migrations.0001_initial','drugs.urls','drugs.apps'
             ,'drugs.migrations.0001_initial','surgeries.urls','surgeries.apps','surgeries.migrations.0001_initial','patients.urls','patients.apps','patients.migrations.0001_initial',
             'rest_framework.authentication'
             ],
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

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='db-management',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir='%TEMP%/hs-cache',
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
