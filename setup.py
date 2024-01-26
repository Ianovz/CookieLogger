from setuptools import setup, find_packages

setup(
    name='CookieLogger',
    version='1.0.0',
    packages=find_packages(),
    author='Alexandru Ianov',
    author_email='ianov.alex@gmail.com',
    description='cookie logger for Quantcast test',

    entry_points={
        'console_scripts' : [
            'cookie_logger = cookie_logger.main:main',
        ],
    },
    python_requires='>=3.6',
)
