#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np
import os

plugins = []
for f in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    if f[-4:] == '.pyx':
        plugins.append(f)


# generate an Extension object from its dotted name
def makeExtension(ext):
    return Extension(ext[:-4], [ext], include_dirs=[np.get_include()], extra_compile_args=["-Ofast", "-march=native"])

extensions = [makeExtension(plugin) for plugin in plugins]

setup(name="quantum",
      ext_modules=extensions,
      cmdclass={'build_ext': build_ext})

# setup(cmdclass={'build_ext': build_ext},
#       ext_modules=[Extension(plugin[:-4], [plugin]) for plugin in plugins],
#       include_dirs=[np.get_include()], define_macros=[("NPY_NO_DEPRECATED_API", None)],
#       extra_compile_args=["-Ofast", "-march=native"])
