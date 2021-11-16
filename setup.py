#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 15/11/2021

"""

from setuptools import setup

import jerimoon


if __name__ == '__main__':

    setup(
        name='jerimoon',
        license='MIT',
        packages=[
            'jerimoon'
        ],
        url=jerimoon.__url__,
        version=jerimoon.__version__,
        author=jerimoon.__author__,
        author_email=jerimoon.__email__,
        description=jerimoon.__description__,
        long_description=jerimoon.__docs__,
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],
        install_requires=[
            'numpy',
            'matplotlib',
            'scipy',
            'sympy'
        ],
        python_requires='>=3.9'
    )
