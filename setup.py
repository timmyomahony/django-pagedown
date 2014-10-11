from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build
from setuptools.command.develop import develop


setup(
  name="django-pagedown",
  version="0.1.0",
  author="Timmy O'Mahony",
  author_email="me@timmyomahony.com",
  url="https://github.com/timmyomahony/django-pagedown",
  description=("A django app that allows the easy addition of Stack Overflow's 'PageDown' markdown editor to a django form field"),
  long_description=open('README.md').read(),
  packages=['pagedown'],
  include_package_data=True,
  install_requires=[
    "Django >= 1.3",
  ],
  license='LICENSE.txt',
  cmdclass={"build": build, "develop": develop},
)
