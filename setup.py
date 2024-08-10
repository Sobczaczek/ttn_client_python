from setuptools import setup, find_packages

setup(
    name='ttn_client',
    version='0.1.0',
    description='A Python client for interacting with The Things Network API.',
    author='Dawid Sobczak',
    author_email='sobczakss111@gmail.com',
    url='',  
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
