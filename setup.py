from setuptools import setup
from BCNF import __version__


setup(
    name='BCNF',
    version=__version__,
    packages=['BCNF'],
    include_package_data=True,
    url='jaantollander/BCNF',
    license='MIT',
    author='Jaan Tollander de Balsch',
    author_email='de.tollander@gmail.com',
    description='BCNF algorithm implementation',
    install_requires=[],
    test_suite='tests',
    tests_require=[],
)
