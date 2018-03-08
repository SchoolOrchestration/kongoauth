import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), './README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-kongoauth',
    version='0.1.8',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  #
    description='A Kong OAuth Utility Library',
    long_description=README,
    url='https://github.com/SchoolOrchestration/kongoauth',
    author='schoolOrchestration',
    author_email='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)