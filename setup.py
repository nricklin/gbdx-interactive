import sys
from setuptools import setup, find_packages

open_kwds = {}
if sys.version_info > (3,):
    open_kwds['encoding'] = 'utf-8'

setup(name='gbdx-interactive',
      version='0.0.2',
      description='gbdxtools, but interactive.',
      classifiers=[],
      keywords='',
      author='Nate Ricklin',
      author_email='nate.ricklin@digitalglobe.com',
      url='https://github.com/nricklin/gbdx-interactive',
      license='MIT',
      packages=find_packages(exclude=['docs','tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['boto3',
                        'gbdxtools>=0.9.2'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest','vcrpy']
      )
