# -*- coding: utf-8 -*-
"""
setupCPU.py — macOS CPU 版本编译脚本（Clang + Homebrew FFTW）
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np
import os, sys, platform, subprocess, shutil

# ---------- 检测编译器 ----------
# 如果用户手动 export CC/CXX=clang/clang++ 就尊重环境变量，
# 否则在 macOS 默认使用 clang。
is_macos = sys.platform == "darwin"
cc_env  = os.environ.get("CC", "")
cxx_env = os.environ.get("CXX", "")
use_clang = is_macos and (not cc_env or "clang" in cc_env)

# ---------- 公共设置 ----------
sources = [
    "src/ccfj.pyx",
    "src/CrossCorr.cpp",
    "src/FJcpu.cpp",
]
include_dirs = ["include", np.get_include(), "/opt/homebrew/include"]
library_dirs = ["/opt/homebrew/lib", "lib"]
libraries    = ["m", "fftw3f"]        # 如需双精度改成 fftw3

# ---------- 针对编译器的差异化参数 ----------
extra_compile_args = ["-O3", "-Wall", "-std=c++17"]

extra_link_args = []
if use_clang:
    # Clang + OpenMP 依赖 libomp
    #   brew install libomp
    extra_compile_args += ["-Xpreprocessor", "-fopenmp"]
    extra_link_args    += ["-lomp"]
else:
    # GCC 情况：沿用原来的 -fopenmp
    extra_compile_args += ["-fopenmp"]
    extra_link_args    += ["-fopenmp"]

# ---------- Extension ----------
ext_modules = [
    Extension(
        "ccfj",
        sources=sources,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        language="c++",
    )
]

setup(
    name="ccfj",
    version="0.1",
    author="Zhengbo Li et al.",
    packages=["ccfj"],
    ext_modules=cythonize(ext_modules, language_level="3"),
)