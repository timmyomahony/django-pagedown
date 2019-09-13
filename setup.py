from os import path
from setuptools import setup
from subprocess import check_call
from distutils.command.build import build
from setuptools.command.develop import develop

from pagedown import VERSION


def get_submodules():
    if path.exists('.git'):
        check_call(['rm', '-rf', 'pagedown/static/pagedown'])
        check_call(['rm', '-rf', 'pagedown/static/pagedown-extra'])
        check_call(['git', 'reset', '--hard'])
        check_call(['git', 'submodule', 'update', '--init', '--recursive'])


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
    version=".".join(map(str, VERSION)),
    author="Timmy O'Mahony",
    author_email="hey@timmyomahony.com",
    url="https://github.com/timmyomahony/django-pagedown",
    description=("A Django app that allows the easy addition of Stack Overflow's 'PageDown' markdown editor to a django form field"),
    long_description=open('README.md').read(),
    packages=['pagedown'],
    include_package_data=True,
    # _Should_ work back to 1.1 but untested
    install_requires=[
        "Django >= 1.11",
    ],
    license='LICENSE.txt',
    cmdclass={"build": build_with_submodules, "develop": develop_with_submodules},
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Text Editors',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)
