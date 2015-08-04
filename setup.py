from setuptools import setup


if __name__ == '__main__':
  setup(
    name='uuiduser',
    version='0.0.2',
    description='Django UUID-based User model.',
    author='Nick Zarczynski',
    author_email='nick@unb.services',
    packages=[
      'uuiduser',
    ],
    include_package_data=True,
    install_requires=[],
    license="MIT",
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
