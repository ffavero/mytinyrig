from setuptools import setup

from mytinyrig import __version__

VERSION = __version__.VERSION
DATE = __version__.DATE
AUTHOR = __version__.AUTHOR
MAIL = __version__.MAIL
WEBSITE = __version__.WEBSITE

install_requires = ['PyYAML']

try:
    import argparse
except ImportError:
    install_requires.append('argparse')

setup(
    name='mytinyrig',
    version=VERSION,
    description='Manage miner and NiceHash automatic switch',
    long_description=('NiceHash best profitable algorith switch - mine with '
                      'whatever command you like'),
    author=AUTHOR,
    author_email=MAIL,
    url=WEBSITE,
    license='GPLv3',
    packages=['mytinyrig', 'mytinyrig.workers'],
    package_data={'mytinyrig.workers': ['*.yaml']},
    entry_points={
        'console_scripts': ['mytinyrig = mytinyrig.commands:main']
    },
    install_requires=install_requires,
    test_suite='test',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
