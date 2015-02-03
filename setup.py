from setuptools import setup, find_packages

setup(
    name='k2catalogue',
    version='0.3.1',
    author='Simon Walker',
    author_email='s.r.walker101@googlemail.com',
    url='https://github.com/mindriot101/k2catalogue',
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
