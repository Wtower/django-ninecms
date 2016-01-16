import os
import ninecms
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ninecms',
    version=ninecms.__version__,
    description="Nine CMS is a Django app to manage content.",
    long_description=README,
    url='https://github.com/Wtower/django-ninecms/',
    author='George Karakostas',
    author_email='info@9-dev.com',
    license='BSD-3 License',
    keywords='cms content management system',
    packages=['ninecms'],
    include_package_data=True,
    install_requires=[
        'Django',
        'django-guardian',
        'django-mptt',
        'bleach',
        'Pillow',
        'pytz',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
