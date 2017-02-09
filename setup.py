#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "qiniu==7.1.1",
    "path.py"
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='publish2cloud', #publish 被用了
    version='0.1.0',
    description="publish your site to qiniu.com",
    long_description=readme + '\n\n' + history,
    author="wenjiewu",
    author_email='wuwenjie718@gmail.com',
    url='https://github.com/wwj718/publish',
    packages=[
        'publish',
    ],
    package_dir={'publish':
                 'publish'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='publish',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
         'console_scripts': [
             'publish = publish.publish:main'
            ]
        }
)
