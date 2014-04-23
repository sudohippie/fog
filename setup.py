try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'Fog',
    'description': 'Fog is an open-source Git style tool to access files on cloud drives',
    'author': 'Raghav Sidhanti',
    'author_email': 'sudohippie@gmail.com',
    'url': 'https://github.com/sudohippie/fog',
    'download_url': 'https://github.com/sudohippie/fog',
    'version': '1.0.0-beta.1',
    'install_requires': ['nose',
                         'google-api-python-client',
                         'distribute',
                         'virtualenv'],
    'packages': ['fog'],
    'scripts': [],
    'license': 'The MIT License'
}

setup(**config)
