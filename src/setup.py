"""Setup file for KVM Manager

Define the options for the "kvm_manager" package
Create source Python packages (python setup.py sdist)
Create binary Python packages (python setup.py bdist)

"""
from distutils.core import setup

from kvm_manager import __version__


with open('README.txt') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(name='kvm_manager',
      version=__version__,
      description='KVM Manager',
      long_description=LONG_DESCRIPTION,
      author='Jeroen Doggen',
      author_email='jeroendoggen@gmail.com',
      url='https://github.com/jeroendoggen/kvm-manager',
      packages=['kvm_manager'],
      package_data={'kvm_manager': ['*.py', '*.conf']},
      license='MIT',
      platforms=['Linux'],
      )
