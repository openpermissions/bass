# -*- coding: utf-8 -*-

# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from setuptools import setup
import re
import os

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'bass/__init__.py'), 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='opp-bass',
    version=version,
    description='Open Permissions Platform Identity Library',
    author='The Open Permissions Platform Coalition',
    author_email='support@openpermissions.org',
    url='https://github.com/openpermissions/bass',
    packages=['bass'],
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    include_package_data=True,
    package_data={
        '': [ 'LICENSE' ]
    }
    )
