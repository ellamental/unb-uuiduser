"""
UUIDUser
=========

Django UUID-based User model.

"""

import os
from setuptools import setup, find_packages


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE_PATH = os.path.join(PROJECT_DIR, 'VERSION')


def read_version():
  if not os.path.isfile(VERSION_FILE_PATH):
    raise EnvironmentError("Version file not found.")
  with open(VERSION_FILE_PATH) as f:
    return f.read().strip()


if __name__ == '__main__':
  setup(
    name='unb-uuiduser',
    version=read_version(),
    description='Django UUID-based User model.',
    author='Nick Frezynski',
    author_email='nick@unb.services',
    url='https://bitbucket.org/unbservices/unb-uuiduser',
    license='MIT',
    packages=['uuiduser'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
      'Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Developers',
      'Environment :: Web Environment',
      'Framework :: Django :: 1.8',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2.7',
    ],
  )
