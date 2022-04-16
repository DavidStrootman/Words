from setuptools import setup, find_packages

setup(
    name='Words',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'wheel',
        'sphinx',
        'pytest',
        'coverage',
        'platformio'
    ],
)
