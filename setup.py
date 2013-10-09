from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build
from setuptools.command.develop import develop


def get_submodules():
    if path.exists('.git'):
        check_call(['rm', '-rf', 'pagedown/static/pagedown'])
        check_call(['git', 'reset', '--hard'])
        check_call(['git', 'submodule', 'init'])
        check_call(['git', 'submodule', 'update'])


class build_with_submodules(build):
    def run(self):
        get_submodules()
        build.run(self)


class develop_with_submodules(develop):
    def run(self):
        get_submodules()
        develop.run(self)


setup(
  name="django-pagedown",
  version="0.0.5",
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
  cmdclass={"build": build_with_submodules, "develop": develop_with_submodules},
)
