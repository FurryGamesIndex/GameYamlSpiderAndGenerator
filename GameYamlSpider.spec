# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pkg.py'],
    pathex=[],
    binaries=[],
    datas=[('gameyamlspiderandgenerator/plugin/gcores.py', 'gameyamlspiderandgenerator/plugin'), ('gameyamlspiderandgenerator/plugin/itchio.py', 'gameyamlspiderandgenerator/plugin'), ('gameyamlspiderandgenerator/plugin/steam.py', 'gameyamlspiderandgenerator/plugin'), ('/mnt/data/Project/GameYamlSpiderAndGenerator/.venv/lib/python3.12/site-packages/language_data/data', 'language_data/data'), ('/mnt/data/Project/GameYamlSpiderAndGenerator/.venv/lib/python3.12/site-packages/ruamel/yaml/string/__plug_in__.py', 'ruamel/yaml/string')],
    hiddenimports=['gameyamlspiderandgenerator.plugin.gcores', 'gameyamlspiderandgenerator.plugin.itchio', 'gameyamlspiderandgenerator.plugin.steam', 'yamlgenerator_hook_search', 'language_data', 'ruamel_yaml_string', 'yamlgenerator_hook_validate'],
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
    [],
    exclude_binaries=True,
    name='GameYamlSpider',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GameYamlSpider',
)
