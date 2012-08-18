from setuptools import setup

setup(
    name='Flask-Locale',
    version='0.1',
    url='https://github.com/whtsky/flask-locale',
    license='MIT',
    author='whtsky',
    author_email='whtsky@me.com',
    description='',
    long_description=open('README.rst', 'r').read(),
    py_modules=['flask_locale'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests.suite'
)
