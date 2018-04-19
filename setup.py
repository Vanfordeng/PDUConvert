#!/usr/bin/env python
# _*_coding:utf-8_*_

from distutils.core import setup
import py2exe

options = {"py2exe":{"compressed":1, #压缩
                      "optimize":2,
                      "bundle_files":1, #所有文件打包成一个exe文件
                      "dll_excludes":["MSVCP90.dll"]
                     }}

#setup(windows=['pduconvert.py'],options = options)
setup(
version = "0.1.0",
description = u"pduconvert",
name = "pduconvert",
options = options,
zipfile = None,
#生成有指定图标的exe
windows = [{"script": "pduconvert.py",
			"icon_resources":[(0,u"./pduconvert.ico")]
		   }]
)