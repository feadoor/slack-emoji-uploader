#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import os

from setuptools import find_packages, setup

def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))

SOURCE = local_file('src')
README = local_file('README.rst')
long_description = codecs.open(README, encoding='utf-8').read()

setup(
    name='slack_emoji_uploader',
    version='0.1.0',
    description='A script for uploading custom emoji to Slack',
    long_description=long_description,
    url='https://github.com/feadoor/slack-emoji-uploader',
    author='Sam Cappleman-Lynes',
    author_email='sam.capplemanlynes@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(SOURCE),
    package_dir={'': SOURCE},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'click',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'slackmoji=slack_emoji_uploader:main',
        ],
    },
)
