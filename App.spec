# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

a = Analysis(['.\\App.py'],
	pathex=['.','.\\UI', '.\\PyQtRibbon'],
	binaries=[],
	datas=[
		('.\\Scripts\\*.sql', 'Scripts'),
		('.\\stylesheets\\*.qss', 'stylesheets'),
		('.\\translates\\*.qm', 'translates'),
		('.\\UI\\*.ui', 'UI')
	],
	hiddenimports=['vtkmodules', 'vtkmodules.all', 'vtkmodules.qt.QVTKRenderWindowInteractor', 'vtkmodules.util', 
	'vtkmodules.util.numpy_support', 'pkg_resources.py2_warn', 'pandas', 'networkx'],
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
	[],
	exclude_binaries=True,
	name='AViewer',
	debug=False,
	bootloader_ignore_signals=False,
	strip=False,
	upx=True,
	console=False,
	icon='.\\res\\AViewer.ico',
	version='version.rc')
coll = COLLECT(exe,
	a.binaries,
	a.zipfiles,
	a.datas,
	strip=False,
	upx=True,
	name='App')