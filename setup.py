from setuptools import setup, find_packages
#from distutils.core import setup

setup(
    name = 'simplemotds',
    packages = ['simplemotds'],
    include_package_data=True,
    version = '0.23',
    description = 'Configurable package that returns the message of the day (motd)',
    author='Rodrigo Garcia',
    author_email="strysg@riseup.net",
    license="GPLv3",
    url="https://github.com/strymsg/python-simplemotds",
    classifiers = ["Programming Language :: Python :: 3","License :: OSI Approved :: GNU General Public License v3 (GPLv3)", "Development Status :: 4 - Beta", "Intended Audience :: Developers", "Operating System :: OS Independent"],
)
