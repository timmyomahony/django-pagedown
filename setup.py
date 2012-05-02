import os
from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build

class build_with_submodules(build):
    def run(self):
        if path.exists('.git'):
            check_call(['git', 'submodule', 'init'])
            check_call(['git', 'submodule', 'update'])
        build.run(self)


setup(
  name = "Django Pagedown",
  version = "0.0.1dev",
  author = "Timmy O'Mahony",
  author_email = "me@timmyomahony.com",
  url = "https://github.com/timmyomahony/django-pagedown",
  description = ("A django app that allows the easy addition of Stack Overflow's 'PageDown' markdown editor to a django form field"),
  long_description=open('README.md').read(),
  packages=['django_pagedown'],
  install_requires=[
    "Django >= 1.2",
  ],
  license='LICENSE.txt',
  cmdclass={"build": build_with_submodules},
)
