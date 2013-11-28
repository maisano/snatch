import os

from setuptools import setup, find_packages


# utility fn to read files
def read(fname):
    with open(fname) as f:
        contents = f.read()
    return contents


requires = [
    'requests>=2.0.0',
    'beautifulsoup4==4.3.2',
    'lxml==3.2.4'
]

license = read('LICENSE')
readme = read('README.rst')
history = read('HISTORY.rst')

setup(
    name='snatch',
    version='0.1.0',
    description='Simple image scraping in Python',
    long_description=readme + '\n\n' + history,
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers'
    ],
    keywords='image scraping',
    author='maisano',
    author_email='rickmaisano@gmail.com',
    maintainer='maisano',
    maintainer_email='rickmaisano@gmail.com',
    url='https://github.com/maisano/snatch',
    packages=find_packages(),
    include_package_data=True,
    license=license,
    zip_safe=False,
    install_requires=requires
)
