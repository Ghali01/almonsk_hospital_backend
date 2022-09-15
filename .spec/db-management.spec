# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
apps=['patients','doctors','drugs','surgeries','directory']
import os
def getMigrations():
    migrations=[]
    for app in apps:
            for i in os.listdir(os.path.join(app,'migrations')):
                if os.path.isfile(os.path.join(app,'migrations',i)) and i.endswith('.py') and not i =='__init__.py':
                    migrations.append('.'.join([app,'migrations',i[:-3]]))
    print(migrations)
    return migrations
hiddenimports = ['doctors.urls','doctors.apps','doctors.migrations.0001_initial','drugs.urls','drugs.apps'
             ,'drugs.migrations.0001_initial','surgeries.urls','surgeries.apps','surgeries.migrations.0001_initial'
             ,'patients.urls','patients.apps','patients.migrations.0001_initial','patients.migrations.0002_auto_20220111_1517'
             ,'directory.urls','directory.apps','directory.migrations.0001_initial',
             'rest_framework.authentication','rest_framework.permissions','rest_framework.parsers','rest_framework.negotiation','rest_framework.negotiation',
             'rest_framework.metadata']
hiddenimports += getMigrations()
print(getMigrations())

block_cipher = None


a = Analysis(['..\db-management.py'],
             pathex=['E:\\projects\\hosiptal\\api'],
             binaries=[],
             datas=[],
             hiddenimports=hiddenimports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,noarchive=False)

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
