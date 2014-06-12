import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-locksmith',
    version='0.1.1',
    packages=['locksmith',
              'locksmith.management',
              'locksmith.management.commands',
              'locksmith.templatetags'],
    include_package_data=True,
    license='MIT License',
    description='Simple access control system.',
    long_description=README,
    url='https://github.com/MichalMazurek/django-locksmith',
    author='Michal Mazurek',
    author_email='me@michalmazurek.eu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)