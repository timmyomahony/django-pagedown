import os
from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build
from distutils.dir_util import copy_tree, remove_tree
from setuptools.command.develop import develop

def get_submodules_and_fix_paths():
    if path.exists('.git'):
        check_call(['git', 'submodule', 'init'])
        check_call(['git', 'submodule', 'update'])
        # Move contents of pagedown and remove .git
        dst = "pagedown/static/pagedown/"
        src = "pagedown/static/pagedown/pagedown/"
        copy_tree(src, dst)
        remove_tree(src)

class build_with_submodules(build):
    def run(self):
        get_submodules_and_fix_paths()
        build.run(self)

class develop_with_submodules(develop):
    def run(self):
        get_submodules_and_fix_paths()
        develop.run(self)


setup(
  name = "django-pagedown",
  version = "0.0.1",
  author = "Timmy O'Mahony",
  author_email = "me@timmyomahony.com",
  url = "https://github.com/timmyomahony/django-pagedown",
  description = ("A django app that allows the easy addition of Stack Overflow's 'PageDown' markdown editor to a django form field"),
  long_description=open('README.md').read(),
  packages=['pagedown'],
  include_package_data=True,
  install_requires=[
    "Django >= 1.3",
  ],
  license='LICENSE.txt',
  cmdclass={"build": build_with_submodules, "develop": develop_with_submodules},
)
