# -*- coding:utf-8 -*-
try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import sys
import info
import version

setup_options = info.INFO
setup_options["version"] = version.VERSION
setup_options["install_requires"] = open('requirements.txt').read().splitlines()
setup_options["packages"] = ['dungeon_generator']

setup(**setup_options)
