import re
import os.path
from setuptools import setup

# reading package's version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'virastar.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

long_description = """
virastar.py
===========

Please check test.py file on how to use the code.

"""

setup(
    name='virastar.py',
    version=package_version,
    author='JKhakpour',
    url='https://github.com/JKhakpour/virastar.py',
    description='Persian text normalizer',
    long_description=long_description,
    py_modules=['virastar'],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)
