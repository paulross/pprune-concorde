#!/usr/bin/env python3
# Part of TotalDepth: Petrophysical data processing and presentation
# Copyright (C) 2011-2021 Paul Ross
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Paul Ross: apaulross@gmail.com
"""The setup script.
copyright 2010-2021, Paul Ross
"""
import os
import sysconfig

from setuptools import Extension, setup, find_packages

COPYRIGHT = '2010-2020, Paul Ross'


# with open('README.rst') as readme_file:
#     readme = readme_file.read()
#
# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

install_requirements = [
    'beautifulsoup4',
    'colorama',
    'lxml',
    'psutil',
    'requests',
]

setup_requirements = [
    'setuptools>=18.0',
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='pprune-concorde',
    version='0.1.0rc0',
    description="Analysis of pprune threads.",
    long_description="Analysis of pprune threads.",
    author="Paul Ross",
    author_email='apaulross@gmail.com',
    url='https://github.com/paulross/pprune-concorde',
    # packages=find_packages('src'),
    # package_dir={'' : 'src'},
    # package_data={'' : ['TotalDepth/util/plot/formats/*.xml']},
    # data_files=data_files,
    entry_points={
        'console_scripts': {
            'pprune_archive_thread=PPRUNE.common.read_html:main',
        },
    },
    include_package_data=True,
    license="GPLv2",
    zip_safe=False,
    keywords='TotalDepth',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    setup_requires=setup_requirements,
    install_requires=install_requirements,
    tests_require=test_requirements,
    # cmdclass = {'build_ext': build_ext},
    # ext_modules=ext_modules
)
