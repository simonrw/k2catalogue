from setuptools import setup, find_packages

setup(
    name='k2catalogue',
    version='0.3.0',
    author='Simon Walker',
    install_requires=['requests', 'sqlalchemy', 'ipython', 'vcrpy',
                      'beautifulsoup4', 'lxml'],
    tests_require=['pytest'],
    packages=find_packages(exclude=['venv']),
    entry_points={
        'console_scripts': [
            'k2cat-search = k2catalogue.cli:main',
        ],
    }
)
