import os
import codecs
from setuptools import setup


__version__ = '0.2'


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


install_requirements = []

test_requirements = [
    'tox==1.9.0',
    'py==1.4.26',
    'pyflakes==0.8.1',
    'pytest==2.6.4',
    'pytest-cov==1.8.1',
    'pytest-cache==1.0',
    'pytest-flakes==0.2',
    'pytest-pep8==1.0.6',
    'cov-core==1.15.0',
    'coverage==3.7.1',
    'execnet==1.2.0',
    'mock==1.0.1',
    'pep8==1.6.2',
]

docs_requirements = [
    'Sphinx==1.2.3',
]

setup(
    name='python-redict',
    version=__version__,
    description='A Python dictionary key remapper',
    long_description=read('README.rst'),
    author='Carlo Smouter',
    author_email='lockwooddev@gmail.com',
    url='https://github.com/lockwooddev/python-redict',
    install_requires=install_requirements,
    extras_require={
        'tests': test_requirements,
        'docs': docs_requirements,
    },
    license='MIT',
    keywords=['python', 'dictionary', 'remap', 'keys', 'remapper'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[
        'redict',
        'redict.remappers',
        'redict.utils',
        'redict.tests',
        'docs',
    ],
)
