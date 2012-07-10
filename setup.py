#! /usr/bin/env python
from setuptools import setup, find_packages

# dynamic retrive version number from macadjan.VERSION
version_tuple = __import__('macadjan').VERSION
version = '.'.join([str(v) for v in version_tuple])

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

REQUIREMENTS = [
    'Django >= 1.3',
]

EXTRAS = {
}

setup(name='macadjan',
      author='Hirunatan',
      author_email='hirunatan@hammo.org',
      description='Mapping and Catalog with Django (entities searchable by categories, keywords or geographic data)',
      license='AGPLv3+',
      version=version,
      url='https://github.com/hirunatan/macadjan',
      packages=find_packages(exclude=['doc*', 'examples*', 'tests*',
                                      'website*']),
      include_package_data=True,
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      extras_require=EXTRAS,
      platforms=['any'],
      zip_safe=False)

