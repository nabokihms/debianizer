import sys

from setuptools import find_packages, setup

_NAME = 'debianizer'

vi = sys.version_info
if vi[:2] < (3, 5):
    raise RuntimeError('Unsupported python version %s.' % vi)

setup(
    name=_NAME,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Command line :: debianizer',
        'License :: OSI Approved :: MIT License',
    ],
    maintainer='Max Nabokikh',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    maintainer_email='max.nabokih@gmail.com',
    platforms=['*nix'],
    description='Create debian folder for packaging with dh-virtualenv.',

    install_requires=[
        'jinja2==2.10',
        'click==7.0',
    ],
    entry_points={
        'console_scripts': [
            '{} = {}.cli:run'.format(_NAME, _NAME),
        ]
    }
)
