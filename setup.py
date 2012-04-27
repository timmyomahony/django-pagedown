import os
from setuptools import setup

setup(
  name = "Django Pagedown",
  version = "0.0.1dev",
  author = "Timmy O'Mahony",
  author_email = "hello@timmyomahony.com",
  url = "https://github.com/pastylegs/django-pagedown",
  description = ("A django app that allows the easy addition of Stack Overflow's 'PageDown' markdown editor to a django form field"),
  long_description=open('README.md').read(),
  packages=['pagedown'],
  install_requires=[
    "Django >= 1.2",
  ],
  license='LICENSE.txt',
)
