from setuptools import setup

setup(
    name='Words',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=['words'],
    install_requires=[
        'sphinx',
        'pytest',
        'coverage',
    ],
)
