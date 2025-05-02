from setuptools import setup, find_packages

setup(
    name='ecc-crypto',
    version='0.1.0',
    author='Khant, Min Thwin',
    author_email='minthwin.khant@sjsu.edu',
    description='A package for Elliptic Curve Cryptography key exchange',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List any dependencies your package needs
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)