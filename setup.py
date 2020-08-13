import setuptools

setuptools.setup(
    name='unifiAdopter',
    version='2.5.1',
    description='Python project who add automaticly all antenna from a subnet to a distant controller',
    py_modules=["unifiAdopter"],
    package_dir={'': 'src'},
    packages=['controllers', 'workers', 'helpers', 'beans', 'files'],
    author="Simon Barras",
    author_email="simon.barras02@gmail.com",
    url="https://github.com/simbarras/unifiAdopter",
    # scripts=['src/unifiAdopter.py', ''],
    install_requires=["paramiko >= 2.7.1"],
    # data_files= [('files'), ['files/config.xml']],
    extras_require={"dev": [
        "pytest>=3.7", ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
