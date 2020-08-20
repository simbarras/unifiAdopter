import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='unifiAdopter',
    version='2.7.0',
    description='Python project who add automatically all antenna from a subnet to a distant controller',
    long_description='README.md',
    long_description_content_type="text/markdown",
    py_modules=["unifiAdopter"],
    package_dir={'': 'src'},
    packages=['beans', 'files'],
    author="Simon Barras",
    author_email="simon.barras02@gmail.com",
    url="https://github.com/simbarras/unifiAdopter",
    # scripts=['src/unifiAdopter.py', ''],
    install_requires=["paramiko >= 2.7.1", "lxml >= 4.5.2"],
    package_data={'files': ['*.xml', 'src/files/*.xml']},
    include_package_data=True,
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
